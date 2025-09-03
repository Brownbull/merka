#!/usr/bin/env python3
"""
DevGo Task Selection Algorithm

Implements the balanced agent progression algorithm for selecting tasks from the queue.
Follows the devgo specification for deterministic task selection.
"""

import hashlib
import re
from collections import defaultdict, Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Task:
    """Represents a task with all its metadata."""
    agent: str
    description: str
    epic_name: str
    story_name: str
    original_line: str
    line_number: int
    epic_order: int
    story_order: int
    task_id: str

    def __post_init__(self):
        """Calculate task ID hash after initialization."""
        if not self.task_id:
            # Calculate SHA256 hash of lowercase trimmed full line up to acceptance criteria
            line_for_hash = self.original_line.strip().lower()
            # Remove acceptance criteria if present (lines after "**Acceptance**:")
            if "**acceptance**:" in line_for_hash:
                line_for_hash = line_for_hash.split("**acceptance**:")[0].strip()
            self.task_id = hashlib.sha256(line_for_hash.encode('utf-8')).hexdigest()[:12]


class DevGoTaskSelector:
    """Implements the devgo task selection algorithm."""
    
    def __init__(self, queue_file: Path, progress_file: Path, limit: int = 1):
        self.queue_file = queue_file
        self.progress_file = progress_file
        self.limit = limit
        self.agents = ["SYRA", "MAKA", "QRA", "LUA", "VIVA"]
        
    def parse_queue_file(self) -> List[Task]:
        """Parse the queue file and extract all unchecked tasks."""
        tasks = []
        
        with open(self.queue_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        current_epic = ""
        current_story = ""
        epic_order = 0
        story_order = 0
        
        # Pattern to match unchecked tasks: - [ ] (AGENT) Task description
        task_pattern = re.compile(r'^\s*-\s*\[\s*\]\s*\(([A-Z]+)\)\s+(.+)$')
        epic_pattern = re.compile(r'^### EPIC:\s+(.+)$')
        story_pattern = re.compile(r'^\s*-\s*STORY:\s+(.+)$')
        
        for line_num, line in enumerate(lines, 1):
            # Check for epic
            epic_match = epic_pattern.match(line)
            if epic_match:
                current_epic = epic_match.group(1).strip()
                epic_order += 1
                story_order = 0
                continue
                
            # Check for story
            story_match = story_pattern.match(line)
            if story_match:
                current_story = story_match.group(1).strip()
                story_order += 1
                continue
                
            # Check for task
            task_match = task_pattern.match(line)
            if task_match and current_epic and current_story:
                agent = task_match.group(1)
                description = task_match.group(2).strip()
                
                # Validate agent
                if agent in self.agents:
                    task = Task(
                        agent=agent,
                        description=description,
                        epic_name=current_epic,
                        story_name=current_story,
                        original_line=line.strip(),
                        line_number=line_num,
                        epic_order=epic_order,
                        story_order=story_order,
                        task_id=""  # Will be calculated in __post_init__
                    )
                    tasks.append(task)
        
        return tasks
    
    def get_tracked_tasks(self) -> Dict[str, str]:
        """Get currently tracked tasks from progress file."""
        tracked = {}
        
        if not self.progress_file.exists():
            return tracked
            
        with open(self.progress_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse entries to find STARTED tasks
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for STARTED entries
            if line.endswith(' STARTED') or line.endswith(' IN_PROGRESS'):
                # Parse the following lines for TaskID, Agent, and OriginalLine
                current_task_id = None
                current_original_line = None
                
                # Look ahead for TaskID and OriginalLine
                for j in range(i + 1, min(i + 10, len(lines))):  # Look ahead up to 10 lines
                    next_line = lines[j].strip()
                    
                    if next_line.startswith('TaskID: sha256:'):
                        current_task_id = next_line.split('sha256:')[1].strip()
                    elif next_line.startswith('OriginalLine: '):
                        current_original_line = next_line.split('OriginalLine: ')[1].strip()
                    elif next_line.startswith('###'):  # Start of next entry
                        break
                
                # Record the tracked task
                if current_task_id:
                    tracked[current_task_id] = 'STARTED'
                
                # Also track by our calculated hash for matching
                if current_original_line:
                    line_for_hash = current_original_line.strip().lower()
                    our_hash = hashlib.sha256(line_for_hash.encode('utf-8')).hexdigest()[:12]
                    tracked[our_hash] = 'STARTED'
            
            i += 1
                
        return tracked
    
    def filter_available_tasks(self, all_tasks: List[Task]) -> List[Task]:
        """Filter out tasks that are already tracked."""
        tracked_tasks = self.get_tracked_tasks()
        available_tasks = []
        
        for task in all_tasks:
            if task.task_id not in tracked_tasks:
                available_tasks.append(task)
                
        return available_tasks
    
    def group_tasks_by_agent(self, tasks: List[Task]) -> Dict[str, List[Task]]:
        """Group tasks by agent."""
        grouped = defaultdict(list)
        for task in tasks:
            grouped[task.agent].append(task)
        return dict(grouped)
    
    def calculate_agent_deficit(self, grouped_tasks: Dict[str, List[Task]]) -> Dict[str, int]:
        """Calculate agent deficit vs ideal uniform distribution."""
        total_tasks = sum(len(tasks) for tasks in grouped_tasks.values())
        if total_tasks == 0:
            return {}
            
        ideal_per_agent = total_tasks / len(self.agents)
        deficits = {}
        
        for agent in self.agents:
            current_count = len(grouped_tasks.get(agent, []))
            deficit = ideal_per_agent - current_count
            deficits[agent] = deficit
            
        return deficits
    
    def sort_tasks_stable(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks using stable ordering: Epic order, Story order, Line order."""
        return sorted(tasks, key=lambda t: (t.epic_order, t.story_order, t.line_number))
    
    def select_tasks_round_robin(self, grouped_tasks: Dict[str, List[Task]], 
                                deficits: Dict[str, int]) -> List[Task]:
        """Select tasks using round-robin starting with highest deficit."""
        selected = []
        
        # Sort agents by deficit (highest first), then by name for determinism
        agents_by_deficit = sorted(self.agents, key=lambda a: (-deficits.get(a, 0), a))
        
        # Sort tasks within each agent group
        for agent in grouped_tasks:
            grouped_tasks[agent] = self.sort_tasks_stable(grouped_tasks[agent])
        
        # Round-robin selection
        agent_indices = {agent: 0 for agent in self.agents}
        
        while len(selected) < self.limit:
            selected_this_round = False
            
            for agent in agents_by_deficit:
                if len(selected) >= self.limit:
                    break
                    
                agent_tasks = grouped_tasks.get(agent, [])
                agent_idx = agent_indices[agent]
                
                if agent_idx < len(agent_tasks):
                    selected.append(agent_tasks[agent_idx])
                    agent_indices[agent] += 1
                    selected_this_round = True
                    
            if not selected_this_round:
                break  # No more tasks available
                
        return selected
    
    def select_tasks(self) -> List[Task]:
        """Main task selection algorithm."""
        # Parse queue file
        all_tasks = self.parse_queue_file()
        
        # Filter available tasks (not already tracked)
        available_tasks = self.filter_available_tasks(all_tasks)
        
        if not available_tasks:
            return []
        
        # Group by agent
        grouped_tasks = self.group_tasks_by_agent(available_tasks)
        
        # Calculate agent deficits
        deficits = self.calculate_agent_deficit(grouped_tasks)
        
        # Select tasks using round-robin
        selected_tasks = self.select_tasks_round_robin(grouped_tasks, deficits)
        
        return selected_tasks
    
    def format_output(self, tasks: List[Task]) -> str:
        """Format selected tasks for output."""
        if not tasks:
            return "No tasks available for selection."
        
        timestamp = datetime.now(timezone.utc).isoformat()
        output = []
        
        output.append("DevGo Task Selection Results")
        output.append("=" * 40)
        output.append(f"Timestamp: {timestamp}")
        output.append(f"Selected Tasks: {len(tasks)}")
        output.append("")
        
        for i, task in enumerate(tasks, 1):
            output.append(f"Task {i}:")
            output.append(f"  TaskID: sha256:{task.task_id}")
            output.append(f"  Agent: {task.agent}")
            output.append(f"  Epic: {task.epic_name}")
            output.append(f"  Story: {task.story_name}")
            output.append(f"  Description: {task.description}")
            output.append(f"  Original Line: {task.original_line}")
            output.append(f"  Line Number: {task.line_number}")
            output.append(f"  Epic Order: {task.epic_order}")
            output.append(f"  Story Order: {task.story_order}")
            output.append(f"  Timestamp: {timestamp}")
            output.append("")
        
        return "\n".join(output)


def main():
    """Main entry point."""
    # File paths
    base_path = Path("/mnt/g/My Drive/AI/projects/merka/docs/progress/pmsort_20250903_1358")
    queue_file = base_path / "epic_stories_tasks_queue.md"
    progress_file = base_path / "epic_stories_tasks_progress.md"
    
    # Create selector
    selector = DevGoTaskSelector(queue_file, progress_file, limit=1)
    
    # Select tasks
    selected_tasks = selector.select_tasks()
    
    # Output results
    output = selector.format_output(selected_tasks)
    print(output)
    
    # Debug information
    if selected_tasks:
        print("\nDebug Information:")
        print("=" * 40)
        
        all_tasks = selector.parse_queue_file()
        available_tasks = selector.filter_available_tasks(all_tasks)
        grouped_tasks = selector.group_tasks_by_agent(available_tasks)
        deficits = selector.calculate_agent_deficit(grouped_tasks)
        
        print(f"Total tasks in queue: {len(all_tasks)}")
        print(f"Available tasks: {len(available_tasks)}")
        print("Tasks per agent:")
        for agent in selector.agents:
            count = len(grouped_tasks.get(agent, []))
            deficit = deficits.get(agent, 0)
            print(f"  {agent}: {count} tasks (deficit: {deficit:.2f})")


if __name__ == "__main__":
    main()