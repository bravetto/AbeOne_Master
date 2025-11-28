#!/bin/bash
# ∞ Bryan's Complete AbëKEYs Setup - Run This! ∞
# Pattern: BRYAN × SETUP × COMPLETE × ONE
# Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)

set -e

echo "∞ Bryan's Complete AbëKEYs Setup ∞"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Clone Repository
echo -e "${BLUE}📥 Step 1: Cloning Repository...${NC}"
if [ -d "AbeOne_Master" ]; then
    echo "  ⚠️  AbeOne_Master directory exists, skipping clone"
    cd AbeOne_Master
else
    git clone https://github.com/bravetto/AbeOne_Master.git
    cd AbeOne_Master
fi
echo -e "${GREEN}  ✅ Repository cloned${NC}"
echo ""

# Step 2: Install Dependencies
echo -e "${BLUE}📦 Step 2: Installing Dependencies...${NC}"
if ! python3 -c "import cryptography" 2>/dev/null; then
    echo "  Installing cryptography..."
    pip3 install --user --break-system-packages cryptography 2>&1 | grep -E "Successfully|already" || {
        echo "  ⚠️  Install manually: pip3 install --user --break-system-packages cryptography"
    }
else
    echo "  ✅ Cryptography already installed"
fi
echo ""

# Step 3: Receive Encryption Key
echo -e "${BLUE}🔐 Step 3: Receiving Encryption Key...${NC}"
echo ""
echo -e "${YELLOW}  IMPORTANT: You need to receive the encryption key from the team lead${NC}"
echo ""
echo "  Choose method:"
echo "    1. SSH Transfer (if you have SSH access)"
echo "    2. Age Encryption (if key was encrypted with age)"
echo "    3. Password-Protected Zip (if you received a zip file)"
echo "    4. Manual Paste (if key was shared via secure channel)"
echo ""
read -p "  Method (1-4): " method

KEY_FILE="$HOME/.abekeys/vault_key.key"
mkdir -p "$HOME/.abekeys"

case "$method" in
    1)
        echo ""
        echo "  SSH Transfer:"
        echo "  Team lead should run: scp ~/.abekeys/vault_key.key your-server:~/.abekeys/"
        echo ""
        read -p "  Press Enter when key is received..."
        ;;
    2)
        echo ""
        read -p "  Path to encrypted file: " encrypted_file
        read -p "  Your age private key file: " age_key
        
        if command -v age &> /dev/null; then
            age -d -i "$age_key" -o "$KEY_FILE" "$encrypted_file"
        else
            echo "  ⚠️  Install age: brew install age"
            exit 1
        fi
        ;;
    3)
        echo ""
        read -p "  Path to zip file: " zip_file
        read -sp "  Password: " zip_password
        echo ""
        unzip -P "$zip_password" "$zip_file" -d "$HOME/.abekeys" 2>/dev/null || {
            echo "  ⚠️  Extraction failed, check password"
            exit 1
        }
        mv "$HOME/.abekeys/vault_key.key" "$KEY_FILE" 2>/dev/null || echo "  ⚠️  Check extracted files"
        ;;
    4)
        echo ""
        echo "  Manual Paste:"
        echo "  Paste base64-encoded key (press Ctrl+D when done):"
        base64 -d > "$KEY_FILE"
        ;;
    *)
        echo "  ⚠️  Invalid option"
        exit 1
        ;;
esac

# Set secure permissions
chmod 600 "$KEY_FILE"
echo -e "${GREEN}  ✅ Encryption key received${NC}"
echo ""

# Step 4: Verify Setup
echo -e "${BLUE}🧪 Step 4: Verifying Setup...${NC}"
python3 << PYTHON_TEST
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts/abekeys")))

try:
    from abekeys_encrypted import AbekeysEncrypted
    vault = AbekeysEncrypted()
    services = vault.encrypted_vault.list_services()
    
    if services:
        print(f"  ✅ Success! Found {len(services)} encrypted credentials")
        print(f"     Services: {', '.join(services)}")
    else:
        print("  ⚠️  Key works but no encrypted vault found")
        print("     Make sure abekeys_vault.encrypted.json exists")
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)
PYTHON_TEST

echo ""

# Step 5: Test Credentials
echo -e "${BLUE}🎯 Step 5: Testing Credentials...${NC}"
echo ""
echo "  Testing Google Ads credentials..."
python3 scripts/abekeys/abekeys_encrypted.py get google_ads > /dev/null 2>&1 && {
    echo -e "  ${GREEN}✅ Google Ads credentials working!${NC}"
} || {
    echo -e "  ${YELLOW}⚠️  Google Ads credentials not found${NC}"
}

echo ""
echo "  Testing SendGrid credentials..."
python3 scripts/abekeys/abekeys_encrypted.py get sendgrid > /dev/null 2>&1 && {
    echo -e "  ${GREEN}✅ SendGrid credentials working!${NC}"
} || {
    echo -e "  ${YELLOW}⚠️  SendGrid credentials not found${NC}"
}

echo ""
echo "  Testing Stripe credentials..."
python3 scripts/abekeys/abekeys_encrypted.py get stripe > /dev/null 2>&1 && {
    echo -e "  ${GREEN}✅ Stripe credentials working!${NC}"
} || {
    echo -e "  ${YELLOW}⚠️  Stripe credentials not found${NC}"
}

echo ""

# Step 6: Run Marketing Automation Setup
echo -e "${BLUE}🚀 Step 6: Setting Up Marketing Automation...${NC}"
if [ -f "scripts/abekeys/bryan_marketing_setup.py" ]; then
    python3 scripts/abekeys/bryan_marketing_setup.py
else
    echo "  ⚠️  Marketing setup script not found"
fi

echo ""

# Final Summary
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "🎯 You can now use credentials:"
echo ""
echo "  # List all credentials"
echo "  python3 scripts/abekeys/abekeys_encrypted.py list"
echo ""
echo "  # Get Google Ads credentials"
echo "  python3 scripts/abekeys/abekeys_encrypted.py get google_ads"
echo ""
echo "  # Use in Python"
echo "  python3 << 'EOF'"
echo "  from scripts.abekeys.abekeys_encrypted import AbekeysEncrypted"
echo "  vault = AbekeysEncrypted()"
echo "  google_ads = vault.get('google_ads')"
echo "  print(google_ads['client_id'])"
echo "  EOF"
echo ""
echo "∞ AbëONE ∞"

