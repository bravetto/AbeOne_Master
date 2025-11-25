# AIGuardian - Secrets Configuration Guide

**Complete Guide for Secrets Management, Environment Variables, and Security Configuration**

*Last Updated: 2025-10-30*

---

##  **SECRETS MANAGEMENT OVERVIEW**

AIGuardian uses AWS Secrets Manager for production secrets with runtime injection via entrypoint scripts. This ensures secrets are never stored in container images or source code.

### Security Principles:
-  **Runtime Injection**: Secrets loaded at container startup
-  **No Build-time Secrets**: Images built without sensitive data
-  **Environment-based**: Different secrets for dev/staging/production
-  **Validation**: Pydantic-based configuration validation
-  **Access Control**: IAM-based secret access permissions

---

##  **REQUIRED SECRETS**

### Core Application Secrets (Required):

```json
{
  "SECRET_KEY": "REPLACE_ME",
  "ENVIRONMENT": "production",
  "DEBUG": "false",

  "DATABASE_URL": "postgresql+asyncpg://username:password@host:port/database_name",
  "POSTGRES_PASSWORD": "your-secure-database-password",

  "REDIS_URL": "REPLACE_MEhost:port/database",
  "REDIS_PASSWORD": "your-secure-redis-password",

  "ALLOWED_ORIGINS": "https://yourdomain.com,https://app.yourdomain.com",
  "ALLOWED_HOSTS": "yourdomain.com,api.yourdomain.com",

  "UNIFIED_API_KEY": "REPLACE_ME"
}
```

### Authentication Secrets (Clerk - Optional):

```json
{
  "CLERK_ENABLED": "true",
  "CLERK_SECRET_KEY": "sk_live_your_clerk_secret_key",
  "CLERK_PUBLISHABLE_KEY": "pk_live_your_clerk_publishable_key",
  "CLERK_WEBHOOK_SECRET": "whsec_your_webhook_secret"
}
```

### Payment Secrets (Stripe - Optional):

```json
{
  "STRIPE_ENABLED": "true",
  "STRIPE_SECRET_KEY": "sk_live_your_stripe_secret_key",
  "STRIPE_PUBLISHABLE_KEY": "pk_live_your_stripe_publishable_key",
  "STRIPE_WEBHOOK_SECRET": "whsec_your_stripe_webhook_secret",
  "STRIPE_PRICE_ID": "price_your_subscription_price_id"
}
```

### AWS Configuration (For Secrets Manager Access):

```json
{
  "AWS_SECRETS_ENABLED": "true",
  "AWS_SECRETS_NAME": "codeguardians-gateway/production",
  "AWS_REGION": "us-east-1"
}
```

---

##  **SECRETS SETUP PROCESS**

### 1. Generate Secure Secrets:

```bash
# Generate application secret key (64 characters)
SECRET_KEY=$(openssl rand -hex 32)
echo "SECRET_KEY: $SECRET_KEY"

# Generate database password
POSTGRES_REPLACE_ME rand -base64 32)
echo "POSTGRES_REPLACE_ME

# Generate Redis password
REDIS_REPLACE_ME rand -base64 32)
echo "REDIS_REPLACE_ME

# Generate API key
UNIFIED_API_KEY=$(openssl rand -hex 16)
echo "UNIFIED_API_KEY: $UNIFIED_API_KEY"
```

### 2. Create Secrets JSON File:

```bash
cat > secrets.json << EOF
{
  "SECRET_KEY": "$SECRET_KEY",
  "ENVIRONMENT": "production",
  "DEBUG": "false",
  "DATABASE_URL": "postgresql+asyncpg://user:$POSTGRES_PASSWORD@your-neon-host:5432/dbname",
  "POSTGRES_PASSWORD": "$POSTGRES_PASSWORD",
  "REDIS_URL": "REPLACE_MEyour-redis-host:6379/0",
  "REDIS_PASSWORD": "$REDIS_PASSWORD",
  "ALLOWED_ORIGINS": "https://yourdomain.com",
  "ALLOWED_HOSTS": "yourdomain.com",
  "UNIFIED_API_KEY": "$UNIFIED_API_KEY",
  "CLERK_ENABLED": "true",
  "CLERK_SECRET_KEY": "sk_live_your_clerk_secret_key",
  "CLERK_PUBLISHABLE_KEY": "pk_live_your_clerk_publishable_key",
  "CLERK_WEBHOOK_SECRET": "whsec_your_clerk_webhook_secret",
  "STRIPE_ENABLED": "true",
  "STRIPE_SECRET_KEY": "sk_live_your_stripe_secret_key",
  "STRIPE_PUBLISHABLE_KEY": "pk_live_your_stripe_publishable_key",
  "STRIPE_WEBHOOK_SECRET": "whsec_your_stripe_webhook_secret",
  "STRIPE_PRICE_ID": "price_your_subscription_price_id",
  "AWS_SECRETS_ENABLED": "true",
  "AWS_SECRETS_NAME": "codeguardians-gateway/production",
  "AWS_REGION": "us-east-1"
}
EOF
```

