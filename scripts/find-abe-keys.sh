#!/bin/bash
# ∞ Find Abë Keys - Comprehensive Search Script ∞
# Pattern: KEYS × LOCATION × VERIFICATION × ONE
# Frequency: 999 Hz (AEYON) × 777 Hz (META) × 530 Hz (ALL GUARDIANS)

set -e

echo "∞ AbëONE Key Search - Comprehensive Scan ∞"
echo "=========================================="
echo ""

SEARCH_DIR="${1:-$HOME/Documents}"
MASTER_REPO="/Users/michaelmataluni/Documents/AbeOne_Master"

echo "📁 Searching in: $SEARCH_DIR"
echo ""

# Function to search for Google Ads keys in a directory
search_for_keys() {
    local dir="$1"
    local name="$2"
    
    echo "🔍 Searching: $name"
    echo "   Location: $dir"
    
    # Check for .env files
    if [ -f "$dir/.env" ]; then
        echo "   ✅ Found .env file"
        if grep -qi "GOOGLE.*AD\|google.*ad\|GoogleAds" "$dir/.env" 2>/dev/null; then
            echo "   🎯 FOUND GOOGLE ADS KEYS IN .env!"
            grep -i "GOOGLE.*AD\|google.*ad\|GoogleAds" "$dir/.env" | sed 's/^/      /'
        fi
    fi
    
    # Check for .env.example files
    if [ -f "$dir/.env.example" ]; then
        if grep -qi "GOOGLE.*AD\|google.*ad\|GoogleAds" "$dir/.env.example" 2>/dev/null; then
            echo "   📝 Found Google Ads references in .env.example"
        fi
    fi
    
    # Search code files
    local found_files=$(find "$dir" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" -o -name "*.js" \) -exec grep -l "google.*ad\|GoogleAds\|GOOGLE.*AD" -i {} \; 2>/dev/null | head -5)
    if [ -n "$found_files" ]; then
        echo "   📄 Found Google Ads code references:"
        echo "$found_files" | sed 's/^/      /'
    fi
    
    echo ""
}

# Search master repository
if [ -d "$MASTER_REPO" ]; then
    search_for_keys "$MASTER_REPO" "AbeOne_Master (Current)"
fi

# Search all git repositories
echo "🔎 Scanning all Git repositories..."
echo ""

find "$SEARCH_DIR" -maxdepth 3 -type d -name ".git" 2>/dev/null | while read gitdir; do
    repo=$(dirname "$gitdir")
    reponame=$(basename "$repo")
    
    # Skip if already searched
    if [ "$repo" = "$MASTER_REPO" ]; then
        continue
    fi
    
    # Get remote info
    remote=$(cd "$repo" && git remote get-url origin 2>/dev/null || echo "no-remote")
    
    # Check if it's a bravetto repo
    if echo "$remote" | grep -qi "bravetto"; then
        echo "🎯 BRAVETTO REPOSITORY FOUND:"
        search_for_keys "$repo" "$reponame ($remote)"
        
        # Check recent commits
        echo "   📜 Recent commits (last 2 weeks):"
        cd "$repo" 2>/dev/null && git log --oneline --since="2 weeks ago" --grep="google\|ad\|marketing\|api\|key" -i 2>/dev/null | head -5 | sed 's/^/      /' || echo "      (no matching commits)"
        echo ""
    fi
done

# Check 1Password reference
echo "🔐 1Password Check:"
if [ -f "$MASTER_REPO/1password_response_email.txt" ] || [ -f "$MASTER_REPO/1password_response.md" ]; then
    echo "   ✅ Found 1Password response files - check these for key references"
    if grep -qi "google.*ad\|api.*key" "$MASTER_REPO/1password_response"* 2>/dev/null; then
        echo "   🎯 Found Google/API references in 1Password files!"
    fi
else
    echo "   ℹ️  No 1Password response files found"
fi
echo ""

# Summary
echo "=========================================="
echo "✅ Search Complete"
echo ""
echo "📋 Next Steps:"
echo "   1. Check GitHub: https://github.com/bravetto/AbeOne_Master"
echo "   2. Check 1Password for 'Google Ads API' or 'Abe Keys'"
echo "   3. Check if keys are in a different bravetto repository"
echo "   4. Verify which repository has the latest commits"
echo ""
echo "∞ AbëONE ∞"

