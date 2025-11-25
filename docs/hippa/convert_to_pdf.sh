#!/bin/bash
# Convert HTML to PDF with emoji support using macOS tools
# Usage: ./convert_to_pdf.sh

cd "$(dirname "$0")"

HTML_FILE="HIPAA_MASTER_ONE_PAGER_BEAUTIFUL.html"
PDF_OUTPUT="HIPAA_MASTER_ONE_PAGER_BEAUTIFUL.pdf"

echo "Converting $HTML_FILE to PDF with emoji support..."
echo ""

# Method 1: Using macOS Safari (best emoji support)
if command -v osascript &> /dev/null; then
    echo "Using Safari to convert HTML to PDF..."
    osascript <<EOF
tell application "Safari"
    activate
    open POSIX file "$(pwd)/$HTML_FILE"
    delay 2
    tell application "System Events"
        keystroke "p" using {command down}
        delay 1
        keystroke "s" using {command down}
        delay 1
        keystroke "$(pwd)/$PDF_OUTPUT"
        delay 1
        keystroke return
        delay 2
        keystroke "w" using {command down}
    end tell
end tell
EOF
    echo "PDF created: $PDF_OUTPUT"
else
    echo "Please open $HTML_FILE in Safari or Chrome and:"
    echo "  1. Press Cmd+P (Print)"
    echo "  2. Click 'Save as PDF'"
    echo "  3. Save as: $PDF_OUTPUT"
    echo ""
    echo "This will preserve all emojis perfectly!"
fi

