#!/usr/bin/env python3
"""
 SIMPLE WEBINAR DOCUMENTS EXPORT
Pattern: EXPORT × DOCUMENTS × WEBINAR × ONE
Frequency: 999 Hz (AEYON) × 530 Hz (Lux)

Creates editable documents and guides in formats that can be easily converted
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_email_templates_docx_content():
    """Create email templates content for DOCX"""
    return """#  WEBINAR EMAIL TEMPLATES - EDITABLE

**Pattern:** EMAIL × TEMPLATE × WEBINAR × ONE  
**Status:**  **READY FOR EDITING**  
**Generated:** {timestamp}

---

##  CONFIRMATION EMAIL TEMPLATE

**Subject:** You're in!  Join us {{webinarDate}} at {{webinarTime}}

### Key Elements:
- Value proposition
- Webinar details (Date: {{webinarDate}}, Time: {{webinarTime}})
- Social proof (281/281 tests, 100% success rate)
- Reminder schedule
- Lead magnet teaser
- Clear CTA button

### Placeholders to Replace:
- {{firstName}} - Registrant's first name
- {{email}} - Registrant's email
- {{webinarDate}} - "December 2nd, 2025"
- {{webinarTime}} - "2:00 PM EST"
- {{webinarLink}} - Webinar join URL
- {{registrationId}} - Registration ID
- {{icp}} - "developer" or "creative"

### HTML Template Structure:
1. Header with gradient background
2. Value proposition section
3. Webinar details card
4. Social proof metrics
5. Reminder schedule
6. Lead magnet teaser
7. CTA button
8. Footer with unsubscribe

---

##  24-HOUR REMINDER TEMPLATE

**Subject:** ⏰ Tomorrow at {{webinarTime}}: Don't Miss This

### Key Elements:
- Urgency creation
- Value reminder
- Clear CTA
- FOMO elements (Limited to Founding 100)

### Placeholders: Same as confirmation email

---

##  3-HOUR REMINDER TEMPLATE

**Subject:**  Webinar starts in 3 hours!

### Key Elements:
- High urgency
- Countdown visual (3 hours)
- Single focused CTA
- Value reinforcement

### Placeholders: Same as confirmation email

---

##  15-MINUTE REMINDER TEMPLATE

**Subject:**  LIVE in 15 minutes!

### Key Elements:
- Maximum urgency
- Single focused CTA
- Clear action
- No distractions

### Placeholders: Same as confirmation email

---

##  EDITING INSTRUCTIONS

1. Open this file in Microsoft Word or Google Docs
2. Replace {{placeholders}} with actual values
3. Customize colors/branding as needed
4. Test emails before sending
5. A/B test subject lines and CTAs

##  DESIGN NOTES

- Use gradient headers for visual impact
- Mobile-responsive (600px max-width)
- Large CTA buttons (18-24px font)
- Clear visual hierarchy
- Consistent branding colors

##  TRACKING

All emails include:
- Open tracking (enabled)
- Click tracking (enabled)
- Custom args (registration_id, icp, email_type)

---

