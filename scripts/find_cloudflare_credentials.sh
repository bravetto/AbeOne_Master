#!/bin/bash
#  FIND CLOUDFLARE CREDENTIALS 
# Searches for Cloudflare credentials in AbëKEYS and 1Password

set -e

echo " SEARCHING FOR CLOUDFLARE CREDENTIALS..."
echo "============================================================"
echo ""

# Check AbëKEYS
echo " Checking AbëKEYS..."
ABEKEYS_FILE="$HOME/.abekeys/credentials/cloudflare.json"
if [ -f "$ABEKEYS_FILE" ]; then
    echo " Found in AbëKEYS: $ABEKEYS_FILE"
    python3 scripts/read_abekeys.py cloudflare 2>/dev/null || echo "     Error reading file"
else
    echo " Not found in AbëKEYS"
fi

echo ""

# Check 1Password
echo " Checking 1Password..."
if command -v op &> /dev/null; then
    # Check if signed in
    if op whoami &> /dev/null; then
        echo " Signed in to 1Password"
        
        # Search for Cloudflare items
        echo "   Searching for Cloudflare items..."
        CLOUDFLARE_ITEMS=$(op item list --format json 2>/dev/null | \
            python3 -c "
import sys, json
try:
    items = json.load(sys.stdin)
    cf_items = [i for i in items if 'cloudflare' in i.get('title', '').lower() or 'cf' in i.get('title', '').lower()]
    if cf_items:
        print(f'Found {len(cf_items)} items:')
        for item in cf_items:
            print(f\"  - {item['title']} (ID: {item.get('id', 'unknown')[:8]}...)\")
    else:
        print('No Cloudflare items found')
except:
    print('Error parsing 1Password items')
" 2>/dev/null || echo "     Error searching 1Password")
        
        echo "$CLOUDFLARE_ITEMS"
        
        # Try to get credentials from first Cloudflare item
        FIRST_ITEM=$(op item list --format json 2>/dev/null | \
            python3 -c "
import sys, json
try:
    items = json.load(sys.stdin)
    cf_items = [i for i in items if 'cloudflare' in i.get('title', '').lower()]
    if cf_items:
        print(cf_items[0]['title'])
except:
    pass
" 2>/dev/null)
        
        if [ -n "$FIRST_ITEM" ]; then
            echo ""
            echo "   Attempting to extract credentials from '$FIRST_ITEM'..."
            op item get "$FIRST_ITEM" --format json 2>/dev/null | \
                python3 -c "
import sys, json
try:
    item = json.load(sys.stdin)
    fields = item.get('fields', [])
    has_token = False
    has_key = False
    has_email = False
    
    for field in fields:
        label = field.get('label', '').lower()
        if 'api token' in label or ('token' in label and 'api' in label):
            has_token = True
            print(f\"   Found: {field.get('label')}\")
        elif 'api key' in label or ('key' in label and 'api' in label):
            has_key = True
            print(f\"   Found: {field.get('label')}\")
        elif 'email' in label:
            has_email = True
            print(f\"   Found: {field.get('label')}\")
    
    if not (has_token or has_key):
        print('    No API Token or API Key found')
        print('   Tip: Add \"API Token\" or \"API Key\" field to this item')
except:
    print('    Error parsing item')
" 2>/dev/null || echo "     Error extracting credentials"
        fi
    else
        echo "  Not signed in to 1Password"
        echo "   Run: eval \$(op signin)"
    fi
else
    echo " 1Password CLI not installed"
fi

echo ""

# Check environment variables
echo " Checking environment variables..."
if [ -n "$CLOUDFLARE_API_TOKEN" ]; then
    echo " CLOUDFLARE_API_TOKEN is set"
elif [ -n "$CLOUDFLARE_EMAIL" ] && [ -n "$CLOUDFLARE_API_KEY" ]; then
    echo " CLOUDFLARE_EMAIL and CLOUDFLARE_API_KEY are set"
else
    echo " No Cloudflare environment variables set"
fi

echo ""
echo "============================================================"
echo " QUICK SETUP:"
echo "   Run: ./scripts/setup_cloudflare_credentials.sh"
echo "============================================================"

