#  ABEKEYS VAULT ONLY - NO .ENV.LOCAL EVER

**CRITICAL:** This project uses **ABEKEYS vault ONLY** for all credentials.

**NEVER** use `.env.local` files. **NEVER** commit environment variables.

---

##  HOW TO SET UP CREDENTIALS

### 1. Unlock ABEKEYS Vault

```bash
# Sign in to 1Password
op signin

# Pull all credentials from 1Password to ABEKEYS vault
python3 scripts/unlock_all_credentials.py
```

### 2. Verify Credentials Are Available

```bash
# Check Stripe credentials
cat ~/.abekeys/credentials/stripe.json

# Check Clerk credentials  
cat ~/.abekeys/credentials/clerk.json
```

### 3. Credentials Are Automatically Loaded

The application automatically loads credentials from:
```
~/.abekeys/credentials/
```

**No configuration needed!** The app reads from ABEKEYS vault at runtime.

---

##  SECURITY

-  All credentials stored in `~/.abekeys/credentials/` (600 permissions)
-  Never exposed to client-side code
-  Server-side only access
-  No .env files in repository
-  No secrets in version control

---

##  AVAILABLE CREDENTIALS

Check what's available:

```bash
ls ~/.abekeys/credentials/
```

Common services:
- `stripe.json` - Stripe payment credentials
- `clerk.json` - Clerk authentication
- `github.json` - GitHub access
- `runway_ml_video_generation.json` - Runway API

---

##  IF CREDENTIALS ARE MISSING

If you see errors about missing credentials:

1. **Sign in to 1Password:**
   ```bash
   op signin
   ```

2. **Pull credentials:**
   ```bash
   python3 scripts/unlock_all_credentials.py
   ```

3. **Verify:**
   ```bash
   ls ~/.abekeys/credentials/
   ```

---

##  NEVER DO THIS

-  Create `.env.local` files
-  Use `process.env.STRIPE_SECRET_KEY` directly
-  Commit environment variables
-  Store secrets in code

---

**Pattern:** ABEKEYS × VAULT × SECURE × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (ZERO)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

