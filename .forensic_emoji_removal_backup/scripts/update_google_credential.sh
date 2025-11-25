#!/bin/bash

# Quick script to update Google credential in ABEKEYS vault
# Usage: ./scripts/update_google_credential.sh "YOUR_API_KEY_HERE" [gemini|calendar|gcp]

set -e

API_KEY="${1}"
API_TYPE="${2:-gemini}"
CREDENTIAL_FILE="$HOME/.abekeys/credentials/google_bravetto.json"

if [ -z "$API_KEY" ]; then
    echo "❌ Error: API key required"
    echo "Usage: $0 \"YOUR_API_KEY_HERE\" [gemini|calendar|gcp]"
    exit 1
fi

echo "🔧 Updating Google credential..."
echo "   API Key: ${API_KEY:0:20}... (${#API_KEY} chars)"
echo "   Type: $API_TYPE"
echo ""

# Backup existing file
if [ -f "$CREDENTIAL_FILE" ]; then
    cp "$CREDENTIAL_FILE" "${CREDENTIAL_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backed up existing credential"
fi

# Create/update credential file
cat > "$CREDENTIAL_FILE" << EOF
{
  "service": "google_bravetto",
  "source": "manual",
  "api_key": "$API_KEY",
  "api_type": "$API_TYPE",
  "title": "Google (Bravetto) - $API_TYPE",
  "vault": "Shared",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "updated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "username": "mike@bravetto.com"
}
EOF

echo "✅ Updated credential file: $CREDENTIAL_FILE"
echo ""

# Validate
echo "🔍 Validating..."
python3 << PYTHON_EOF
import sys
import json
from pathlib import Path

cred_file = Path("$CREDENTIAL_FILE")
if cred_file.exists():
    with open(cred_file) as f:
        cred = json.load(f)
    
    api_key = cred.get('api_key', '')
    api_type = cred.get('api_type', 'unknown')
    
    print(f"✅ Service: {cred.get('service')}")
    print(f"✅ API Type: {api_type}")
    print(f"✅ API Key: {api_key[:20]}... ({len(api_key)} chars)")
    
    # Basic validation
    if api_type == 'gemini' and api_key.startswith('AIza'):
        print("✅ Format: Valid Gemini API key")
    elif api_type == 'calendar' and len(api_key) >= 30:
        print("✅ Format: Valid Calendar API key")
    elif api_type == 'gcp' and len(api_key) >= 20:
        print("✅ Format: Valid GCP credential")
    else:
        print("⚠️ Format: Unknown format (may still be valid)")
    
    print("")
    print("✅ Google credential updated successfully!")
else:
    print("❌ Credential file not found")
    sys.exit(1)
PYTHON_EOF

echo ""
echo "🎯 Next steps:"
echo "   1. Test credential: python3 scripts/read_abekeys.py google_bravetto"
echo "   2. System will auto-load on next backend start"
echo ""

