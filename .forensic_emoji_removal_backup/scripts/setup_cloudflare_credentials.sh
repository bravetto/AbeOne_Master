#!/bin/bash
# 🔐 SETUP CLOUDFLARE CREDENTIALS 🔐
# Interactive setup for Cloudflare API credentials

set -e

echo "🔐" | tr -d '\n'
for i in {1..30}; do echo -n "🔐"; done
echo ""
echo "CLOUDFLARE CREDENTIALS SETUP"
echo "🔐" | tr -d '\n'
for i in {1..30}; do echo -n "🔐"; done
echo ""
echo ""

ABEKEYS_DIR="$HOME/.abekeys/credentials"
CREDENTIAL_FILE="$ABEKEYS_DIR/cloudflare.json"

# Create AbëKEYS directory if it doesn't exist
mkdir -p "$ABEKEYS_DIR"

echo "📋 Setting up Cloudflare credentials..."
echo "============================================================"
echo ""

# Check if already exists
if [ -f "$CREDENTIAL_FILE" ]; then
    echo "⚠️  Cloudflare credentials already exist at:"
    echo "   $CREDENTIAL_FILE"
    echo ""
    read -p "Do you want to overwrite? (y/n): " OVERWRITE
    if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
        echo "✅ Keeping existing credentials"
        exit 0
    fi
fi

echo "Choose authentication method:"
echo "1. API Token (Recommended - most secure)"
echo "2. Email + API Key (Legacy)"
echo ""
read -p "Enter choice (1 or 2): " METHOD

if [ "$METHOD" = "1" ]; then
    echo ""
    echo "📝 API Token Setup"
    echo "   Get your token from: https://dash.cloudflare.com/profile/api-tokens"
    echo "   Use template: 'Edit zone DNS'"
    echo "   Select zone: bravetto.ai"
    echo ""
    read -p "Enter Cloudflare API Token: " API_TOKEN
    
    if [ -z "$API_TOKEN" ]; then
        echo "❌ API Token cannot be empty"
        exit 1
    fi
    
    # Create credential file
    cat > "$CREDENTIAL_FILE" << EOF
{
  "service": "cloudflare",
  "api_token": "$API_TOKEN",
  "source": "manual",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

elif [ "$METHOD" = "2" ]; then
    echo ""
    echo "📝 Email + API Key Setup"
    echo "   Get your API key from: https://dash.cloudflare.com/profile/api-tokens"
    echo ""
    read -p "Enter Cloudflare Email: " EMAIL
    read -p "Enter Cloudflare API Key: " API_KEY
    
    if [ -z "$EMAIL" ] || [ -z "$API_KEY" ]; then
        echo "❌ Email and API Key cannot be empty"
        exit 1
    fi
    
    # Create credential file
    cat > "$CREDENTIAL_FILE" << EOF
{
  "service": "cloudflare",
  "email": "$EMAIL",
  "api_key": "$API_KEY",
  "source": "manual",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

else
    echo "❌ Invalid choice"
    exit 1
fi

# Set secure permissions
chmod 600 "$CREDENTIAL_FILE"
chmod 700 "$ABEKEYS_DIR"

echo ""
echo "✅ Credentials saved to:"
echo "   $CREDENTIAL_FILE"
echo ""
echo "🔒 File permissions set to 600 (owner read/write only)"
echo ""

# Test authentication
echo "🧪 Testing authentication..."
echo "============================================================"
python3 scripts/cloudflare_dns_automation.py bravetto.ai --list > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Authentication successful!"
    echo ""
    echo "You can now use:"
    echo "  python3 scripts/cloudflare_dns_automation.py bravetto.ai --list"
    echo "  ./scripts/bravetto_ai_dns_setup.sh"
else
    echo "⚠️  Authentication test failed"
    echo "   Please verify your credentials are correct"
    echo "   Check: https://dash.cloudflare.com/profile/api-tokens"
fi

echo ""