### 3. Create AWS Secrets Manager Secret:

```bash
# Create the secret
aws secretsmanager create-secret \
  --name codeguardians-gateway/production \
  --secret-string file://secrets.json \
  --region us-east-1 \
  --description "AIGuardian production secrets"

# Verify secret creation
aws secretsmanager describe-secret \
  --secret-id codeguardians-gateway/production \
  --region us-east-1
```

### 4. Configure IAM Permissions:

Create an IAM policy for ECS task execution:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:us-east-1:ACCOUNT-ID:secret:codeguardians-gateway/production-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:us-east-1:ACCOUNT-ID:log-group:/ecs/codeguardians-gateway:*",
        "arn:aws:logs:us-east-1:ACCOUNT-ID:log-group:/ecs/*:*"
      ]
    }
  ]
}
```

---

##  **ENTRYPOINT SCRIPT CONFIGURATION**

### Runtime Secrets Injection:

The gateway container uses an entrypoint script to load secrets at runtime:

```bash
#!/bin/bash
# Load secrets from AWS Secrets Manager
SECRETS=$(aws secretsmanager get-secret-value \
  --secret-id $AWS_SECRETS_NAME \
  --region $AWS_REGION \
  --query SecretString \
  --output text)

# Export secrets as environment variables
for key in $(echo $SECRETS | jq -r 'keys[]'); do
  value=$(echo $SECRETS | jq -r ".$key")
  export $key="$value"
done

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### ECS Task Definition Configuration:

```json
{
  "family": "codeguardians-gateway",
  "taskRoleArn": "arn:aws:iam::ACCOUNT-ID:role/ECSTaskRole",
  "executionRoleArn": "arn:aws:iam::ACCOUNT-ID:role/ECSTaskExecutionRole",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "codeguardians-gateway",
      "image": "ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/codeguardians-gateway:latest",
      "essential": true,
      "entryPoint": ["/app/entrypoint.sh"],
      "environment": [
        {
          "name": "AWS_SECRETS_ENABLED",
          "value": "true"
        },
        {
          "name": "AWS_SECRETS_NAME",
          "value": "codeguardians-gateway/production"
        },
        {
          "name": "AWS_REGION",
          "value": "us-east-1"
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
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

---

##  **WEBHOOK SECURITY CONFIGURATION**

### Stripe Webhooks:

#### 1. Configure Webhook Endpoint:
```bash
# In Stripe Dashboard > Webhooks
# Add endpoint: https://yourdomain.com/api/webhooks/stripe
# Select events: checkout.session.completed, invoice.payment_succeeded, etc.
```

#### 2. Environment Variables:
```bash
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_from_stripe_dashboard
STRIPE_WEBHOOK_TOLERANCE=300  # 5 minutes tolerance
```

#### 3. Webhook Verification:
```python
import stripe
from fastapi import HTTPException

async def verify_stripe_webhook(request: Request, body: bytes) -> dict:
    """Verify Stripe webhook signature"""
    sig_header = request.headers.get('stripe-signature')
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing signature")

    try:
        event = stripe.Webhook.construct_event(
            body, sig_header, STRIPE_WEBHOOK_SECRET
        )
        return event
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
```

### Clerk Webhooks:

#### 1. Configure Webhook Endpoint:
```bash
# In Clerk Dashboard > Webhooks
# Add endpoint: https://yourdomain.com/api/webhooks/clerk
# Select events: user.created, user.updated, user.deleted, etc.
```

#### 2. Environment Variables:
```bash
CLERK_WEBHOOK_SECRET=whsec_your_webhook_secret_from_clerk_dashboard
```

#### 3. Webhook Verification:
```python
import hmac
import hashlib
from fastapi import HTTPException

