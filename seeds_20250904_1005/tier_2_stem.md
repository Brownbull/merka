# Tier 2: Stem (Essential Features)
*Reliability & Mobile Experience - Building Market Readiness*

## Overview
**Duration**: 6 weeks | **Budget**: $28,000 | **Features**: 35% complete

The Stem tier transforms the MVP into a reliable, mobile-first platform. Users gain offline capability, dual OCR reliability, and comprehensive spending analytics. This tier creates market-ready functionality with professional-grade reliability.

## Essential Features

### 🔄 OCR Reliability & Failover
- **Tasks**: t012
- **Value**: Enterprise-grade reliability with Azure backup
- **Deliverable**: Automatic failover when Google Vision fails, <45s p95

### 📊 Spending Analytics Foundation  
- **Tasks**: t013, t018
- **Value**: Transform receipts into actionable spending insights
- **Deliverable**: PostgreSQL models + web dashboard with peso formatting

### 🧾 Mexican Receipt Intelligence
- **Tasks**: t015
- **Value**: Extract line items from Mexican receipt formats
- **Deliverable**: Parser handles date, merchant, items, prices, tax >85% accuracy

### 📱 Mobile-First Experience
- **Tasks**: t017
- **Value**: Native mobile app with offline queuing
- **Deliverable**: React Native app with camera integration + Spanish UI

### ✅ Quality Assurance Foundation
- **Tasks**: t021
- **Value**: Systematic OCR accuracy validation
- **Deliverable**: Comprehensive test suite with Mexican receipt corpus

## Task Breakdown

| Task ID | Agent | Description | Effort | Dependencies |
|---------|-------|-------------|--------|--------------|
| t012 | MAKA | Build Azure Computer Vision fallback OCR | 5 | t002, t011 |
| t013 | MAKA | Create PostgreSQL models for spending data | 6 | t004 |
| t015 | MAKA | Implement Mexican receipt format parser | 8 | t011 |
| t017 | MAKA | Create React Native mobile app | 10 | - |
| t018 | MAKA | Build React web dashboard with analytics | 8 | t013 |
| t021 | QRA | Create OCR accuracy validation test suite | 6 | t011, t012 |

**Total Effort**: 43 points across 6 tasks

## Agent Allocation

| Agent | Tasks | Effort Points | Focus Area |
|-------|-------|---------------|------------|
| **MAKA** | 5 | 37 | Core platform development |
| **QRA** | 1 | 6 | Quality assurance framework |

## Success Criteria

### Reliability & Performance
- [ ] **OCR Failover**: Automatic Azure fallback functional within 5 seconds
- [ ] **Processing Speed**: p95 <45 seconds end-to-end with dual providers
- [ ] **Mobile Performance**: App loads and queues receipts on 3G networks
- [ ] **Data Integrity**: Zero data loss during offline→online synchronization

### User Experience Enhancement
- [ ] **Line Item Extraction**: >85% accuracy extracting individual receipt items
- [ ] **Dashboard Speed**: Analytics load <2 seconds with peso formatting
- [ ] **Offline Capability**: Mobile app queues 50+ receipts offline
- [ ] **Spanish Interface**: Native Spanish UI rated >4.2/5.0 by users

### Technical Quality
- [ ] **Test Coverage**: >90% test coverage for OCR pipeline
- [ ] **Database Performance**: Analytics queries execute <500ms
- [ ] **Mobile App Store**: Ready for App Store/Play Store submission
- [ ] **Cross-Platform**: Web dashboard works on mobile browsers

## Feature Deep Dives

### Dual OCR Provider Architecture
**Primary**: Google Vision API (optimized for Mexican formats)  
**Fallback**: Azure Computer Vision (automatic when Google fails)
**Intelligence**: Route based on image quality and historical accuracy

### Mexican Receipt Parser Intelligence
- **Formats Supported**: Supermarket chains, gas stations, restaurants
- **Data Extracted**: Date, merchant name, line items, subtotal, tax, total
- **Validation**: Cross-reference totals, detect parsing errors
- **Regional Support**: Northern Mexico formats (Monterrey) vs Southern (Mexico City)

### Mobile-First Analytics
- **Dashboard Features**: Monthly spending, category breakdowns, trends
- **Peso Formatting**: Mexican currency display with proper thousands separators
- **Responsive Design**: Optimized for Mexican mobile screen preferences
- **Offline Sync**: Analytics update when connectivity restored

## Risk Mitigation

### Technical Risks
1. **Azure OCR Quality Differences**
   - *Testing*: Parallel processing to compare accuracy rates
   - *Optimization*: Provider-specific image preprocessing

2. **PostgreSQL Schema Changes**
   - *Mitigation*: Database migrations planned from Tier 1
   - *Versioning*: Backward-compatible analytics queries

3. **React Native Performance**
   - *Optimization*: Image compression and background uploading
   - *Testing*: Performance testing on Mexican Android devices

### User Experience Risks
1. **Receipt Parser Edge Cases**
   - *Solution*: Comprehensive Mexican receipt corpus collection
   - *Fallback*: Manual correction interface for failed parsing

2. **Mobile Data Usage Concerns**
   - *Optimization*: Image compression before upload
   - *Feature*: WiFi-only upload preference setting

## Dependencies & Integration

### Tier 1 Dependencies
- WhatsApp API webhook system (t009) → Mobile app integration
- Google Vision OCR (t011) → Baseline for dual provider comparison  
- PostgreSQL foundation (t013) → Analytics data models
- User authentication (t019) → Mobile app login

### New Infrastructure Requirements
- Azure Computer Vision API account
- React Native development environment  
- App Store developer accounts (iOS + Android)
- CDN setup for dashboard static assets

## Quality Gates

### Pre-Deployment Validation
- [ ] **Load Testing**: 1000 concurrent receipt uploads
- [ ] **Device Testing**: Top 10 Android devices in Mexico
- [ ] **Network Testing**: Performance on Telcel, Movistar, AT&T networks
- [ ] **Accuracy Testing**: 500+ Mexican receipts with manual validation

### User Acceptance Testing
- [ ] **Hispanic Beta Group**: 25 family testers in LA/Houston
- [ ] **Language Quality**: Native Spanish speaker UI review
- [ ] **Cultural Appropriateness**: Advisory board app review
- [ ] **Accessibility**: Basic screen reader compatibility

## Graduation Criteria

**Ready for Tier 3 when:**
- ✅ Dual OCR system maintains >90% combined accuracy
- ✅ Mobile app successfully submitted to App Store + Play Store
- ✅ Dashboard analytics provide actionable spending insights  
- ✅ Receipt parser handles 80% of Mexican receipt formats
- ✅ QRA test suite validates all reliability claims
- ✅ Beta user group achieves 50% weekly retention

## Market Positioning

With Tier 2 complete, Merka transitions from "interesting MVP" to "competitive product":

**Competitive Advantages Unlocked:**
- ✅ **Reliability**: Only Spanish-first app with dual OCR providers
- ✅ **Mobile-Native**: Offline-capable receipt processing
- ✅ **Mexican-Optimized**: Receipt parser trained on regional formats  
- ✅ **Analytics-Ready**: Spending insights in pesos with cultural categories

**Next**: Tier 3 adds ML-powered categorization, cultural validation, and user workflow optimization to achieve market leadership in Hispanic financial tools.