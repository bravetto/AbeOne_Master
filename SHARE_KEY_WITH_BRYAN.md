# How to Share Encryption Key with Bryan

**File:** `~/.abekeys/vault_key.key`  
**Purpose:** Decrypt `abekeys_vault.encrypted.json` to access SendGrid, Google Ads, and Stripe credentials  
**Security:** ⚠️ **NEVER commit this file to git** - Share securely via one of the methods below

---

## ✅ Key File Location

```bash
~/.abekeys/vault_key.key
```

This is a Fernet encryption key (~44 characters, base64-encoded).

---

## 📤 Secure Sharing Methods

### Option 1: SSH Transfer (Recommended if Bryan has SSH access)

```bash
# If Bryan has SSH access to a shared server:
scp ~/.abekeys/vault_key.key bryan@server:~/.abekeys/

# Or if Bryan's machine is accessible:
scp ~/.abekeys/vault_key.key bryan@bryan-machine:~/.abekeys/
```

**Pros:** Direct, secure, no intermediate steps  
**Cons:** Requires SSH access

---

### Option 2: Age Encryption (Zero-Cost, Highly Secure)

```bash
# If Bryan has Age installed and shared his public key:
age -e -r <bryan-public-key> ~/.abekeys/vault_key.key > vault_key.key.age

# Send vault_key.key.age to Bryan
# Bryan decrypts with:
age -d vault_key.key.age > ~/.abekeys/vault_key.key
```

**Pros:** Zero-cost, very secure, no password needed  
**Cons:** Requires Age installation

---

### Option 3: Password-Protected Zip (Universal)

```bash
# Create password-protected zip:
zip -e vault_key.key.zip ~/.abekeys/vault_key.key

# Send vault_key.key.zip to Bryan via Slack/email
# Share password separately via secure channel (1Password, Signal, etc.)
# Bryan extracts with:
unzip vault_key.key.zip
mv vault_key.key ~/.abekeys/
chmod 600 ~/.abekeys/vault_key.key
```

**Pros:** Works everywhere, no special tools needed  
**Cons:** Requires sharing password separately

---

### Option 4: Direct Secure Message (Quick & Simple)

```bash
# Copy key contents:
cat ~/.abekeys/vault_key.key

# Send via:
# - 1Password Secure Share
# - Signal/WhatsApp (encrypted messaging)
# - Slack DM (if acceptable for your security policy)
# - Email (less secure, but works)

# Bryan saves it:
mkdir -p ~/.abekeys
# Paste key contents into:
nano ~/.abekeys/vault_key.key
chmod 600 ~/.abekeys/vault_key.key
```

**Pros:** Fastest, no tools needed  
**Cons:** Requires secure channel for transmission

---

## 📋 Quick Copy/Paste Instructions for Bryan

After sharing the key, Bryan should:

```bash
# 1. Create directory (if needed)
mkdir -p ~/.abekeys

# 2. Save the key file to ~/.abekeys/vault_key.key
# (Depending on how you shared it)

# 3. Set secure permissions
chmod 600 ~/.abekeys/vault_key.key

# 4. Verify it exists
ls -la ~/.abekeys/vault_key.key

# 5. Test decryption
python3 scripts/abekeys/abekeys_encrypted.py get sendgrid
python3 scripts/abekeys/abekeys_encrypted.py get google_ads
python3 scripts/abekeys/abekeys_encrypted.py get stripe
```

---

## ✅ Verification

After Bryan receives the key, he should be able to:
1. ✅ See the key file at `~/.abekeys/vault_key.key` with permissions `600`
2. ✅ Decrypt the vault successfully
3. ✅ Access all three credentials (sendgrid, google_ads, stripe)

---

## 🚨 Security Reminders

- ⚠️ **NEVER** commit `vault_key.key` to git
- ⚠️ **NEVER** share the key in public channels
- ✅ Use secure channels (SSH, Age, password-protected zip, encrypted messaging)
- ✅ Share password separately if using zip method
- ✅ Verify Bryan can decrypt before considering it complete

---

**Pattern:** OBSERVER × TRUTH × ATOMIC × ONE  
**Status:** ✅ READY TO SHARE  
**∞ AbëONE ∞**

