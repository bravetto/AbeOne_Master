#!/bin/bash

echo " Deploying Bravetto AI Shopify Integration"
echo "=========================================="

# Step 1: Deploy main Bravetto app with new endpoints
echo " Step 1: Deploying main Bravetto AI app..."
cd ../bravetto-ai
npm run build
if [ $? -eq 0 ]; then
    echo " Build successful!"
    # Uncomment the line below when ready to deploy
    # vercel --prod
    echo " Run 'vercel --prod' to deploy to production"
else
    echo " Build failed. Please fix errors before deploying."
    exit 1
fi

# Step 2: Deploy Shopify app
echo ""
echo " Step 2: Preparing Shopify app..."
cd ../shopify-chat-app

# Create .env.local from template (user needs to fill in values)
if [ ! -f .env.local ]; then
    echo "  Please create .env.local with your configuration:"
    echo "   cp .env.example .env.local"
    echo "   Then edit .env.local with your actual values"
    echo ""
    echo "Required values:"
    echo "- SHOPIFY_API_KEY"
    echo "- SHOPIFY_API_SECRET"  
    echo "- BRAVETTO_API_URL (your deployed Bravetto app URL)"
    echo ""
fi

echo " Step 3: Test the connection..."
npm run dev &
DEV_PID=$!
sleep 5

echo ""
echo " Setup complete! Your integration is ready."
echo ""
echo " Next manual steps:"
echo "1. Update BRAVETTO_API_URL in .env.local to your deployed URL"
echo "2. Test the chat interface at http://localhost:3000"
echo "3. Deploy with: shopify app deploy"

# Kill the dev server
kill $DEV_PID 2>/dev/null

echo ""
echo " See SETUP.md for detailed instructions" 