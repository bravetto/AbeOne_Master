#!/bin/bash
#  BRAVETTO.AI DNS AUTOMATION SCRIPT 
# Automated DNS configuration for bravetto.ai using Cloudflare API

set -e

echo "" | tr -d '\n'
for i in {1..30}; do echo -n ""; done
echo ""
echo "BRAVETTO.AI DNS AUTOMATION"
echo "AEYON ATOMIC EXECUTION"
echo "" | tr -d '\n'
for i in {1..30}; echo -n ""; done
echo ""
echo ""

DOMAIN="bravetto.ai"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python script exists
if [ ! -f "$SCRIPT_DIR/cloudflare_dns_automation.py" ]; then
    echo " cloudflare_dns_automation.py not found"
    exit 1
fi

# Step 1: Check authentication
echo " Step 1: Checking Cloudflare authentication..."
echo "============================================================"
python3 "$SCRIPT_DIR/cloudflare_dns_automation.py" "$DOMAIN" --list > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "  Authentication failed or domain not found"
    echo ""
    echo "   Setting up credentials..."
    echo ""
    
    # Try to pull from 1Password
    if command -v op &> /dev/null; then
        echo "   Attempting to pull Cloudflare credentials from 1Password..."
        eval $(op signin) 2>/dev/null || true
        
        # Try to get Cloudflare credentials
        CLOUDFLARE_TOKEN=$(op item get "Cloudflare" --field "API Token" 2>/dev/null || echo "")
        
        if [ -n "$CLOUDFLARE_TOKEN" ]; then
            echo " Found Cloudflare token in 1Password"
            export CLOUDFLARE_API_TOKEN="$CLOUDFLARE_TOKEN"
        fi
    fi
    
    # Check if credentials are set
    if [ -z "$CLOUDFLARE_API_TOKEN" ] && [ -z "$CLOUDFLARE_EMAIL" ]; then
        echo ""
        echo " No Cloudflare credentials found!"
        echo ""
        echo "   Options:"
        echo "   1. Add to AbëKEYS:"
        echo "      ~/.abekeys/credentials/cloudflare.json"
        echo ""
        echo "   2. Store in 1Password as 'Cloudflare' with:"
        echo "      - API Token (or API Key + Email)"
        echo ""
        echo "   3. Set environment variables:"
        echo "      export CLOUDFLARE_API_TOKEN='your-token'"
        echo "      # OR"
        echo "      export CLOUDFLARE_EMAIL='your-email'"
        echo "      export CLOUDFLARE_API_KEY='your-key'"
        echo ""
        exit 1
    fi
fi

echo " Authentication successful"
echo ""

# Step 2: List current DNS records
echo " Step 2: Current DNS records for $DOMAIN"
echo "============================================================"
python3 "$SCRIPT_DIR/cloudflare_dns_automation.py" "$DOMAIN" --list
echo ""

# Step 3: Prompt for Vercel configuration
echo " Step 3: Vercel DNS Configuration"
echo "============================================================"
echo ""
echo "Do you want to configure DNS for Vercel deployment? (y/n)"
read -r CONFIGURE_VERCEL

if [ "$CONFIGURE_VERCEL" = "y" ] || [ "$CONFIGURE_VERCEL" = "Y" ]; then
    echo ""
    echo "Enter Vercel IP address (or press Enter to skip A record):"
    read -r VERCEL_IP
    
    echo ""
    echo "Enter Vercel CNAME (e.g., cname.vercel-dns.com, or press Enter to skip):"
    read -r VERCEL_CNAME
    
    echo ""
    echo " Configuring DNS records..."
    
    if [ -n "$VERCEL_IP" ] || [ -n "$VERCEL_CNAME" ]; then
        python3 "$SCRIPT_DIR/cloudflare_dns_automation.py" "$DOMAIN" \
            --configure-vercel \
            ${VERCEL_IP:+--vercel-ip "$VERCEL_IP"} \
            ${VERCEL_CNAME:+--vercel-cname "$VERCEL_CNAME"}
    else
        echo "  No Vercel DNS information provided. Skipping configuration."
    fi
else
    echo "Skipping Vercel configuration."
fi

echo ""
echo "=" | tr -d '\n'
for i in {1..60}; do echo -n "="; done
echo ""
echo " DNS AUTOMATION COMPLETE"
echo "=" | tr -d '\n'
for i in {1..60}; do echo -n "="; done
echo ""
echo ""
echo "Next steps:"
echo "1. Wait 5-60 minutes for DNS propagation"
echo "2. Check DNS propagation: https://dnschecker.org"
echo "3. Verify SSL certificate in Vercel dashboard"
echo "4. Test: https://$DOMAIN"
echo ""

