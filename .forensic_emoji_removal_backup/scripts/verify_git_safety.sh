#!/bin/bash
# 🔒 VERIFY GIT SAFETY - Final check before commit 🔒

set -e

echo "🔒 VERIFYING GIT SAFETY..."
echo "============================================================"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Check 1: No credential files in git
echo ""
echo "📋 Check 1: Credential files in git..."
TRACKED=$(git ls-files | grep -iE "(credential|api.*key|\.key$|secret|password|\.env$|abekeys)" || true)
if [ -z "$TRACKED" ]; then
    echo "   ✅ No credential files tracked in git"
else
    echo "   ❌ CRITICAL: Credential files tracked in git:"
    echo "$TRACKED" | head -10
    exit 1
fi

# Check 2: .gitignore exists and protects
echo ""
echo "📋 Check 2: .gitignore protection..."
if [ -f ".gitignore" ]; then
    if grep -qE "(\.abekeys|credentials|\.key$|secret|password)" .gitignore; then
        echo "   ✅ .gitignore protects sensitive files"
    else
        echo "   ⚠️  .gitignore missing some patterns"
    fi
else
    echo "   ❌ CRITICAL: .gitignore missing"
    exit 1
fi

# Check 3: No staged sensitive files
echo ""
echo "📋 Check 3: Staged files..."
STAGED=$(git diff --cached --name-only | grep -iE "(credential|api.*key|\.key$|secret|password|\.env$|abekeys)" || true)
if [ -z "$STAGED" ]; then
    echo "   ✅ No sensitive files staged"
else
    echo "   ❌ CRITICAL: Sensitive files staged:"
    echo "$STAGED"
    exit 1
fi

# Check 4: File permissions
echo ""
echo "📋 Check 4: Credential file permissions..."
if [ -d "$HOME/.abekeys/credentials" ]; then
    INSECURE=$(find "$HOME/.abekeys/credentials" -type f -perm -004 2>/dev/null || true)
    if [ -z "$INSECURE" ]; then
        echo "   ✅ Credential files have secure permissions"
    else
        echo "   ⚠️  Some files have insecure permissions"
    fi
else
    echo "   ✅ Credentials directory doesn't exist (using encrypted vault)"
fi

echo ""
echo "=" | tr -d '\n'
for i in {1..60}; do echo -n "="; done
echo ""
echo "✅ GIT SAFETY VERIFIED"
echo "✅ READY TO COMMIT"
echo "=" | tr -d '\n'
for i in {1..60}; do echo -n "="; done
echo ""

