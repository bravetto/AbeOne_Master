#!/bin/bash
# ∞ Receive Encryption Key Securely - For Bryan & Team ∞
# Pattern: RECEIVE × KEY × SECURE × ONE
# Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ZERO)

set -e

KEY_FILE="$HOME/.abekeys/vault_key.key"
KEY_DIR="$HOME/.abekeys"

echo "∞ Receive Encryption Key Securely ∞"
echo "==================================="
echo ""

mkdir -p "$KEY_DIR"

echo "📥 Choose method to receive key:"
echo ""
echo "1. SSH Transfer (if sender has your SSH access)"
echo "2. Age-encrypted file (if sender used age)"
echo "3. Password-protected zip (if sender sent zip)"
echo "4. QR Code scan (if in-person)"
echo "5. Manual paste (secure channel)"
echo ""

read -p "Method (1-5): " method

case "$method" in
    1)
        echo ""
        echo "SSH Transfer:"
        echo "  Sender runs: scp ~/.abekeys/vault_key.key your-server:~/.abekeys/"
        echo "  Or: cat ~/.abekeys/vault_key.key | ssh your-server 'cat > ~/.abekeys/vault_key.key'"
        echo ""
        echo "Waiting for key via SSH..."
        # Key should arrive at $KEY_FILE
        ;;
    2)
        echo ""
        echo "Age Decryption:"
        read -p "Path to encrypted file: " encrypted_file
        read -p "Your age private key file: " age_key
        
        if command -v age &> /dev/null; then
            age -d -i "$age_key" -o "$KEY_FILE" "$encrypted_file"
        else
            echo "Install age: brew install age"
            exit 1
        fi
        ;;
    3)
        echo ""
        echo "Password-Protected Zip:"
        read -p "Path to zip file: " zip_file
        unzip -P "" "$zip_file" -d "$KEY_DIR"
        mv "$KEY_DIR/vault_key.key" "$KEY_FILE" 2>/dev/null || echo "Extract manually"
        ;;
    4)
        echo ""
        echo "QR Code Scan:"
        echo "  Scan QR code with phone"
        echo "  Copy base64 content"
        echo "  Paste here (press Ctrl+D when done):"
        base64 -d > "$KEY_FILE"
        ;;
    5)
        echo ""
        echo "Manual Paste:"
        echo "  Paste base64-encoded key (press Ctrl+D when done):"
        base64 -d > "$KEY_FILE"
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

# Set secure permissions
chmod 600 "$KEY_FILE"

echo ""
echo "✅ Key received and saved to: $KEY_FILE"
echo ""
echo "🧪 Testing decryption..."
python3 << PYTHON_TEST
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts/abekeys")))
try:
    from abekeys_encrypted import AbekeysEncrypted
    vault = AbekeysEncrypted()
    services = vault.encrypted_vault.list_services()
    if services:
        print(f"✅ Success! Found {len(services)} encrypted credentials")
        print(f"   Services: {', '.join(services[:5])}")
    else:
        print("⚠️  Key works but no encrypted vault found in repo")
        print("   Clone repo or get abekeys_vault.encrypted.json")
except Exception as e:
    print(f"❌ Error: {e}")
PYTHON_TEST

echo ""
echo "✅ Ready to use encrypted credentials!"
echo ""
echo "∞ AbëONE ∞"

