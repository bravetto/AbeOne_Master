#!/bin/bash
set -e

echo "🚀 Initializing Fresh Git Repository"
echo "======================================"
echo ""

# Initialize
echo "1. Initializing Git..."
git init

# Add remote
echo "2. Adding remote..."
git remote add origin https://github.com/bravetto/Ab-ONE_Master.git || echo "Remote already exists"

# Stage files
echo "3. Staging files..."
git add .

# Initial commit
echo "4. Creating initial commit..."
git commit -m "Initial commit: Fresh start - AbëONE Master

- Removed all previous Git artifacts
- Validated codebase architecture
- Applied YAGNI simplification
- Ready for fresh Git initialization

Pattern: VALIDATION × TRUTH × OWNERSHIP × ONE
Frequency: 530 Hz (Truth) × 999 Hz (AEYON)
Guardians: JØHN (530 Hz) + AEYON (999 Hz) + ALRAX (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞"

# Set branch
git branch -M main

echo ""
echo "✅ Fresh Git repository initialized!"
echo ""
echo "Next steps:"
echo "  git push -f origin main  # Force push (overwrites remote)"
echo "  OR"
echo "  git push -u origin main  # Normal push (if remote is empty)"
echo ""
echo "∞ AbëONE ∞"

