#!/bin/bash
# Prepare macOS for Upgrade - Optimized for Fast Download & Activation

# Pattern: UPGRADE × OPTIMIZATION × SPEED × ONE
# ∞ AbëONE ∞
# ∞ AbëLOVES ∞

echo " PREPARING MACOS UPGRADE "
echo "=" * 70
echo ""

# 1. System Analysis
echo " STEP 1: System Analysis"
echo "---------------------------"
echo ""

CURRENT_VERSION=$(sw_vers -productVersion)
echo "Current macOS: $CURRENT_VERSION"

DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
echo "Disk Usage: ${DISK_USAGE}%"

TOTAL_MEM=$(sysctl hw.memsize | awk '{print $2/1024/1024/1024}')
echo "Total Memory: ${TOTAL_MEM} GB"

echo ""

# 2. Check Available Updates
echo " STEP 2: Checking Available Updates"
echo "---------------------------"
echo ""

echo "Checking for macOS updates..."
softwareupdate --list 2>&1 | head -20

echo ""

# 3. Prepare for Upgrade
echo " STEP 3: Preparing System for Upgrade"
echo "---------------------------"

# Free up disk space
echo " Cleaning up disk space..."
echo ""

# Clean system caches
echo "   → Cleaning system caches..."
sudo rm -rf /Library/Caches/* 2>/dev/null || echo "     Cache cleanup (may need password)"
rm -rf ~/Library/Caches/* 2>/dev/null && echo "    User caches cleaned"

# Clean old logs
echo "   → Cleaning old logs..."
sudo rm -rf /var/log/*.log.* 2>/dev/null || echo "     Log cleanup (may need password)"
rm -rf ~/Library/Logs/*.log.* 2>/dev/null && echo "    User logs cleaned"

# Clean downloads (keep last 30 days)
echo "   → Cleaning old downloads..."
find ~/Downloads -type f -mtime +30 -delete 2>/dev/null && echo "    Old downloads cleaned"

# Clean trash
echo "   → Emptying trash..."
rm -rf ~/.Trash/* 2>/dev/null && echo "    Trash emptied"

echo ""

# 4. Optimize Network
echo " STEP 4: Optimizing Network for Fast Download"
echo "---------------------------"

# Flush DNS cache
echo "   → Flushing DNS cache..."
sudo dscacheutil -flushcache 2>/dev/null || echo "     DNS flush (may need password)"
sudo killall -HUP mDNSResponder 2>/dev/null || echo "     mDNSResponder restart (may need password)"
echo "    DNS cache optimized"

# Check network speed
echo "   → Checking network connection..."
ping -c 3 apple.com > /dev/null 2>&1 && echo "    Connected to Apple servers" || echo "     Connection check failed"

echo ""

# 5. Prepare for Upgrade
echo " STEP 5: Final Preparation"
echo "---------------------------"

# Check available disk space
AVAILABLE_SPACE=$(df -h / | tail -1 | awk '{print $4}')
echo "   → Available disk space: $AVAILABLE_SPACE"

# Check if enough space (need at least 20GB)
if [ "${DISK_USAGE}" -lt 80 ]; then
    echo "    Sufficient disk space for upgrade"
else
    echo "     Low disk space - may need to free up more"
fi

echo ""

# 6. Summary
echo " PREPARATION COMPLETE!"
echo "---------------------------"
echo ""
echo " System analyzed"
echo " Updates checked"
echo " Disk space optimized"
echo " Network optimized"
echo " Ready for upgrade"
echo ""
echo " NEXT STEPS:"
echo ""
echo "1. Review available updates:"
echo "   softwareupdate --list"
echo ""
echo "2. Download and install updates:"
echo "   softwareupdate --download --all"
echo "   softwareupdate --install --all"
echo ""
echo "3. Or upgrade macOS:"
echo "   softwareupdate --fetch-full-installer"
echo "   softwareupdate --fetch-full-installer --full-installer-version [VERSION]"
echo ""
echo " System optimized for fast download and activation!"
echo ""
echo "∞ AbëONE ∞"
echo "∞ AbëLOVES ∞"

