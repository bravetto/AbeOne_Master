# Final AWS Secret Update

## ✅ What's Good

- ✅ STRIPE_WEBHOOK_SECRET is set correctly
- ✅ All other configuration looks good
- ✅ Keys are properly formatted

## ⚠️ What Needs Updating

1. **CLERK_WEBHOOK_SECRET** - Currently a placeholder
   - Current: `"whsec_your_clerk_webhook_secret"`
   - Need: Get real secret from Clerk dashboard

2. **ALLOWED_HOSTS** - Missing (needed for ngrok webhooks)
   - Need to add: Your ngrok host

## 📝 Complete Updated Secret JSON

Here's your complete secret with the fixes:

```json
{
  "SECRET_KEY": "REPLACE_ME",
  "POSTGRES_PASSWORD": "npq_queEC1k7QZG5v",
  "REDIS_PASSWORD": "redis-password-dev",
  "DATABASE_URL": "postgresql+asyncpg://neondb_owner:npg_quEClk7QZG5v@ep-shiny-dew-afsoljvy-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
  "REDIS_URL": "redis=REPLACE_MEcodeguardians-gateway-dev-redis:6379/0",
  "DEV_DATABASE_URL": "postgresql+asyncpg://gateway:aiguardian-secure-password-2024@gateway-dev-postgresql:5432/gateway_db",
  "DEV_REDIS_URL": "redis=REPLACE_MEgateway-dev-redis:6379/0",
  "DEV_POSTGRES_PASSWORD": "aiguardian-secure-password-2024",
  "DEV_REDIS_PASSWORD": "REPLACE_ME",
  "PROD_DATABASE_URL": "postgresql+asyncpg://codeguardians_gateway:kJ8mN2pQr5sT9vXz3bCd6fGh8jKl2nPq@codeguardians-gateway-prod-postgres.ctsg0mkmy2lr.us-east-1.rds.amazonaws.com:5432/codeguardians_gateway_db",
  "PROD_REDIS_URL": "rediss://:7vBn9mQw2xZc4jKh6pLs8tYu3aRd5fGv@master.codeguardians-gateway-prod-redis.0ngil8.use1.cache.amazonaws.com:6379",
  "PROD_POSTGRES_PASSWORD": "REPLACE_ME",
  "PROD_REDIS_AUTH_TOKEN": "REPLACE_ME",
  "AWS_SECRETS_ENABLED": "true",
  "AWS_SECRETS_NAME": "codeguardians-gateway/production",
  "AWS_REGION": "us-east-1",
  "ENVIRONMENT": "production",
  "LOG_LEVEL": "DEBUG",
  "DEBUG": "true",
  "CLERK_ENABLED": "true",
  "CLERK_SECRET_KEY": "REPLACE_ME",
  "CLERK_PUBLISHABLE_KEY": "REPLACE_ME",
  "CLERK_WEBHOOK_SECRET": "whsec_YOUR_REAL_CLERK_SECRET_HERE",
  "STRIPE_ENABLED": "true",
  "STRIPE_SECRET_KEY": "REPLACE_ME",
  "STRIPE_PUBLISHABLE_KEY": "REPLACE_ME",
  "STRIPE_WEBHOOK_SECRET": "REPLACE_ME",
  "UNIFIED_API_KEY": "REPLACE_ME",
  "API_PORT": "8004",
  "NODE_ENV": "development",
  "SENDGRID_API_KEY": "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",
  "HUBSPOT_PRIVATE_API_KEY": "dummy_key_to_prevent_errors",
  "SENDGRID_AI_GUARDIAN_GROUP_ID": "REPLACE_ME",
  "SENDGRID_FROM_EMAIL": "support@aiguardian.ai",
  "ALLOWED_HOSTS": "localhost,127.0.0.1,aciform-tyisha-semipictorially.ngrok-free.dev,*.ngrok-free.dev,aiguardian.ai,api.aiguardian.ai,dashboard.aiguardian.ai"
}
```

## 🔧 Action Items

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

## ✅ After Update

Once you update the secret with:
- ✅ Real CLERK_WEBHOOK_SECRET
- ✅ ALLOWED_HOSTS with ngrok host

Everything will work! The gateway will:
- Load all secrets from AWS
- Allow ngrok webhook requests (403 fixed)
- Process Stripe and Clerk webhooks correctly

