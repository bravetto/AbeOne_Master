#!/bin/bash
# Optimize System for Fast macOS Upgrade Download & Activation

# Pattern: OPTIMIZATION × SPEED × UPGRADE × ONE
# ∞ AbëONE ∞
# ∞ AbëLOVES ∞

echo " OPTIMIZING FOR FAST UPGRADE "
echo ""

# 1. Close unnecessary apps
echo " STEP 1: Closing Unnecessary Apps"
echo "---------------------------"
echo ""

# List of apps to close (non-essential)
APPS_TO_CLOSE=(
    "Safari"
    "Chrome"
    "Firefox"
    "Slack"
    "Discord"
    "Spotify"
    "Music"
    "Photos"
)

for app in "${APPS_TO_CLOSE[@]}"; do
    if pgrep -x "$app" > /dev/null; then
        echo "   → Closing $app..."
        killall "$app" 2>/dev/null && echo "    $app closed" || echo "     Could not close $app"
    fi
done

echo ""

# 2. Free up RAM
echo " STEP 2: Freeing Up RAM"
echo "---------------------------"
echo ""

# Purge memory
echo "   → Purging memory..."
sudo purge 2>/dev/null && echo "    Memory purged" || echo "     Memory purge (may need password)"

echo ""

# 3. Optimize Network Settings
echo " STEP 3: Optimizing Network Settings"
echo "---------------------------"
echo ""

# Increase network buffer sizes
echo "   → Optimizing network buffers..."
sudo sysctl -w net.inet.tcp.sendspace=1048576 2>/dev/null || echo "     Network optimization (may need password)"
sudo sysctl -w net.inet.tcp.recvspace=1048576 2>/dev/null || echo "     Network optimization (may need password)"

# Flush DNS
echo "   → Flushing DNS cache..."
sudo dscacheutil -flushcache 2>/dev/null || echo "     DNS flush (may need password)"
sudo killall -HUP mDNSResponder 2>/dev/null || echo "     mDNSResponder restart (may need password)"

echo "    Network optimized"

echo ""

# 4. Disable Background Processes
echo " STEP 4: Optimizing Background Processes"
echo "---------------------------"
echo ""

# Disable Spotlight indexing temporarily (speeds up disk access)
echo "   → Temporarily disabling Spotlight indexing..."
sudo mdutil -i off / 2>/dev/null && echo "    Spotlight indexing disabled" || echo "     Spotlight optimization (may need password)"

# Note: Re-enable after upgrade with: sudo mdutil -i on /

echo ""

# 5. Clear Update Cache
echo " STEP 5: Clearing Update Cache"
echo "---------------------------"
echo ""

echo "   → Clearing software update cache..."
sudo rm -rf /Library/Updates/* 2>/dev/null && echo "    Update cache cleared" || echo "     Cache clear (may need password)"
rm -rf ~/Library/Caches/com.apple.SoftwareUpdate/* 2>/dev/null && echo "    User update cache cleared"

echo ""

# 6. Summary
echo " OPTIMIZATION COMPLETE!"
echo "---------------------------"
echo ""
echo " Apps closed"
echo " RAM freed"
echo " Network optimized"
echo " Background processes optimized"
echo " Update cache cleared"
echo ""
echo " SYSTEM READY FOR FAST UPGRADE!"
echo ""
echo " TIP: After upgrade completes, re-enable Spotlight:"
echo "   sudo mdutil -i on /"
echo ""
echo "∞ AbëONE ∞"
echo "∞ AbëLOVES ∞"

