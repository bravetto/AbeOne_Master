#!/bin/bash
# Quick share script for Thanksgiving video
# Opens the video location and provides sharing options

VIDEO_PATH="abeone_app/assets/videos/thanksgiving_video.mp4"
VIDEO_DIR="abeone_app/assets/videos"

echo "∞ AbëONE ∞"
echo "Thanksgiving Video for: JAH, JESS, JORDAN, JANEL & DEVON"
echo ""

if [ -f "$VIDEO_PATH" ]; then
    echo "✓ Video found: $VIDEO_PATH"
    echo ""
    echo "Opening video location..."
    open "$VIDEO_DIR"
    echo ""
    echo "You can now:"
    echo "  • Drag the video to Messages/iMessage"
    echo "  • Attach to email"
    echo "  • Share via AirDrop"
    echo "  • Upload to cloud storage"
    echo ""
    echo "Or use the send script:"
    echo "  python3 scripts/send_thanksgiving_video.py"
else
    echo "⚠ Video not found. Generating..."
    python3 scripts/generate_thanksgiving_video.py
    if [ -f "$VIDEO_PATH" ]; then
        open "$VIDEO_DIR"
    fi
fi

echo "Pattern: SHARING × LOVE × GRATITUDE × CONNECTION × ONE"
echo "∞ AbëONE ∞"

