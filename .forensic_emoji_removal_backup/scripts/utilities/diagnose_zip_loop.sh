#!/bin/bash
# SAFETY: Diagnostic script to find stuck zip extraction loops
# ASSUMES: macOS system with zip extraction issues

echo "🔍 ZIP EXTRACTION LOOP DIAGNOSTIC"
echo "=================================="
echo ""

# 1. Check StreamingUnzipService processes
echo "📦 StreamingUnzipService Processes:"
ps aux | grep -i "StreamingUnzip" | grep -v grep
echo ""

# 2. Check for Archive Utility processes
echo "📦 Archive Utility Processes:"
ps aux | grep -i "Archive\|BOMArchiveHelper" | grep -v grep
echo ""

# 3. Check recently modified zip files
echo "📦 Recently Modified Zip Files (last 24h):"
find ~/Downloads -name "*.zip" -type f -mtime -1 -exec ls -lh {} \; 2>/dev/null
echo ""

# 4. Check for extraction directories
echo "📦 Recently Created Extraction Directories:"
find ~/Downloads -type d -mtime -1 -exec ls -ld {} \; 2>/dev/null | head -10
echo ""

# 5. Check system logs for zip-related errors
echo "📦 Recent Zip-Related System Logs:"
log show --predicate 'eventMessage contains "zip" OR eventMessage contains "extract" OR eventMessage contains "archive"' --last 10m --style syslog 2>/dev/null | tail -20
echo ""

# 6. Check for stuck file handles on zip files
echo "📦 Open File Handles on Zip Files:"
lsof 2>/dev/null | grep -i "\.zip" | head -10
echo ""

# 7. Check CPU usage of zip-related processes
echo "📦 CPU Usage of Zip-Related Processes:"
ps aux | grep -iE "zip|unzip|archive|extract" | grep -v grep | awk '{printf "PID: %s, CPU: %s%%, CMD: %s\n", $2, $3, $11}'
echo ""

echo "✅ Diagnostic complete"
echo ""
echo "💡 RECOMMENDATIONS:"
echo "1. If you see high CPU usage, kill the process: kill -9 <PID>"
echo "2. If a zip file is stuck, try: killall StreamingUnzipService"
echo "3. Check Activity Monitor for 'Archive Utility' or 'StreamingUnzipService'"
echo "4. Try moving problematic zip files to a different location"

