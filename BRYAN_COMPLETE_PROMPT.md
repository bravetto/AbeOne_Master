# ∞ Bryan's Complete Setup Prompt - Copy & Run This! ∞

**Pattern:** BRYAN × COMPLETE × PROMPT × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)  
**Guardians:** AEYON (999 Hz) + META (777 Hz) + ALL GUARDIANS (530 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🚀 COMPLETE PROMPT FOR BRYAN

**Copy this entire section and run it on your system:**

---

```bash
#!/bin/bash
# ∞ Bryan's Complete AbëKEYs Setup ∞

set -e

echo "∞ Bryan's Complete AbëKEYs Setup ∞"
echo "=================================="
echo ""

# Step 1: Clone Repository
echo "📥 Step 1: Cloning Repository..."
git clone https://github.com/bravetto/AbeOne_Master.git
cd AbeOne_Master
echo "✅ Repository cloned"
echo ""

# Step 2: Install Dependencies
echo "📦 Step 2: Installing Dependencies..."
pip3 install --user --break-system-packages cryptography 2>&1 | grep -E "Successfully|already" || {
    echo "⚠️  Install manually: pip3 install --user --break-system-packages cryptography"
}
echo ""

# Step 3: Receive Encryption Key
echo "🔐 Step 3: Receiving Encryption Key..."
echo ""
echo "IMPORTANT: You need to receive the encryption key from the team lead"
echo ""
echo "Choose method:"
echo "  1. SSH Transfer (if you have SSH access)"
echo "  2. Age Encryption (if key was encrypted with age)"
echo "  3. Password-Protected Zip (if you received a zip file)"
echo "  4. Manual Paste (if key was shared via secure channel)"
echo ""
read -p "Method (1-4): " method

KEY_FILE="$HOME/.abekeys/vault_key.key"
mkdir -p "$HOME/.abekeys"

case "$method" in
    1)
        echo ""
        echo "SSH Transfer:"
        echo "Team lead should run: scp ~/.abekeys/vault_key.key your-server:~/.abekeys/"
        echo ""
        read -p "Press Enter when key is received..."
        ;;
    2)
        echo ""
        read -p "Path to encrypted file: " encrypted_file
        read -p "Your age private key file: " age_key
        
        if command -v age &> /dev/null; then
            age -d -i "$age_key" -o "$KEY_FILE" "$encrypted_file"
        else
            echo "⚠️  Install age: brew install age"
            exit 1
        fi
        ;;
    3)
        echo ""
        read -p "Path to zip file: " zip_file
        read -sp "Password: " zip_password
        echo ""
        unzip -P "$zip_password" "$zip_file" -d "$HOME/.abekeys" 2>/dev/null || {
            echo "⚠️  Extraction failed, check password"
            exit 1
        }
        mv "$HOME/.abekeys/vault_key.key" "$KEY_FILE" 2>/dev/null || echo "⚠️  Check extracted files"
        ;;
    4)
        echo ""
        echo "Manual Paste:"
        echo "Paste base64-encoded key (press Ctrl+D when done):"
        base64 -d > "$KEY_FILE"
        ;;
    *)
        echo "⚠️  Invalid option"
        exit 1
        ;;
esac

chmod 600 "$KEY_FILE"
echo "✅ Encryption key received"
echo ""

# Step 4: Verify Setup
echo "🧪 Step 4: Verifying Setup..."
python3 << 'PYTHON_TEST'
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts/abekeys")))

try:
    from abekeys_encrypted import AbekeysEncrypted
    vault = AbekeysEncrypted()
    services = vault.encrypted_vault.list_services()
    
    if services:
        print(f"✅ Success! Found {len(services)} encrypted credentials")
        print(f"   Services: {', '.join(services)}")
    else:
        print("⚠️  Key works but no encrypted vault found")
        print("   Make sure abekeys_vault.encrypted.json exists")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
PYTHON_TEST

echo ""

# Step 5: Test Credentials
echo "🎯 Step 5: Testing Credentials..."
echo ""
echo "Testing Google Ads credentials..."
python3 scripts/abekeys/abekeys_encrypted.py get google_ads > /dev/null 2>&1 && {
    echo "✅ Google Ads credentials working!"
} || {
    echo "⚠️  Google Ads credentials not found"
}

echo ""
echo "Testing SendGrid credentials..."
python3 scripts/abekeys/abekeys_encrypted.py get sendgrid > /dev/null 2>&1 && {
    echo "✅ SendGrid credentials working!"
} || {
    echo "⚠️  SendGrid credentials not found"
}

echo ""
echo "Testing Stripe credentials..."
python3 scripts/abekeys/abekeys_encrypted.py get stripe > /dev/null 2>&1 && {
    echo "✅ Stripe credentials working!"
} || {
    echo "⚠️  Stripe credentials not found"
}

echo ""

# Step 6: Run Marketing Automation Setup
echo "🚀 Step 6: Setting Up Marketing Automation..."
if [ -f "scripts/abekeys/bryan_marketing_setup.py" ]; then
    python3 scripts/abekeys/bryan_marketing_setup.py
else
    echo "⚠️  Marketing setup script not found"
fi

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "🎯 You can now use credentials:"
echo ""
echo "# List all credentials"
echo "python3 scripts/abekeys/abekeys_encrypted.py list"
echo ""
echo "# Get Google Ads credentials"
echo "python3 scripts/abekeys/abekeys_encrypted.py get google_ads"
echo ""
echo "# Use in Python"
echo "python3 << 'EOF'"
echo "from scripts.abekeys.abekeys_encrypted import AbekeysEncrypted"
echo "vault = AbekeysEncrypted()"
echo "google_ads = vault.get('google_ads')"
echo "print(google_ads['client_id'])"
echo "EOF"
```

---

## 📋 QUICK START (One-Liner)

**Or use the automated script:**

```bash
curl -sSL https://raw.githubusercontent.com/bravetto/AbeOne_Master/main/BRYAN_COMPLETE_SETUP.sh | bash
```

**Or download and run:**

```bash
# Download script
curl -o bryan_setup.sh https://raw.githubusercontent.com/bravetto/AbeOne_Master/main/BRYAN_COMPLETE_SETUP.sh

# Make executable
chmod +x bryan_setup.sh

# Run it
./bryan_setup.sh
```

---

## 🎯 MANUAL STEPS (If Script Doesn't Work)

### **1. Clone Repository**
```bash
git clone https://github.com/bravetto/AbeOne_Master.git
cd AbeOne_Master
```

### **2. Install Dependencies**
```bash
pip3 install --user --break-system-packages cryptography
```

### **3. Receive Encryption Key**
```bash
# Use the receive script
./scripts/abekeys/receive_key_secure.sh

# Or manually:
mkdir -p ~/.abekeys
# Get key from team lead and save to ~/.abekeys/vault_key.key
chmod 600 ~/.abekeys/vault_key.key
```

### **4. Test Setup**
```bash
python3 scripts/abekeys/abekeys_encrypted.py list
python3 scripts/abekeys/abekeys_encrypted.py get google_ads
```

### **5. Run Marketing Setup**
```bash
python3 scripts/abekeys/bryan_marketing_setup.py
```

---

## ✅ WHAT YOU'LL GET

After setup, you'll have:
- ✅ Access to encrypted credentials (google_ads, sendgrid, stripe)
- ✅ Marketing automation setup
- ✅ Zero-effort credential access
- ✅ Ready to use immediately!

---

## 🆘 TROUBLESHOOTING

### **If cryptography install fails:**
```bash
# Try with virtual environment
python3 -m venv venv
source venv/bin/activate
pip install cryptography
```

### **If key doesn't work:**
- Verify key file exists: `ls -la ~/.abekeys/vault_key.key`
- Check permissions: `chmod 600 ~/.abekeys/vault_key.key`
- Verify encrypted vault exists: `ls -la abekeys_vault.encrypted.json`

### **If credentials not found:**
- Make sure you're in the repo directory
- Check encrypted vault exists: `test -f abekeys_vault.encrypted.json`
- List available: `python3 scripts/abekeys/abekeys_encrypted.py list`

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