async def verify_clerk_webhook(request: Request, body: bytes) -> dict:
    """Verify Clerk webhook signature"""
    sig_header = request.headers.get('clerk-signature')
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing signature")

    # Parse signature components
    timestamp = sig_header.split(',')[0].split('=')[1]
    signatures = sig_header.split(',')[1].split('=')[1].split()

    # Verify timestamp (within 5 minutes)
    import time
    if abs(time.time() - int(timestamp)) > 300:
        raise HTTPException(status_code=400, detail="Timestamp too old")

    # Verify signature
    signed_payload = f"{timestamp}.{body.decode()}"
    expected_signature = hmac.new(
        CLERK_WEBHOOK_SECRET.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    if not any(hmac.compare_digest(expected_signature, sig) for sig in signatures):
        raise HTTPException(status_code=400, detail="Invalid signature")

    return json.loads(body)
```

---

##  **SECRETS VERIFICATION**

### Verify Secrets Loading:

```bash
# Check if secrets are loaded in container
docker exec -it container_name env | grep -E "(SECRET_KEY|DATABASE_URL|REDIS_URL)"

# Test database connection
docker exec -it container_name python -c "
import os
import asyncpg
async def test():
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    await conn.close()
    print('Database connection successful')
import asyncio
asyncio.run(test())
"

# Test Redis connection
docker exec -it container_name python -c "
import os
import redis
r = redis.from_url(os.getenv('REDIS_URL'))
r.ping()
print('Redis connection successful')
"
```

### Health Check Validation:

```bash
# Check application health
curl https://your-api-domain.com/health

# Check webhook endpoints
curl -X POST https://your-api-domain.com/api/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "stripe-signature: t=123456,v1=test_signature" \
  -d '{"type": "test"}'

curl -X POST https://your-api-domain.com/api/webhooks/clerk \
  -H "Content-Type: application/json" \
  -H "clerk-signature: t=123456,v1=test_signature" \
  -d '{"type": "test"}'
```

---

##  **SECRETS ROTATION**

### Rotate Application Secrets:

```bash
# Generate new secrets
NEW_SECRET_KEY=$(openssl rand -hex 32)
NEW_API_KEY=$(openssl rand -hex 16)

# Update secrets in AWS
aws secretsmanager update-secret \
  --secret-id codeguardians-gateway/production \
  --secret-string "{
    \"SECRET_KEY\": \"$NEW_SECRET_KEY\",
    \"UNIFIED_API_KEY\": \"$NEW_API_KEY\"
  }" \
  --region us-east-1

# Force ECS service deployment to pick up new secrets
aws ecs update-service \
  --cluster codeguardians-gateway-cluster \
  --service codeguardians-gateway-service \
  --force-new-deployment
```

### Rotate Database Credentials:

```bash
# Generate new password
NEW_DB_REPLACE_ME rand -base64 32)

# Update database password in Neon/AWS RDS
# Update secrets in AWS Secrets Manager
# Update DATABASE_URL with new password
# Force service restart
```

---

##  **DEVELOPMENT VS PRODUCTION**

### Development Environment:

For local development, use `.env` file instead of AWS Secrets Manager:

```bash
# .env file for development
SECRET_KEY=dev-secret-key-64-characters-long-for-testing-only
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/aiguardian_dev
POSTGRES_REPLACE_ME
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
ALLOWED_HOSTS=localhost
UNIFIED_API_KEY=dev-api-key
```

### Environment Detection:

The application automatically detects the environment:

```python
import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

if ENVIRONMENT == "production":
    # Use AWS Secrets Manager
    secrets = load_aws_secrets()
else:
    # Use environment variables directly
    secrets = os.environ
```

---

##  **SECURITY BEST PRACTICES**

### Secrets Management:
-  **Never commit secrets** to version control
-  **Use different secrets** for each environment
-  **Rotate secrets regularly** (at least quarterly)
-  **Monitor secret access** via CloudTrail
-  **Use least-privilege IAM** roles

### Application Security:
-  **Validate all inputs** and sanitize data
-  **Use HTTPS only** in production
-  **Implement rate limiting** and DDoS protection
-  **Log security events** for monitoring
-  **Regular security updates** and patches

### Webhook Security:
-  **Verify all webhook signatures** before processing
-  **Implement timestamp validation** (prevent replay attacks)
-  **Use secure webhook endpoints** (HTTPS only)
-  **Log webhook events** for debugging
-  **Handle webhook failures gracefully**

---

##  **RELATED DOCUMENTATION**

- **[EXTERNAL_SERVICES_SETUP.md](EXTERNAL_SERVICES_SETUP.md)** - Setting up Stripe, Clerk, Neon, Redis
- **[AWS_DEPLOYMENT_READINESS.md](AWS_DEPLOYMENT_READINESS.md)** - AWS infrastructure setup
- **[DEVOPS_GUIDE.md](DEVOPS_GUIDE.md)** - Complete production deployment
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

---

##  **TROUBLESHOOTING SECRETS ISSUES**

### Common Issues:

1. **Secrets Not Loading**:
   ```bash
   # Check IAM permissions
   aws sts get-caller-identity

   # Check secret exists
   aws secretsmanager describe-secret --secret-id codeguardians-gateway/production

   # Check CloudWatch logs for errors
   aws logs tail /ecs/codeguardians-gateway --follow
   ```

2. **Invalid Secret Format**:
   ```bash
   # Validate JSON format
   cat secrets.json | jq .

   # Check for special characters in passwords
   grep -E "(PASSWORD|SECRET)" secrets.json
   ```

3. **Webhook Verification Failing**:
   ```bash
   # Check webhook secrets are loaded
   docker exec container env | grep WEBHOOK

   # Test webhook signature manually
   # (Use Stripe/Clerk dashboard for test webhooks)
   ```

4. **Database Connection Issues**:
   ```bash
   # Test connection string
   docker exec container python -c "
   import os
   from sqlalchemy import create_engine
   engine = create_engine(os.getenv('DATABASE_URL'))
   engine.connect()
   print('Connection successful')
   "
   ```

---

** Secrets Configuration: COMPLETE AND SECURE**

All secrets properly configured with AWS Secrets Manager, webhook security implemented, and comprehensive validation procedures in place.
