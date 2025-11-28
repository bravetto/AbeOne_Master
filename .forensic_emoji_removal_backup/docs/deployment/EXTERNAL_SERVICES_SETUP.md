# External Services Setup Guide

**Complete Setup Instructions for Stripe, Clerk, Neon, and AWS Services**

---

## 📋 Overview

This guide provides step-by-step instructions for setting up all external services required by AIGuardian:

- **Stripe** - Payment processing and subscriptions
- **Clerk** - User authentication and management
- **Neon** - Serverless PostgreSQL database
- **AWS Services** - ECS, Secrets Manager, ElastiCache

---

## 💳 Stripe Setup

### 1. Create Stripe Account
```bash
# Visit: https://dashboard.stripe.com/register
# Complete account verification and setup
```

### 2. Get API Keys
```bash
# In Stripe Dashboard:
# 1. Go to Developers → API Keys
# 2. Copy your keys:

# Publishable Key (starts with pk_live_ or pk_test_)
STRIPE_PUBLISHABLE_KEY=pk_live_...

# Secret Key (starts with sk_live_ or sk_test_)
STRIPE_SECRET_KEY=sk_live_...
```

### 3. Configure Webhooks
```bash
# In Stripe Dashboard:
# 1. Go to Developers → Webhooks
# 2. Click "Add endpoint"
# 3. Set URL: https://your-api-domain.com/api/v1/webhooks/stripe
# 4. Select events:
#    - checkout.session.completed
#    - invoice.payment_succeeded
#    - invoice.payment_failed
#    - customer.subscription.created
#    - customer.subscription.updated
#    - customer.subscription.deleted

# Copy the webhook signing secret
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 4. Create Products and Prices
```bash
# In Stripe Dashboard:
# 1. Go to Products
# 2. Create your subscription plans
# 3. Note the price IDs for each plan

# Example Price IDs:
PRICE_BASIC=price_...
PRICE_PRO=price_...
PRICE_ENTERPRISE=price_...
```

### 5. Test Integration
```bash
# Test webhook endpoint
curl -X POST https://your-api-domain.com/api/v1/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: t=123456,v1=test_signature" \
  -d '{"type":"checkout.session.completed","data":{"object":{"id":"cs_test_..."}}}'

# Expected: 200 OK response
```

---

## 🔐 Clerk Setup

### 1. Create Clerk Account
```bash
# Visit: https://clerk.com
# Sign up and create your application
```

### 2. Configure Application
```bash
# In Clerk Dashboard:
# 1. Go to your application
# 2. Configure authentication methods:
#    - Email & Password
#    - Social Providers (Google, GitHub, etc.)
# 3. Set up custom domain (optional)
```

### 3. Get API Keys
```bash
# In Clerk Dashboard:
# 1. Go to API Keys section
# 2. Copy your keys:

# Publishable Key (starts with pk_live_ or pk_test_)
CLERK_PUBLISHABLE_KEY=pk_live_...

# Secret Key (starts with sk_live_ or sk_test_)
CLERK_SECRET_KEY=sk_live_...
```

### 4. Configure JWT Settings
```bash
# In Clerk Dashboard:
# 1. Go to JWT Templates
# 2. Create a custom template for your app
# 3. Configure claims as needed

# Default JWT settings should work for most cases
```

### 5. Set Up Redirect URLs
```bash
# In Clerk Dashboard:
# 1. Go to Domains & URLs
# 2. Add your application URLs:
#    - Development: http://localhost:3000
#    - Production: https://yourdomain.com
# 3. Configure authorized redirect URLs
```

### 6. Test Authentication
```bash
# Test Clerk API
curl https://api.clerk.com/v1/users \
  -H "Authorization: Bearer $CLERK_SECRET_KEY"

# Expected: List of users or empty array
```

---

## 🗄️ Neon Database Setup

### 1. Create Neon Account
```bash
# Visit: https://neon.tech
# Sign up and create your account
```

### 2. Create Project
```bash
# In Neon Dashboard:
# 1. Click "Create a project"
# 2. Choose your region (match your AWS region)
# 3. Set project name: "aiguardian-prod"
```

### 3. Configure Database
```bash
# In your project:
# 1. Go to Databases
# 2. Create database: "aiguardian_db"
# 3. Create user: "aiguardian_user"
# 4. Set password for the user
```

### 4. Get Connection Details
```bash
# In Neon Dashboard:
# 1. Go to Connection Details
# 2. Copy the connection string:

