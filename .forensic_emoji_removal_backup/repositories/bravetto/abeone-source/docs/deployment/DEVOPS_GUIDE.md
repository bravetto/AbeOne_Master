# AIGuardian DevOps & Deployment Guide

**Complete Production Deployment • AWS Infrastructure • Monitoring & Troubleshooting**

---

## 📚 Quick Navigation

| Document | Audience | Purpose |
|----------|----------|---------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | **Users** | Quick start and testing guide |
| **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** | **Developers** | Development setup and contribution |
| **[DEVOPS_GUIDE.md](DEVOPS_GUIDE.md)** | **DevOps** | Production deployment and AWS setup |
| **[USER_GUIDE.md](USER_GUIDE.md)** | **End Users** | Simple API usage and examples |

---

## 🚀 Quick Start (5 Steps)

### Step 1: Verify Prerequisites
```bash
# Check AWS CLI
aws --version

# Check Docker
docker --version

# Verify AWS credentials
aws sts get-caller-identity
```

### Step 2: Set Environment Variables
```bash
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export TAG=latest
```

### Step 3: Push All Containers to ECR
```bash
bash scripts/push-all-to-ecr.sh
```
**Time:** ~30-45 minutes

### Step 4: Create AWS Secrets Manager Secret
```bash
# Generate secrets
SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=REPLACE_ME rand -hex 16)
REDIS_PASSWORD=REPLACE_ME rand -hex 16)
UNIFIED_API_KEY=$(openssl rand -hex 32)

# Create secrets.json with your actual values
cat > secrets.json << EOF
{
  "SECRET_KEY": "$SECRET_KEY",
  "POSTGRES_PASSWORD": "$POSTGRES_PASSWORD",
  "REDIS_PASSWORD": "$REDIS_PASSWORD",
  "DATABASE_URL": "YOUR_DATABASE_URL_HERE",
  "REDIS_URL": "YOUR_REDIS_URL_HERE",
  "UNIFIED_API_KEY": "$UNIFIED_API_KEY",
  "ALLOWED_ORIGINS": "https://yourdomain.com",
  "ALLOWED_HOSTS": "yourdomain.com"
}
EOF

# Create secret
aws secretsmanager create-secret \
  --name codeguardians-gateway/production \
  --secret-string file://secrets.json \
  --region $AWS_REGION
```

### Step 5: Deploy to ECS
```bash
# Create ECS cluster (if not exists)
aws ecs create-cluster \
  --cluster-name codeguardians-gateway-cluster \
  --region $AWS_REGION || true

# Use deployment scripts or follow detailed steps below
```

---

## 🏗️ Architecture Overview

### Multi-Container Architecture

The AIGuards Backend uses a **multi-container microservices architecture** where all guard services route through a single gateway container.

#### Container Structure
- **1 Gateway Container** (`codeguardians-gateway`) - Routes all requests
- **5 Guard Service Containers** (tokenguard, trustguard, contextguard, biasguard, healthguard)
- **2 Infrastructure Containers** (postgres, redis)
- **4 Monitoring Containers** (elasticsearch, kibana, prometheus, grafana)

**Total: 12 containers** (all run in dev environment, DevOps handles production)

#### Network Architecture
- All containers communicate via Docker network: `aiguards-network`
- **Only gateway exposes external port** (8000)
- Guard services are **internal-only** (accessed via gateway)
- Gateway performs request routing, load balancing, and health checks

#### Guard Services

| Service | Port | Purpose | Directory |
|---------|------|----------|-----------|
| **TokenGuard** | 8001 | Token optimization & cost management | `guards/tokenguard/` |
| **TrustGuard** | 8002 | Trust validation & reliability | `guards/trust-guard/` |
| **ContextGuard** | 8003 | Context drift detection & memory management | `guards/contextguard/` |
| **BiasGuard** | 8004 | Bias detection & content analysis | `guards/biasguard-backend/` |
| **HealthGuard** | 8005 | Health monitoring & validation | `guards/healthguard/` |

---

## 🔐 Prerequisites

