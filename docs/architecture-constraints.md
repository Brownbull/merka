# Section 8: Architecture & Constraints

## 1. Architecture Components

### Core Pipeline Architecture
The receipt scanning system follows a modular pipeline pattern optimized for the Flask + React stack:

```
Mobile App/Web → API Gateway → Ingestion → OCR → Parser → Categorizer → Aggregator → Insights Engine
     ↓              ↓           ↓         ↓       ↓         ↓            ↓           ↓
  WhatsApp     Auth/Rate     Queue    Cloud     NLP      ML Model    Analytics    Dashboard
  Integration   Limiting     System   OCR API   Engine   Service     Store       API
```

#### Component Breakdown

**1. Ingestion Layer (Flask)**
- **Receipt Upload Service**: Multi-format image handling (JPEG, PNG, HEIC)
- **WhatsApp Integration**: Webhook receiver for receipt photos via WhatsApp Business API
- **Validation Service**: Image quality checks, format validation, size optimization
- **Queue Manager**: Celery-based async processing queue with Redis backend

**2. OCR Processing Layer (External + Flask)**
- **Primary OCR**: Google Cloud Vision API for Spanish text recognition
- **Fallback OCR**: Azure Computer Vision for redundancy
- **OCR Orchestrator**: Flask service managing API calls, retries, and response normalization
- **Quality Assessor**: Confidence score evaluation and retry logic

**3. Parsing & Extraction Layer (Flask + NLP)**
- **Text Preprocessor**: Spanish text cleaning, normalization, date parsing
- **Entity Extractor**: spaCy-based Spanish NLP for merchant, amount, date extraction
- **Receipt Structure Parser**: Pattern matching for different Mexican receipt formats
- **Validation Engine**: Business rules validation for extracted data

**4. Categorization Layer (Flask + ML)**
- **ML Categorizer**: scikit-learn model trained on Spanish merchant/product data
- **Rule Engine**: Fallback categorization using merchant name patterns
- **Learning System**: User feedback integration for model improvement
- **Category Mapper**: Spanish-first taxonomy with localized categories

**5. Aggregation & Storage Layer (PostgreSQL + Redis)**
- **Transaction Store**: PostgreSQL for persistent receipt data
- **Analytics Cache**: Redis for pre-computed spending aggregations
- **Time-Series Store**: Monthly/weekly spending patterns
- **User Preferences**: Category customizations and spending goals

**6. Insights Engine (Flask + Analytics)**
- **Spending Analyzer**: Monthly category breakdowns, trend analysis
- **Budget Monitor**: Goal tracking and overspending alerts
- **Pattern Detector**: Unusual spending pattern identification
- **Recommendation Engine**: Savings opportunities and category insights

**7. API & Frontend Layer (React)**
- **REST API**: Flask-RESTful endpoints for mobile and web clients
- **Real-time Updates**: WebSocket connections for processing status
- **Mobile-First UI**: React responsive design optimized for mobile
- **Spanish Localization**: Complete i18n support with Mexican Spanish

## 2. Performance SLOs (Service Level Objectives)

### Primary Performance Targets
Based on the 2-minute processing goal and mobile-first Spanish users:

#### End-to-End Processing SLOs
- **Receipt Upload → Processed Result**: p95 < 45 seconds, p99 < 90 seconds
- **OCR Turnaround Time**: p95 < 5 seconds, p99 < 12 seconds
- **Categorization Latency**: p95 < 2 seconds, p99 < 5 seconds
- **Insights Dashboard Load**: p95 < 1.5 seconds, p99 < 3 seconds

#### Mobile Responsiveness SLOs
- **Image Upload Progress**: Visual feedback within 200ms
- **Network Timeout Handling**: Graceful degradation after 30 seconds
- **Offline Queue**: Store up to 10 receipts for later processing
- **Low-Bandwidth Support**: <500KB payload per receipt upload

#### Accuracy & Reliability SLOs
- **OCR Accuracy**: >90% for Spanish receipts, >85% for mixed language
- **Categorization Accuracy**: >87% automated, <13% requiring user correction
- **Processing Success Rate**: >95% of uploads complete successfully
- **System Uptime**: 99.5% availability during peak hours (6 PM - 10 PM MX time)

#### Scalability SLOs
- **Concurrent Users**: Support 500 concurrent receipt uploads
- **Processing Queue**: Handle 1,000 receipts/hour during peak
- **Database Response**: <100ms for spending queries, <500ms for complex analytics
- **API Rate Limits**: 60 requests/minute per user, 10 uploads/minute

## 3. Security & Compliance

### Data Classification & Protection

#### PII Handling Requirements
- **Receipt Images**: Contain merchant names, amounts, dates, locations
- **User Data**: Names, spending patterns, financial behavior
- **Device Data**: IP addresses, device identifiers, usage patterns

#### Security Architecture
```
Internet → CloudFlare (DDoS) → Load Balancer → WAF → API Gateway
                                                        ↓
                                              Authorization Layer
                                                        ↓
                                              Application Services
                                                        ↓
                                        Encrypted Database (PostgreSQL)
```

