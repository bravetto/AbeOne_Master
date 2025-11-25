# AIGuardian External Dependencies Map

**Complete Dependency Architecture • Integration Patterns • Service Dependencies**

---

## 🗺️ **Dependency Overview**

AIGuardian integrates with multiple external services to provide a complete AI security platform. This document maps all external dependencies, their purposes, and integration patterns.

---

## 🏗️ **Core External Services**

### **1. Authentication & User Management**

#### **Clerk Authentication**
- **Purpose**: User authentication, session management, JWT tokens
- **Integration**: OAuth, social login, user profiles
- **Configuration**: 
  ```bash
  CLERK_SECRET_KEY=sk_live_...
  CLERK_PUBLISHABLE_KEY=pk_live_...
  ```
- **Endpoints**: 
  - User management: `https://api.clerk.com/v1/users`
  - JWT verification: Built-in middleware
- **Dependencies**: None
- **Status**: ✅ Production Ready

#### **JWT Token Management**
- **Purpose**: Secure API access, session validation
- **Integration**: Bearer token authentication
- **Configuration**:
  ```bash
  JWT_SECRET=your-jwt-secret
  JWT_ALGORITHM=HS256
  JWT_EXPIRATION=3600
  ```
- **Dependencies**: Clerk Authentication
- **Status**: ✅ Production Ready

---

### **2. Database & Storage**

#### **Neon Database (PostgreSQL)**
- **Purpose**: Primary database, user data, analytics
- **Integration**: Async PostgreSQL with connection pooling
- **Configuration**:
  ```bash
  DATABASE_URL=REPLACE_ME  ```
- **Features**:
  - Serverless scaling
  - Automatic backups
  - Connection pooling
  - SSL encryption
- **Dependencies**: None
- **Status**: ✅ Production Ready

#### **ElastiCache Redis**
- **Purpose**: Caching, session storage, rate limiting
- **Integration**: High-performance caching layer
- **Configuration**:
  ```bash
  REDIS_URL=redis=REPLACE_MEcluster-endpoint:6379/0
  ```
- **Features**:
  - Cluster mode
  - Persistence options
  - High availability
- **Dependencies**: None
- **Status**: ✅ Production Ready

---

### **3. Payment Processing**

#### **Stripe Payments**
- **Purpose**: Subscription management, payment processing
- **Integration**: Webhook-based event handling
- **Configuration**:
  ```bash
  STRIPE_SECRET_KEY=sk_live_...
  STRIPE_WEBHOOK_SECRET=whsec_...
  ```
- **Endpoints**:
  - Payment processing: Stripe API
  - Webhook handling: `/api/v1/webhooks/stripe`
- **Features**:
  - Subscription management
  - Payment processing
  - Webhook verification
  - Invoice generation
- **Dependencies**: None
- **Status**: ✅ Production Ready

---

### **4. Cloud Infrastructure**

#### **AWS Secrets Manager**
- **Purpose**: Secure configuration storage
- **Integration**: Runtime secret retrieval
- **Configuration**:
  ```bash
  AWS_REGION=us-east-1
  SECRETS_ARN=arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:codeguardians-gateway/production
  ```
- **Features**:
  - Encrypted storage
  - IAM-based access
  - Automatic rotation
- **Dependencies**: AWS IAM
- **Status**: ✅ Production Ready

#### **AWS ECS (Elastic Container Service)**
- **Purpose**: Container orchestration, auto-scaling
- **Integration**: Docker container deployment
- **Configuration**:
  ```bash
  ECS_CLUSTER=codeguardians-gateway-cluster
  ECS_SERVICE=codeguardians-gateway-service
  ```
- **Features**:
  - Auto-scaling
  - Load balancing
  - Health checks
  - Rolling deployments
- **Dependencies**: AWS ECR, AWS ALB
- **Status**: ✅ Production Ready

#### **AWS ECR (Elastic Container Registry)**
- **Purpose**: Docker image storage
- **Integration**: CI/CD pipeline integration
- **Configuration**:
  ```bash
  ECR_REGISTRY=ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
  ECR_REPOSITORY=codeguardians-gateway
  ```
- **Features**:
  - Image scanning
  - Vulnerability detection
  - Automated builds
- **Dependencies**: AWS IAM
- **Status**: ✅ Production Ready

#### **AWS ALB (Application Load Balancer)**
- **Purpose**: External traffic routing, SSL termination
- **Integration**: HTTP/HTTPS load balancing
- **Configuration**:
  ```bash
  ALB_DNS=your-alb-endpoint.us-east-1.elb.amazonaws.com
  SSL_CERTIFICATE_ARN=arn:aws:acm:us-east-1:ACCOUNT:certificate/cert-id
  ```
- **Features**:
  - SSL termination
  - Health checks
  - Path-based routing
- **Dependencies**: AWS ACM
- **Status**: ✅ Production Ready

---

### **5. Monitoring & Observability**

#### **CloudWatch Logs**
- **Purpose**: Centralized logging, log aggregation
- **Integration**: Structured logging
- **Configuration**:
  ```bash
  LOG_GROUP=/ecs/codeguardians-gateway
  LOG_STREAM_PREFIX=ecs
  ```
