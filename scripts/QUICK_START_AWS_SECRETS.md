# Quick Start: AWS Secrets Manager for Webhooks

##  Configuration Added

I've added AWS Secrets Manager configuration to your `.env`:
- `AWS_SECRETS_ENABLED=true`
- `AWS_SECRETS_NAME=codeguardians-gateway/production`
- `AWS_REGION=us-east-1`

##  Next Steps

### 1. Update Your AWS Secret with Webhook Info

You can use the Python script I created:

```bash
python scripts/update_aws_secret_for_webhooks.py
```

Or manually update in AWS Console:
1. Go to: https://console.aws.amazon.com/secretsmanager/us-east-1/secret?name=codeguardians-gateway/production
2. Click "Retrieve secret value" → "Edit"
3. Add these keys to your existing JSON:
   ```json
   {
     "STRIPE_WEBHOOK_SECRET": "whsec_YOUR_STRIPE_SECRET",
     "CLERK_WEBHOOK_SECRET": "whsec_YOUR_CLERK_SECRET",
     "ALLOWED_HOSTS": "localhost,127.0.0.1,aciform-tyisha-semipictorially.ngrok-free.dev,*.ngrok-free.dev,aiguardian.ai,api.aiguardian.ai"
   }
   ```

### 2. Restart Gateway

After updating the secret:

```bash
docker-compose restart codeguardians-gateway
```

### 3. Verify

Check logs to confirm secrets loaded:

```bash
docker logs codeguardians-gateway-dev | grep -i "aws secrets"
```

You should see:
```
 Successfully loaded X secrets from AWS Secrets Manager
```

##  How It Works

The gateway code in `app/core/config.py` automatically:
1. Checks if `AWS_SECRETS_ENABLED=true`
2. Connects to AWS Secrets Manager using your credentials
3. Loads all secrets from `codeguardians-gateway/production`
4. Overrides environment variables with AWS secrets
5. Uses those secrets throughout the application

##  Benefits

-  No secrets in `.env` file
-  Centralized secret management
-  Version control and rotation
-  IAM access control
-  Audit logging

##  Your AWS Secret Structure

Based on your code snippet, the secret should be JSON format:

```json
{
  "STRIPE_WEBHOOK_SECRET": "...",
  "CLERK_WEBHOOK_SECRET": "...",
  "ALLOWED_HOSTS": "...",
  // ... other existing keys
}
```

The gateway will automatically parse and use all keys in the secret.