# Connection String Format:
postgresql=REPLACE_MEep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# Extract components:
DATABASE_HOST=ep-xxx.us-east-1.aws.neon.tech
DATABASE_NAME=neondb
DATABASE_USER=aiguardian_user
DATABASE_PASSWORD=your_password_here
DATABASE_SSLMODE=require
```

### 5. Configure Connection Pooling (Optional)
```bash
# In Neon Dashboard:
# 1. Go to Connection Pooling
# 2. Enable connection pooling
# 3. Set pool size based on your needs
# 4. Get the pooled connection string

# Pooled Connection String:
postgresql=REPLACE_MEep-xxx-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### 6. Test Database Connection
```bash
# Test connection
psql "postgresql=REPLACE_MEep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require" \
  -c "SELECT version();"

# Expected: PostgreSQL version information
```

---

## ☁️ AWS Services Setup

### 1. AWS Secrets Manager

#### Create Secret
```bash
# Create the secrets JSON
cat > production-secrets.json << EOF
{
  "SECRET_KEY": "$(openssl rand -hex 32)",
  "DATABASE_URL": "postgresql+asyncpg://aiguardian_user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require",
  "REDIS_URL": "redis=REPLACE_MEyour-elasticache-endpoint:6379/0",
  "ALLOWED_ORIGINS": "https://yourdomain.com,https://api.yourdomain.com",
  "ALLOWED_HOSTS": "yourdomain.com,api.yourdomain.com",
  "STRIPE_SECRET_KEY": "sk_live_your_stripe_secret_key",
  "STRIPE_WEBHOOK_SECRET": "whsec_your_webhook_secret",
  "CLERK_SECRET_KEY": "sk_live_your_clerk_secret_key",
  "CLERK_PUBLISHABLE_KEY": "pk_live_your_clerk_publishable_key",
  "AWS_REGION": "us-east-1",
  "ENVIRONMENT": "production"
}
EOF

# Create AWS Secrets Manager secret
aws secretsmanager create-secret \
  --name "codeguardians-gateway/production" \
  --description "AIGuardian Production Secrets" \
  --secret-string file://production-secrets.json \
  --region us-east-1
```

#### Configure IAM Permissions
```bash
# Create IAM policy
cat > secrets-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT:secret:codeguardians-gateway/production*"
      ]
    }
  ]
}
EOF

# Create and attach policy
POLICY_ARN=$(aws iam create-policy \
  --policy-name AIGuardianSecretsAccess \
  --policy-document file://secrets-policy.json \
  --query 'Policy.Arn' \
  --output text)

aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn "$POLICY_ARN"
```

### 2. ElastiCache Redis Setup

#### Create Redis Cluster
```bash
# Create subnet group
aws elasticache create-cache-subnet-group \
  --cache-subnet-group-name aiguardian-redis-subnet \
  --cache-subnet-group-description "Subnet group for AIGuardian Redis" \
  --subnet-ids subnet-xxx subnet-yyy

# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id aiguardian-redis \
  --cache-node-type cache.t3.micro \
  --num-cache-nodes 1 \
  --engine redis \
  --cache-subnet-group-name aiguardian-redis-subnet \
  --security-group-ids sg-xxx \
  --snapshot-retention-limit 7

# Get Redis endpoint
REDIS_ENDPOINT=$(aws elasticache describe-cache-clusters \
  --cache-cluster-id aiguardian-redis \
  --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' \
  --output text)

# Set Redis password (optional but recommended)
REDIS_PASSWORD=REPLACE_ME rand -base64 32)
```

#### Test Redis Connection
```bash
# Test Redis connectivity
redis-cli -h $REDIS_ENDPOINT ping

# Expected: PONG
```

### 3. ECS Cluster Setup

#### Create ECS Resources
```bash
# Create ECS cluster
aws ecs create-cluster \
  --cluster-name codeguardians-gateway-cluster \
  --capacity-providers FARGATE FARGATE_SPOT \
  --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1

# Create CloudWatch log group
aws logs create-log-group \
  --log-group-name "/ecs/codeguardians-gateway" \
  --region us-east-1
```

