#!/bin/bash
# Setup script for cloning AbeOne_Master repository
# Run this on Bryan's Mac after connecting via ethernet

set -e

echo "🚀 AbeOne Master Clone Setup"
echo "================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Xcode Command Line Tools:"
    echo "   xcode-select --install"
    exit 1
fi

# Determine clone method
echo "Select clone method:"
echo "1) GitHub (requires access to bravetto/abe-one-source)"
echo "2) SSH from Michael's Mac (192.168.6.252)"
echo "3) Local bundle (if bundle file provided)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "📦 Cloning from GitHub..."
        cd ~/Documents
        if [ -d "AbeOne_Master" ]; then
            echo "⚠️  AbeOne_Master already exists. Removing..."
            rm -rf AbeOne_Master
        fi
        git clone https://github.com/bravetto/abe-one-source.git AbeOne_Master
        cd AbeOne_Master
        echo "✅ Cloned successfully!"
        ;;
    2)
        echo ""
        echo "🔐 Cloning via SSH..."
        echo "Make sure SSH is enabled on Michael's Mac and you have credentials."
        read -p "Enter SSH username [michaelmataluni]: " ssh_user
        ssh_user=${ssh_user:-michaelmataluni}
        cd ~/Documents
        if [ -d "AbeOne_Master" ]; then
            echo "⚠️  AbeOne_Master already exists. Removing..."
            rm -rf AbeOne_Master
        fi
        git clone ssh://${ssh_user}@192.168.6.252/Users/michaelmataluni/Documents/AbeOne_Master
        cd AbeOne_Master
        echo "✅ Cloned successfully!"
        ;;
    3)
        echo ""
        read -p "Enter path to bundle file: " bundle_path
        if [ ! -f "$bundle_path" ]; then
            echo "❌ Bundle file not found: $bundle_path"
            exit 1
        fi
        cd ~/Documents
        if [ -d "AbeOne_Master" ]; then
            echo "⚠️  AbeOne_Master already exists. Removing..."
            rm -rf AbeOne_Master
        fi
        git clone "$bundle_path" AbeOne_Master
        cd AbeOne_Master
        git remote add origin https://github.com/bravetto/abe-one-source.git 2>/dev/null || true
        echo "✅ Cloned successfully!"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "📋 Post-clone setup..."
echo ""

# Check for package.json
if [ -f "package.json" ]; then
    echo "📦 Found package.json - installing Node dependencies..."
    if command -v npm &> /dev/null; then
        npm install
    else
        echo "⚠️  npm not found. Install Node.js to install dependencies."
    fi
fi

# Check for requirements.txt
if [ -f "requirements.txt" ]; then
    echo "🐍 Found requirements.txt - installing Python dependencies..."
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    else
        echo "⚠️  pip3 not found. Install Python to install dependencies."
    fi
fi

# Verify git setup
echo ""
echo "🔍 Verifying git setup..."
git remote -v
echo ""
git status

echo ""
echo "✅ Setup complete!"
echo "📁 Repository location: $(pwd)"
echo ""
echo "Next steps:"
echo "  - Review BRYAN_CLONE_SETUP.md for additional setup"
echo "  - Check for any environment variables or config files needed"
echo "  - Run any initialization scripts if present"

