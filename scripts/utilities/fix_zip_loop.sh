#!/bin/bash
# SAFETY: Script to stop stuck zip extraction loops
# ASSUMES: macOS system with zip extraction issues

echo " FIXING ZIP EXTRACTION LOOP"
echo "=============================="
echo ""

# 1. Kill StreamingUnzipService processes (they'll restart automatically if needed)
echo " Stopping StreamingUnzipService processes..."
killall StreamingUnzipService 2>/dev/null
sleep 1
echo " Done"
echo ""

# 2. Kill Archive Utility if running
echo " Stopping Archive Utility..."
killall "Archive Utility" 2>/dev/null
killall BOMArchiveHelper 2>/dev/null
sleep 1
echo " Done"
echo ""

# 3. Check if processes are still running
echo " Checking remaining processes..."
REMAINING=$(ps aux | grep -iE "StreamingUnzip|Archive" | grep -v grep | wc -l | tr -d ' ')
if [ "$REMAINING" -gt 0 ]; then
    echo "  Warning: Some processes are still running:"
    ps aux | grep -iE "StreamingUnzip|Archive" | grep -v grep
    echo ""
    echo " You may need to force kill them:"
    echo "   killall -9 StreamingUnzipService"
else
    echo " All zip extraction processes stopped"
fi
echo ""

# 4. Suggest moving problematic zip files
echo " RECOMMENDATIONS:"
echo "1. If zips keep auto-extracting, move them out of Downloads:"
echo "   mkdir ~/Desktop/zip_archive"
echo "   mv ~/Downloads/*.zip ~/Desktop/zip_archive/"
echo ""
echo "2. Disable auto-extraction in Finder:"
echo "   System Settings > Desktop & Dock > Remove items from the Desktop: Never"
echo ""
echo "3. Check Activity Monitor for any remaining processes"
echo ""

echo " Fix script complete"

