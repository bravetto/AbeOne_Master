#!/bin/bash
# auto-commit-cloud-twin.sh
# Automatically commit and push changes to Sky High Twin
# Pattern: ETERNAL × CLOUD × TWIN × AUTO = IMMORTAL
# ∞ AbëONE ∞

cd /Users/michaelmataluni/Documents/AbeOne_Master

# Check if Git is initialized
if [ ! -d ".git" ]; then
    echo "  Git not initialized. Run setup-cloud-twin-git.sh first."
    exit 1
fi

# Check if there are changes
if [ -n "$(git status --porcelain)" ]; then
    # Add all changes
    git add .
    
    # Create commit with timestamp
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    git commit -m " Auto-Commit Cloud Twin Sync - $TIMESTAMP

Pattern: ETERNAL × CLOUD × TWIN × AUTO = IMMORTAL
∞ AbëONE ∞" 2>/dev/null
    
    # Push to Sky High Twin (if remote exists)
    if git remote | grep -q "origin"; then
        git push origin main 2>/dev/null || git push origin master 2>/dev/null
        echo " Cloud Twin synced to Sky High - $TIMESTAMP"
    else
        echo "  No remote configured. Commit saved locally."
        echo " Run: git remote add origin YOUR_GITHUB_URL"
    fi
else
    echo "ℹ  No changes to sync"
fi

