#!/bin/bash
# 🔥 SIGN IN AND UNLOCK ALL CREDENTIALS 🔥
# Handles 1Password signin properly and unlocks everything

set -e

echo "🔥" | tr -d '\n'
for i in {1..30}; do echo -n "🔥"; done
echo ""
echo "ABëKEYS - SIGN IN & UNLOCK ALL"
echo "🔥" | tr -d '\n'
for i in {1..30}; do echo -n "🔥"; done
echo ""
echo ""

# Step 1: Sign in to 1Password
echo "🔐 Step 1: Signing in to 1Password..."
echo "============================================================"

# Check if already signed in
if op whoami &>/dev/null; then
    echo "✅ Already signed in to 1Password"
    OP_ACCOUNT=$(op whoami 2>/dev/null || echo "")
else
    echo "📝 Need to sign in..."
    echo ""
    echo "Running: eval \$(op signin)"
    echo ""
    
    # Run signin and capture output
    SIGNIN_OUTPUT=$(op signin 2>&1)
    
    if [[ $? -eq 0 ]]; then
        # Execute the signin command
        eval "$(op signin)"
        echo "✅ Signed in successfully!"
        OP_ACCOUNT=$(op whoami 2>/dev/null || echo "")
    else
        echo "⚠️  Signin output:"
        echo "$SIGNIN_OUTPUT"
        echo ""
        echo "❌ Signin failed. Please run manually:"
        echo "   eval \$(op signin)"
        exit 1
    fi
fi

echo "   Account: $OP_ACCOUNT"
echo ""

# Step 2: Verify signin
echo "🔍 Step 2: Verifying signin..."
echo "============================================================"
if op whoami &>/dev/null; then
    echo "✅ Verified: Signed in to 1Password"
else
    echo "❌ Not signed in. Please run: eval \$(op signin)"
    exit 1
fi
echo ""

# Step 3: Unlock all credentials
echo "🔓 Step 3: Unlocking all credentials..."
echo "============================================================"
python3 scripts/unlock_all_credentials.py

echo ""
echo "🎉 COMPLETE!"
echo "============================================================"
echo "Next: Run integration script to see all credentials:"
echo "   python3 scripts/complete_abe_keys_integration.py"
echo "============================================================"