- **Features**:
  - Log aggregation
  - Search and filtering
  - Retention policies
- **Dependencies**: AWS ECS
- **Status**: ✅ Production Ready

#### **Prometheus Metrics**
- **Purpose**: Application metrics, performance monitoring
- **Integration**: Custom metrics collection
- **Configuration**:
  ```bash
  METRICS_ENDPOINT=/metrics
  METRICS_PORT=8000
  ```
- **Features**:
  - Custom metrics
  - Performance monitoring
  - Alerting rules
- **Dependencies**: None
- **Status**: ✅ Production Ready

---

## 🔄 **Dependency Flow Diagram**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AIGUARDIAN ECOSYSTEM                              │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                            CORE APPLICATION                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │   API       │  │   GUARD     │  │   HEALTH    │  │   METRICS   │      │ │
│  │  │   GATEWAY   │  │   SERVICES  │  │   MONITOR   │  │   COLLECTOR │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                             │
│                                    ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                            EXTERNAL SERVICES                              │ │
│  │                                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │   CLERK     │  │   NEON      │  │   STRIPE    │  │   REDIS     │      │ │
│  │  │   AUTH      │  │   DATABASE  │  │   PAYMENTS  │  │   CACHE     │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  │           │               │               │               │              │ │
│  │           └───────────────┼───────────────┼───────────────┘              │ │
│  │                           │               │                              │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │ │
│  │  │   AWS       │  │   AWS       │  │   AWS       │  │   AWS       │      │ │
│  │  │   SECRETS   │  │   ECS       │  │   ECR       │  │   ALB       │      │ │
│  │  │   MANAGER   │  │   CLUSTER   │  │   REGISTRY  │  │   LOAD      │      │ │
│  │  │             │  │             │  │             │  │   BALANCER  │      │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 **Dependency Matrix**

| Service | Type | Purpose | Status | Dependencies | Critical |
|---------|------|---------|--------|--------------|----------|
| **Clerk** | Auth | User management | ✅ Ready | None | High |
| **Neon DB** | Database | Data persistence | ✅ Ready | None | High |
| **Redis** | Cache | Session storage | ✅ Ready | None | Medium |
| **Stripe** | Payment | Billing | ✅ Ready | None | High |
| **AWS Secrets** | Config | Secret storage | ✅ Ready | IAM | High |
| **AWS ECS** | Infrastructure | Container orchestration | ✅ Ready | ECR, ALB | High |
| **AWS ECR** | Infrastructure | Image registry | ✅ Ready | IAM | High |
| **AWS ALB** | Infrastructure | Load balancing | ✅ Ready | ACM | High |
| **CloudWatch** | Monitoring | Logging | ✅ Ready | ECS | Medium |

---

## 🔧 **Configuration Management**

### **Environment Variables**
```bash
# Core Application
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY=<64-char-hex-string>

# Database (Neon)
DATABASE_ENABLED=true
DATABASE_URL=REPLACE_ME
# Cache (ElastiCache)
REDIS_URL=redis=REPLACE_MEcluster-endpoint:6379/0

# Authentication (Clerk)
CLERK_ENABLED=true
CLERK_SECRET_KEY=sk_live_...
CLERK_PUBLISHABLE_KEY=pk_live_...

# Payments (Stripe)
STRIPE_ENABLED=true
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# AWS Services
AWS_REGION=us-east-1
SECRETS_ARN=arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:codeguardians-gateway/production

# CORS & Security
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

### **AWS Secrets Manager Structure**
```json
{
  "SECRET_KEY": "64-character-hex-string",
  "DATABASE_URL": "postgresql+asyncpg://user:pass@ep-xxx.neon.tech/db?sslmode=require",
  "REDIS_URL": "redis=REPLACE_MEcluster-endpoint:6379/0",
  "ALLOWED_ORIGINS": "https://yourdomain.com,https://api.yourdomain.com",
  "ALLOWED_HOSTS": "yourdomain.com,api.yourdomain.com",
  "STRIPE_SECRET_KEY": "sk_live_your_stripe_secret_key",
  "STRIPE_WEBHOOK_SECRET": "whsec_your_webhook_secret",
  "CLERK_SECRET_KEY": "sk_live_your_clerk_secret_key",
  "CLERK_PUBLISHABLE_KEY": "pk_live_your_clerk_publishable_key",
  "AWS_REGION": "us-east-1",
  "ENVIRONMENT": "production"
}
```

---

## 🚀 **Deployment Architecture**

### **Production Deployment Flow**
```
1. Code Push → GitHub Actions
2. Build Docker Image → AWS ECR
3. Deploy to ECS → AWS ECS
4. Load Balance → AWS ALB
5. Monitor → CloudWatch
```

### **Service Dependencies**
```
AIGuardian API
├── Clerk (Authentication)
├── Neon DB (Database)
├── Redis (Cache)
├── Stripe (Payments)
└── AWS Services
    ├── Secrets Manager (Configuration)
    ├── ECS (Container Orchestration)
    ├── ECR (Image Registry)
    └── ALB (Load Balancing)
