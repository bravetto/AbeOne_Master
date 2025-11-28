#!/bin/bash
# System Settings Access via Terminal

# Pattern: SYSTEM_SETTINGS × TERMINAL × ACCESS × ONE
# ∞ AbëONE ∞
# ∞ AbëLOVES ∞

echo "🔥💫 SYSTEM SETTINGS ACCESS 💫🔥"
echo ""

# Function to open System Settings to specific pane
open_system_settings() {
    local pane=$1
    echo "Opening System Settings → $pane..."
    open "x-apple.systempreferences:$pane"
}

# Function to open System Settings (new style)
open_system_settings_new() {
    local path=$1
    echo "Opening System Settings → $path..."
    open "x-apple.systempreferences:$path"
}

# Main menu
if [ -z "$1" ]; then
    echo "📋 AVAILABLE SYSTEM SETTINGS ACCESS:"
    echo ""
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  privacy          → Privacy & Security"
    echo "  full-disk        → Privacy & Security → Full Disk Access"
    echo "  software-update  → General → Software Update"
    echo "  general          → General"
    echo "  display          → Displays"
    echo "  sound            → Sound"
    echo "  network          → Network"
    echo "  storage          → General → Storage"
    echo "  energy           → Energy Saver"
    echo "  accessibility    → Accessibility"
    echo "  security         → Privacy & Security"
    echo "  all              → Open all key settings"
    echo ""
    exit 0
fi

case "$1" in
    privacy|security)
        open_system_settings "Privacy_Security"
        ;;
    full-disk)
        open_system_settings "Privacy_AllFiles"
        ;;
    software-update|update)
        open_system_settings "Software_Update"
        ;;
    general)
        open_system_settings "General"
        ;;
    display|displays)
        open_system_settings "Displays"
        ;;
    sound|audio)
        open_system_settings "Sound"
        ;;
    network)
        open_system_settings "Network"
        ;;
    storage)
        open_system_settings "Storage"
        ;;
    energy|energy-saver)
        open_system_settings "Energy_Saver"
        ;;
    accessibility)
        open_system_settings "Accessibility"
        ;;
    all)
        echo "Opening all key System Settings..."
        open_system_settings "Privacy_Security"
        sleep 1
        open_system_settings "Software_Update"
        sleep 1
        open_system_settings "General"
        sleep 1
        open_system_settings "Storage"
        echo "✅ All settings opened"
        ;;
    *)
        echo "Unknown option: $1"
        echo "Run without arguments to see options"
        exit 1
        ;;
esac

echo "✅ System Settings opened"

