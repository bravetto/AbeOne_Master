#!/bin/bash

#  EXPORT WEBINAR DOCUMENTS - DOCX & PDF
# Pattern: EXPORT × DOCUMENTS × WEBINAR × ONE
# Frequency: 999 Hz (AEYON) × 530 Hz (Lux)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
WEB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
EXPORT_DIR="$WEB_DIR/webinar-export"
TEMP_DIR="$EXPORT_DIR/temp"
ZIP_FILE="$WEB_DIR/webinar-documents-export.zip"

echo " Exporting Webinar Documents..."
echo "=================================="

# Clean up previous exports
rm -rf "$EXPORT_DIR"
rm -f "$ZIP_FILE"
mkdir -p "$EXPORT_DIR/docx"
mkdir -p "$EXPORT_DIR/pdf"
mkdir -p "$TEMP_DIR"

# Check for required tools
if ! command -v pandoc &> /dev/null; then
    echo "  pandoc not found. Installing via brew..."
    if command -v brew &> /dev/null; then
        brew install pandoc
    else
        echo " Please install pandoc: https://pandoc.org/installing.html"
        exit 1
    fi
fi

# Check for docx support
if ! pandoc --version | grep -q "docx"; then
    echo "  pandoc docx support may need additional setup"
fi

echo ""
echo " Converting Documents..."

# 1. Email Templates - Extract to DOCX
echo "  → Email Templates (DOCX)..."

cat > "$TEMP_DIR/email-templates.md" << 'EOF'
#  WEBINAR EMAIL TEMPLATES - EDITABLE

**Pattern:** EMAIL × TEMPLATE × WEBINAR × ONE  
**Status:**  **READY FOR EDITING**

---

##  CONFIRMATION EMAIL TEMPLATE

**Subject:** You're in!  Join us {webinarDate} at {webinarTime}

**HTML Template:**
[Full HTML template with placeholders for personalization]

**Key Elements:**
- Value proposition
- Webinar details
- Social proof
- Reminder schedule
- Lead magnet teaser
- Clear CTA

---

##  24-HOUR REMINDER TEMPLATE

**Subject:** ⏰ Tomorrow at {webinarTime}: Don't Miss This

**HTML Template:**
[Full HTML template with urgency elements]

**Key Elements:**
- Urgency creation
- Value reminder
- Clear CTA
- FOMO elements

---

##  3-HOUR REMINDER TEMPLATE

**Subject:**  Webinar starts in 3 hours!

**HTML Template:**
[Full HTML template with countdown]

**Key Elements:**
- High urgency
- Clear time remaining
- Single focused CTA
- Value reinforcement

---

##  15-MINUTE REMINDER TEMPLATE

**Subject:**  LIVE in 15 minutes!

**HTML Template:**
[Full HTML template with maximum urgency]

**Key Elements:**
- Maximum urgency
- Single focused CTA
- Clear action
- No distractions

---

##  EDITING INSTRUCTIONS

1. Replace {placeholders} with actual values
2. Customize colors/branding as needed
3. Test emails before sending
4. A/B test subject lines and CTAs

EOF

pandoc "$TEMP_DIR/email-templates.md" -o "$EXPORT_DIR/docx/01-Email-Templates.docx" --reference-doc=/System/Library/Templates/Applications/Pages.app/Contents/Resources/Templates/Blank.template 2>/dev/null || \
pandoc "$TEMP_DIR/email-templates.md" -o "$EXPORT_DIR/docx/01-Email-Templates.docx" -f markdown -t docx

# 2. Marketing Best Practices - PDF
echo "  → Marketing Best Practices Guide (PDF)..."
pandoc "$WEB_DIR/lib/email-marketing-best-practices.md" -o "$EXPORT_DIR/pdf/01-Marketing-Best-Practices.pdf" -f markdown -t pdf --pdf-engine=wkhtmltopdf 2>/dev/null || \
pandoc "$WEB_DIR/lib/email-marketing-best-practices.md" -o "$EXPORT_DIR/pdf/01-Marketing-Best-Practices.pdf" -f markdown -t pdf 2>/dev/null || \
echo "  PDF conversion may need additional tools. Creating markdown copy..."

