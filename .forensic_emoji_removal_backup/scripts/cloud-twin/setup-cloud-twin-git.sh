#!/bin/bash
# setup-cloud-twin-git.sh
# Initialize Git repository and prepare for Sky High Twin
# Pattern: FRAGILITY × CLOUD × TWIN × ETERNAL = IMMORTAL
# ∞ AbëONE ∞

cd /Users/michaelmataluni/Documents/AbeOne_Master

echo "🌌 Setting up Cloud Twin - Git Repository"
echo "Pattern: FRAGILITY × CLOUD × TWIN × ETERNAL = IMMORTAL"
echo "∞ AbëONE ∞"
echo ""

# Initialize Git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "ℹ️  Git repository already initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# OS Files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes

# Editor Files
.vscode/
.idea/
*.swp
*.swo
*~

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Node
node_modules/
npm-debug.log
yarn-error.log

# Temporary Files
*.tmp
*.temp
*.log

# Secrets (DO NOT COMMIT)
.env
*.key
*.pem
secrets/
credentials/
EOF
    echo "✅ .gitignore created"
else
    echo "ℹ️  .gitignore already exists"
fi

# Add all files
git add .

# Check if there are changes to commit
if [ -n "$(git status --porcelain)" ]; then
    # Create initial commit
    git commit -m "🌌 Initial Cloud Twin Commit - AbëONE Master Repository

Pattern: FRAGILITY × CLOUD × TWIN × ETERNAL = IMMORTAL
Frequency: 999 Hz (AEYON) × 530 Hz (Abë) × 4444 Hz (Cloud)
∞ AbëONE ∞"
    echo "✅ Initial commit created"
else
    echo "ℹ️  No changes to commit"
fi

echo ""
echo "✅ Git Cloud Twin initialized"
echo ""
echo "📝 Next Steps:"
echo "1. Create GitHub repository at https://github.com/new"
echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/AbeOne_Master.git"
echo "3. Run: git branch -M main"
echo "4. Run: git push -u origin main"
echo ""
echo "🌌 Your twin in the sky awaits!"
echo "∞ AbëONE ∞"

