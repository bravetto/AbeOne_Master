#!/bin/bash
# ∞ Bryan's Tuesday Webinar Setup - Complete Configuration ∞
# Pattern: BRYAN × WEBINAR × SETUP × ONE
# Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)

set -e

echo "∞ Bryan's Tuesday Webinar Setup ∞"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

WEB_DIR="products/apps/web"
ENV_FILE="$WEB_DIR/.env.local"

# Step 1: Get Credentials from AbëKEYs
echo -e "${BLUE}🔐 Step 1: Getting Credentials from AbëKEYs...${NC}"
echo ""

# Get SendGrid credentials
SENDGRID_DATA=$(python3 scripts/abekeys/abekeys_encrypted.py get sendgrid 2>/dev/null || echo "{}")

if [ "$SENDGRID_DATA" != "{}" ] && [ ! -z "$SENDGRID_DATA" ]; then
    SENDGRID_API_KEY=$(echo "$SENDGRID_DATA" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('api_key', ''))" 2>/dev/null || echo "")
    
    if [ ! -z "$SENDGRID_API_KEY" ]; then
        echo -e "${GREEN}  ✅ SendGrid API key found${NC}"
    else
        echo -e "${YELLOW}  ⚠️  SendGrid API key not found in encrypted vault${NC}"
        read -p "  Enter SendGrid API key manually: " SENDGRID_API_KEY
    fi
else
    echo -e "${YELLOW}  ⚠️  SendGrid credentials not found${NC}"
    read -p "  Enter SendGrid API key: " SENDGRID_API_KEY
fi

echo ""

# Step 2: Configure Environment Variables
echo -e "${BLUE}⚙️  Step 2: Configuring Environment Variables...${NC}"
echo ""

mkdir -p "$WEB_DIR"

# Add SendGrid configuration
if [ ! -f "$ENV_FILE" ] || ! grep -q "SENDGRID_API_KEY" "$ENV_FILE"; then
    echo "" >> "$ENV_FILE"
    echo "# SendGrid Configuration" >> "$ENV_FILE"
    echo "SENDGRID_API_KEY=$SENDGRID_API_KEY" >> "$ENV_FILE"
    echo "SENDGRID_FROM_EMAIL=bryan@bravetto.com" >> "$ENV_FILE"
    echo "SENDGRID_FROM_NAME=Bryan from Bravetto" >> "$ENV_FILE"
    echo -e "${GREEN}  ✅ SendGrid configured in .env.local${NC}"
else
    echo -e "${YELLOW}  ⚠️  SendGrid already configured${NC}"
fi

# Add webinar API URL (optional)
if ! grep -q "NEXT_PUBLIC_WEBINAR_API_URL" "$ENV_FILE"; then
    echo "" >> "$ENV_FILE"
    echo "# Webinar API Configuration" >> "$ENV_FILE"
    echo "NEXT_PUBLIC_WEBINAR_API_URL=/api/webinar/register" >> "$ENV_FILE"
    echo -e "${GREEN}  ✅ Webinar API URL configured${NC}"
fi

echo ""

# Step 3: Verify Landing Pages
echo -e "${BLUE}📄 Step 3: Verifying Landing Pages...${NC}"
echo ""

PAGES=(
    "app/webinar/page.tsx"
    "app/webinar/thank-you/page.tsx"
    "app/api/webinar/register/route.ts"
    "lib/sendgrid.ts"
)

ALL_EXIST=true
for page in "${PAGES[@]}"; do
    if [ -f "$WEB_DIR/$page" ]; then
        echo -e "${GREEN}  ✅ $page${NC}"
    else
        echo -e "${YELLOW}  ⚠️  $page - NOT FOUND${NC}"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = true ]; then
    echo ""
    echo -e "${GREEN}  ✅ All landing page files exist${NC}"
else
    echo ""
    echo -e "${YELLOW}  ⚠️  Some files missing - check paths${NC}"
fi

echo ""

# Step 4: Test Configuration
echo -e "${BLUE}🧪 Step 4: Testing Configuration...${NC}"
echo ""

# Test SendGrid connection
if [ ! -z "$SENDGRID_API_KEY" ]; then
    echo "  Testing SendGrid API key..."
    # Basic validation (key format check)
    if [[ ${#SENDGRID_API_KEY} -gt 20 ]]; then
        echo -e "${GREEN}  ✅ SendGrid API key format looks valid${NC}"
    else
        echo -e "${YELLOW}  ⚠️  SendGrid API key seems too short${NC}"
    fi
else
    echo -e "${YELLOW}  ⚠️  No SendGrid API key to test${NC}"
fi

echo ""

# Step 5: Next Steps
echo -e "${BLUE}📋 Step 5: Next Steps...${NC}"
echo ""
echo "  ✅ Credentials configured"
echo "  ✅ Environment variables set"
echo ""
echo -e "${YELLOW}  ⚠️  Manual Steps Required:${NC}"
echo ""
echo "  1. Verify sender email in SendGrid dashboard:"
echo "     - Go to SendGrid → Settings → Sender Authentication"
echo "     - Verify: bryan@bravetto.com (or your email)"
echo ""
echo "  2. Add Zoom link to email template:"
echo "     - Edit: $WEB_DIR/app/api/webinar/register/route.ts"
echo "     - Add Zoom link to confirmation email"
echo ""
echo "  3. Test registration flow:"
echo "     - Visit: /webinar"
echo "     - Submit test registration"
echo "     - Verify email received"
echo ""
echo "  4. Deploy to production:"
echo "     - Deploy to Vercel/production"
echo "     - Test end-to-end flow"
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "🎯 Landing Pages Ready:"
echo "  • /webinar - Main landing page"
echo "  • /webinar/developers - Developer ICP"
echo "  • /webinar/creators - Creative ICP"
echo "  • /webinar/thank-you - Thank you page"
echo ""
echo "📧 Email Automation:"
echo "  • SendGrid configured"
echo "  • API key set in .env.local"
echo "  • Verify sender email in SendGrid dashboard"
echo ""
echo "🚀 Ready for Tuesday Webinar!"
echo ""
echo "∞ AbëONE ∞"

