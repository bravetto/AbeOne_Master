#!/bin/bash
echo "🔥💫 QUICK STATUS CHECK 💫🔥"
echo ""
echo "📋 System:"
sysctl -n machdep.cpu.brand_string
df -h / | tail -1
echo ""
echo "📋 Project:"
cd ~/Documents/AbeOne_Master
git status --short 2>/dev/null | head -5
echo ""
echo "📋 Permissions:"
python3 scripts/check_permissions.py 2>/dev/null | grep -E "✅|❌"