### Required Tools
- Docker & Docker Compose
- AWS CLI configured
- AWS Secrets Manager access
- ECS/EKS cluster (for containerized deployment)
- RDS PostgreSQL database (or Neon)
- ElastiCache Redis cluster (optional)

### Required AWS Resources

**Must Have:**
- ✅ ECR Repositories (6)
- ✅ ECS Cluster
- ✅ ECS Task Definitions (6)
- ✅ ECS Services (6)
- ✅ AWS Secrets Manager Secret
- ✅ IAM Roles (Task Execution + Task Role)
- ✅ CloudWatch Log Groups (6)
- ✅ VPC & Security Groups

**Optional but Recommended:**
- ⚠️ Application Load Balancer
- ⚠️ RDS PostgreSQL (or use Neon)
- ⚠️ ElastiCache Redis (or use external)
- ⚠️ CloudWatch Alarms
- ⚠️ Route 53 DNS

---

## 🔧 Pre-Deployment Configuration

### 1. Generate Production Secrets

```bash
# Option A: Use the deploy script
./scripts/deploy.sh setup-secrets

# Option B: Manual generation
export SECRET_KEY=$(openssl rand -hex 32)
export POSTGRES_PASSWORD=REPLACE_ME rand -base64 32 | tr -d "=+/" | cut -c1-25)
export REDIS_PASSWORD=REPLACE_ME rand -base64 32 | tr -d "=+/" | cut -c1-25)
```

### 2. Configure Required Environment Variables

**Absolute Minimum (Container will start):**
```bash
SECRET_KEY=REPLACE_ME
ALLOWED_ORIGINS=https://yourdomain.com
DATABASE_ENABLED=false  # or true with DATABASE_URL
```

**Recommended Production:**
```bash
# Core
ENVIRONMENT=production
SECRET_KEY=<generated-secure-key>
DEBUG=false
LOG_LEVEL=INFO

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com

# Database
DATABASE_ENABLED=true
DATABASE_URL=REPLACE_ME
# Redis (optional but recommended)
REDIS_URL=redis=REPLACE_MEelasticache-endpoint:6379/0

# Optional integrations
CLERK_ENABLED=false
STRIPE_ENABLED=false

# AWS Secrets Manager
AWS_SECRETS_ENABLED=true
AWS_SECRETS_NAME=codeguardians-gateway/production
AWS_REGION=us-east-1
```

### 3. Create AWS Resources

```bash
# Create ECR repository
aws ecr create-repository \
  --repository-name codeguardians-gateway \
  --region us-east-1

# Create ECS cluster
aws ecs create-cluster \
  --cluster-name codeguardians-gateway-cluster \
  --region us-east-1
```

---

## ☁️ AWS Secrets Manager Setup

### Required Secrets in AWS Secrets Manager

Store these secrets in AWS Secrets Manager under `codeguardians-gateway/production`:

```json
{
  "SECRET_KEY": "REPLACE_ME",
  "POSTGRES_PASSWORD": "your-secure-database-password",
  "REDIS_PASSWORD": "your-secure-redis-password",
  "DATABASE_URL": "postgresql+asyncpg://codeguardians-gateway:password@rds-endpoint:5432/codeguardians_db",
  "REDIS_URL": "redis=REPLACE_MEelasticache-endpoint:6379/0",
  "ALLOWED_ORIGINS": "https://yourdomain.com,https://api.yourdomain.com",
  "ALLOWED_HOSTS": "yourdomain.com,api.yourdomain.com"
}
```

### Automated Setup

```bash
# Use the unified script to setup secrets automatically
./scripts/deploy.sh setup-secrets

# This will:
# 1. Generate secure random secrets
# 2. Create AWS Secrets Manager secret
# 3. Display generated secrets for backup
```

### Manual Setup Steps

#### 1. Prerequisites
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
```

#### 2. Generate Secure Secrets
```bash
# Generate cryptographically secure secrets
SECRET_KEY=$(openssl rand -hex 32)        # 64 characters
POSTGRES_PASSWORD=REPLACE_ME rand -hex 16) # 32 characters
REDIS_PASSWORD=REPLACE_ME rand -hex 16)    # 32 characters

