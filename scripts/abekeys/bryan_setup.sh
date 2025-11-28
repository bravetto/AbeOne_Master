#!/bin/bash
# ∞ Bryan's AbëKEYs Setup - Zero-Effort Credential Access ∞
# Pattern: SETUP × BRYAN × CREDENTIALS × ONE
# Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)

set -e

echo "∞ Bryan's AbëKEYs Setup ∞"
echo "=========================="
echo ""

# Check if cryptography is installed (optional - only needed for encrypted vault)
if ! python3 -c "import cryptography" 2>/dev/null; then
    echo "⚠️  Cryptography not installed (optional - only needed for encrypted vault)"
    echo "   To install: pip3 install --user cryptography"
    echo "   Or: python3 -m pip install --user cryptography"
    echo "   Local vault works without it!"
fi

# Check if encrypted vault exists
if [ -f "abekeys_vault.encrypted.json" ]; then
    echo "✅ Found encrypted vault: abekeys_vault.encrypted.json"
else
    echo "⚠️  No encrypted vault found. Using local credentials."
fi

# Check if encryption key exists
KEY_PATH="$HOME/.abekeys/vault_key.key"
if [ -f "$KEY_PATH" ]; then
    echo "✅ Found encryption key: $KEY_PATH"
else
    echo "⚠️  No encryption key found."
    echo "   If using encrypted vault, get the key from:"
    echo "   - 1Password (search for 'AbëKEYs vault key')"
    echo "   - Team lead"
    echo "   - Secure team channel"
    echo ""
    echo "   Save it to: $KEY_PATH"
    echo "   Then run: chmod 600 $KEY_PATH"
fi

# Check local credentials
CRED_PATH="$HOME/.abekeys/credentials"
if [ -d "$CRED_PATH" ] && [ "$(ls -A $CRED_PATH/*.json 2>/dev/null | wc -l)" -gt 0 ]; then
    echo "✅ Found local credentials: $CRED_PATH"
    echo "   Available credentials:"
    ls -1 $CRED_PATH/*.json 2>/dev/null | xargs -n1 basename | sed 's/\.json$//' | sed 's/^/     • /'
else
    echo "⚠️  No local credentials found."
fi

echo ""
echo "🧪 Testing credential access..."
echo ""

# Test getting a credential
python3 << 'PYTHON_TEST'
import sys
from pathlib import Path

# Try encrypted vault first
try:
    sys.path.insert(0, str(Path("scripts/abekeys")))
    from abekeys_encrypted import AbekeysEncrypted
    
    vault = AbekeysEncrypted()
    google_ads = vault.get('google_ads')
    if google_ads:
        print("✅ Encrypted vault working!")
        print(f"   Google Ads customer_id: {google_ads.get('customer_id', 'N/A')}")
    else:
        print("⚠️  Encrypted vault empty or key missing")
except Exception as e:
    print(f"⚠️  Encrypted vault error: {e}")

# Try local vault
try:
    from scripts.abekeys.abekeys import get
    
    google_ads = get('google_ads')
    if google_ads:
        print("✅ Local vault working!")
        print(f"   Google Ads customer_id: {google_ads.get('customer_id', 'N/A')}")
    else:
        print("⚠️  Local vault empty")
except Exception as e:
    print(f"⚠️  Local vault error: {e}")

PYTHON_TEST

echo ""
echo "📋 Quick Start:"
echo ""
echo "  # Get a credential"
echo "  python3 scripts/abekeys/abekeys.py get google_ads"
echo ""
echo "  # Run marketing automation setup"
echo "  python3 scripts/abekeys/bryan_marketing_setup.py"
echo ""
echo "✅ Setup complete!"
echo ""
echo "∞ AbëONE ∞"

