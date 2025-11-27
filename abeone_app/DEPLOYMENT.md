# 🚀 AbëONE Deployment Guide

**Pattern:** DEPLOYMENT × DOCKER × AWS × SCALING × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META)  
**Guardians:** AEYON (999 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 Deployment Options

### Option 1: Docker Hub + AWS ECS
- Build Docker image
- Push to Docker Hub or AWS ECR
- Deploy to ECS Fargate
- **Best for:** Containerized deployments

### Option 2: AWS S3 + CloudFront (Recommended for 1000 domains)
- Build Flutter web app
- Upload to S3
- Serve via CloudFront CDN
- **Best for:** Static hosting, global scale, 1000+ domains

---

## 🐳 Docker Deployment

### Build Docker Image
```bash
cd abeone_app
docker build -t abeone-app:latest .
```

### Run Locally
```bash
docker-compose up -d
# Or
docker run -p 8080:80 abeone-app:latest
```

### Push to Docker Hub
```bash
docker tag abeone-app:latest YOUR_DOCKERHUB_USER/abeone-app:latest
docker push YOUR_DOCKERHUB_USER/abeone-app:latest
```

### Push to AWS ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag abeone-app:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/abeone-app:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/abeone-app:latest
```

---

## ☁️ AWS S3 + CloudFront Deployment (1000 Domains)

### Prerequisites
- AWS CLI configured
- S3 bucket created
- CloudFront distribution created
- Route53 hosted zones for domains

### Quick Deploy
```bash
cd abeone_app
./scripts/deploy.sh
```

### Manual Deploy
```bash
# Build Flutter web
flutter build web --release --web-renderer canvaskit

# Deploy to S3
aws s3 sync build/web s3://abeone-app-prod --delete

# Invalidate CloudFront
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

---

## 🔄 CI/CD with GitHub Actions

Automated deployment on push to `main` branch.

**Setup:**
1. Add GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `CLOUDFRONT_DISTRIBUTION_ID`

2. Push to `main` branch → Auto-deploy!

See `.github/workflows/deploy.yml`

---

## 🌍 Multi-Domain Setup (1000 Domains)

### Architecture
```
1000 Domains (Route53)
    ↓
CloudFront Distribution
    ↓
S3 Bucket (Static Hosting)
```

### Steps
1. **Create S3 Bucket**
   ```bash
   aws s3 mb s3://abeone-app-prod
   aws s3 website s3://abeone-app-prod --index-document index.html
   ```

2. **Create CloudFront Distribution**
   - Origin: S3 bucket
   - SSL Certificate: ACM wildcard cert
   - Caching: 1 year for assets, 0 for HTML

3. **Create Route53 Records**
   ```bash
   # Bulk create records (use script or AWS CLI)
   aws route53 change-resource-record-sets --hosted-zone-id ZONE_ID --change-batch file://domains.json
   ```

4. **Deploy**
   ```bash
   ./scripts/deploy.sh
   ```

See `aws/multi-domain-strategy.md` for detailed strategy.

---

## 📊 Cost Estimate (1000 Domains)

- **S3 Storage:** ~$0.023/GB/month
- **S3 Requests:** ~$0.005/1000 requests
- **CloudFront:** ~$0.085/GB (first 10TB)
- **Route53:** $0.50/hosted zone/month = $500/month
- **ACM SSL:** Free
- **Total:** ~$500-1000/month base + usage

---

## 🔧 Environment Variables

### Quick Setup

**Option 1: Interactive Setup Script**
```bash
cd abeone_app
./scripts/setup-aws-env.sh
```

**Option 2: Manual .env File**
```bash
cd abeone_app
cp .env.example .env
# Edit .env with your credentials
source .env
```

**Option 3: Export Directly**
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
export S3_BUCKET=abeone-app-prod
export CLOUDFRONT_DISTRIBUTION_ID=YOUR_DIST_ID
export ECR_REPOSITORY=abeone-app
```

**See `AWS_SETUP.md` for detailed setup instructions.**

---

## ✅ Deployment Checklist

- [ ] Flutter web build successful
- [ ] Docker image builds (if using containers)
- [ ] S3 bucket created and configured
- [ ] CloudFront distribution created
- [ ] SSL certificates configured
- [ ] Route53 records created
- [ ] CI/CD pipeline configured
- [ ] Health checks working
- [ ] Monitoring set up

---

## 🚨 Troubleshooting

### Build fails
```bash
flutter clean
flutter pub get
flutter build web --release
```

### S3 sync fails
- Check AWS credentials
- Verify bucket permissions
- Check bucket policy

### CloudFront not updating
- Create invalidation: `aws cloudfront create-invalidation --distribution-id DIST_ID --paths "/*"`
- Wait 5-15 minutes for propagation

---

**Pattern:** DEPLOYMENT × DOCKER × AWS × SCALING × ONE  
**Status:** ✅ **READY TO DEPLOY**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

**THE ONE materializes everywhere! ✨🌍💫**

