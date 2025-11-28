#!/bin/bash
# Transfer AbeOne_Master to Bryan - Excludes problematic files
# Run this on Michael's Mac to prepare for transfer

set -e

REPO_PATH="/Users/michaelmataluni/Documents/AbeOne_Master"
OUTPUT_DIR="${HOME}/Desktop"
ARCHIVE_NAME="AbeOne_Master_Transfer"

echo "🚀 Preparing AbeOne_Master for transfer to Bryan..."
echo "=================================================="
echo ""

# Method 1: Create Git Bundle (BEST - Smallest, Fastest)
echo "📦 Method 1: Creating Git Bundle (RECOMMENDED)..."
cd "$REPO_PATH"
if [ -d ".git" ]; then
    git bundle create "${OUTPUT_DIR}/${ARCHIVE_NAME}.bundle" --all 2>/dev/null || {
        echo "⚠️  Creating bundle with current branch only..."
        CURRENT_BRANCH=$(git branch --show-current)
        git bundle create "${OUTPUT_DIR}/${ARCHIVE_NAME}.bundle" "$CURRENT_BRANCH" 2>/dev/null || {
            echo "⚠️  Bundle creation failed, trying HEAD..."
            git bundle create "${OUTPUT_DIR}/${ARCHIVE_NAME}.bundle" HEAD
        }
    }
    
    if [ -f "${OUTPUT_DIR}/${ARCHIVE_NAME}.bundle" ]; then
        BUNDLE_SIZE=$(du -h "${OUTPUT_DIR}/${ARCHIVE_NAME}.bundle" | cut -f1)
        echo "✅ Git Bundle created: ${OUTPUT_DIR}/${ARCHIVE_NAME}.bundle"
        echo "   Size: $BUNDLE_SIZE"
        echo "   Bryan can clone with: git clone ${ARCHIVE_NAME}.bundle AbeOne_Master"
        echo ""
    fi
else
    echo "⚠️  Not a git repository, skipping bundle creation"
    echo ""
fi

# Method 2: Create tar archive excluding venv directories (if bundle fails)
if [ ! -f "${OUTPUT_DIR}/${ARCHIVE_NAME}.bundle" ] || [ "$1" == "--force-tar" ]; then
    echo "📦 Method 2: Creating tar archive (excludes venv directories)..."
    echo "   This may take a while for large repositories..."
    cd "$(dirname "$REPO_PATH")"
    
    # Use find + tar for better performance on large repos
    find "$(basename "$REPO_PATH")" \
        -type f \
        ! -path "*/venv/*" \
        ! -path "*/.venv/*" \
        ! -path "*/__pycache__/*" \
        ! -path "*/.git/objects/*" \
        ! -path "*/node_modules/*" \
        ! -path "*/.next/*" \
        ! -path "*/dist/*" \
        ! -path "*/build/*" \
        ! -name ".DS_Store" \
        -print0 | tar -czf "${OUTPUT_DIR}/${ARCHIVE_NAME}.tar.gz" --null -T - 2>/dev/null || {
        echo "⚠️  Tar creation timed out or failed (repository too large)"
        echo "   Recommendation: Use Git Bundle or GitHub clone instead"
    }
    
    if [ -f "${OUTPUT_DIR}/${ARCHIVE_NAME}.tar.gz" ]; then
        ARCHIVE_SIZE=$(du -h "${OUTPUT_DIR}/${ARCHIVE_NAME}.tar.gz" | cut -f1)
        echo "✅ Archive created: ${OUTPUT_DIR}/${ARCHIVE_NAME}.tar.gz"
        echo "   Size: $ARCHIVE_SIZE"
        echo ""
    fi
fi

# Method 3: Terminal-based rsync instructions
echo "📋 Method 3: Terminal-based transfer (for Bryan's Mac)"
echo "=================================================="
echo ""
echo "On Bryan's Mac, connect via SMB and use rsync:"
echo ""
echo "  # Connect to server first:"
echo "  mkdir -p ~/smb_mount"
echo "  mount_smbfs //michaelmataluni@192.168.6.252/Documents ~/smb_mount"
echo ""
echo "  # Transfer excluding venv directories:"
echo "  rsync -av --progress \\"
echo "    --exclude='*/venv/*' \\"
echo "    --exclude='*/.venv/*' \\"
echo "    --exclude='*/__pycache__/*' \\"
echo "    --exclude='*/.git/objects/*' \\"
echo "    --exclude='*/node_modules/*' \\"
echo "    ~/smb_mount/AbeOne_Master/ \\"
echo "    ~/Documents/AbeOne_Master/"
echo ""
echo "  # Unmount when done:"
echo "  umount ~/smb_mount"
echo ""

# Summary
echo "=================================================="
echo "✅ Transfer preparation complete!"
echo ""
echo "📦 Archives created on Desktop:"
if [ -f "${OUTPUT_DIR}/${ARCHIVE_NAME}.tar.gz" ]; then
    echo "   • ${ARCHIVE_NAME}.tar.gz ($ARCHIVE_SIZE)"
fi
if [ -f "${OUTPUT_DIR}/${ARCHIVE_NAME}.zip" ]; then
    echo "   • ${ARCHIVE_NAME}.zip ($ZIP_SIZE)"
fi
echo ""
echo "💡 Recommended: Use tar.gz archive (smaller, faster)"
echo "   Bryan can extract with: tar -xzf ${ARCHIVE_NAME}.tar.gz"
echo ""
echo "🔗 Or use GitHub clone (easiest):"
echo "   git clone https://github.com/bravetto/abe-one-source.git AbeOne_Master"
echo ""

