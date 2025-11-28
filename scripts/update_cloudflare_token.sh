#!/bin/bash
#  UPDATE CLOUDFLARE API TOKEN 
# Quick helper to update just the API token

set -e

ABEKEYS_DIR="$HOME/.abekeys/credentials"
CREDENTIAL_FILE="$ABEKEYS_DIR/cloudflare.json"

echo " UPDATE CLOUDFLARE API TOKEN"
echo "============================================================"
echo ""

if [ ! -f "$CREDENTIAL_FILE" ]; then
    echo " Credential file not found. Run setup_cloudflare_credentials.sh first."
    exit 1
fi

echo " Current credential file: $CREDENTIAL_FILE"
echo ""
echo " To get your Cloudflare API Token:"
echo "   1. Go to: https://dash.cloudflare.com/profile/api-tokens"
echo "   2. Click 'Create Token'"
echo "   3. Use template: 'Edit zone DNS'"
echo "   4. Select your zone"
echo "   5. Copy the token"
echo ""
echo "============================================================"
echo ""

read -p "Enter your Cloudflare API Token: " API_TOKEN

if [ -z "$API_TOKEN" ]; then
    echo " API Token cannot be empty"
    exit 1
fi

# Update credential file
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

echo ""
echo " API Token updated!"
echo "   File: $CREDENTIAL_FILE"
echo ""

# Test authentication
echo " Testing authentication..."
echo "============================================================"
python3 scripts/cloudflare_dns_automation.py bravetto.ai --list 2>&1 | head -30

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo " Authentication successful!"
else
    echo ""
    echo "  Authentication test failed"
    echo "   Please verify:"
    echo "   1. Token is correct"
    echo "   2. Token has 'Edit zone DNS' permissions"
    echo "   3. Token has access to your zone"
fi

echo ""

