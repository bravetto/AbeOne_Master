# AWS Credentials Configuration Guide

**AWS Username**: `mxm0118`  
**AWS Account**: `730335329303`  
**Region**: `us-east-1`

---

## Quick Setup Options

### Option 1: AWS CLI Configure (Recommended)

```bash
aws configure
```

**Enter when prompted**:
- AWS Access Key ID: `[your access key]`
- AWS Secret Access Key: `[your secret key]`
- Default region name: `us-east-1`
- Default output format: `json`

### Option 2: Set Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_DEFAULT_REGION=us-east-1
```

### Option 3: AWS SSO (If Using SSO)

```bash
aws configure sso --profile mxm0118
# Follow prompts to configure SSO
```

Then use profile:
```bash
export AWS_PROFILE=mxm0118
```

---

## Verify Credentials

```bash
# Test credentials
aws sts get-caller-identity --region us-east-1

# Should return something like:
# {
#     "UserId": "AIDA...",
#     "Account": "730335329303",
#     "Arn": "arn:aws:iam::730335329303:user/mxm0118"
# }
```

---

## Test ECR Access

```bash
# Test ECR login
aws ecr get-login-password --region us-east-1

# Should return a password token (long string)
```

---

## Once Credentials Configured

Run ECR deployment:
```bash
cd /Users/michaelmataluni/Desktop/AbëONE/quarantine/aiguards-backend-clone/codeguardians-gateway/codeguardians-gateway

python3 /Users/michaelmataluni/Desktop/AbëONE/local-ai-assistant/scripts/aeyon_ecr_deploy_gatewest.py
```

---

**Note**: The ECR script will automatically:
1. Check environment variables
2. Check `~/.aws/credentials` file
3. Try vault-first protocol (1Password/AbëKEYS)
4. Use AWS CLI default profile