echo "Generated Secrets:"
echo "SECRET_KEY: $SECRET_KEY"
echo "POSTGRES_PASSWORD="REPLACE_ME"
echo "REDIS_PASSWORD="REPLACE_ME"
```

#### 3. Create Secrets JSON
```bash
# Create the secrets JSON file
cat > secrets.json << EOF
{
  "SECRET_KEY": "$SECRET_KEY",
  "POSTGRES_PASSWORD": "$POSTGRES_PASSWORD",
  "REDIS_PASSWORD": "$REDIS_PASSWORD",
  "DATABASE_URL": "postgresql+asyncpg://codeguardians-gateway:$POSTGRES_PASSWORD@postgres:5432/codeguardians-gateway_db",
  "REDIS_URL": "redis=REPLACE_MEredis:6379/0",
  "ALLOWED_ORIGINS": "https://yourdomain.com,https://api.yourdomain.com",
  "ALLOWED_HOSTS": "yourdomain.com,api.yourdomain.com",
  "STRIPE_SECRET_KEY": "sk_live_your_actual_stripe_secret_key",
  "CLERK_SECRET_KEY": "sk_live_your_actual_clerk_secret_key",
  "AWS_REGION": "us-east-1",
  "ENVIRONMENT": "production"
}
EOF
```

#### 4. Create AWS Secrets Manager Secret
```bash
# Set variables
AWS_REGION="us-east-1"
SECRET_NAME="codeguardians-gateway/production"

# Create the secret
aws secretsmanager create-secret \
  --name "$SECRET_NAME" \
  --description "AIGuardian Production Secrets - Managed by DevOps" \
  --secret-string file://secrets.json \
  --region "$AWS_REGION" \
  --tags \
    Key=Project,Value=AIGuardian \
    Key=Environment,Value=Production \
    Key=ManagedBy,Value=DevOps \
    Key=LastUpdated,Value="$(date +%Y-%m-%d)"

# Verify secret creation
aws secretsmanager describe-secret \
  --secret-id "$SECRET_NAME" \
  --region "$AWS_REGION"
```

#### 5. Configure IAM Permissions
```bash
# Create IAM policy for ECS task execution
cat > ecs-secrets-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": [
        "arn:aws:secretsmanager:$AWS_REGION:$AWS_ACCOUNT:secret:$SECRET_NAME*"
      ]
    }
  ]
}
EOF

# Create the policy
POLICY_ARN=$(aws iam create-policy \
  --policy-name AIGuardianSecretsAccess \
  --policy-document file://ecs-secrets-policy.json \
  --query 'Policy.Arn' \
  --output text)

# Attach to ECS task execution role
aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn "$POLICY_ARN"
```

### Secrets Reference

| Secret Key | Purpose | Format | Example |
|------------|---------|--------|---------|
| `SECRET_KEY` | JWT signing | 64+ hex chars | `a1b2c3d4...` |
| `POSTGRES_PASSWORD` | Database auth | 32+ chars | `secure-db-pass-123` |
| `REDIS_PASSWORD` | Cache auth | 32+ chars | `secure-redis-pass-456` |
| `DATABASE_URL` | Full DB connection | URL format | `postgresql+asyncpg://user:pass@host:5432/db` |
| `REDIS_URL` | Full Redis connection | URL format | `redis=REPLACE_MEhost:6379/0` |
| `ALLOWED_ORIGINS` | CORS origins | Comma-separated | `https://app.com,https://api.app.com` |
| `ALLOWED_HOSTS` | Django hosts | Comma-separated | `app.com,api.app.com` |
| `STRIPE_SECRET_KEY` | Payment processing | Stripe key | `sk_live_...` |
| `CLERK_SECRET_KEY` | Authentication | Clerk key | `sk_live_...` |

---

## 🐳 Docker Compose Configuration

### Single Configuration File

The system uses one `docker-compose.yml` file that handles:
- Gateway service (port 8000)
- PostgreSQL database (port 5433)
- Redis cache (port 6380)
- 6 Guard services (ports 8001-8005)

