# Pending Questions & Decision Points (pmsort snapshot: 2025-09-03 13:58)

<!--
Source files:
- PRD.md (hash: d61f9f075aefacb5f16a69f41725ff57)
- PRD.refined.md (hash: 4844089a8d0a1438198c286c0fe10fa2)
Generation timestamp: 2025-09-03T13:58:00Z
pmsort command execution: /pmsort
-->

| ID | Topic | Question / Decision | Options (if any) | Proposed Owner | Priority | Source Ref |
|----|-------|---------------------|------------------|----------------|----------|------------|
| Q1 | Market Strategy | Should we target Mexican-Americans specifically or broader Hispanic/Latino community initially? | Focused (Mexican-Americans) vs. Broad (All Hispanic/Latino) | VIVA | P1 | PRD.refined.md:1842 |
| Q2 | Market Strategy | What's the optimal balance between US-born Hispanic families vs. recent Mexican immigrants? | US-born focus vs. Recent immigrant focus vs. Balanced approach | VIVA + Community Advisory Board | P1 | PRD.refined.md:1848 |
| Q3 | Cultural Strategy | How do we handle regional Mexican cultural differences (Northern vs. Southern Mexico origins)? | Unified approach vs. Regional customization | QRA + LUA | P2 | PRD.refined.md:1854 |
| Q4 | Competitive Strategy | How do we respond when major competitors (Mint, YNAB) add Spanish language support? | Feature differentiation vs. Cultural authenticity vs. Partnership | VIVA + MAKA | P1 | PRD.refined.md:1861 |
| Q5 | Partnership Strategy | Should we partner with or compete against existing Hispanic fintech companies? | Partnership vs. Competition vs. Hybrid approach | VIVA + Business Development | P2 | PRD.refined.md:1867 |
| Q6 | Technical Strategy | What OCR accuracy threshold justifies the cost vs. manual entry alternative? | 85% vs. 90% vs. 95% accuracy thresholds | SYRA + VIVA | P1 | PRD.refined.md:1876 |
| Q7 | Technical Implementation | How do we handle receipt formats from small Mexican businesses that don't fit standard patterns? | Custom parsing vs. Crowdsourced training vs. Manual fallback | SYRA + MAKA | P2 | PRD.refined.md:1882 |
| Q8 | Technical Strategy | Should we build our own Spanish receipt categorization model or enhance existing providers? | Build custom vs. Enhance existing vs. Hybrid approach | SYRA + MAKA | P1 | PRD.refined.md:1888 |
| Q9 | Infrastructure | What's our cloud infrastructure strategy for handling peak usage during tax season? | AWS scaling vs. Multi-cloud vs. Dedicated resources | SYRA + VIVA | P2 | PRD.refined.md:1895 |
| Q10 | Performance | How do we optimize for Mexican network infrastructure and device limitations? | Progressive loading vs. Offline-first vs. Lite version | SYRA + LUA | P1 | PRD.refined.md:1901 |
| Q11 | Localization | What level of Spanish language sophistication should we target (elementary vs. native fluency)? | Elementary (6th grade) vs. Native fluency vs. Adaptive | QRA + Community Advisory Board | P2 | PRD.refined.md:1910 |
| Q12 | User Experience | How do we handle users who prefer English for financial terms but Spanish for interface? | Hybrid language mode vs. Full localization vs. User choice | QRA + MAKA | P2 | PRD.refined.md:1916 |
| Q13 | Cultural Strategy | Should we include Mexican slang and regional expressions or maintain formal Spanish? | Formal Spanish vs. Regional slang vs. Context-adaptive | QRA + Community Advisory Board | P3 | PRD.refined.md:1922 |
| Q14 | User Experience | How do we balance individual privacy with Hispanic family financial transparency expectations? | Individual privacy vs. Family transparency vs. Configurable levels | LUA + QRA | P1 | PRD.refined.md:1929 |
| Q15 | Market Strategy | What's the appropriate way to handle remittance and cross-border family financial support? | Track remittances vs. Exclude vs. Optional feature | VIVA + QRA | P2 | PRD.refined.md:1935 |
| Q16 | Compliance | What specific Mexican data protection requirements apply to US-based app serving Mexican nationals? | Mexican compliance vs. US compliance vs. Dual compliance | SYRA + Legal Counsel | P1 | PRD.refined.md:1944 |
| Q17 | Tax Strategy | How do we handle tax implications for users who earn income in both US and Mexico? | Dual tax tracking vs. Disclaimer vs. Professional referral | VIVA + Legal/Tax Advisory | P2 | PRD.refined.md:1950 |
| Q18 | Compliance | What anti-money laundering or financial monitoring requirements might apply? | Full AML compliance vs. Basic monitoring vs. Threshold-based | SYRA + Legal Counsel | P1 | PRD.refined.md:1956 |
| Q19 | Monetization | What pricing sensitivity exists in Hispanic market for financial tools vs. mainstream market? | Premium pricing vs. Freemium vs. Community-based | VIVA + Community Research | P1 | PRD.refined.md:1965 |
| Q20 | Product Strategy | Should we offer family plans that accommodate extended Hispanic family structures? | Nuclear family focus vs. Extended family plans vs. Flexible sharing | VIVA + QRA | P2 | PRD.refined.md:1971 |
| Q21 | Monetization | How do we handle users who prefer cash payments for app subscriptions (cultural preference)? | Cash payment options vs. Digital only vs. Partner integration | VIVA + SYRA | P2 | PRD.refined.md:1977 |
| Q22 | Growth Strategy | Which Hispanic community organizations provide most authentic pathway to user acquisition? | Churches vs. Community centers vs. Business associations | VIVA + Community Relations | P2 | PRD.refined.md:1986 |
| Q23 | Partnership Strategy | Should we partner with Mexican consulates for financial literacy programming? | Government partnership vs. Independent vs. NGO collaboration | VIVA + Community Relations | P3 | PRD.refined.md:1992 |
| Q24 | Distribution Strategy | What role should Hispanic financial advisors and tax preparers play in our distribution strategy? | Professional referrals vs. B2B partnership vs. Educational content | VIVA + Business Development | P2 | PRD.refined.md:1998 |

