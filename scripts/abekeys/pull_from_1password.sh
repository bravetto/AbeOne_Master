#!/bin/bash
# ∞ Pull Credentials from 1Password - For Bryan ∞
# Pattern: PULL × 1PASSWORD × BRYAN × ONE

set -e

echo "∞ Pull Credentials from 1Password ∞"
echo "===================================="
echo ""

# Check if 1Password CLI is installed
if ! command -v op &> /dev/null; then
    echo "❌ 1Password CLI not found"
    echo ""
    echo "Install it:"
    echo "  brew install --cask 1password-cli"
    echo ""
    echo "Or download from: https://developer.1password.com/docs/cli/get-started"
    exit 1
fi

# Check if signed in
if ! op account list &> /dev/null; then
    echo "🔐 Signing into 1Password..."
    op signin
fi

# Create credentials directory
CRED_DIR="$HOME/.abekeys/credentials"
mkdir -p "$CRED_DIR"

echo "📋 Searching 1Password for AbëKEYs credentials..."
echo ""

# List of credentials to pull
CREDENTIALS=(
    "google_ads:Google Ads API"
    "sendgrid:SendGrid API"
    "stripe:Stripe API"
    "aws:AWS"
    "github:GitHub"
    "clerk:Clerk"
)

PULLED=0
MISSING=0

for cred_info in "${CREDENTIALS[@]}"; do
    IFS=':' read -r service_name search_term <<< "$cred_info"
    
    echo "  Searching for: $search_term..."
    
    # Search 1Password
    ITEMS=$(op item list --format json 2>/dev/null | jq -r ".[] | select(.title | test(\"$search_term\"; \"i\")) | .id" 2>/dev/null || echo "")
    
    if [ -z "$ITEMS" ]; then
        echo "    ⚪ Not found in 1Password"
        ((MISSING++))
        continue
    fi
    
    # Get first matching item
    ITEM_ID=$(echo "$ITEMS" | head -1)
    
    # Get item details
    ITEM=$(op item get "$ITEM_ID" --format json 2>/dev/null || echo "")
    
    if [ -z "$ITEM" ]; then
        echo "    ⚠️  Found but couldn't retrieve"
        continue
    fi
    
    # Extract fields and create JSON
    JSON_FILE="$CRED_DIR/${service_name}.json"
    
    # Use jq to extract fields and create credential JSON
    python3 << PYTHON_SCRIPT
import json
import sys

item_data = json.loads('''$ITEM''')
cred_data = {}

# Extract common fields
for field in item_data.get('fields', []):
    label = field.get('label', '').lower().replace(' ', '_')
    value = field.get('value', '')
    
    # Map common field names
    if 'api_key' in label or 'apikey' in label:
        cred_data['api_key'] = value
    elif 'client_id' in label:
        cred_data['client_id'] = value
    elif 'client_secret' in label or 'secret' in label:
        cred_data['client_secret'] = value
    elif 'token' in label:
        cred_data['token'] = value
    elif 'refresh_token' in label:
        cred_data['refresh_token'] = value
    elif 'customer_id' in label or 'customer' in label:
        cred_data['customer_id'] = value
    elif 'developer_token' in label:
        cred_data['developer_token'] = value
    else:
        # Keep other fields
        cred_data[label] = value

# Add service name
cred_data['service'] = '$service_name'
cred_data['source'] = '1password'

# Write JSON file
with open('$JSON_FILE', 'w') as f:
    json.dump(cred_data, f, indent=2)

print(f"    ✅ Pulled: {len(cred_data)} fields")
PYTHON_SCRIPT
    
    # Set secure permissions
    chmod 600 "$JSON_FILE"
    ((PULLED++))
done

echo ""
echo "===================================="
echo "📊 Summary:"
echo "  ✅ Pulled: $PULLED credentials"
echo "  ⚪ Missing: $MISSING credentials"
echo ""
echo "Credentials saved to: $CRED_DIR"
echo ""
echo "✅ Ready to use!"
echo ""
echo "Test:"
echo "  python3 scripts/abekeys/abekeys.py list"
echo ""
echo "∞ AbëONE ∞"