### Key Configuration Points

```yaml
# Gateway (Main Entry Point)
codeguardians-gateway:
  image: aiguards-gateway:dev
  ports:
    - "8000:8000"  # Only external port
  environment:
    - ENVIRONMENT=development
    - DEBUG=true
  networks:
    - aiguards-network

# Guard Services (Internal Only)
tokenguard:
  image: aiguards-tokenguard:dev
  # No exposed ports - internal network only
  networks:
    - aiguards-network
```

### Production Override

Create `docker-compose.prod.yml` for production-specific settings:

```yaml
services:
  codeguardians-gateway:
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
      - LOG_LEVEL=INFO
      - READ_ONLY=true
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
        reservations:
          memory: 1G
          cpus: '1.0'
    restart: always
    
  postgres:
    environment:
      - POSTGRES_PASSWORD=REPLACE_ME
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always
    
  redis:
    environment:
      - REDIS_PASSWORD=REPLACE_ME
    volumes:
      - redis_data:/data
    restart: always
```

---

## 🚀 ECS Deployment Methods

### Method 1: Unified Script (Recommended)

```bash
# Deploy to AWS ECS with secrets management
./scripts/deploy.sh prod

# This handles:
# - Building and pushing Docker image
# - Creating/updating ECS service
# - Setting up secrets injection
# - Health checks and monitoring
```

### Method 2: Manual ECS Deployment

#### Step 1: Build and Push Image
```bash
# Build image
cd codeguardians-gateway/codeguardians-gateway
docker build -t codeguardians-gateway:latest .

# Tag for ECR
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
docker tag codeguardians-gateway:latest \
  ${AWS_ACCOUNT}.dkr.ecr.us-east-1.amazonaws.com/codeguardians-gateway:latest

# Push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  ${AWS_ACCOUNT}.dkr.ecr.us-east-1.amazonaws.com/codeguardians-gateway:latest
docker push ${AWS_ACCOUNT}.dkr.ecr.us-east-1.amazonaws.com/codeguardians-gateway:latest
```

#### Step 2: Create Task Definition with Secrets
```json
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
    "portMappings": [{"containerPort": 8000}],
    "environment": [
      {"name": "ENVIRONMENT", "value": "production"},
      {"name": "DEBUG", "value": "false"},
      {"name": "LOG_LEVEL", "value": "INFO"},
      {"name": "DATABASE_ENABLED", "value": "true"},
      {"name": "ALLOWED_ORIGINS", "value": "https://yourdomain.com"}
    ],
    "secrets": [
      {
        "name": "SECRET_KEY",
        "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT:secret:codeguardians-gateway/production:SECRET_KEY::"
      },
      {
        "name": "DATABASE_URL",
        "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT:secret:codeguardians-gateway/production:DATABASE_URL::"
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
```

#### Step 3: Register and Deploy
```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create/update service
aws ecs create-service \
  --cluster codeguardians-gateway-cluster \
  --service-name codeguardians-gateway-service \
  --task-definition codeguardians-gateway \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

---

## 📊 Container Information

| Service | Image URI | CPU | Memory | Internal Port | Image Size |
|---------|-----------|-----|--------|---------------|------------|
| Gateway | `codeguardians-gateway` | 1024 | 2048 | 8000 | 1.48 GB |
| TokenGuard | `tokenguard` | 512 | 1024 | 8000 | 382 MB |
| TrustGuard | `trustguard` | 512 | 1024 | 8000 | 452 MB |
| ContextGuard | `contextguard` | 512 | 1024 | 8000 | 566 MB |
| BiasGuard | `biasguard` | 512 | 1024 | 8004 | ~500 MB |
| HealthGuard | `healthguard` | 512 | 1024 | 8000 | 683 MB ✅ |

**Total Image Size:** ~4.0 GB (all containers optimized)

**Full Image URI Format:**
```
${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${SERVICE_NAME}:${TAG}
```

---

## 🔄 Deployment Process

### 1. Pre-deployment
```bash
# Backup current deployment
docker-compose down
docker-compose pull

# Verify secrets are available
echo $POSTGRES_PASSWORD
echo $REDIS_PASSWORD
echo $SECRET_KEY
```

### 2. Deploy
```bash
# Local development
docker-compose up -d

# Production deployment is handled by DevOps team
```

### 3. Post-deployment
```bash
# Health checks
curl -f http://localhost:8000/health/live
curl -f http://localhost:8000/health/ready

# Test API
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"service_type":"tokenguard","payload":{"text":"test"},"user_id":"test","session_id":"test"}'
```

---

## 📊 Monitoring & Health Checks

### Health Endpoints

| Endpoint | Purpose | Expected Response |
|----------|---------|-------------------|
| `GET /health/live` | Liveness probe | `{"status":"alive"}` |
| `GET /health/ready` | Readiness probe | `{"status":"ready"}` |
| `GET /api/v1/guards/services` | Service discovery | `{"services":{...}}` |
| `GET /metrics` | Prometheus metrics | Metrics data |

### Health Check Commands
```bash
# Basic health
curl -f http://localhost:8000/health/live

