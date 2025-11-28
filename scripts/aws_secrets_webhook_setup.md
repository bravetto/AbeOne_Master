# AWS Secrets Manager Webhook Setup

## Your AWS Secret Configuration

**Secret Name**: `codeguardians-gateway/production`  
**Region**: `us-east-1`

 **Already configured in your codebase!**

## Quick Setup Options

### Option 1: Use Python Script (Recommended)

I've created a script to help you update your AWS secret:

```bash
python scripts/update_aws_secret_for_webhooks.py
```

This script will:
1. Fetch your current secret from AWS
2. Prompt you for webhook secrets
3. Add ngrok host to ALLOWED_HOSTS
4. Update the secret in AWS

### Option 2: Manual AWS Console Update

1. **Go to AWS Console**: https://console.aws.amazon.com/secretsmanager/us-east-1/secret?name=codeguardians-gateway/production

2. **Click "Retrieve secret value"** → **"Edit"**

3. **Add/Update these keys**:

```json
{
  "STRIPE_ENABLED": "true",
  "STRIPE_WEBHOOK_SECRET": "whsec_YOUR_STRIPE_SECRET",
  "CLERK_ENABLED": "true",
  "CLERK_WEBHOOK_SECRET": "whsec_YOUR_CLERK_SECRET",
  "ALLOWED_HOSTS": "localhost,127.0.0.1,aciform-tyisha-semipictorially.ngrok-free.dev,*.ngrok-free.dev,aiguardian.ai,api.aiguardian.ai"
}
```

4. **Save the secret**

### Option 3: Use AWS CLI

```bash
# Get current secret
aws secretsmanager get-secret-value \
  --secret-id codeguardians-gateway/production \
  --region us-east-1 \
  --query SecretString \
  --output text > current_secret.json

# Edit the JSON file to add:
# - STRIPE_WEBHOOK_SECRET
# - CLERK_WEBHOOK_SECRET  
# - Update ALLOWED_HOSTS

# Update secret
aws secretsmanager put-secret-value \
  --secret-id codeguardians-gateway/production \
  --region us-east-1 \
  --secret-string file://current_secret.json
```

## Enable AWS Secrets Manager in Gateway

Ensure your `.env` file has:

```env
AWS_SECRETS_ENABLED=true
AWS_SECRETS_NAME=codeguardians-gateway/production
AWS_REGION=us-east-1
```

**Note**: If using AWS credentials (not IAM role), also add:
```env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

## Restart Gateway

After updating the secret:

```bash
docker-compose restart codeguardians-gateway
```

## Verify Secrets Loaded

Check the gateway logs:

```bash
docker logs codeguardians-gateway-dev | grep -i "aws secrets"
```

You should see:
```
 Successfully loaded X secrets from AWS Secrets Manager
```

## Test Webhooks

After restart, test your webhooks:

1. **Stripe**: `https://aciform-tyisha-semipictorially.ngrok-free.dev/webhooks/stripe`
2. **Clerk**: `https://aciform-tyisha-semipictorially.ngrok-free.dev/webhooks/clerk`

## How It Works

The gateway automatically loads secrets from AWS Secrets Manager when:
- `AWS_SECRETS_ENABLED=true`
- AWS credentials are configured (IAM role or access keys)
- Secret exists and is accessible

Secrets from AWS **override** values in `.env` file.

## Troubleshooting

### Secrets not loading?
1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify secret exists: `aws secretsmanager describe-secret --secret-id codeguardians-gateway/production --region us-east-1`
3. Check gateway logs for errors
4. Verify `AWS_SECRETS_ENABLED=true` in `.env`

### Still getting 403?
1. Verify `ALLOWED_HOSTS` includes your ngrok host
2. Check gateway logs for "Blocked webhook request"
3. Restart gateway after updating secret