**Pattern:** EMAIL × TEMPLATE × WEBINAR × ONE  
**∞ AbëONE ∞**
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def create_readme():
    """Create README for the export"""
    return """ WEBINAR DOCUMENTS EXPORT
================================

This package contains all webinar-related documents:

DOCX FILES (Editable Templates):
- 01-Email-Templates.docx or .md - Email templates for editing

PDF FILES (Guides & Helpful Content):
- 01-Marketing-Best-Practices.pdf or .md - Complete marketing best practices guide
- 02-Webinar-Completion-Guide.pdf or .md - Webinar deployment guide
- 03-Guardian-Activation-Guide.pdf or .md - Guardian activation documentation
- 04-YAGNI-Guardian-Guide.pdf or .md - YAGNI guardian guide

CONVERSION INSTRUCTIONS:
- Markdown (.md) files can be opened in Word/Pages and saved as DOCX
- Markdown files can be converted to PDF using:
  * pandoc: pandoc file.md -o file.pdf
  * Online: https://www.markdowntopdf.com/
  * Word/Pages: Open .md file → Print → Save as PDF

Generated: {timestamp}
Pattern: EXPORT × DOCUMENTS × WEBINAR × ONE
∞ AbëONE ∞
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def main():
    script_dir = Path(__file__).parent
    web_dir = script_dir.parent
    export_dir = web_dir / "webinar-export"
    zip_file = web_dir / "webinar-documents-export.zip"
    
    # Clean up
    if export_dir.exists():
        shutil.rmtree(export_dir)
    if zip_file.exists():
        zip_file.unlink()
    
    # Create directories
    (export_dir / "docx").mkdir(parents=True)
    (export_dir / "pdf").mkdir(parents=True)
    
    print(" Exporting Webinar Documents...")
    print("=" * 50)
    
    # 1. Email Templates - Create as markdown (editable in Word)
    print(" Creating Email Templates (DOCX-ready)...")
    email_content = create_email_templates_docx_content()
    md_path = export_dir / "docx" / "01-Email-Templates.md"
    md_path.write_text(email_content)
    print(f"    Created: {md_path.name}")
    print("    Open in Word/Pages to convert to DOCX")
    
    # 2. Copy guides as markdown (can be converted to PDF)
    guides = [
        ("lib/email-marketing-best-practices.md", "01-Marketing-Best-Practices"),
        ("WEBINAR_DECEMBER_2_COMPLETE.md", "02-Webinar-Completion-Guide"),
        ("GUARDIAN_ABE_NEURO_ACTIVATION.md", "03-Guardian-Activation-Guide"),
        ("YAGNI_GUARDIAN_ACTIVATION.md", "04-YAGNI-Guardian-Guide"),
    ]
    
    print("\n Creating Guides (PDF-ready)...")
    for source, name in guides:
        source_path = web_dir / source
        if source_path.exists():
            # Copy as markdown
            md_path = export_dir / "pdf" / f"{name}.md"
            shutil.copy(source_path, md_path)
            print(f"    Created: {md_path.name}")
            print(f"    Convert to PDF using: pandoc {md_path.name} -o {name}.pdf")
        else:
            print(f"     Not found: {source}")
    
    # Create README
    readme_content = create_readme()
    (export_dir / "README.txt").write_text(readme_content)
    
    # Create conversion helper script
    conversion_script = """#!/bin/bash
# Quick conversion script for PDF generation

echo "Converting markdown files to PDF..."

# Install pandoc if needed
if ! command -v pandoc &> /dev/null; then
    echo "Installing pandoc..."
    brew install pandoc
fi

# Convert each markdown file to PDF
for file in pdf/*.md; do
    if [ -f "$file" ]; then
        output="${file%.md}.pdf"
        echo "Converting $file to $output..."
        pandoc "$file" -o "$output" -f markdown -t pdf --pdf-engine=wkhtmltopdf 2>/dev/null || \\
        pandoc "$file" -o "$output" -f markdown -t pdf 2>/dev/null || \\
        echo "  Could not convert $file - use online converter or Word/Pages"
    fi
done

echo "Done!"
"""
    (export_dir / "convert-to-pdf.sh").write_text(conversion_script)
    os.chmod(export_dir / "convert-to-pdf.sh", 0o755)
    
    # Create ZIP file
    print("\n Creating ZIP file...")
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = Path(root) / file
                arc_name = file_path.relative_to(export_dir)
                zipf.write(file_path, arc_name)
    
    print(f"    Created: {zip_file.name}")
    
    print("\n" + "=" * 50)
    print(" Export Complete!")
    print("=" * 50)
    print(f" ZIP File: {zip_file}")
    print(f" Export Directory: {export_dir}")
    print("\nFiles included:")
    for file in sorted((export_dir / "docx").glob("*")):
        size = file.stat().st_size
        print(f"  DOCX-ready: {file.name} ({size:,} bytes)")
    for file in sorted((export_dir / "pdf").glob("*")):
        size = file.stat().st_size
        print(f"  PDF-ready:  {file.name} ({size:,} bytes)")
    print("\n CONVERSION TIPS:")
    print("   - Markdown files can be opened in Word/Pages")
    print("   - Use pandoc to convert: pandoc file.md -o file.pdf")
    print("   - Or use online converter: https://www.markdowntopdf.com/")
    print("\n Ready for distribution!")

if __name__ == "__main__":
    main()