# Full readiness
curl -f http://localhost:8000/health/ready

# Service status
curl http://localhost:8000/api/v1/guards/services

# Container status
docker-compose ps
```

### Monitoring Services

**Prometheus** (Metrics): `http://localhost:9090`  
**Grafana** (Dashboards): `http://localhost:3000` (admin/admin)  
**Elasticsearch** (Logs): `http://localhost:9200`  
**Kibana** (Log Visualization): `http://localhost:5601`

### Container Logs

```bash
# Gateway logs
docker-compose logs -f codeguardians-gateway

# All services logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f tokenguard
docker-compose logs -f trustguard

# AWS CloudWatch logs
aws logs tail /ecs/codeguardians-gateway --follow --region $AWS_REGION
```

---

## 📋 Production Checklist

### Pre-Deployment

- [ ] Secrets configured in AWS Secrets Manager
- [ ] Environment variables set correctly
- [ ] Docker images built and pushed to ECR
- [ ] ECS cluster and services created
- [ ] IAM roles and permissions configured
- [ ] Security groups and networking set up
- [ ] Health checks configured

### Post-Deployment

- [ ] ECS service running with desired count
- [ ] Tasks show HEALTHY status
- [ ] Health endpoints responding
- [ ] API endpoints functional
- [ ] Database connectivity verified
- [ ] Redis connectivity verified
- [ ] Guard services healthy
- [ ] Logs being collected in CloudWatch
- [ ] Metrics being collected

### Post-Deployment Verification

#### 1. Check Service Status
```bash
aws ecs describe-services \
  --cluster codeguardians-gateway-cluster \
  --services codeguardians-gateway-service
```

**Look for:**
- `runningCount: 2` (matches desired count)
- `desiredCount: 2`
- `deploymentStatus: PRIMARY`

#### 2. Verify Task Health
```bash
aws ecs describe-tasks \
  --cluster codeguardians-gateway-cluster \
  --tasks $(aws ecs list-tasks --cluster codeguardians-gateway-cluster --service-name codeguardians-gateway-service --query 'taskArns[0]' --output text)
```

**Look for:**
- `lastStatus: RUNNING`
- `healthStatus: HEALTHY`

#### 3. Test Health Endpoints
```bash
# Get ALB DNS name (if using ALB)
ALB_DNS=$(aws elbv2 describe-load-balancers --query 'LoadBalancers[0].DNSName' --output text)

# Test health
curl http://${ALB_DNS}/health/live

# Expected: {"status":"alive","service":"codeguardians-gateway"}
```

#### 4. Check CloudWatch Logs
```bash
aws logs tail /ecs/codeguardians-gateway --follow
```

**Look for:**
- "Uvicorn running on http://0.0.0.0:8000"
- "✅ Database initialized" (if database enabled)
- No ERROR or CRITICAL messages

