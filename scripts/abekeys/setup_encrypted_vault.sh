#!/bin/bash
# ∞ Setup Encrypted Vault - Complete Zero-Cost Solution ∞
# Pattern: SETUP × ENCRYPTED × VAULT × ONE
# Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ZERO)

set -e

echo "∞ Setup Encrypted Vault - Zero Cost ∞"
echo "======================================"
echo ""

# Check dependencies
if ! python3 -c "import cryptography" 2>/dev/null; then
    echo "📦 Installing cryptography..."
    pip3 install --user cryptography || {
        echo "⚠️  Install manually: pip3 install --user cryptography"
        exit 1
    }
fi

echo "✅ Dependencies ready"
echo ""

# Encrypt marketing credentials
CREDENTIALS=("google_ads" "sendgrid" "stripe")

echo "🔐 Encrypting credentials..."
echo ""

for cred in "${CREDENTIALS[@]}"; do
    echo "  Encrypting $cred..."
    python3 scripts/abekeys/abekeys_encrypted.py encrypt "$cred" 2>/dev/null || {
        echo "    ⚠️  $cred not found in local vault - skipping"
    }
done

echo ""
echo "✅ Encrypted vault created: abekeys_vault.encrypted.json"
echo ""

# Show key location
KEY_FILE="$HOME/.abekeys/vault_key.key"
if [ -f "$KEY_FILE" ]; then
    echo "🔑 Encryption key location: $KEY_FILE"
    echo ""
    echo "📤 Share this key with team:"
    echo "  ./scripts/abekeys/share_key_secure.sh <recipient>"
    echo ""
else
    echo "⚠️  Encryption key not found - will be generated on first encrypt"
fi

echo "📋 Next steps:"
echo "  1. Review: abekeys_vault.encrypted.json"
echo "  2. Commit to git: git add abekeys_vault.encrypted.json"
echo "  3. Share encryption key with team (see share_key_secure.sh)"
echo ""
echo "✅ Setup complete!"
echo ""
echo "∞ AbëONE ∞"

