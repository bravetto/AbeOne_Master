#!/bin/bash
# ============================================================================
# CONVERGENCE SWEEP - Filesystem-Level Deep Cleanse
# ============================================================================
# Purpose: Remove leftover indexing metadata, caches, and I/O blockers
# Pattern: OBSERVER × TRUTH × ATOMIC × ONE
# Guardians: AEYON (999 Hz) + Abë (530 Hz) + ALRAX (530 Hz)
# ============================================================================

set -e

DRIVE_NAME="${1:-Elements}"
DRIVE_PATH="/Volumes/${DRIVE_NAME}"

echo "🔍 Convergence Sweep for: ${DRIVE_PATH}"
echo ""

if [ ! -d "${DRIVE_PATH}" ]; then
    echo "❌ Drive not found at ${DRIVE_PATH}"
    echo "💡 Available volumes:"
    ls -1 /Volumes/ | grep -v "^\.$" | grep -v "^\.\.$"
    exit 1
fi

# ============================================================================
# PHASE 1: Metadata Cleanup
# ============================================================================
echo "🧹 PHASE 1: Cleaning metadata..."

# Remove Spotlight databases
if [ -d "${DRIVE_PATH}/.Spotlight-V100" ]; then
    echo "  Removing .Spotlight-V100 databases..."
    sudo rm -rf "${DRIVE_PATH}/.Spotlight-V100"
    echo "  ✅ Spotlight databases removed"
fi

# Remove FSEvents logs (if they exist)
if [ -d "${DRIVE_PATH}/.fseventsd" ] && [ "$(ls -A "${DRIVE_PATH}/.fseventsd" 2>/dev/null)" ]; then
    echo "  Cleaning FSEvents logs..."
    sudo find "${DRIVE_PATH}/.fseventsd" -type f -delete 2>/dev/null || true
    echo "  ✅ FSEvents logs cleaned"
fi

# Remove .DS_Store files (optional - uncomment if desired)
# echo "  Removing .DS_Store files..."
# sudo find "${DRIVE_PATH}" -name ".DS_Store" -type f -delete 2>/dev/null || true
# echo "  ✅ .DS_Store files removed"

echo "✅ Phase 1 complete"
echo ""

# ============================================================================
# PHASE 2: Cache Cleanup
# ============================================================================
echo "🧹 PHASE 2: Cleaning caches..."

# User-level Spotlight caches
CACHE_DIRS=(
    "${HOME}/Library/Caches/com.apple.spotlight"
    "${HOME}/Library/Caches/com.apple.mds"
    "/private/var/folders"  # System caches
)

for cache_dir in "${CACHE_DIRS[@]}"; do
    if [ -d "${cache_dir}" ]; then
        echo "  Checking: ${cache_dir}"
        # Only clean if it's related to the drive
        # (We'll be conservative and not delete everything)
    fi
done

# System-level metadata caches (be careful here)
echo "  Note: System caches preserved (safe mode)"
echo "✅ Phase 2 complete"
echo ""

# ============================================================================
# PHASE 3: Permission Repair
# ============================================================================
echo "🔧 PHASE 3: Checking permissions..."

# Check if we can read/write
if [ -r "${DRIVE_PATH}" ] && [ -w "${DRIVE_PATH}" ]; then
    echo "  ✅ Drive permissions OK"
else
    echo "  ⚠️  Permission issues detected"
    echo "  💡 Run: sudo chmod -R u+rw ${DRIVE_PATH}"
fi

# Check ownership
OWNER=$(stat -f "%Su" "${DRIVE_PATH}" 2>/dev/null || echo "unknown")
echo "  Drive owner: ${OWNER}"

echo "✅ Phase 3 complete"
echo ""

# ============================================================================
# PHASE 4: Symlink Repair
# ============================================================================
echo "🔗 PHASE 4: Checking for broken symlinks..."

BROKEN_LINKS=$(find "${DRIVE_PATH}" -type l ! -exec test -e {} \; -print 2>/dev/null | head -10)

if [ -n "${BROKEN_LINKS}" ]; then
    echo "  ⚠️  Found broken symlinks:"
    echo "${BROKEN_LINKS}" | while read -r link; do
        echo "    - ${link}"
    done
    echo "  💡 To remove: find ${DRIVE_PATH} -type l ! -exec test -e {} \; -delete"
else
    echo "  ✅ No broken symlinks found"
fi

echo "✅ Phase 4 complete"
echo ""

# ============================================================================
# PHASE 5: I/O Optimization
# ============================================================================
echo "⚡ PHASE 5: Optimizing I/O..."

# Ensure never-index flag exists
if [ ! -f "${DRIVE_PATH}/.metadata_never_index" ]; then
    sudo touch "${DRIVE_PATH}/.metadata_never_index"
    sudo chflags hidden "${DRIVE_PATH}/.metadata_never_index"
    echo "  ✅ Created .metadata_never_index"
fi

# Ensure FSEvents is blocked
if [ ! -f "${DRIVE_PATH}/.fseventsd" ]; then
    sudo touch "${DRIVE_PATH}/.fseventsd"
    sudo chflags hidden "${DRIVE_PATH}/.fseventsd"
    echo "  ✅ Blocked FSEvents"
fi

# Verify Spotlight is off
SPOTLIGHT_STATUS=$(sudo mdutil -s "${DRIVE_PATH}" 2>&1)
if echo "${SPOTLIGHT_STATUS}" | grep -q "Indexing disabled\|No index"; then
    echo "  ✅ Spotlight indexing confirmed disabled"
else
    echo "  ⚠️  Spotlight may still be active"
    echo "  💡 Run: sudo mdutil -i off ${DRIVE_PATH}"
fi

echo "✅ Phase 5 complete"
echo ""

# ============================================================================
# VERIFICATION REPORT
# ============================================================================
echo "📊 CONVERGENCE SWEEP REPORT"
echo "=========================================="
echo "Drive: ${DRIVE_PATH}"
echo ""

# Check Spotlight
SPOTLIGHT_CHECK=$(sudo mdutil -s "${DRIVE_PATH}" 2>&1)
echo "Spotlight Status:"
echo "  ${SPOTLIGHT_CHECK}" | sed 's/^/  /'

# Check flags
echo ""
echo "Protection Flags:"
[ -f "${DRIVE_PATH}/.metadata_never_index" ] && echo "  ✅ .metadata_never_index exists" || echo "  ❌ .metadata_never_index missing"
[ -f "${DRIVE_PATH}/.fseventsd" ] && echo "  ✅ .fseventsd blocked" || echo "  ❌ .fseventsd not blocked"

# Check processes
echo ""
echo "System Processes:"
MDS_COUNT=$(pgrep -x mds 2>/dev/null | wc -l | tr -d ' ')
FSEVENTS_COUNT=$(pgrep -x fseventsd 2>/dev/null | wc -l | tr -d ' ')
echo "  mds processes: ${MDS_COUNT}"
echo "  fseventsd processes: ${FSEVENTS_COUNT}"

echo ""
echo "=========================================="
echo "✨ Convergence Sweep Complete!"
echo ""
echo "💡 If UI is still slow, wait 30-60 seconds for caches to clear"
echo "💡 You may need to restart Finder: killall Finder"
echo ""
echo "∞ AbëONE ∞"