#### 5. Test API Functionality
```bash
# Test service discovery
curl http://${ALB_DNS}/api/v1/guards/services

# Test guard processing
curl -X POST http://${ALB_DNS}/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"service_type":"tokenguard","payload":{"text":"test"},"user_id":"test"}'
```

---

## 🛠️ Troubleshooting

### Common Issues

#### Container Exits Immediately

**Symptoms:** ECS task stops after <5 seconds

**Diagnosis:**
```bash
# Check CloudWatch logs
aws logs tail /ecs/codeguardians-gateway --follow
```

**Common Causes & Fixes:**

1. **Missing SECRET_KEY**
   ```bash
   # Fix: Ensure SECRET_KEY is set (32+ characters)
   SECRET_KEY=<64-char-random-string>
   ```

2. **DATABASE_URL invalid but DATABASE_ENABLED=true**
   ```bash
   # Fix A: Disable database
   DATABASE_ENABLED=false

   # Fix B: Provide valid DATABASE_URL
   DATABASE_URL=REPLACE_ME   ```

3. **ALLOWED_ORIGINS parsing error**
   ```bash
   # Fix: Use comma-separated string
   ALLOWED_ORIGINS=https://domain1.com,https://domain2.com
   ```

#### Health Check Failing

**Symptoms:** Task keeps restarting, shows "unhealthy"

**Diagnosis:**
```bash
# Check health endpoint directly
aws ecs execute-command \
  --cluster codeguardians-gateway-cluster \
  --task TASK_ID \
  --container gateway \
  --interactive \
  --command "/bin/bash"

# Inside container:
curl http://localhost:8000/health/live
```

#### Database Connection Errors

**Symptoms:** "Connection refused" or "Could not connect to server"

**Fixes:**
1. **Check RDS security group** allows ECS security group
2. **Verify DATABASE_URL format:**
   ```bash
   postgresql+asyncpg://username:password@endpoint:5432/database_name
   ```
3. **Ensure RDS is accessible** from ECS subnets

#### Secrets Not Loading

**Symptoms:** "Secret not found" or empty environment variables

**Fixes:**
1. **Task execution role permissions:**
   ```json
   {
     "Effect": "Allow",
     "Action": ["secretsmanager:GetSecretValue"],
     "Resource": ["arn:aws:secretsmanager:region:account:secret:name*"]
   }
   ```

2. **Correct secret ARN format:**
   ```
   arn:aws:secretsmanager:region:account:secret:name:KEY_NAME::
   ```

#### Guard Services Unavailable

**Symptoms:** Service discovery shows services as "unhealthy"

**Diagnosis:**
```bash
curl http://localhost:8000/api/v1/guards/services
docker-compose logs tokenguard  # Check specific service
```

**Expected Behavior:**
- Gateway continues to function
- Requests to unavailable services return error
- Other healthy services continue processing

**Fix:**
- Check guard service container logs
- Verify guard service dependencies installed
- Check network connectivity

### Debug Commands

```bash
# Container status
docker-compose ps

# Resource usage
docker stats

# Network connectivity
docker-compose exec codeguardians-gateway curl http://tokenguard:8001/health

# Check service status
aws ecs describe-services \
  --cluster codeguardians-gateway-cluster \
  --services codeguardians-gateway-service \
  --query 'services[0].{Running:runningCount,Desired:desiredCount,Deployments:deployments}'
```

---

## 🔐 Security Configuration

### Network Security
- Services communicate via internal Docker network
- Only gateway exposes external ports (8000)
- Health checks use internal network

### Secrets Security
- Use AWS Secrets Manager for production secrets
- Never commit secrets to repository
- Rotate secrets regularly
- Use Docker secrets in production

### Container Security
- Read-only filesystem in production
- No new privileges
- Resource limits
- Health checks

---

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale gateway (if needed)
docker-compose up -d --scale codeguardians-gateway=3

# ECS scaling
aws ecs update-service \
  --cluster codeguardians-gateway-cluster \
  --service codeguardians-gateway-service \
  --desired-count 4
```

### Resource Limits
```yaml
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '2.0'
    reservations:
      memory: 1G
      cpus: '1.0'
