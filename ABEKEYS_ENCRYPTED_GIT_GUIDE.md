# ∞ AbëKEYs Encrypted Vault - Git-Safe Credential Storage ∞

**Pattern:** ENCRYPTION × VAULT × GIT × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ZERO)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ZERO (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## ✅ YES: Encrypted Keys CAN Be in Git

**Answer:** Yes, encrypted credentials can be safely stored in git if:
1. ✅ Properly encrypted (Fernet/AES-256)
2. ✅ Encryption key is NOT in git
3. ✅ Strong encryption algorithm
4. ✅ Key stored separately (local or secure key manager)

---

## 🔐 HOW IT WORKS

### **Two Vault System**

1. **Encrypted Vault** (`abekeys_vault.encrypted.json`)
   - ✅ CAN be in git (it's encrypted)
   - ✅ Shared with team
   - ✅ Contains encrypted credentials
   - ✅ Safe to commit

2. **Encryption Key** (`~/.abekeys/vault_key.key`)
   - ❌ NOT in git (gitignored)
   - ❌ Personal/team secret
   - ❌ Required to decrypt
   - ❌ Must be shared securely (1Password, etc.)

3. **Local Vault** (`~/.abekeys/credentials/`)
   - ❌ NOT in git (gitignored)
   - ❌ Personal credentials
   - ❌ Overrides encrypted vault
   - ❌ For local-only secrets

---

## 🚀 QUICK START

### **Step 0: Install Dependencies**

```bash
# Install cryptography library
pip3 install cryptography>=41.0.0

# Or use requirements file
pip3 install -r scripts/abekeys/requirements.txt
```

### **Step 1: Encrypt Existing Credentials**

```bash
cd /Users/michaelmataluni/Documents/AbeOne_Master

# Encrypt Google Ads credentials
python3 scripts/abekeys/abekeys_encrypted.py encrypt google_ads

# Encrypt SendGrid credentials
python3 scripts/abekeys/abekeys_encrypted.py encrypt sendgrid

# Encrypt Stripe credentials
python3 scripts/abekeys/abekeys_encrypted.py encrypt stripe
```

This creates `abekeys_vault.encrypted.json` which CAN be committed to git.

### **Step 2: Add to Git**

```bash
# Add encrypted vault (safe to commit)
git add abekeys_vault.encrypted.json

# Ensure key is NOT committed
echo "~/.abekeys/vault_key.key" >> .gitignore
echo "abekeys_vault.encrypted.json" >> .gitignore  # Actually, this CAN be in git
# Remove it from gitignore if you want it in git

# Commit
git commit -m "feat: Add encrypted credential vault (git-safe)"
```

### **Step 3: Share Encryption Key Securely**

The encryption key at `~/.abekeys/vault_key.key` must be shared securely:
- ✅ 1Password (recommended)
- ✅ Secure team chat
- ✅ Encrypted email
- ❌ NOT in git
- ❌ NOT in Slack/email unencrypted

---

## 📋 USAGE

### **Using Encrypted Vault**

```python
from scripts.abekeys.abekeys_encrypted import AbekeysEncrypted

# Initialize (reads encrypted vault from repo)
vault = AbekeysEncrypted(
    vault_path=Path("abekeys_vault.encrypted.json"),  # In git
    key_path=Path.home() / ".abekeys" / "vault_key.key"  # NOT in git
)

# Get credential (automatically decrypts)
google_ads = vault.get('google_ads')
client_id = google_ads['client_id']
```

### **CLI Usage**

```bash
# List all credentials (encrypted + local)
python3 scripts/abekeys/abekeys_encrypted.py list

# Get decrypted credential
python3 scripts/abekeys/abekeys_encrypted.py get google_ads

# Encrypt local credential to vault
python3 scripts/abekeys/abekeys_encrypted.py encrypt google_ads
```

---

## 🔐 SECURITY MODEL

### **What CAN Be in Git**

- ✅ `abekeys_vault.encrypted.json` - Encrypted vault
- ✅ `scripts/abekeys/abekeys_encrypted.py` - Encryption code
- ✅ Documentation

### **What MUST NOT Be in Git**

- ❌ `~/.abekeys/vault_key.key` - Encryption key
- ❌ `~/.abekeys/credentials/*.json` - Unencrypted local credentials
- ❌ `.env.marketing` - Generated env files
- ❌ `marketing_config.py` - Generated config files

### **Encryption Details**

- **Algorithm:** Fernet (symmetric encryption)
- **Key Size:** 256 bits
- **Key Derivation:** PBKDF2HMAC (if using password)
- **Format:** Base64-encoded encrypted JSON

---

## 🎯 WORKFLOW

### **For Team Members**

1. **Clone Repository**
   ```bash
   git clone <repo>
   ```

2. **Get Encryption Key** (from 1Password or team lead)
   ```bash
   # Save key to ~/.abekeys/vault_key.key
   # Set secure permissions
   chmod 600 ~/.abekeys/vault_key.key
   ```

3. **Use Credentials**
   ```python
   from scripts.abekeys.abekeys_encrypted import AbekeysEncrypted
   vault = AbekeysEncrypted()
   creds = vault.get('google_ads')
   ```

### **For Adding New Credentials**

1. **Add to Local Vault First**
   ```bash
   # Create credential file
   cat > ~/.abekeys/credentials/my_service.json << 'EOF'
   {
     "api_key": "your_key_here"
   }
   EOF
   ```

2. **Encrypt and Add to Git**
   ```bash
   python3 scripts/abekeys/abekeys_encrypted.py encrypt my_service
   git add abekeys_vault.encrypted.json
   git commit -m "feat: Add my_service credentials"
   ```

---

## ✅ BENEFITS

### **Encrypted Vault in Git**

- ✅ **Team Sharing:** All team members get credentials automatically
- ✅ **Version Control:** Track credential changes
- ✅ **Backup:** Credentials backed up in git
- ✅ **CI/CD:** Can use in automated deployments
- ✅ **Audit Trail:** See who changed what credentials

### **Security**

- ✅ **Encrypted:** Credentials are encrypted at rest
- ✅ **Key Separation:** Encryption key not in git
- ✅ **Strong Encryption:** Fernet/AES-256
- ✅ **Zero Trust:** Validates everything

---

## 🔧 INTEGRATION

### **Update AbëKEYs to Support Both**

The system automatically tries:
1. Encrypted vault (from git)
2. Local vault (personal overrides)

This gives you:
- **Team credentials** in encrypted vault (git)
- **Personal credentials** in local vault (not in git)
- **Seamless access** to both

---

## 📝 .gitignore UPDATES

```gitignore
# AbëKEYs - Encryption Key (MUST NOT be in git)
~/.abekeys/vault_key.key
*.key

# AbëKEYs - Local Credentials (MUST NOT be in git)
~/.abekeys/credentials/
*.abekeys

# AbëKEYs - Encrypted Vault (CAN be in git)
# abekeys_vault.encrypted.json  # Remove from gitignore if you want it in git
```

---

## 🎯 RECOMMENDED APPROACH

### **Option 1: Encrypted Vault in Git (Recommended for Teams)**

```bash
# 1. Encrypt credentials
python3 scripts/abekeys/abekeys_encrypted.py encrypt google_ads

# 2. Add to git
git add abekeys_vault.encrypted.json
git commit -m "feat: Add encrypted credential vault"

# 3. Share encryption key via 1Password
```

### **Option 2: Local Vault Only (Current Approach)**

```bash
# Keep credentials in ~/.abekeys/credentials/
# NOT in git
# Each team member manages their own
```

### **Option 3: Hybrid (Best of Both)**

```bash
# Team credentials → Encrypted vault (in git)
# Personal credentials → Local vault (not in git)
# System automatically uses both
```

---

## ✅ SUMMARY

**Question:** Can encrypted keys be in git?  
**Answer:** ✅ **YES** - If properly encrypted with key stored separately

**Implementation:**
- ✅ Encrypted vault: `abekeys_vault.encrypted.json` (CAN be in git)
- ✅ Encryption key: `~/.abekeys/vault_key.key` (NOT in git)
- ✅ Local vault: `~/.abekeys/credentials/` (NOT in git)

**Security:**
- ✅ Fernet encryption (AES-256)
- ✅ Key stored separately
- ✅ Strong encryption algorithm
- ✅ Zero-trust validation

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

