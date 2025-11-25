#!/bin/bash
#  ONE COMMAND DEPLOYMENT
# Automates everything: Token check → Project creation → Domain binding

set -e

PROJECT_NAME="${1:-abeone-web}"
DOMAIN="${2:-bravetto.ai}"

echo " ONE COMMAND DEPLOYMENT"
echo "============================================================"
echo "Project: $PROJECT_NAME"
echo "Domain: $DOMAIN"
echo ""

# Step 1: Check token
echo " Step 1: Checking credentials..."
if python3 scripts/validate_cloudflare_credentials.py > /dev/null 2>&1; then
    echo " Credentials valid"
else
    echo " Credentials need fixing"
    echo "   Run: python3 scripts/set_cloudflare_token.py YOUR_TOKEN"
    exit 1
fi

# Step 2: Create project
echo ""
echo " Step 2: Creating Cloudflare Pages project..."
if python3 scripts/automate_cloudflare_pages_setup.py --project-name "$PROJECT_NAME" 2>&1 | tee /tmp/cf_setup.log; then
    echo " Project created"
else
    echo "  Project creation may have failed or project already exists"
    echo "   Check Cloudflare dashboard or run manually"
fi

# Step 3: Bind domain
echo ""
echo " Step 3: Binding domain..."
if python3 scripts/cloudflare_pages_auto_bind.py \
    --domain "$DOMAIN" \
    --project-name "$PROJECT_NAME" 2>&1; then
    echo " Domain bound"
else
    echo "  Domain binding may have failed or domain already bound"
    echo "   Check Cloudflare dashboard"
fi

echo ""
echo "============================================================"
echo " DEPLOYMENT COMPLETE"
echo " Site: https://$DOMAIN"
echo " Pages: https://$PROJECT_NAME.pages.dev"
echo ""