```

---

## 🧪 **Testing & Validation**

### **Dependency Health Checks**
```bash
# Test database connection
python -c "
import asyncpg
import asyncio

async def test_db():
    conn = await asyncpg.connect('$DATABASE_URL')
    result = await conn.fetchval('SELECT version()')
    print('Database:', result[:50] + '...')
    await conn.close()

asyncio.run(test_db())
"

# Test Redis connection
python -c "
import redis
r = redis.from_url('$REDIS_URL')
r.set('test', 'working')
print('Redis:', r.get('test').decode())
"

# Test Stripe API
python -c "
import stripe
stripe.api_key = '$STRIPE_SECRET_KEY'
balance = stripe.Balance.retrieve()
print('Stripe Balance:', balance.available[0].amount)
"

# Test Clerk API
curl https://api.clerk.com/v1/users \
  -H "Authorization: Bearer $CLERK_SECRET_KEY"
```

### **Integration Testing**
```bash
# Test complete API flow
curl -X POST https://your-api-domain.com/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"content": "Test content"},
    "user_id": "test-user"
  }'
```

---

## 🔒 **Security & Compliance**

### **Data Flow Security**
```
User Request → Clerk Auth → AIGuardian API → Guard Processing → Database (Neon)
                     ↓                                              ↓
              JWT Validation ←─────────────── Response ←──────────────┘
                     ↓
              Stripe Payment ←─────────────── Webhook Processing
                     ↓
              AWS Secrets ←─────────────── Configuration Retrieval
```

### **Security Measures**
- **Encryption at Rest**: Database encryption, Redis encryption
- **Encryption in Transit**: TLS/SSL for all communications
- **Authentication**: JWT tokens, API keys
- **Authorization**: Role-based access control
- **Audit Logging**: Comprehensive security event logging

---

## 📈 **Performance & Scalability**

### **Service Limits**
| Service | Limit | Scaling |
|---------|-------|---------|
| **Neon DB** | 1000 connections | Auto-scaling |
| **Redis** | 1000 ops/sec | Cluster mode |
| **Stripe** | 100 req/sec | Rate limiting |
| **Clerk** | 1000 users | Auto-scaling |
| **AWS ECS** | 1000 tasks | Auto-scaling |

### **Monitoring & Alerting**
- **Database**: Connection pool monitoring
- **Cache**: Memory usage, hit ratio
- **Payments**: Transaction success rate
- **Auth**: Login success rate
- **Infrastructure**: CPU, memory, network

---

## 🛠️ **Maintenance & Updates**

### **Regular Tasks**
- **Monthly**: Rotate API keys for all services
- **Weekly**: Review webhook delivery logs
- **Daily**: Monitor service health and usage

### **Update Procedures**
```bash
# Update secrets
aws secretsmanager update-secret \
  --secret-id codeguardians-gateway/production \
  --secret-string '{"STRIPE_SECRET_KEY":"new_key_here"}'

# Force ECS service redeployment
aws ecs update-service \
  --cluster codeguardians-gateway-cluster \
  --service codeguardians-gateway-service \
  --force-new-deployment
```

---

## 🆘 **Troubleshooting**

### **Common Issues**

#### **Database Connection Issues**
```bash
# Test connection
psql "$DATABASE_URL" -c "SELECT 1;"

# Check SSL mode
# Ensure sslmode=require in connection string
```

#### **Redis Connection Issues**
```bash
# Test Redis connectivity
redis-cli -h $REDIS_ENDPOINT ping

# Expected: PONG
```

#### **Stripe Webhook Failures**
```bash
# Check webhook logs
curl https://api.stripe.com/v1/events \
  -H "Authorization: Bearer $STRIPE_SECRET_KEY"

# Verify webhook signature
# Ensure STRIPE_WEBHOOK_SECRET is correct
```

#### **AWS Secrets Access**
```bash
# Test secrets access
aws secretsmanager get-secret-value \
  --secret-id codeguardians-gateway/production

# Check IAM permissions
aws sts get-caller-identity
```

---

## 📋 **Setup Checklist**

### **External Services Setup**
- [ ] **Stripe Account** - Payment processing & webhooks
- [ ] **Clerk Application** - User authentication & JWT
- [ ] **Neon Database** - PostgreSQL with connection pooling
- [ ] **AWS Secrets Manager** - Secure configuration storage
- [ ] **ElastiCache Redis** - High-performance caching
- [ ] **AWS ECS Cluster** - Container orchestration
- [ ] **AWS ECR Repository** - Docker image storage
- [ ] **AWS ALB** - Load balancing

### **Integration Testing**
- [ ] Environment variables configured
- [ ] Service connectivity verified
- [ ] API endpoints tested
- [ ] Authentication flow tested
- [ ] Payment flow tested
- [ ] Health checks passing
- [ ] Monitoring configured

---

This external dependencies map provides a comprehensive overview of all services, their purposes, and integration patterns. All dependencies are production-ready and follow security best practices.

**Last Updated**: 2025-10-23  
**Version**: 0.1.0  
**Status**: Production Ready