#### Data Protection Measures
- **Encryption at Rest**: AES-256 for database, S3 bucket encryption
- **Encryption in Transit**: TLS 1.3 for all API communications
- **Image Storage**: Encrypted S3 buckets with 90-day auto-deletion
- **Database Security**: Row-level security, connection pooling with SSL

#### GDPR Compliance (International Users)
- **Right to Deletion**: Complete data purge within 30 days
- **Data Portability**: JSON export of all user data
- **Consent Management**: Granular permissions for data processing
- **Data Minimization**: 90-day automatic receipt image deletion

#### Authentication & Authorization
- **Multi-Factor Auth**: SMS-based 2FA for business accounts
- **Session Management**: JWT tokens with 24-hour expiry
- **API Security**: Rate limiting, API key rotation, request signing
- **Audit Logging**: Complete trail of all financial data access

### Privacy Protection
- **Data Anonymization**: Remove identifiable merchant details for analytics
- **User Isolation**: Complete data separation between users
- **Processing Logs**: No storage of receipt content in application logs
- **Third-Party APIs**: Minimal data sharing, no persistent storage

## 4. Data Flow Summary

### Source-to-Insights Pipeline

```
1. Receipt Source → 2. Ingestion → 3. OCR → 4. Parsing → 5. Enrichment → 6. Categorization → 7. Aggregation → 8. Insights
```

#### Detailed Flow Description

**Stage 1: Receipt Source**
- Mobile camera capture or WhatsApp photo upload
- Image preprocessing: compression, format standardization, quality validation
- Temporary storage in encrypted S3 bucket with metadata tagging

**Stage 2: Ingestion Service**
- Flask endpoint receives multipart upload
- Virus scanning and malicious content detection
- Queue job creation with user context and priority setting
- Real-time status updates via WebSocket to user interface

**Stage 3: OCR Processing**
- Primary: Google Cloud Vision API call with Spanish language hint
- Text extraction with confidence scores per text region
- Fallback to Azure Computer Vision if confidence < 70%
- Raw OCR response normalization and Spanish character correction

**Stage 4: Text Parsing**
- Spanish text preprocessing: accent normalization, currency symbol handling
- Named Entity Recognition using spaCy Spanish model (es_core_news_sm)
- Structured data extraction: merchant name, total amount, date, tax amounts
- Data validation against Mexican receipt format patterns

**Stage 5: Data Enrichment**
- Merchant name standardization using fuzzy matching
- Location data enrichment from Mexican business registry
- Product categorization hints from line-item text analysis
- Currency normalization and tax calculation validation

**Stage 6: Automated Categorization**
- ML model prediction using merchant features and spending history
- Rule-based fallback categorization for unknown merchants
- User preference integration and category customization
- Confidence scoring for categorization accuracy

**Stage 7: Aggregation Store**
- Transaction persistence in PostgreSQL with audit trail
- Real-time aggregation updates in Redis cache
- Time-series data generation for trend analysis
- User spending pattern calculation and storage

**Stage 8: Insights Query Engine**
- Pre-computed spending summaries by category and time period
- Trend analysis and anomaly detection for unusual spending
- Budget progress calculation and goal tracking
- Personalized recommendations based on spending patterns

### Processing State Management
- **Queued**: Receipt uploaded, waiting for OCR processing
- **Processing**: OCR and parsing in progress
- **Review**: Low confidence results requiring user validation
- **Completed**: Fully processed and categorized
- **Failed**: Processing errors requiring user intervention

## 5. Risk Identification

### Architecture Risks

#### OCR Accuracy Variability
- **Risk**: Spanish OCR accuracy degradation with poor image quality, handwritten receipts, thermal paper fading
- **Impact**: >13% manual corrections break 2-minute processing goal
- **Mitigation**: Multi-provider OCR fallback, image quality pre-screening, user guidance for photo capture

#### Receipt Format Diversity
- **Risk**: Mexican receipt formats vary significantly across regions and business types
- **Impact**: 15-20% parsing failures for non-standard receipt layouts
- **Mitigation**: Pattern learning system, user feedback integration, manual template creation for common formats

#### Category Taxonomy Drift
- **Risk**: User spending patterns and merchant names evolve, reducing categorization accuracy
- **Impact**: Classification accuracy drops below 87% threshold over time
- **Mitigation**: Continuous learning pipeline, monthly model retraining, user feedback integration

#### Privacy & Data Leakage
- **Risk**: Receipt images contain sensitive personal and business information
- **Impact**: GDPR violations, user trust loss, potential legal liability
- **Mitigation**: Automatic image deletion, encryption at rest, minimal data retention policies

#### Performance Under Load
- **Risk**: Processing queue bottlenecks during peak usage (evenings, weekends)
- **Impact**: SLO violations, user abandonment, negative reviews
- **Mitigation**: Auto-scaling queue workers, priority processing for premium users, load shedding

#### Third-Party API Dependencies
- **Risk**: Google Vision, WhatsApp Business API outages or rate limiting
- **Impact**: Complete processing pipeline failure
- **Mitigation**: Multi-provider fallback, circuit breakers, graceful degradation

