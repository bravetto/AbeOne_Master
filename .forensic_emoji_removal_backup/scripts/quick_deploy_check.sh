#!/bin/bash
# 🔍 QUICK DEPLOYMENT READINESS CHECK
# Verifies all systems are ready for deployment

set -e

# Get absolute paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔍 DEPLOYMENT READINESS CHECK"
echo "============================================================"
echo ""

# Check 1: Build Status
echo "📦 CHECK 1: Build Status"
cd "$PROJECT_ROOT/apps/web" 2>/dev/null || { echo "❌ Cannot find apps/web directory"; exit 1; }
if npm run build > /dev/null 2>&1; then
    echo "✅ Build successful"
else
    echo "❌ Build failed"
    exit 1
fi
echo ""

# Check 2: Output Directory
echo "📁 CHECK 2: Output Directory"
if [ -d "out" ] && [ -f "out/index.html" ]; then
    echo "✅ Output directory exists with index.html"
    PAGE_COUNT=$(find out -name "*.html" | wc -l | tr -d ' ')
    echo "   Found $PAGE_COUNT HTML files"
else
    echo "❌ Output directory missing or incomplete"
    exit 1
fi
echo ""

# Check 3: Cloudflare Credentials
echo "🔐 CHECK 3: Cloudflare Credentials"
cd "$PROJECT_ROOT" || exit 1
if python3 "$SCRIPT_DIR/validate_cloudflare_credentials.py" > /dev/null 2>&1; then
    echo "✅ Cloudflare credentials valid"
else
    echo "⚠️  Cloudflare credentials need fixing"
    echo "   Run: python3 scripts/validate_cloudflare_credentials.py"
fi
echo ""

# Check 4: Automation Scripts
echo "🤖 CHECK 4: Automation Scripts"
SCRIPTS=(
    "cloudflare_pages_auto_bind.py"
    "zero_effort_cloudflare_auth.py"
    "validate_cloudflare_credentials.py"
)

ALL_EXIST=true
for script in "${SCRIPTS[@]}"; do
    if [ -f "$SCRIPT_DIR/$script" ]; then
        echo "✅ $script exists"
    else
        echo "❌ $script missing"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = false ]; then
    exit 1
fi
echo ""

# Check 5: GitHub Actions Workflow
echo "🔄 CHECK 5: CI/CD Workflow"
cd "$PROJECT_ROOT/.github/workflows" 2>/dev/null || { echo "❌ Cannot find .github/workflows"; exit 1; }
if [ -f "cloudflare-pages.yml" ]; then
    echo "✅ GitHub Actions workflow exists"
else
    echo "❌ GitHub Actions workflow missing"
    exit 1
fi
echo ""

# Summary
echo "============================================================"
echo "✅ DEPLOYMENT READINESS: READY"
echo ""
echo "📋 Next Steps:"
echo "   1. Fix Cloudflare token (if needed)"
echo "   2. Create Cloudflare Pages project"
echo "   3. Bind domain"
echo ""
echo "💡 Quick Start:"
echo "   python3 scripts/cloudflare_pages_auto_bind.py \\"
echo "     --domain bravetto.ai \\"
echo "     --project-name abeone-web"
echo ""

