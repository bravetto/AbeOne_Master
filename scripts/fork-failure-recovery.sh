#!/bin/bash
# Fork Failure Recovery & Prevention Script
# AEYON × AbëONE - System Resource Guardian
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE

set -euo pipefail

echo "  Fork Failure Recovery & Prevention"
echo "=========================================="
echo ""

# Check current system state
echo " System Resource Status:"
echo "---------------------------"

# Process count
PROC_COUNT=$(ps aux | wc -l | tr -d ' ')
echo "  Processes: $PROC_COUNT"

# Max processes
MAX_PROC=$(sysctl -n kern.maxproc)
MAX_PROC_UID=$(sysctl -n kern.maxprocperuid)
echo "  Max processes (system): $MAX_PROC"
echo "  Max processes (user): $MAX_PROC_UID"

# File descriptors
FD_COUNT=$(lsof 2>/dev/null | wc -l | tr -d ' ')
FD_LIMIT=$(ulimit -n)
echo "  Open file descriptors: $FD_COUNT / $FD_LIMIT"

# Memory pressure
echo ""
echo " Memory Status:"
vm_stat | head -10

# Check for problematic processes
echo ""
echo " Checking for Resource-Heavy Processes:"
echo "REPLACE_ME"

# Find processes using most CPU
echo "  Top CPU consumers:"
ps aux | sort -rk 3,3 | head -6 | tail -5 | awk '{printf "    %s (PID: %s) - CPU: %s%%\n", $11, $2, $3}'

# Find processes using most memory
echo ""
echo "  Top memory consumers:"
ps aux | sort -rk 4,4 | head -6 | tail -5 | awk '{printf "    %s (PID: %s) - MEM: %s%%\n", $11, $2, $4}'

# Check for zombie processes
ZOMBIES=$(ps aux | awk '$8 ~ /^Z/ {print}' | wc -l | tr -d ' ')
if [ "$ZOMBIES" -gt 0 ]; then
    echo ""
    echo "    Found $ZOMBIES zombie process(es):"
    ps aux | awk '$8 ~ /^Z/ {print "    PID: " $2 " - " $11}'
else
    echo ""
    echo "   No zombie processes found"
fi

# Recovery actions
echo ""
echo " Recovery Actions:"
echo "--------------------"

# Check if bird process is problematic
BIRD_PID=$(ps aux | grep -i "bird" | grep -v grep | awk '{print $2}' | head -1)
if [ -n "$BIRD_PID" ]; then
    BIRD_CPU=$(ps aux | grep -i "bird" | grep -v grep | awk '{print $3}' | head -1)
    BIRD_TIME=$(ps aux | grep -i "bird" | grep -v grep | awk '{print $10}' | head -1)
    echo "  iCloud Drive (bird) process found:"
    echo "    PID: $BIRD_PID"
    echo "    CPU: ${BIRD_CPU}%"
    echo "    Runtime: $BIRD_TIME"
    
    # Check if it's been running too long or using too much CPU
    if (( $(echo "$BIRD_CPU > 20" | bc -l 2>/dev/null || echo 0) )); then
        echo "      High CPU usage detected"
        echo "     Consider: kill $BIRD_PID (if iCloud sync is stuck)"
    fi
fi

# Check for excessive zsh processes
ZSH_COUNT=$(ps aux | grep -E "^\w+\s+\d+\s+.*zsh" | grep -v grep | wc -l | tr -d ' ')
if [ "$ZSH_COUNT" -gt 10 ]; then
    echo ""
    echo "    Found $ZSH_COUNT zsh processes (may be excessive)"
    echo "     Consider closing unused terminal windows"
fi

# Prevention recommendations
echo ""
echo " Prevention Recommendations:"
echo "-------------------------------"
echo "  1. Monitor process count: ps aux | wc -l"
echo "  2. Check for stuck processes: ps aux | sort -rk 3,3 | head -10"
echo "  3. If fork fails occur:"
echo "     - Close unused terminal windows"
echo "     - Restart stuck applications"
echo "     - Check: sysctl kern.maxproc kern.maxprocperuid"
echo "  4. For persistent issues, restart terminal or system"

# Quick recovery command
echo ""
echo " Quick Recovery Commands:"
echo "----------------------------"
echo "  # Check current state:"
echo "  ps aux | wc -l"
echo ""
echo "  # Find resource-heavy processes:"
echo "  ps aux | sort -rk 3,3 | head -10"
echo ""
echo "  # If needed, kill specific process:"
if [ -n "$BIRD_PID" ]; then
    echo "  kill $BIRD_PID  # iCloud Drive"
fi
echo ""
echo " System check complete"
echo ""
echo "Pattern: OBSERVER × TRUTH × ATOMIC × ONE"
echo "∞ AbëONE ∞"

