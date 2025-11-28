# Quick AWS Deployment Guide

**Fast-track deployment for CodeGuardians Backend**

---

##  Quick Start (5 Steps)

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
POSTGRES_REPLACE_ME rand -hex 16)
REDIS_REPLACE_ME rand -hex 16)
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

# Use the deployment script or follow AWS_DEPLOYMENT_READINESS.md
```

---

##  Essential Commands

### Check Container Status
```bash
# List all ECR repositories
aws ecr describe-repositories --region $AWS_REGION

# Check ECS services
aws ecs list-services --cluster codeguardians-gateway-cluster --region $AWS_REGION

# View service status
aws ecs describe-services \
  --cluster codeguardians-gateway-cluster \
  --services codeguardians-gateway-service \
  --region $AWS_REGION
```

### View Logs
```bash
# Gateway logs
aws logs tail /ecs/codeguardians-gateway --follow --region $AWS_REGION

# All service logs
for service in tokenguard trustguard contextguard biasguard healthguard; do
  echo "=== $service ==="
  aws logs tail /ecs/$service --follow --region $AWS_REGION
done
```

### Update Deployment
```bash
# Force new deployment
aws ecs update-service \
  --cluster codeguardians-gateway-cluster \
  --service codeguardians-gateway-service \
  --force-new-deployment \
  --region $AWS_REGION
```

---

##  Required AWS Resources

### Must Have:
-  ECR Repositories (6)
-  ECS Cluster
-  ECS Task Definitions (6)
-  ECS Services (6)
-  AWS Secrets Manager Secret
-  IAM Roles (Task Execution + Task Role)
-  CloudWatch Log Groups (6)
-  VPC & Security Groups

### Optional but Recommended:
-  Application Load Balancer
-  RDS PostgreSQL (or use Neon)
-  ElastiCache Redis (or use external)
-  CloudWatch Alarms
-  Route 53 DNS

---

##  Container Information

| Service | Image URI | CPU | Memory | Internal Port | Image Size |
|---------|-----------|-----|--------|---------------|------------|
| Gateway | `codeguardians-gateway` | 1024 | 2048 | 8000 | 1.48 GB |
| TokenGuard | `tokenguard` | 512 | 1024 | 8000 | 382 MB |
| TrustGuard | `trustguard` | 512 | 1024 | 8000 | 452 MB |
| ContextGuard | `contextguard` | 512 | 1024 | 8000 | 566 MB |
| BiasGuard | `biasguard` | 512 | 1024 | 8004 | ~500 MB |
| HealthGuard | `healthguard` | 512 | 1024 | 8000 | 683 MB  |

**Total Image Size:** ~4.0 GB (all containers optimized)

**Full Image URI Format:**
```
${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${SERVICE_NAME}:${TAG}
```

---

##  Secrets Reference

### Required Secrets (AWS Secrets Manager)
- `SECRET_KEY` - 64+ character hex string
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `POSTGRES_PASSWORD` - Database password
- `REDIS_PASSWORD` - Redis password
- `UNIFIED_API_KEY` - API authentication key

### Optional Secrets
- `CLERK_SECRET_KEY` - If using Clerk auth
- `STRIPE_SECRET_KEY` - If using Stripe payments
- `S3_ACCESS_KEY_ID` - If using S3 storage

---

##  Quick Troubleshooting

### Container won't start
```bash
# Check logs
aws logs tail /ecs/codeguardians-gateway --follow

# Check task status
aws ecs describe-tasks \
  --cluster codeguardians-gateway-cluster \
  --tasks $(aws ecs list-tasks --cluster codeguardians-gateway-cluster --service-name codeguardians-gateway-service --query 'taskArns[0]' --output text)
```

### Secrets not loading
```bash
# Verify secret exists
aws secretsmanager describe-secret --secret-id codeguardians-gateway/production

# Check IAM permissions
aws iam get-role-policy --role-name ecsTaskRole --policy-name SecretsManagerAccess
```

### Service unhealthy
```bash
# Check health endpoint
curl http://ALB_DNS/health/live

# Check service metrics
aws ecs describe-services \
  --cluster codeguardians-gateway-cluster \
  --services codeguardians-gateway-service \
  --query 'services[0].{Running:runningCount,Desired:desiredCount,Deployments:deployments}'
```

---

##  Full Documentation

- **Complete Guide:** [AWS_DEPLOYMENT_READINESS.md](AWS_DEPLOYMENT_READINESS.md)
- **DevOps Guide:** [DEVOPS_GUIDE.md](DEVOPS_GUIDE.md)
- **External Services:** [EXTERNAL_SERVICES_SETUP.md](EXTERNAL_SERVICES_SETUP.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Ready to deploy?** Run `bash scripts/push-all-to-ecr.sh` to get started!