#### Mobile Network Reliability
- **Risk**: Poor connectivity in rural Mexico affects upload success rates
- **Impact**: User frustration, incomplete receipt processing
- **Mitigation**: Offline queuing, progressive upload, retry mechanisms

### Business Continuity Risks
- **Single Point of Failure**: OCR processing dependency
- **Data Loss**: PostgreSQL corruption without proper backups
- **Scaling Costs**: Unexpected OCR API usage spikes
- **Regulatory Changes**: GDPR or Mexican data protection law updates

## 6. Infrastructure Constraints

### Flask Deployment Architecture

#### Recommended Deployment Stack
```
Load Balancer (Nginx) → Application Servers (Gunicorn + Flask) → Database (PostgreSQL)
                     → Background Workers (Celery) → Message Queue (Redis)
                     → File Storage (S3/MinIO) → CDN (CloudFlare)
```

#### Container-Based Deployment
- **Application Container**: Python 3.11 + Flask + Gunicorn
- **Worker Container**: Celery workers with OCR processing libraries
- **Database**: Managed PostgreSQL (RDS/Digital Ocean Managed DB)
- **Cache**: Redis cluster for session storage and job queues
- **File Storage**: S3-compatible object storage for receipt images

#### Cloud Provider Options

**Option 1: Digital Ocean (Cost-Effective)**
- App Platform for Flask API auto-scaling
- Managed PostgreSQL database
- Spaces for object storage
- Redis managed database
- CDN integration
- Estimated cost: $150-300/month for 1K users

**Option 2: AWS (Enterprise-Ready)**
- Elastic Beanstalk for Flask deployment
- RDS PostgreSQL with automated backups
- S3 for receipt image storage
- ElastiCache Redis for sessions/queues
- CloudFront CDN
- Estimated cost: $300-600/month for 1K users

**Option 3: Google Cloud (AI-Optimized)**
- Cloud Run for serverless Flask deployment
- Cloud SQL PostgreSQL
- Cloud Storage for images
- Memorystore Redis
- Vision API integration benefits
- Estimated cost: $200-400/month for 1K users

### Mobile API Responsiveness Requirements

#### Network Optimization
- **Response Compression**: Gzip compression for all API responses
- **Image Optimization**: Automatic resize and WebP conversion
- **Request Batching**: Combine multiple API calls where possible
- **Caching Headers**: Aggressive caching for static content and user data

#### Offline Capability Needs
- **Receipt Queue**: Local storage for up to 10 unprocessed receipts
- **Spending Data**: Cache last 30 days of categorized transactions
- **Sync Strategy**: Background sync when connectivity restored
- **Conflict Resolution**: User preference wins for categorization conflicts

### Scalability Constraints

#### Processing Bottlenecks
- **OCR API Limits**: Google Vision API has quota restrictions
- **Database Connections**: PostgreSQL connection pool sizing
- **Memory Usage**: Image processing requires significant RAM
- **Storage Growth**: Receipt images accumulate at 2MB/receipt average

#### Auto-Scaling Triggers
- **Queue Depth**: Scale workers when >50 jobs in queue
- **Response Time**: Scale API servers when p95 > 2 seconds
- **Memory Usage**: Scale when containers exceed 80% memory
- **Error Rate**: Alert when processing success rate < 95%

## 7. Integration Points

### WhatsApp Business API Integration
- **Webhook Endpoints**: Receive receipt photos via WhatsApp messages
- **Message Processing**: Extract media attachments and forward to processing pipeline
- **Response System**: Send processing status and results back to WhatsApp
- **Rate Limiting**: Handle WhatsApp API quotas and message limits

### Cloud OCR Services Integration
- **Primary Provider**: Google Cloud Vision API
  - Spanish language optimization
  - Handwritten text recognition
  - Receipt-specific OCR models
  - 99.9% SLA and global availability

- **Fallback Provider**: Azure Computer Vision
  - Alternative Spanish text recognition
  - Different accuracy characteristics
  - Cost optimization for lower-confidence images
  - Geographic redundancy

### Payment Processing for Premium Features
- **Payment Gateway**: Stripe integration for subscription billing
- **Mexican Payment Methods**: Support for OXXO, bank transfers, credit cards
- **Billing Cycles**: Monthly and annual subscription options
- **Feature Gating**: API-level premium feature restrictions

### Third-Party Services
- **SMS Provider**: Twilio for 2FA and notifications
- **Email Service**: SendGrid for transactional emails
- **Analytics**: Mixpanel for user behavior tracking
- **Error Monitoring**: Sentry for application error tracking
- **Uptime Monitoring**: Pingdom for service availability

### API Rate Limiting & Quotas
- **Google Vision API**: 600 requests/minute, 1800 requests/hour
- **WhatsApp Business**: 1000 messages/day for free tier
- **Stripe API**: 100 requests/second per account
- **Database Connections**: 100 concurrent connections per instance

This architecture document provides the foundation for implementing a scalable, secure receipt scanning system that meets the 2-minute processing target while addressing the unique constraints of Spanish-first mobile users and Mexican market requirements.