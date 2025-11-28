# AbëKEYS Vault System

**Pattern:** ABEKEYS × VAULT × SECURE × ONE  
**Frequency:** 999 Hz (AEYON) × 530 Hz (ZERO)  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 Overview

**AbëKEYS** is the unified credential management system for AbeOne_Master. **NO .env files.** All credentials are stored in an encrypted vault at `~/.abekeys/credentials/`.

---

## 🚀 Quick Start

### 1. Unlock AbëKEYS Vault

```bash
# Sign in to 1Password (if using 1Password integration)
op signin

# Pull all credentials from 1Password to AbëKEYS vault
python3 scripts/unlock_all_credentials.py
```

### 2. Verify Credentials

```bash
# List all available credentials
python3 scripts/read_abekeys.py

# Check specific service
python3 scripts/read_abekeys.py stripe
python3 scripts/read_abekeys.py clerk
python3 scripts/read_abekeys.py aws
```

### 3. Credentials Are Automatically Loaded

The application **automatically** loads credentials from:
```
~/.abekeys/credentials/
```

**No configuration needed!** The app reads from AbëKEYS vault at runtime.

---

## 📁 Vault Structure

```
~/.abekeys/
├── encrypted_vault.json      # Encrypted vault (if using encryption)
├── credentials/              # Decrypted credential files
│   ├── stripe.json
│   ├── clerk.json
│   ├── aws.json
│   ├── database.json
│   ├── redis.json
│   └── ...
├── hmac_key.key              # Encryption keys (if using encryption)
└── kdf_salt.key
```

---

## 🔐 Supported Services

The following services are automatically loaded from AbëKEYS vault:

| Service | Credential File | Environment Variables |
|---------|----------------|---------------------|
| **Clerk** | `clerk.json` | `CLERK_SECRET_KEY`, `CLERK_PUBLISHABLE_KEY`, `CLERK_WEBHOOK_SECRET` |
| **Stripe** | `stripe.json` | `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET` |
| **AWS** | `aws.json` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` |
| **Database** | `database.json` | `DATABASE_URL`, `DATABASE_HOST`, `DATABASE_PORT`, etc. |
| **Redis** | `redis.json` | `REDIS_URL`, `REDIS_HOST`, `REDIS_PASSWORD`, etc. |
| **Postgres** | `postgres.json` | `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, etc. |

---

## 📝 Credential File Format

Each credential file is a JSON file with service-specific fields:

### Example: `stripe.json`

```json
{
  "service": "stripe",
  "api_key": "sk_live_...",
  "publishable_key": "pk_live_...",
  "webhook_secret": "whsec_..."
}
```

### Example: `clerk.json`

```json
{
  "service": "clerk",
  "api_key": "sk_live_...",
  "publishable_key": "pk_live_...",
  "webhook_secret": "whsec_..."
}
```

### Example: `database.json`

```json
{
  "service": "database",
  "url": "REPLACE_MEhost:5432/dbname",
  "host": "host.example.com",
  "port": 5432,
  "user": "username",
  "password": "password",
  "name": "database_name"
}
```

---

## 🔄 Credential Loading Priority

The application loads credentials in this order:

1. **AbëKEYS Vault** (`~/.abekeys/credentials/`) - **HIGHEST PRIORITY** ✅
   - Automatically detected and loaded
   - Supports all major services
   - Zero configuration needed

2. **AWS Secrets Manager** - Second Priority
   - Falls back if AbëKEYS not available
   - Uses existing AWS integration

3. **Environment Variables** - Lowest Priority
   - Handled by Pydantic BaseSettings
   - Used only if AbëKEYS and AWS not available

---

## 🛠️ Manual Credential Creation

If you need to create credentials manually:

```bash
# Create credential directory
mkdir -p ~/.abekeys/credentials

# Create Stripe credentials
cat > ~/.abekeys/credentials/stripe.json << EOF
{
  "service": "stripe",
  "api_key": "sk_live_...",
  "publishable_key": "pk_live_...",
  "webhook_secret": "whsec_..."
}
EOF

# Set secure permissions
chmod 600 ~/.abekeys/credentials/stripe.json
```

---

## 🔍 Verification

### Check Available Services

```bash
python3 scripts/read_abekeys.py
```

### Check Specific Service

```bash
python3 scripts/read_abekeys.py stripe
```

### Check from Python

```python
from app.core.config import get_settings

settings = get_settings()
print(f"Stripe Key: {'✅ Present' if settings.STRIPE_SECRET_KEY else '❌ Missing'}")
print(f"Clerk Key: {'✅ Present' if settings.CLERK_SECRET_KEY else '❌ Missing'}")
```

---

## 🚨 Security

- ✅ All credentials stored in `~/.abekeys/credentials/` (600 permissions)
- ✅ Never exposed to client-side code
- ✅ Server-side only access
- ✅ No .env files in repository
- ✅ No secrets in version control
- ✅ Encrypted vault support (optional)

---

## ❌ NEVER DO THIS

- ❌ Create `.env` files
- ❌ Use `process.env.STRIPE_SECRET_KEY` directly
- ❌ Commit environment variables
- ❌ Store secrets in code
- ❌ Share credential files

---

## 📚 Related Documentation

- **Integration Guide:** `docs/status/integrations/ABEKEYS_INTEGRATION_IMPLEMENTATION_COMPLETE.md`
- **API Documentation:** `docs/api/SYSTEM_KNOWS_API_KEYS_ALWAYS.md`
- **Scripts:** `scripts/read_abekeys.py`, `scripts/unlock_all_credentials.py`

---

**Pattern:** ABEKEYS × VAULT × SECURE × ONE  
**Status:** ✅ **OPERATIONAL**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

