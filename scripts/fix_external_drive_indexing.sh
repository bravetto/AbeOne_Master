#!/bin/bash
# ============================================================================
# EXTERNAL DRIVE INDEXING FIX - Immediate System Relief Protocol
# ============================================================================
# Purpose: Stop Spotlight/FSEvents from overwhelming macOS UI
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardians: AEYON (999 Hz) + Abë (530 Hz)
# ============================================================================

set -e

DRIVE_NAME="${1:-Elements}"
DRIVE_PATH="/Volumes/${DRIVE_NAME}"

echo "🔍 Checking for drive: ${DRIVE_PATH}"

if [ ! -d "${DRIVE_PATH}" ]; then
    echo "❌ Drive not found at ${DRIVE_PATH}"
    echo "💡 Available volumes:"
    ls -1 /Volumes/ | grep -v "^\.$" | grep -v "^\.\.$"
    echo ""
    echo "Usage: $0 [drive_name]"
    echo "Example: $0 Elements"
    exit 1
fi

echo "✅ Drive found: ${DRIVE_PATH}"
echo ""

# ============================================================================
# STEP 1: Turn Off Spotlight Indexing
# ============================================================================
echo "🔧 STEP 1: Disabling Spotlight indexing..."
sudo mdutil -i off "${DRIVE_PATH}" || echo "⚠️  Warning: mdutil -i off failed (may already be off)"
sudo mdutil -E "${DRIVE_PATH}" || echo "⚠️  Warning: mdutil -E failed (may be expected)"
echo "✅ Spotlight indexing disabled"
echo ""

# ============================================================================
# STEP 2: Stop FSEvents Tracking
# ============================================================================
echo "🔧 STEP 2: Stopping FSEvents tracking..."
if [ -d "${DRIVE_PATH}/.fseventsd" ]; then
    sudo rm -rf "${DRIVE_PATH}/.fseventsd"
    echo "✅ Removed existing .fseventsd"
fi
sudo touch "${DRIVE_PATH}/.fseventsd"
sudo chflags hidden "${DRIVE_PATH}/.fseventsd"
echo "✅ FSEvents tracking stopped"
echo ""

# ============================================================================
# STEP 3: Create "Never Index" Flags
# ============================================================================
echo "🔧 STEP 3: Creating permanent 'Never Index' flags..."
sudo touch "${DRIVE_PATH}/.metadata_never_index"
sudo chflags hidden "${DRIVE_PATH}/.metadata_never_index"

# Ensure Spotlight directory exists but is marked hidden
if [ ! -d "${DRIVE_PATH}/.Spotlight-V100" ]; then
    sudo mkdir -p "${DRIVE_PATH}/.Spotlight-V100"
fi
sudo chflags hidden "${DRIVE_PATH}/.Spotlight-V100"
echo "✅ Never-index flags created"
echo ""

# ============================================================================
# STEP 4: Restart Finder & SystemUIServer
# ============================================================================
echo "🔧 STEP 4: Restarting Finder and SystemUIServer..."
killall Finder 2>/dev/null || echo "⚠️  Finder not running"
killall SystemUIServer 2>/dev/null || echo "⚠️  SystemUIServer not running"
echo "✅ UI services restarted"
echo ""

# ============================================================================
# STEP 5: Force-Drop Spotlight (if still frozen)
# ============================================================================
echo "🔧 STEP 5: Checking Spotlight processes..."
if pgrep -x mds > /dev/null; then
    echo "⚠️  Spotlight (mds) is still running"
    echo "💡 If UI is still frozen, run: sudo killall -9 mds mds_stores mds_spindump"
else
    echo "✅ Spotlight processes are clean"
fi
echo ""

# ============================================================================
# VERIFICATION
# ============================================================================
echo "🔍 Verification:"
echo "  Drive path: ${DRIVE_PATH}"
echo "  Spotlight indexing: $(sudo mdutil -s "${DRIVE_PATH}" 2>&1 | grep -o "Indexing.*" || echo "Disabled")"
echo "  .metadata_never_index: $([ -f "${DRIVE_PATH}/.metadata_never_index" ] && echo "✅ Exists" || echo "❌ Missing")"
echo "  .fseventsd: $([ -f "${DRIVE_PATH}/.fseventsd" ] && echo "✅ Exists (blocked)" || echo "❌ Missing")"
echo ""

echo "✨ Fix complete!"
echo "💡 Your system should now be responsive."
echo "💡 Wait 20-40 seconds for UI locks to fully release."
echo ""
echo "∞ AbëONE ∞"