## Answers Done
Q1 All Hispanic/Latino.
Q2 Balanced approach.
Q3 Unified approach, this will firstly be implemented in Villarrica, Chile.
Q4 Feature differentiation, aiming for simplicity in handling the app.
Q5 Competition for now.
Q6 90%.
Q7 Crowdsourced Training.
Q8 Our own spanish receipt categorization.
Q9 AWS scaling.
Q10 Offline-first.
Q11 Native fluency, using more icons than words, it should be like navigate into a game dashboard.
Q12 User choice, but the app will be in spanish or english, not a mix.
Q13 Formal spanish.
Q14 All the personal data must be stored locally only, the uploaded data for stats comparison must be unidentifiable.
Q15 Exclude Remittances.
Q16 Only any applicable Chilean compliance requirements.
Q17 Consider the Chilean tax code only.
Q18 Threshold based.
Q19 Freemium.
Q20 Flexible sharing.
Q21 Digital only.
Q22 Business associations.
Q23 no.
Q24 educational content.

## Questions Explained (Archived 2025-09-03)

### Q5: Partnership Strategy - Should we partner with or compete against existing Hispanic fintech companies?

**Strategic Analysis:**
The partnership vs. competition decision requires evaluating market dynamics, resource allocation, and competitive positioning in the Hispanic fintech space.

**Reasoning:**
- **Partnership Benefits**: Faster market entry, shared customer acquisition costs, established trust relationships, complementary capabilities
- **Competition Benefits**: Full control over user experience, 100% revenue capture, differentiated positioning, brand ownership
- **Market Reality**: Hispanic fintech market is fragmented with no dominant player, creating opportunity for both approaches

**Impact Analysis:**
- **Partnership**: Lower risk, faster validation, but potential feature conflicts and revenue sharing
- **Competition**: Higher investment required, longer time to market, but full strategic control
- **Hybrid Approach**: Selective partnerships for distribution while competing on core features

**Recommendation Options:**
1. **Strategic Partnerships**: Partner for distribution (tax preparers, community organizations) while competing on core financial management
2. **Technology Partnerships**: Integrate with established payment processors while owning the user experience
3. **Competitive Focus**: Build proprietary advantages in cultural authenticity and Spanish-first experience

**Additional Considerations:**
- Monitor competitive responses from major fintech companies adding Spanish support
- Evaluate partnership opportunities with Mexican financial institutions for cross-border features
- Consider white-label opportunities with Hispanic-serving organizations

---

### Q7: Technical Implementation - How do we handle receipt formats from small Mexican businesses that don't fit standard patterns?

**Technical Analysis:**
Small Mexican businesses often use non-standard receipt formats, handwritten receipts, or simplified formats that challenge traditional OCR and categorization systems.

