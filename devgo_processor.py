#!/usr/bin/env python3
"""
Development Execution Orchestrator (devgo) implementation
"""

import re
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class Task:
    """Represents a task from the queue"""
    task_id: str
    agent: str
    epic: str
    story: str
    original_line: str
    acceptance: Optional[str] = None
    is_completed: bool = False


@dataclass
class ProgressEntry:
    """Represents an entry in the progress log"""
    timestamp: str
    state: str
    task_id: str
    agent: Optional[str] = None
    epic: Optional[str] = None
    story: Optional[str] = None
    note: Optional[str] = None
    evidence: Optional[List[str]] = None
    verifier: Optional[str] = None
    result: Optional[str] = None


class DevgoProcessor:
    """Handles devgo command processing"""
    
    VALID_AGENTS = {"VIVA", "SYRA", "MAKA", "QRA", "LUA"}
    VALID_STATES = {"STARTED", "IN_PROGRESS", "BLOCKED", "RESOLVED", "COMPLETED", "VERIFIED"}
    
    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path)
        self.queue_file = self.folder_path / "epic_stories_tasks_queue.md"
        self.progress_file = self.folder_path / "epic_stories_tasks_progress.md"
        self.issues_file = self.folder_path / "issues_resolved.md"
        self.done_file = self.folder_path / "epic_stories_tasks_done.md"
        
        self.tasks: List[Task] = []
        self.progress_entries: List[ProgressEntry] = []
        self.existing_task_states: Dict[str, str] = {}
        
    def generate_task_id(self, line: str) -> str:
        """Generate stable hash for task identification"""
        clean_line = line.strip().lower()
        # Remove checkbox and normalize whitespace
        clean_line = re.sub(r'^\s*-\s*\[\s*[x\s]*\]\s*', '', clean_line)
        clean_line = re.sub(r'\s+', ' ', clean_line)
        return hashlib.sha256(clean_line.encode()).hexdigest()[:12]
    
    def parse_queue_file(self) -> Tuple[List[Task], List[str]]:
        """Parse the queue file and extract tasks"""
        if not self.queue_file.exists():
            raise FileNotFoundError(f"Queue file not found: {self.queue_file}")
        
        content = self.queue_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        tasks = []
        warnings = []
        current_epic = ""
        current_story = ""
        
        epic_pattern = r'^###\s*EPIC:\s*(.+)$'
        story_pattern = r'^\s*-\s*STORY:\s*(.+)$'
        task_pattern = r'^\s*-\s*\[\s*([x\s])\s*\]\s*\(([^)]+)\)\s*(.+)$'
        acceptance_pattern = r'^\s*\*\*Acceptance\*\*:\s*(.+)$'
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for epic
            epic_match = re.match(epic_pattern, line)
            if epic_match:
                current_epic = epic_match.group(1).strip()
                current_story = ""
                i += 1
                continue
            
            # Check for story
            story_match = re.match(story_pattern, line)
            if story_match:
                current_story = story_match.group(1).strip()
                i += 1
                continue
            
            # Check for task
            task_match = re.match(task_pattern, line)
            if task_match:
                checkbox_state = task_match.group(1).strip()
                agent = task_match.group(2).strip()
                task_desc = task_match.group(3).strip()
                
                # Validate agent
                if agent not in self.VALID_AGENTS:
                    warnings.append(f"Invalid agent '{agent}' in task: {line}")
                    i += 1
                    continue
                
                is_completed = checkbox_state.lower() == 'x'
                task_id = self.generate_task_id(line)
                
                # Look for acceptance criteria on the next line
                acceptance = None
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    acceptance_match = re.match(acceptance_pattern, next_line)
                    if acceptance_match:
                        acceptance = acceptance_match.group(1).strip()
                
                task = Task(
                    task_id=task_id,
                    agent=agent,
                    epic=current_epic,
                    story=current_story,
                    original_line=line,
                    acceptance=acceptance,
                    is_completed=is_completed
                )
                tasks.append(task)
            
            i += 1
        
        return tasks, warnings
    
    def load_existing_progress(self) -> Dict[str, str]:
        """Load existing progress entries to track task states"""
        if not self.progress_file.exists():
            return {}
        
        content = self.progress_file.read_text(encoding='utf-8')
        task_states = {}
        
        # Parse progress entries to get latest state for each task
        entry_pattern = r'^### (.+) (STARTED|IN_PROGRESS|BLOCKED|RESOLVED|COMPLETED|VERIFIED)$'
        current_task_id = None
        
        for line in content.split('\n'):
            line = line.strip()
            entry_match = re.match(entry_pattern, line)
            if entry_match:
                timestamp = entry_match.group(1)
                state = entry_match.group(2)
                current_task_id = None  # Will be set from TaskID line
                continue
            
            if line.startswith('TaskID:') and current_task_id is None:
                task_id = line.split(':', 1)[1].strip()
                if task_id.startswith('sha256:'):
                    task_id = task_id[7:]
                current_task_id = task_id
                task_states[task_id] = state
        
        return task_states
    
    def select_tasks(self, limit: int = 1, agent_filter: Optional[str] = None) -> List[Task]:
        """Select tasks to start using round-robin agent balancing"""
        # Filter available tasks (not completed, not already started)
        available_tasks = [
            task for task in self.tasks 
            if not task.is_completed and task.task_id not in self.existing_task_states
        ]
        
        # Apply agent filter if specified
        if agent_filter and agent_filter != "*":
            available_tasks = [task for task in available_tasks if task.agent == agent_filter]
        
        if not available_tasks:
            return []
        
        # Count current tasks per agent
        agent_counts = defaultdict(int)
        for task_id, state in self.existing_task_states.items():
            if state not in ["COMPLETED", "VERIFIED"]:
                # Find the agent for this task
                for task in self.tasks:
                    if task.task_id == task_id:
                        agent_counts[task.agent] += 1
                        break
        
        # Group available tasks by agent
        tasks_by_agent = defaultdict(list)
        for task in available_tasks:
            tasks_by_agent[task.agent].append(task)
        
        # Calculate agent deficits (fewer current tasks = higher priority)
        agent_priorities = []
        for agent in self.VALID_AGENTS:
            if agent in tasks_by_agent:
                deficit = -agent_counts[agent]  # Negative for min-heap behavior
                agent_priorities.append((deficit, agent))
        
        agent_priorities.sort()
        
        # Round-robin selection
        selected = []
        agent_index = 0
        
        while len(selected) < limit and agent_priorities:
            agent = agent_priorities[agent_index % len(agent_priorities)][1]
            
            if tasks_by_agent[agent]:
                # Take first available task for this agent (maintains epic/story order)
                task = tasks_by_agent[agent].pop(0)
                selected.append(task)
                
                # Update agent count for next iteration
                agent_counts[agent] += 1
                agent_priorities[agent_index % len(agent_priorities)] = (-agent_counts[agent], agent)
                agent_priorities.sort()
            else:
                # No more tasks for this agent, remove from rotation
                agent_priorities = [ap for ap in agent_priorities if ap[1] != agent]
                if not agent_priorities:
                    break
            
            agent_index += 1
        
        return selected
    
    def initialize_progress_file(self):
        """Create progress file if it doesn't exist"""
        if self.progress_file.exists():
            return
        
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        content = f"""# Execution Progress Log (devgo)

## Metadata
- Snapshot Folder: {self.folder_path.name}
- First Run: {now}
- Last Run: {now}
- Runs: 1

## Entries
"""
        self.progress_file.write_text(content, encoding='utf-8')
    
    def add_progress_entries(self, selected_tasks: List[Task]):
        """Add STARTED entries for selected tasks"""
        if not selected_tasks:
            return
        
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        # Read existing content
        content = ""
        if self.progress_file.exists():
            content = self.progress_file.read_text(encoding='utf-8')
        else:
            self.initialize_progress_file()
            content = self.progress_file.read_text(encoding='utf-8')
        
        # Update run count and last run time in metadata
        lines = content.split('\n')
        updated_lines = []
        
        for line in lines:
            if line.startswith('- Last Run:'):
                updated_lines.append(f'- Last Run: {now}')
            elif line.startswith('- Runs:'):
                runs_match = re.search(r'- Runs:\s*(\d+)', line)
                if runs_match:
                    runs = int(runs_match.group(1)) + 1
                    updated_lines.append(f'- Runs: {runs}')
                else:
                    updated_lines.append('- Runs: 1')
            else:
                updated_lines.append(line)
        
        # Add new entries
        for task in selected_tasks:
            entry = f"""
### {now} STARTED
TaskID: sha256:{task.task_id}
Agent: {task.agent}
Epic: {task.epic}
Story: {task.story}
OriginalLine: {task.original_line}
Note: Task selected for execution via devgo
"""
            updated_lines.append(entry.strip())
        
        # Write updated content
        self.progress_file.write_text('\n'.join(updated_lines), encoding='utf-8')
    
    def generate_integrity_report(self, warnings: List[str]) -> Dict:
        """Generate integrity checks for the queue"""
        integrity = {
            "missing_files": [],
            "duplicate_task_ids": [],
            "invalid_agent_tags": []
        }
        
        # Check for missing required files
        if not self.queue_file.exists():
            integrity["missing_files"].append(str(self.queue_file))
        
        # Check for duplicate task IDs
        task_ids = {}
        for task in self.tasks:
            if task.task_id in task_ids:
                integrity["duplicate_task_ids"].append({
                    "task_id": task.task_id,
                    "lines": [task_ids[task.task_id], task.original_line]
                })
            else:
                task_ids[task.task_id] = task.original_line
        
        # Extract invalid agent warnings
        for warning in warnings:
            if "Invalid agent" in warning:
                integrity["invalid_agent_tags"].append(warning)
        
        return integrity
    
    def process(self, limit: int = 1, agent_filter: Optional[str] = None, 
                apply_done: bool = False, dry_run: bool = False) -> Dict:
        """Main processing function"""
        
        # Parse queue file
        self.tasks, warnings = self.parse_queue_file()
        
        # Load existing progress
        self.existing_task_states = self.load_existing_progress()
        
        # Select tasks to start
        selected_tasks = self.select_tasks(limit=limit, agent_filter=agent_filter)
        
        # Count agent distribution
        agent_counts = defaultdict(int)
        for task in self.tasks:
            agent_counts[task.agent] += 1
        
        # Generate result
        result = {
            "folder": str(self.folder_path),
            "selected_started": len(selected_tasks),
            "advanced": {
                "in_progress": 0,
                "completed": 0,
                "verified": 0
            },
            "applied_to_queue": 0,
            "issues": {
                "opened": 0,
                "closed": 0,
                "open_total": 0
            },
            "filters": {
                "agent": agent_filter or "*",
                "epic": "*",
                "story": "*", 
                "limit": limit
            },
            "dry_run": dry_run,
            "warnings": warnings,
            "integrity": self.generate_integrity_report(warnings),
            "agent_distribution": dict(agent_counts),
            "selected_tasks": [
                {
                    "task_id": task.task_id,
                    "agent": task.agent,
                    "epic": task.epic,
                    "story": task.story,
                    "original_line": task.original_line
                }
                for task in selected_tasks
            ]
        }
        
        # Actually perform operations if not dry run
        if not dry_run and selected_tasks:
            self.initialize_progress_file()
            self.add_progress_entries(selected_tasks)
        
        return result


def main():
    """Main entry point for devgo command"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python devgo_processor.py <snapshot_folder> [--limit N] [--agent AGENT] [--dry-run]")
        sys.exit(1)
    
    folder_arg = sys.argv[1]
    
    # Parse arguments
    limit = 1
    agent_filter = None
    dry_run = False
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--agent" and i + 1 < len(sys.argv):
            agent_filter = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--dry-run":
            dry_run = True
            i += 1
        else:
            i += 1
    
    # Resolve folder path
    if '/' not in folder_arg:
        folder_path = f"docs/progress/{folder_arg}"
    else:
        folder_path = folder_arg
    
    try:
        processor = DevgoProcessor(folder_path)
        result = processor.process(limit=limit, agent_filter=agent_filter, dry_run=dry_run)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "folder": folder_path,
            "selected_started": 0,
            "warnings": [f"Processing failed: {e}"]
        }, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()