#### Create Task Definition
```bash
# Create task definition JSON
cat > task-definition.json << EOF
{
  "family": "codeguardians-gateway",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [{
    "name": "gateway",
    "image": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/codeguardians-gateway:latest",
    "essential": true,
    "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
    "environment": [
      {"name": "ENVIRONMENT", "value": "production"},
      {"name": "DEBUG", "value": "false"},
      {"name": "LOG_LEVEL", "value": "INFO"},
      {"name": "DATABASE_ENABLED", "value": "true"},
      {"name": "CLERK_ENABLED", "value": "true"},
      {"name": "STRIPE_ENABLED", "value": "true"}
    ],
    "secrets": [
      {
        "name": "SECRET_KEY",
        "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT:secret:codeguardians-gateway/production:SECRET_KEY::"
      },
      {
        "name": "DATABASE_URL",
        "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT:secret:codeguardians-gateway/production:DATABASE_URL::"
      },
      {
        "name": "REDIS_URL",
        "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT:secret:codeguardians-gateway/production:REDIS_URL::"
      },
      {
        "name": "STRIPE_SECRET_KEY",
        "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT:secret:codeguardians-gateway/production:STRIPE_SECRET_KEY::"
      },
      {
        "name": "CLERK_SECRET_KEY",
        "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT:secret:codeguardians-gateway/production:CLERK_SECRET_KEY::"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/codeguardians-gateway",
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "ecs"
      }
    },
    "healthCheck": {
      "command": ["CMD-SHELL", "curl -f http://localhost:8000/health/live || exit 1"],
      "interval": 30,
      "timeout": 5,
      "retries": 3,
      "startPeriod": 60
    }
  }]
}
EOF

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

---

## 🔗 Integration Configuration

### Environment Variables Summary
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

# CORS & Security
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

### Service Dependencies
```mermaid
graph TB
    A[AIGuardian API] --> B[Clerk Auth]
    A --> C[Neon Database]
    A --> D[ElastiCache Redis]
    A --> E[Stripe Payments]
    A --> F[AWS Secrets Manager]

    B --> G[User Management]
    C --> H[Data Persistence]
    D --> I[Caching & Sessions]
    E --> J[Subscriptions & Payments]
    F --> K[Secure Configuration]
```

---

## 🧪 Testing Integrations

### 1. Test All Services
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
```

### 2. End-to-End Test
```bash
# Test complete API flow
curl -X POST https://your-api-domain.com/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "service_type": "tokenguard",
    "payload": {"text": "Test content"},
    "user_id": "test-user"
  }'

# Expected: Successful processing with all services integrated
```

---

## 📋 Setup Checklist

### Stripe Setup
- [ ] Account created and verified
- [ ] API keys obtained
- [ ] Webhooks configured
- [ ] Products and prices created
- [ ] Webhook endpoint tested

### Clerk Setup
- [ ] Account created
- [ ] Application configured
- [ ] API keys obtained
- [ ] Authentication methods set up
- [ ] Redirect URLs configured
- [ ] JWT settings verified

### Neon Setup
- [ ] Account created
- [ ] Project created
- [ ] Database configured
- [ ] User created with permissions
- [ ] Connection string obtained
- [ ] Connection tested

### AWS Setup
- [ ] Secrets Manager secret created
- [ ] IAM permissions configured
- [ ] ElastiCache Redis cluster created
- [ ] ECS cluster created
- [ ] Task definition registered
- [ ] All services tested

### Integration Testing
- [ ] Environment variables configured
- [ ] Service connectivity verified
- [ ] API endpoints tested
- [ ] Authentication flow tested
- [ ] Payment flow tested

---

## 🆘 Troubleshooting

### Common Issues

#### Stripe Webhook Failures
```bash
# Check webhook logs
curl https://api.stripe.com/v1/events \
  -H "Authorization: Bearer $STRIPE_SECRET_KEY"

# Verify webhook signature
# Ensure STRIPE_WEBHOOK_SECRET is correct
```

#### Clerk Authentication Errors
```bash
# Test Clerk API
curl https://api.clerk.com/v1/users \
  -H "Authorization: Bearer $CLERK_SECRET_KEY"

# Check JWT token validity
# Verify CLERK_PUBLISHABLE_KEY in frontend
```

#### Neon Connection Issues
```bash
# Test connection
psql "$DATABASE_URL" -c "SELECT 1;"

# Check SSL mode
# Ensure sslmode=require in connection string
```

#### AWS Secrets Access
```bash
# Test secrets access
aws secretsmanager get-secret-value \
  --secret-id codeguardians-gateway/production

# Check IAM permissions
aws sts get-caller-identity
```

---

## 🔄 Maintenance & Updates

### Regular Tasks
- **Monthly**: Rotate API keys for all services
- **Weekly**: Review webhook delivery logs
- **Daily**: Monitor service health and usage

### Updating Secrets
```bash
# Update individual secret values
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

**All external services are now fully configured and ready for production use!** 🎉</content>
<parameter name="filePath">c:\Users\jimmy\.cursor\AIGuards-Backend-1\EXTERNAL_SERVICES_SETUP.md