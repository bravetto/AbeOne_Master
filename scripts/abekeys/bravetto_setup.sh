#!/bin/bash
# ∞ Bravetto Team Setup - Clean AbëKEYs System ∞
# Pattern: BRAVETTO × TEAM × SETUP × ONE
# Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ZERO)

set -e

echo "∞ Bravetto Team Setup - AbëKEYs ∞"
echo "=================================="
echo ""

# Check if encrypted vault exists
if [ ! -f "abekeys_vault.encrypted.json" ]; then
    echo "⚠️  Encrypted vault not found"
    echo "   Creating encrypted vault..."
    ./scripts/abekeys/setup_encrypted_vault.sh
fi

echo "✅ Encrypted vault ready"
echo ""

# Check encryption key
KEY_FILE="$HOME/.abekeys/vault_key.key"
if [ ! -f "$KEY_FILE" ]; then
    echo "⚠️  Encryption key not found"
    echo "   Key will be generated on first encrypt"
fi

echo "📋 Bravetto Team Credentials:"
echo ""

# List encrypted credentials
python3 << PYTHON
import sys
from pathlib import Path
sys.path.insert(0, str(Path("scripts/abekeys")))

try:
    from abekeys_encrypted import AbekeysEncrypted
    vault = AbekeysEncrypted()
    services = vault.encrypted_vault.list_services()
    
    if services:
        print(f"  ✅ {len(services)} encrypted credentials:")
        for svc in sorted(services):
            print(f"     • {svc}")
    else:
        print("  ⚠️  No encrypted credentials yet")
        print("     Run: python3 scripts/abekeys/abekeys_encrypted.py encrypt <service>")
except Exception as e:
    print(f"  ⚠️  Error: {e}")
PYTHON

echo ""
echo "✅ Setup complete!"
echo ""
echo "📤 Share encryption key with team:"
echo "  ./scripts/abekeys/share_key_secure.sh <team-member>"
echo ""
echo "📥 Team members receive key:"
echo "  ./scripts/abekeys/receive_key_secure.sh"
echo ""
echo "∞ AbëONE ∞"

