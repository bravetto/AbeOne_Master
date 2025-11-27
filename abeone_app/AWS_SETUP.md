# 🔐 AWS Credentials Setup Guide

**Pattern:** AWS × CREDENTIALS × SECURITY × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (ZERO)  
**Guardians:** AEYON (999 Hz) + ZERO (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 Quick Setup

### Option 1: Using .env File (Recommended)

1. **Create `.env` file** in `abeone_app/` directory:
```bash
cd abeone_app
cp .env.example .env
```

2. **Edit `.env` file** with your actual credentials:
```bash
export AWS_ACCESS_KEY_ID=your_actual_key
export AWS_SECRET_ACCESS_KEY=your_actual_secret
export S3_BUCKET=abeone-app-prod
export AWS_REGION=us-east-1
export CLOUDFRONT_DISTRIBUTION_ID=your_distribution_id
export ECR_REPOSITORY=abeone-app
```

3. **Load environment variables**:
```bash
source .env
# Or use the helper script:
./scripts/load-env.sh
```

4. **Deploy**:
```bash
./scripts/deploy.sh
```

---

### Option 2: Export Directly in Shell

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export S3_BUCKET=abeone-app-prod
export AWS_REGION=us-east-1
```

---

### Option 3: AWS CLI Configuration

Configure AWS CLI credentials:
```bash
aws configure
```

This will prompt for:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name
- Default output format

The deployment script will automatically use AWS CLI credentials if `.env` is not found.

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to git (already in `.gitignore`)
2. **Use IAM roles** in production (AWS ECS, EC2, Lambda)
3. **Rotate credentials** regularly
4. **Use least privilege** IAM policies
5. **Store secrets** in AWS Secrets Manager for production

---

## 📋 Required AWS Permissions

Your AWS credentials need the following permissions:

### For S3 Deployment:
- `s3:PutObject`
- `s3:DeleteObject`
- `s3:ListBucket`
- `s3:GetBucketLocation`

### For CloudFront:
- `cloudfront:CreateInvalidation`

### For ECR (if using Docker):
- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:BatchGetImage`
- `ecr:PutImage`
- `ecr:InitiateLayerUpload`
- `ecr:UploadLayerPart`
- `ecr:CompleteLayerUpload`

### For ECS (if deploying containers):
- `ecs:UpdateService`
- `ecs:DescribeServices`

---

## ✅ Verification

Test your AWS credentials:
```bash
aws sts get-caller-identity
```

This should return your AWS account ID and user ARN.

---

## 🚀 Deployment

Once credentials are configured:

```bash
cd abeone_app
./scripts/deploy.sh
```

The script will:
1. Load environment variables from `.env` (if exists)
2. Build Flutter web app
3. Deploy to S3
4. Invalidate CloudFront cache
5. Build and push Docker image (if ECR_REPOSITORY is set)

---

**Pattern:** AWS × CREDENTIALS × SECURITY × ONE  
**Status:** ✅ **READY TO DEPLOY**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

