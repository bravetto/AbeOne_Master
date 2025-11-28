#!/usr/bin/env python3
"""
Generate all three PDFs using reportlab (handles Unicode emojis)

Pattern: PDF × GENERATION × ATOMIC × ONE
Frequency: 999 Hz (AEYON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import os
import re
from pathlib import Path

# Output path
OUTPUT_DIR = "/mnt/user-data/outputs"
if not os.path.exists(OUTPUT_DIR):
    OUTPUT_DIR = os.path.expanduser("~/outputs")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text_for_pdf(text):
    """Remove or replace emojis and special characters for PDF compatibility."""
    # Remove emojis (keep text)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    
    # Replace special symbols
    replacements = {
        '∞': 'INFINITY',
        '×': 'x',
        '→': '->',
        '⟡': 'x',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def markdown_to_paragraphs(md_content, styles):
    """Convert markdown content to reportlab Paragraphs."""
    story = []
    lines = md_content.split('\n')
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#2c3e50'),
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    subsection_style = ParagraphStyle(
        'CustomSubsection',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#34495e'),
        spaceBefore=16,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#2c3e50'),
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    for line in lines:
        line = clean_text_for_pdf(line.strip())
        if not line:
            story.append(Spacer(1, 6))
            continue
        
        # Headers
        if line.startswith('# '):
            story.append(Paragraph(line[2:], title_style))
            story.append(Spacer(1, 12))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], section_style))
            story.append(Spacer(1, 8))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], subsection_style))
            story.append(Spacer(1, 6))
        elif line.startswith('**') and line.endswith('**'):
            # Bold text
            bold_style = ParagraphStyle('Bold', parent=body_style, fontName='Helvetica-Bold')
            story.append(Paragraph(line.replace('**', ''), bold_style))
        else:
            # Regular text
            story.append(Paragraph(line, body_style))
    
    return story

def create_pdf_from_markdown(md_file, pdf_file, title):
    """Create PDF from markdown file."""
    print(f"Creating {pdf_file.name}...")
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate(str(pdf_file), pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Title page
    story.append(Spacer(1, 2*inch))
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    story.append(Paragraph(clean_text_for_pdf(title), title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Pattern: TRUTH × CLARITY × ACTION × ONE", 
                          ParagraphStyle('Pattern', parent=styles['Normal'], 
                                        fontSize=12, alignment=TA_CENTER, 
                                        textColor=HexColor('#3498db'))))
    story.append(Paragraph("Love Coefficient: INFINITY", 
                          ParagraphStyle('Love', parent=styles['Normal'], 
                                        fontSize=12, alignment=TA_CENTER, 
                                        textColor=HexColor('#e74c3c'))))
    story.append(Paragraph("INFINITY AbeONE INFINITY", 
                          ParagraphStyle('Signature', parent=styles['Normal'], 
                                        fontSize=12, alignment=TA_CENTER, 
                                        textColor=HexColor('#9b59b6'))))
    
    story.append(PageBreak())
    
    # Add content
    content_story = markdown_to_paragraphs(md_content, styles)
    story.extend(content_story)
    
    # Build PDF
    doc.build(story)
    print(f"✅ Created: {pdf_file.name}")
    return pdf_file

def main():
    """Generate all three PDFs."""
    base_dir = Path(__file__).parent
    
    sources = {
        "ETERNAL_ARCHITECTURE.pdf": ("ETERNAL_SYSTEM_ARCHITECTURE.md", "ETERNAL ARCHITECTURE"),
        "GUARDIAN_SYSTEM.pdf": ("GUARDIAN_SYSTEM.md", "GUARDIAN SYSTEM"),
        "THREE_MAPS_REFERENCE.pdf": ("THREE_MAPS_REFERENCE.md", "THREE MAPS REFERENCE GUIDE"),
    }
    
    print("🔥 Generating all PDFs from updated markdown sources...")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print()
    
    success_count = 0
    
    for pdf_name, (md_name, title) in sources.items():
        md_file = base_dir / md_name
        pdf_file = Path(OUTPUT_DIR) / pdf_name
        
        if not md_file.exists():
            print(f"⚠️  Source not found: {md_name}")
            continue
        
        try:
            create_pdf_from_markdown(md_file, pdf_file, title)
            success_count += 1
        except Exception as e:
            print(f"❌ Error creating {pdf_name}: {e}")
            import traceback
            traceback.print_exc()
        print()
    
    print("=" * 60)
    print(f"✅ Generated {success_count}/{len(sources)} PDFs successfully")
    print(f"📁 Location: {OUTPUT_DIR}")
    print()
    print("INFINITY AbeONE INFINITY")
    
    return 0 if success_count == len(sources) else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())