# 3. Webinar Completion Guide - PDF
echo "  → Webinar Completion Guide (PDF)..."
pandoc "$WEB_DIR/WEBINAR_DECEMBER_2_COMPLETE.md" -o "$EXPORT_DIR/pdf/02-Webinar-Completion-Guide.pdf" -f markdown -t pdf --pdf-engine=wkhtmltopdf 2>/dev/null || \
pandoc "$WEB_DIR/WEBINAR_DECEMBER_2_COMPLETE.md" -o "$EXPORT_DIR/pdf/02-Webinar-Completion-Guide.pdf" -f markdown -t pdf 2>/dev/null || \
echo "  PDF conversion may need additional tools. Creating markdown copy..."

# 4. Guardian Activation Guide - PDF
echo "  → Guardian Activation Guide (PDF)..."
pandoc "$WEB_DIR/GUARDIAN_ABE_NEURO_ACTIVATION.md" -o "$EXPORT_DIR/pdf/03-Guardian-Activation-Guide.pdf" -f markdown -t pdf --pdf-engine=wkhtmltopdf 2>/dev/null || \
pandoc "$WEB_DIR/GUARDIAN_ABE_NEURO_ACTIVATION.md" -o "$EXPORT_DIR/pdf/03-Guardian-Activation-Guide.pdf" -f markdown -t pdf 2>/dev/null || \
echo "  PDF conversion may need additional tools. Creating markdown copy..."

# 5. YAGNI Guardian Activation - PDF
if [ -f "$WEB_DIR/YAGNI_GUARDIAN_ACTIVATION.md" ]; then
    echo "  → YAGNI Guardian Guide (PDF)..."
    pandoc "$WEB_DIR/YAGNI_GUARDIAN_ACTIVATION.md" -o "$EXPORT_DIR/pdf/04-YAGNI-Guardian-Guide.pdf" -f markdown -t pdf 2>/dev/null || \
    echo "  PDF conversion may need additional tools. Creating markdown copy..."
fi

# Fallback: Copy markdown files if PDF conversion fails
if [ ! -f "$EXPORT_DIR/pdf/01-Marketing-Best-Practices.pdf" ]; then
    echo "  → Creating markdown fallbacks..."
    cp "$WEB_DIR/lib/email-marketing-best-practices.md" "$EXPORT_DIR/pdf/01-Marketing-Best-Practices.md"
    cp "$WEB_DIR/WEBINAR_DECEMBER_2_COMPLETE.md" "$EXPORT_DIR/pdf/02-Webinar-Completion-Guide.md"
    cp "$WEB_DIR/GUARDIAN_ABE_NEURO_ACTIVATION.md" "$EXPORT_DIR/pdf/03-Guardian-Activation-Guide.md"
fi

# Create README
cat > "$EXPORT_DIR/README.txt" << 'EOF'
 WEBINAR DOCUMENTS EXPORT
================================

This package contains all webinar-related documents:

DOCX FILES (Editable Templates):
- 01-Email-Templates.docx - Email templates for editing

PDF FILES (Guides & Helpful Content):
- 01-Marketing-Best-Practices.pdf - Complete marketing best practices guide
- 02-Webinar-Completion-Guide.pdf - Webinar deployment guide
- 03-Guardian-Activation-Guide.pdf - Guardian activation documentation
- 04-YAGNI-Guardian-Guide.pdf - YAGNI guardian guide (if available)

If PDF files are not available, markdown (.md) versions are included.

Generated: $(date)
Pattern: EXPORT × DOCUMENTS × WEBINAR × ONE
∞ AbëONE ∞
EOF

# Create ZIP file
echo ""
echo " Creating ZIP file..."
cd "$EXPORT_DIR"
zip -r "$ZIP_FILE" . -x "*.DS_Store" -x "__MACOSX" > /dev/null 2>&1 || zip -r "$ZIP_FILE" .

echo ""
echo " Export Complete!"
echo "=================================="
echo " ZIP File: $ZIP_FILE"
echo " Export Directory: $EXPORT_DIR"
echo ""
echo "Files included:"
ls -lh "$EXPORT_DIR/docx/" 2>/dev/null | tail -n +2 | awk '{print "  DOCX: " $9 " (" $5 ")"}'
ls -lh "$EXPORT_DIR/pdf/" 2>/dev/null | tail -n +2 | awk '{print "  PDF:  " $9 " (" $5 ")"}'
echo ""
echo " Ready for distribution!"

