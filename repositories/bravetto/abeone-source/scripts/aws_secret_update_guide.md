# AWS Secrets Manager Update Guide

## What to Add to Your Secret

Update your AWS secret `codeguardians-gateway/production` with these keys:

### Required Additions

```json
{
  // ... your existing keys ...
  
  "STRIPE_WEBHOOK_SECRET": "whsec_YOUR_STRIPE_SECRET_HERE",
  "STRIPE_ENABLED": "true",
  "CLERK_WEBHOOK_SECRET": "whsec_YOUR_CLERK_SECRET_HERE",
  "CLERK_ENABLED": "true",
  "ALLOWED_HOSTS": "localhost,127.0.0.1,aciform-tyisha-semipictorially.ngrok-free.dev,*.ngrok-free.dev,aiguardian.ai,api.aiguardian.ai"
}
```

## Step-by-Step: Update in AWS Console

1. **Go to AWS Secrets Manager**:
   https://console.aws.amazon.com/secretsmanager/us-east-1/secret?name=codeguardians-gateway/production

2. **Click "Retrieve secret value"** → **"Edit"**

3. **Add the keys above** to your existing JSON (or merge with existing keys)

4. **Save** the secret

## Step-by-Step: Update via AWS CLI

If you have AWS CLI configured:

```bash
# 1. Get current secret
aws secretsmanager get-secret-value \
  --secret-id codeguardians-gateway/production \
  --region us-east-1 \
  --query SecretString \
  --output text > current_secret.json

# 2. Edit the JSON file to add the keys above

# 3. Update the secret
aws secretsmanager put-secret-value \
  --secret-id codeguardians-gateway/production \
  --region us-east-1 \
  --secret-string file://current_secret.json
```

## After Updating

1. **Restart the gateway**:
   ```bash
   docker-compose restart codeguardians-gateway
   ```

2. **Verify secrets loaded**:
   ```bash
   docker logs codeguardians-gateway-dev | grep -i "aws secrets"
   ```

   You should see:
   ```
    Successfully loaded X secrets from AWS Secrets Manager
   ```

3. **Test webhooks**:
   - Stripe: `https://aciform-tyisha-semipictorially.ngrok-free.dev/webhooks/stripe`
   - Clerk: `https://aciform-tyisha-semipictorially.ngrok-free.dev/webhooks/clerk`

## Current Configuration

Your `.env` already has:
-  `AWS_SECRETS_ENABLED=true`
-  `AWS_SECRETS_NAME=codeguardians-gateway/production`
-  `AWS_REGION=us-east-1`

The gateway will automatically load secrets from AWS on startup!

