# Final AWS Secret Update

##  What's Good

-  STRIPE_WEBHOOK_SECRET is set correctly
-  All other configuration looks good
-  Keys are properly formatted

##  What Needs Updating

1. **CLERK_WEBHOOK_SECRET** - Currently a placeholder
   - Current: `"whsec_your_clerk_webhook_secret"`
   - Need: Get real secret from Clerk dashboard

2. **ALLOWED_HOSTS** - Missing (needed for ngrok webhooks)
   - Need to add: Your ngrok host

##  Complete Updated Secret JSON

Here's your complete secret with the fixes:

```json
{
  "SECRET_KEY": "REPLACE_ME_WITH_SECURE_SECRET_KEY_MIN_32_CHARS",
  "POSTGRES_PASSWORD": "REPLACE_ME",
  "REDIS_PASSWORD": "REPLACE_ME",
  "DATABASE_URL": "REPLACE_ME_WITH_DATABASE_URL",
  "REDIS_URL": "REPLACE_ME_WITH_REDIS_URL",
  "DEV_DATABASE_URL": "REPLACE_ME_WITH_DEV_DATABASE_URL",
  "DEV_REDIS_URL": "REPLACE_ME_WITH_DEV_REDIS_URL",
  "DEV_POSTGRES_PASSWORD": "REPLACE_ME",
  "DEV_REDIS_PASSWORD": "REPLACE_ME",
  "PROD_DATABASE_URL": "REPLACE_ME_WITH_PROD_DATABASE_URL",
  "PROD_REDIS_URL": "REPLACE_ME_WITH_PROD_REDIS_URL",
  "PROD_POSTGRES_PASSWORD": "REPLACE_ME",
  "PROD_REDIS_AUTH_TOKEN": "REPLACE_ME",
  "AWS_SECRETS_ENABLED": "true",
  "AWS_SECRETS_NAME": "codeguardians-gateway/production",
  "AWS_REGION": "us-east-1",
  "ENVIRONMENT": "production",
  "LOG_LEVEL": "DEBUG",
  "DEBUG": "true",
  "CLERK_ENABLED": "true",
  "CLERK_SECRET_KEY": "sk_test_REPLACE_WITH_YOUR_CLERK_SECRET_KEY",
  "CLERK_PUBLISHABLE_KEY": "pk_test_REPLACE_WITH_YOUR_CLERK_PUBLISHABLE_KEY",
  "CLERK_WEBHOOK_SECRET": "whsec_YOUR_REAL_CLERK_SECRET_HERE",
  "STRIPE_ENABLED": "true",
  "STRIPE_SECRET_KEY": "sk_test_REPLACE_WITH_YOUR_STRIPE_SECRET_KEY",
  "STRIPE_PUBLISHABLE_KEY": "pk_test_REPLACE_WITH_YOUR_STRIPE_PUBLISHABLE_KEY",
  "STRIPE_WEBHOOK_SECRET": "whsec_REPLACE_WITH_YOUR_STRIPE_WEBHOOK_SECRET",
  "UNIFIED_API_KEY": "tg_REPLACE_WITH_YOUR_UNIFIED_API_KEY",
  "API_PORT": "8004",
  "NODE_ENV": "development",
  "SENDGRID_API_KEY": "SG.REPLACE_WITH_YOUR_SENDGRID_API_KEY",
  "HUBSPOT_PRIVATE_API_KEY": "dummy_key_to_prevent_errors",
  "SENDGRID_AI_GUARDIAN_GROUP_ID": "REPLACE_ME",
  "SENDGRID_FROM_EMAIL": "support@aiguardian.ai",
  "ALLOWED_HOSTS": "localhost,127.0.0.1,aciform-tyisha-semipictorially.ngrok-free.dev,*.ngrok-free.dev,aiguardian.ai,api.aiguardian.ai,dashboard.aiguardian.ai"
}
```

##  Action Items

### 1. Get Clerk Webhook Secret

1. Go to Clerk Dashboard: https://dashboard.clerk.com/apps/YOUR_APP/webhooks
2. Create/edit webhook endpoint: `https://aciform-tyisha-semipictorially.ngrok-free.dev/webhooks/clerk`
3. Copy the **Signing secret** (starts with `whsec_`)
4. Replace `"whsec_YOUR_REAL_CLERK_SECRET_HERE"` in the JSON above

### 2. Update AWS Secret

1. Go to: https://console.aws.amazon.com/secretsmanager/us-east-1/secret?name=codeguardians-gateway/production
2. Click "Edit"
3. Paste the complete JSON above (with real Clerk secret)
4. Save

### 3. Restart Gateway

```bash
docker-compose restart codeguardians-gateway
```

### 4. Verify

```bash
docker logs codeguardians-gateway-dev | grep -i "aws secrets"
```

##  After Update

Once you update the secret with:
-  Real CLERK_WEBHOOK_SECRET
-  ALLOWED_HOSTS with ngrok host

Everything will work! The gateway will:
- Load all secrets from AWS
- Allow ngrok webhook requests (403 fixed)
- Process Stripe and Clerk webhooks correctly