```

---

## 🔄 Updates & Maintenance

### Rolling Updates
```bash
# Update images
docker-compose pull

# Rolling restart
docker-compose up -d --no-deps codeguardians-gateway

# Force ECS deployment
aws ecs update-service \
  --cluster codeguardians-gateway-cluster \
  --service codeguardians-gateway-service \
  --force-new-deployment
```

### Backup
```bash
# Database backup
docker-compose exec postgres pg_dump -U codeguardians-gateway codeguardians-gateway_db > backup.sql

# Volume backup
docker run --rm -v aiguardian_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz /data
```

### Secret Rotation
```bash
# Generate new secrets
NEW_SECRET_KEY=$(openssl rand -hex 32)
NEW_POSTGRES_PASSWORD=REPLACE_ME rand -hex 16)
NEW_REDIS_PASSWORD=REPLACE_ME rand -hex 16)

# Update secret
aws secretsmanager update-secret \
  --secret-id "$SECRET_NAME" \
  --secret-string "{
    \"SECRET_KEY\": \"$NEW_SECRET_KEY\",
    \"POSTGRES_PASSWORD\": \"$NEW_POSTGRES_PASSWORD\",
    \"REDIS_PASSWORD\": \"$NEW_REDIS_PASSWORD\",
    \"DATABASE_URL\": \"postgresql+asyncpg://codeguardians-gateway:$NEW_POSTGRES_PASSWORD@postgres:5432/codeguardians-gateway_db\",
    \"REDIS_URL\": \"redis=REPLACE_MEredis:6379/0\"
  }" \
  --region "$AWS_REGION"

# Force ECS service deployment
aws ecs update-service \
  --cluster codeguardians-gateway-cluster \
  --service codeguardians-gateway-service \
  --force-new-deployment
```

---

## 🆘 Emergency Procedures

### Service Recovery
```bash
# Restart failed service
docker-compose restart <service-name>

# Full system restart
docker-compose down && docker-compose up -d

# ECS service restart
aws ecs update-service \
  --cluster codeguardians-gateway-cluster \
  --service codeguardians-gateway-service \
  --force-new-deployment
```

### Rollback
```bash
# Rollback to previous version
docker-compose down
docker-compose up -d

# ECS rollback (update to previous task definition)
aws ecs update-service \
  --cluster codeguardians-gateway-cluster \
  --service codeguardians-gateway-service \
  --task-definition codeguardians-gateway:PREVIOUS_REVISION
```

---

## 📚 Quick Reference Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart gateway
docker-compose restart codeguardians-gateway

# Check service status
docker-compose ps

# Health check
curl http://localhost:8000/health/live

# Service discovery
curl http://localhost:8000/api/v1/guards/services

# Test TokenGuard
curl -X POST http://localhost:8000/api/v1/guards/process \
  -H "Content-Type: application/json" \
  -d '{"service_type":"tokenguard","payload":{"text":"test"},"user_id":"test"}'

# List ECR repositories
aws ecr describe-repositories --region $AWS_REGION

# Check ECS services
aws ecs list-services --cluster codeguardians-gateway-cluster --region $AWS_REGION

# View service status
aws ecs describe-services \
  --cluster codeguardians-gateway-cluster \
  --services codeguardians-gateway-service \
  --region $AWS_REGION

# Update deployment
aws ecs update-service \
  --cluster codeguardians-gateway-cluster \
  --service codeguardians-gateway-service \
  --force-new-deployment \
  --region $AWS_REGION
```

---

## 📚 Additional Documentation

- **Complete Guide:** [AWS_DEPLOYMENT_READINESS.md](AWS_DEPLOYMENT_READINESS.md)
- **External Services:** [EXTERNAL_SERVICES_SETUP.md](EXTERNAL_SERVICES_SETUP.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **API Reference:** [docs/api/README.md](api/README.md)
- **User Guide:** [USER_GUIDE.md](USER_GUIDE.md)

---

**Ready to deploy?** Run `bash scripts/push-all-to-ecr.sh` to get started!