**Reasoning:**
- **Custom Parsing**: Build specialized models for Mexican receipt patterns, including handwritten text recognition
- **Crowdsourced Training**: Leverage user corrections to continuously improve recognition accuracy
- **Manual Fallback**: Provide streamlined manual entry with smart suggestions and templates

**Impact Analysis:**
- **Custom Parsing**: High development cost, ongoing maintenance, but superior user experience
- **Crowdsourced Training**: Lower initial cost, community engagement, but requires user participation incentives
- **Manual Fallback**: Immediate solution, lower technical complexity, but increased user friction

**Technical Implementation Strategy:**
1. **Phase 1**: Implement manual fallback with smart templates for common Mexican business types
2. **Phase 2**: Build crowdsourced training system where users verify and correct OCR results
3. **Phase 3**: Develop custom models based on collected data patterns

**Additional Technical Considerations:**
- Support for Spanish text extraction with Mexican-specific terms and abbreviations
- Handle mixed-language receipts (Spanish/English) common in border regions
- Optimize for low-quality images from budget smartphones
- Create templates for common Mexican business categories (taquerias, tiendas, farmacias)

**User Experience Mitigation:**
- Gamify the correction process with points/badges for improving recognition accuracy
- Provide visual feedback showing how user corrections help the entire community
- Offer bulk correction tools for users with multiple similar receipts

---

### Q15: Market Strategy - What's the appropriate way to handle remittance and cross-border family financial support?

**Market Analysis:**
Remittances are a critical financial flow for Mexican-American families, representing $60+ billion annually. This presents both opportunity and complexity for financial management apps.

**Strategic Reasoning:**
- **Track Remittances**: Provides complete financial picture, enables better budgeting and family financial planning
- **Exclude Remittances**: Avoids regulatory complexity and focuses on domestic financial management
- **Optional Feature**: Allows users to choose based on their family situation and comfort level

**Impact Analysis:**
- **Tracking Benefits**: Complete financial visibility, family budget coordination, remittance optimization insights
- **Tracking Challenges**: Regulatory compliance (AML, international transfers), privacy concerns, technical complexity
- **Market Opportunity**: Significant differentiation from mainstream apps that ignore this major expense category

**Implementation Strategy:**
1. **Phase 1**: Optional remittance tracking with manual entry and categorization
2. **Phase 2**: Integration with major remittance providers (Western Union, Remitly, Wise) for automatic tracking
3. **Phase 3**: Advanced features like family budget sharing and remittance optimization suggestions

**Compliance Considerations:**
- Partner with established remittance providers rather than facilitating transfers directly
- Implement appropriate AML monitoring for large or frequent transfers
- Ensure data protection for cross-border family financial information

**Cultural Sensitivity:**
- Recognize remittances as cultural obligation, not discretionary spending
- Provide family-oriented budgeting tools that account for extended family support
- Offer privacy controls for sensitive family financial relationships

---

### Q16: Compliance - What specific Mexican data protection requirements apply to US-based app serving Mexican nationals?

**Regulatory Analysis:**
Mexican data protection landscape involves multiple frameworks affecting US-based apps serving Mexican users, particularly around financial data.

**Legal Framework:**
- **LFPDPPP (Mexican Federal Data Protection Law)**: Applies when processing personal data of Mexican residents
- **Fintech Law**: Specific requirements for financial technology companies operating in Mexico
- **Cross-Border Considerations**: US-Mexico data transfer agreements and safe harbor provisions

**Compliance Impact:**
- **Mexican Compliance**: Required if targeting Mexican residents or marketing in Mexico
- **US Compliance**: CCPA, financial regulations apply regardless
- **Dual Compliance**: Most comprehensive approach but highest cost and complexity

**Risk Assessment:**
- **High Risk**: Serving Mexican nationals without Mexican compliance
- **Medium Risk**: US-only compliance with Mexican user base
- **Low Risk**: Full dual compliance with proper legal framework

**Implementation Strategy:**
1. **Immediate**: Engage Mexican data protection counsel for specific requirements assessment
2. **Short-term**: Implement privacy controls meeting both US and Mexican standards
3. **Long-term**: Consider Mexican entity for direct compliance if user base justifies

**Technical Requirements:**
- Data localization requirements for Mexican financial data
- Consent mechanisms compliant with Mexican standards
- Right to erasure and data portability implementations
- Cross-border transfer agreements with cloud providers

**Operational Considerations:**
- Privacy policy translations and Mexican-specific terms
- User consent flows adapted to Mexican legal requirements
- Data breach notification procedures for both jurisdictions
- Regular compliance audits covering both regulatory frameworks