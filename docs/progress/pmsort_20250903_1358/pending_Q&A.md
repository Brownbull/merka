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

## Answers
Q1 All Hispanic/Latino.
Q2 Balanced approach.
Q3 Unified approach, this will firstly be implemented in Villarrica, Chile.
Q4 Feature differentiation, aiming for simplicity in handling the app.
Q5 !EXPLAIN
Q6 90%.
Q7 !EXPLAIN
Q8 Our own spanish receipt categorization.
Q9 AWS scaling.
Q10 Offline-first.
Q11 Native fluency, using more icons than words, it should be like navigate into a game dashboard.
Q12 User choice, but the app will be in spanish or english, not a mix.
Q13 Formal spanish.
Q14 All the personal data must be stored locally only, the uploaded data for stats comparison must be unidentifiable.
Q15 !EXPLAIN
Q16 !EXPLAIN
Q17 Consider the Chilean tax code only.
Q18 Threshold based.
Q19 Freemium.
Q20 Flexible sharing.
Q21 Digital only.
Q22 Business associations.
Q23 no.
Q24 educational content.