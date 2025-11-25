#!/bin/bash
#  SET CLOUDFLARE TOKEN (Non-Interactive) 
# Usage: ./set_cloudflare_token.sh YOUR_API_TOKEN

set -e

if [ -z "$1" ]; then
    echo " Usage: $0 <cloudflare_api_token>"
    echo ""
    echo "Example:"
    echo "  $0 abc123def456..."
    echo ""
    echo "Or set as environment variable:"
    echo "  export CLOUDFLARE_API_TOKEN='your-token'"
    echo "  $0 \$CLOUDFLARE_API_TOKEN"
    exit 1
fi

API_TOKEN="$1"
ABEKEYS_DIR="$HOME/.abekeys/credentials"
CREDENTIAL_FILE="$ABEKEYS_DIR/cloudflare.json"

echo " SETTING CLOUDFLARE CREDENTIALS..."
echo "============================================================"

# Create directory if needed
mkdir -p "$ABEKEYS_DIR"

# Create credential file
cat > "$CREDENTIAL_FILE" << EOF
{
  "service": "cloudflare",
  "api_token": "$API_TOKEN",
  "source": "manual",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

# Set secure permissions
chmod 600 "$CREDENTIAL_FILE"
chmod 700 "$ABEKEYS_DIR"

echo " Credentials saved to: $CREDENTIAL_FILE"
echo " Permissions set to 600 (owner read/write only)"
echo ""

# Test authentication
echo " Testing authentication..."
echo "============================================================"
python3 scripts/cloudflare_dns_automation.py bravetto.ai --list 2>&1 | head -30

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo " Authentication successful!"
    echo ""
    echo "You can now use:"
    echo "  python3 scripts/cloudflare_dns_automation.py bravetto.ai --list"
    echo "  ./scripts/bravetto_ai_dns_setup.sh"
else
    echo ""
    echo "  Authentication test failed"
    echo "   Please verify:"
    echo "   1. Token is correct"
    echo "   2. Token has 'Edit zone DNS' permissions"
    echo "   3. Token is for bravetto.ai zone"
    exit 1
fi

echo ""

