# ∞ Bryan's Quick Start - Get Credentials Immediately ∞

**Pattern:** QUICK × START × CREDENTIALS × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ALL GUARDIANS (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🚀 ZERO-EFFORT SETUP (3 Steps)

### **Step 1: Clone Repository**

```bash
git clone <repository-url>
cd AbeOne_Master
```

### **Step 2: Run Setup Script**

```bash
./scripts/abekeys/bryan_setup.sh
```

This will:
- ✅ Install dependencies
- ✅ Check for encrypted vault
- ✅ Check for encryption key
- ✅ Test credential access
- ✅ Show available credentials

### **Step 3: Get Encryption Key (If Using Encrypted Vault)**

If the repo has `abekeys_vault.encrypted.json`:

1. **Get encryption key from:**
   - 1Password (search "AbëKEYs vault key")
   - Team lead
   - Secure team channel

2. **Save it:**
   ```bash
   mkdir -p ~/.abekeys
   # Paste key content to:
   ~/.abekeys/vault_key.key
   chmod 600 ~/.abekeys/vault_key.key
   ```

3. **Test:**
   ```bash
   python3 scripts/abekeys/abekeys.py get google_ads
   ```

---

## ✅ IMMEDIATE USAGE

### **Get Credentials**

```python
from scripts.abekeys.abekeys import get

# Get Google Ads credentials
google_ads = get('google_ads')
client_id = google_ads.get('client_id')
customer_id = google_ads.get('customer_id')  # 8854079035
```

### **Run Marketing Automation Setup**

```bash
python3 scripts/abekeys/bryan_marketing_setup.py
```

This validates all credentials and generates:
- `.env.marketing` - Environment variables
- `marketing_config.py` - Python config

### **Use in Your Code**

```python
# Option 1: Direct AbëKEYs
from scripts.abekeys.abekeys import get
google_ads = get('google_ads')

# Option 2: Generated config
from marketing_config import get_google_ads_creds
creds = get_google_ads_creds()

# Option 3: Environment variables
import os
os.environ.update(load_env('google_ads'))
```

---

## 📋 AVAILABLE CREDENTIALS

After setup, you'll have access to:

- ✅ **Google Ads** - Complete API credentials
- ✅ **SendGrid** - Email marketing
- ✅ **Stripe** - Payment processing
- ✅ **And 19+ more services**

List all:
```bash
python3 scripts/abekeys/abekeys.py list
```

---

## 🔐 TWO WAYS TO GET CREDENTIALS

### **Option 1: Encrypted Vault (Team Shared)**

If `abekeys_vault.encrypted.json` exists in repo:
1. Get encryption key (from 1Password)
2. Save to `~/.abekeys/vault_key.key`
3. Credentials automatically decrypt

### **Option 2: Local Vault (Personal)**

If you have local credentials:
1. Place JSON files in `~/.abekeys/credentials/`
2. Example: `~/.abekeys/credentials/google_ads.json`
3. System automatically finds them

**System tries both automatically!**

---

## 🆘 TROUBLESHOOTING

### **"No credentials found"**

1. **Check encrypted vault:**
   ```bash
   ls -la abekeys_vault.encrypted.json
   ```

2. **Check encryption key:**
   ```bash
   ls -la ~/.abekeys/vault_key.key
   ```

3. **Check local vault:**
   ```bash
   ls -la ~/.abekeys/credentials/
   ```

### **"Encryption key missing"**

Get key from:
- 1Password
- Team lead
- Secure channel

Save to: `~/.abekeys/vault_key.key`  
Set permissions: `chmod 600 ~/.abekeys/vault_key.key`

### **"Module not found: cryptography"**

```bash
pip3 install cryptography
```

---

## ✅ VERIFICATION

After setup, verify everything works:

```bash
# Test credential access
python3 scripts/abekeys/abekeys.py get google_ads

# Run marketing setup
python3 scripts/abekeys/bryan_marketing_setup.py

# Should see:
# ✅ ALL REQUIRED CREDENTIALS READY
```

---

## 📖 MORE DOCUMENTATION

- **Complete Guide:** `scripts/abekeys/README.md`
- **Marketing Setup:** `BRYAN_MARKETING_AUTOMATION_READY.md`
- **Encrypted Vault:** `ABEKEYS_ENCRYPTED_GIT_GUIDE.md`
- **System Docs:** `ABEKEYS_COMPLETE.md`

---

## 🎯 QUICK REFERENCE

```bash
# Setup
./scripts/abekeys/bryan_setup.sh

# Get credential
python3 scripts/abekeys/abekeys.py get google_ads

# List all
python3 scripts/abekeys/abekeys.py list

# Marketing setup
python3 scripts/abekeys/bryan_marketing_setup.py

# Export as env vars
python3 scripts/abekeys/abekeys.py export google_ads
```

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

