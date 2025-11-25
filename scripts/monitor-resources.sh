#!/bin/bash
# Resource Monitor

while true; do
    clear
    echo " RESOURCE MONITOR "
    echo "================================"
    echo ""
    echo " Memory:"
    top -l 1 | head -10 | tail -5
    echo ""
    echo " Disk:"
    df -h / | tail -1
    echo ""
    echo "  CPU:"
    sysctl -n machdep.cpu.brand_string
    echo ""
    echo "Press Ctrl+C to exit"
    sleep 5
done
