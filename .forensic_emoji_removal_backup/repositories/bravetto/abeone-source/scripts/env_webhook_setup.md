# Webhook Setup via .env File

## ✅ Configuration Added to .env

I've added the webhook configuration to your `.env` file:

- ✅ `STRIPE_WEBHOOK_SECRET` - From your AWS secret
- ✅ `CLERK_WEBHOOK_SECRET` - Placeholder (update with real value)
- ✅ `ALLOWED_HOSTS` - Includes ngrok host (already added)
- ✅ Stripe and Clerk API keys - From your AWS secret

## ⚠️ One More Step: Update CLERK_WEBHOOK_SECRET

In your `.env` file, update:
```env
CLERK_WEBHOOK_SECRET=REPLACE_ME
```

Replace `whsec_your_clerk_webhook_secret` with the real secret from Clerk dashboard.

## 🔄 Using .env vs AWS Secrets Manager

**Current Setup:**
- AWS Secrets Manager is enabled (`AWS_SECRETS_ENABLED=true`)
- **BUT** you can override specific values in `.env`
- Gateway loads from AWS first, then `.env` can override

**To use .env exclusively (disable AWS):**
```env
AWS_SECRETS_ENABLED=false
```

**To use AWS but override specific keys:**
Keep `AWS_SECRETS_ENABLED=true` and the keys in `.env` will be used as overrides.

## 🚀 Next Steps

1. **Update CLERK_WEBHOOK_SECRET** in `.env` with real value

2. **Restart gateway**:
   ```bash
   docker-compose restart codeguardians-gateway
   ```

3. **Test webhooks**:
   - Stripe: `https://aciform-tyisha-semipictorially.ngrok-free.dev/webhooks/stripe`
   - Clerk: `https://aciform-tyisha-semipictorially.ngrok-free.dev/webhooks/clerk`

4. **Check logs**:
   ```bash
   docker logs codeguardians-gateway-dev --tail 50
   ```

## 📝 Current .env Configuration

Your `.env` now has:
- ✅ ALLOWED_HOSTS with ngrok host
- ✅ STRIPE_WEBHOOK_SECRET
- ✅ CLERK_WEBHOOK_SECRET (needs real value)
- ✅ All Stripe/Clerk API keys
- ✅ AWS Secrets Manager config

After updating CLERK_WEBHOOK_SECRET and restarting, everything should work!

