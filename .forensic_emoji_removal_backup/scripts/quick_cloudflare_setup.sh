#!/bin/bash
# ⚡ QUICK CLOUDFLARE SETUP ⚡
# Creates credential file template and provides setup instructions

set -e

ABEKEYS_DIR="$HOME/.abekeys/credentials"
CREDENTIAL_FILE="$ABEKEYS_DIR/cloudflare.json"

echo "⚡ QUICK CLOUDFLARE SETUP"
echo "============================================================"
echo ""

# Check if already exists
if [ -f "$CREDENTIAL_FILE" ]; then
    echo "✅ Cloudflare credentials already exist!"
    echo "   File: $CREDENTIAL_FILE"
    echo ""
    read -p "Do you want to overwrite? (y/n): " OVERWRITE
    if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
        echo "✅ Keeping existing credentials"
        exit 0
    fi
fi

echo "📋 To get your Cloudflare API Token:"
echo ""
echo "1. Go to: https://dash.cloudflare.com/profile/api-tokens"
echo "2. Click 'Create Token'"
echo "3. Use template: 'Edit zone DNS'"
echo "4. Select zone: bravetto.ai"
echo "5. Copy the token"
echo ""
echo "============================================================"
echo ""

read -p "Do you have your Cloudflare API Token ready? (y/n): " READY

if [ "$READY" != "y" ] && [ "$READY" != "Y" ]; then
    echo ""
    echo "⚠️  Please get your API token first, then run this script again"
    echo ""
    echo "Quick link: https://dash.cloudflare.com/profile/api-tokens"
    exit 0
fi

echo ""
read -p "Enter your Cloudflare API Token: " API_TOKEN

if [ -z "$API_TOKEN" ]; then
    echo "❌ API Token cannot be empty"
    exit 1
fi

# Create credential file
mkdir -p "$ABEKEYS_DIR"
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

echo ""
echo "✅ Credentials saved!"
echo "   File: $CREDENTIAL_FILE"
echo "   Permissions: 600 (owner read/write only)"
echo ""

# Test authentication
echo "🧪 Testing authentication..."
echo "============================================================"
python3 scripts/cloudflare_dns_automation.py bravetto.ai --list 2>&1 | head -20

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "✅ Authentication successful!"
    echo ""
    echo "You can now use:"
    echo "  python3 scripts/cloudflare_dns_automation.py bravetto.ai --list"
    echo "  ./scripts/bravetto_ai_dns_setup.sh"
else
    echo ""
    echo "⚠️  Authentication test failed"
    echo "   Please verify:"
    echo "   1. Token is correct"
    echo "   2. Token has 'Edit zone DNS' permissions"
    echo "   3. Token is for bravetto.ai zone"
fi

echo ""

