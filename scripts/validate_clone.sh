#!/bin/bash
# Validation script to verify AbeOne_Master clone is complete and correct
# Run this on Bryan's Mac after cloning

set -e

echo " Validating AbeOne_Master Clone"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "BRYAN_CLONE_INSTRUCTIONS.md" ]; then
    echo " ERROR: Not in AbeOne_Master directory"
    echo "   Please run: cd ~/Documents/AbeOne_Master"
    exit 1
fi

echo " Found repository directory"
echo ""

# Check git setup
echo " Checking Git Setup..."
if [ -d ".git" ]; then
    echo " Git repository initialized"
    
    # Check remotes
    echo ""
    echo " Git Remotes:"
    git remote -v
    
    # Check current status
    echo ""
    echo " Git Status:"
    git status --short | head -20
    if [ $(git status --short | wc -l) -gt 20 ]; then
        echo "... (showing first 20 files)"
    fi
else
    echo "  Warning: .git directory not found"
    echo "   Run: git init"
fi

echo ""

# Check key files
echo " Checking Key Files..."
key_files=(
    "BRYAN_CLONE_INSTRUCTIONS.md"
    "BRYAN_QUICK_START.md"
    "README.md"
    "package.json"
    "scripts/setup_bryan_clone.sh"
)

missing_files=()
for file in "${key_files[@]}"; do
    if [ -f "$file" ]; then
        echo " $file"
    else
        echo " $file (MISSING)"
        missing_files+=("$file")
    fi
done

echo ""

# Check directory structure
echo " Checking Directory Structure..."
important_dirs=(
    "scripts"
    "apps"
    "EMERGENT_OS"
    "PRODUCTS"
    "DASHBOARDS"
)

for dir in "${important_dirs[@]}"; do
    if [ -d "$dir" ]; then
        file_count=$(find "$dir" -type f | wc -l | tr -d ' ')
        echo " $dir/ ($file_count files)"
    else
        echo "  $dir/ (not found)"
    fi
done

echo ""

# Check repository size
echo " Repository Size:"
repo_size=$(du -sh . 2>/dev/null | awk '{print $1}')
echo "   Total: $repo_size"

file_count=$(find . -type f | wc -l | tr -d ' ')
dir_count=$(find . -type d | wc -l | tr -d ' ')
echo "   Files: $file_count"
echo "   Directories: $dir_count"

echo ""

# Summary
echo "=================================="
if [ ${#missing_files[@]} -eq 0 ]; then
    echo " VALIDATION PASSED"
    echo ""
    echo "Repository appears to be cloned correctly!"
    echo ""
    echo "Next steps:"
    echo "  1. Check git remote: git remote -v"
    echo "  2. Install dependencies if needed"
    echo "  3. Review BRYAN_CLONE_INSTRUCTIONS.md"
else
    echo "  VALIDATION WARNINGS"
    echo ""
    echo "Missing files:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "Repository may be incomplete. Check connection and try copying again."
fi
echo ""

