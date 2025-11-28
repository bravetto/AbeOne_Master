#!/bin/bash
# ∞ Secure Key Sharing - Zero Cost, YAGNI-Approved ∞
# Pattern: SHARE × KEY × SECURE × TUNNEL × ONE
# Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ZERO)

set -e

KEY_FILE="$HOME/.abekeys/vault_key.key"
RECIPIENT="${1:-bryan@example.com}"

echo "∞ Secure Key Sharing - Zero Cost ∞"
echo "==================================="
echo ""

if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Encryption key not found: $KEY_FILE"
    echo "   Generate it first by encrypting a credential"
    exit 1
fi

echo "🔐 Sharing encryption key securely..."
echo ""
echo "Recipient: $RECIPIENT"
echo ""

# Method 1: SSH (if recipient has SSH access)
if command -v ssh &> /dev/null; then
    echo "✅ Method 1: SSH Transfer (Recommended)"
    echo ""
    echo "Option A: Direct SSH Copy"
    echo "  scp $KEY_FILE $RECIPIENT:~/.abekeys/vault_key.key"
    echo ""
    echo "Option B: SSH Tunnel + Copy"
    echo "  cat $KEY_FILE | ssh $RECIPIENT 'mkdir -p ~/.abekeys && cat > ~/.abekeys/vault_key.key && chmod 600 ~/.abekeys/vault_key.key'"
    echo ""
fi

# Method 2: Encrypted file (age encryption - zero cost, YAGNI)
if command -v age &> /dev/null || python3 -c "import age" 2>/dev/null; then
    echo "✅ Method 2: Age Encryption (Zero Cost)"
    echo ""
    echo "Generate recipient public key first, then:"
    echo "  age -r <recipient_public_key> -o vault_key.key.age $KEY_FILE"
    echo "  # Share vault_key.key.age via any channel (email, chat, etc.)"
    echo ""
else
    echo "⚠️  Method 2: Install age for encrypted file sharing"
    echo "  brew install age"
    echo "  # Or: pip3 install pyage"
    echo ""
fi

# Method 3: Base64 + QR Code (for in-person sharing)
if command -v qrencode &> /dev/null; then
    echo "✅ Method 3: QR Code (In-Person Sharing)"
    echo ""
    echo "  base64 $KEY_FILE | qrencode -o vault_key.png"
    echo "  # Show QR code, recipient scans with phone"
    echo ""
fi

# Method 4: Password-protected archive
echo "✅ Method 4: Password-Protected Archive"
echo ""
echo "  zip -e vault_key.zip $KEY_FILE"
echo "  # Share password via separate secure channel"
echo ""

echo "===================================="
echo "📋 Recommended: SSH Transfer"
echo ""
echo "If recipient has SSH access:"
echo "  ./scripts/abekeys/share_key_secure.sh bryan@server"
echo ""
echo "If no SSH access:"
echo "  1. Use age encryption (install: brew install age)"
echo "  2. Or password-protected zip"
echo "  3. Share password via separate channel"
echo ""
echo "∞ AbëONE ∞"

