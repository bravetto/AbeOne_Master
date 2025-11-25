#!/usr/bin/env python3
"""
Generate all three PDFs from updated markdown sources
Handles Unicode emojis by converting to HTML first, then PDF

Pattern: PDF × GENERATION × ATOMIC × ONE
Frequency: 999 Hz (AEYON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import subprocess
import sys
import re
from pathlib import Path
import tempfile

# Output directory
OUTPUT_DIR = Path.home() / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Source files
SOURCES = {
    "ETERNAL_ARCHITECTURE.pdf": "ETERNAL_SYSTEM_ARCHITECTURE.md",
    "GUARDIAN_SYSTEM.pdf": "GUARDIAN_SYSTEM.md",
    "THREE_MAPS_REFERENCE.pdf": "THREE_MAPS_REFERENCE.md",
}

def markdown_to_html(md_content: str) -> str:
    """Convert markdown to HTML, preserving emojis."""
    # Use pandoc to convert markdown to HTML
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_md:
        tmp_md.write(md_content)
        tmp_md_path = tmp_md.name
    
    try:
        result = subprocess.run(
            ["pandoc", tmp_md_path, "-t", "html", "--standalone"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            raise Exception(f"Pandoc HTML conversion failed: {result.stderr}")
    finally:
        Path(tmp_md_path).unlink()

def html_to_pdf(html_content: str, pdf_file: Path) -> bool:
    """Convert HTML to PDF using weasyprint or wkhtmltopdf."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp_html:
        tmp_html.write(html_content)
        tmp_html_path = tmp_html.name
    
    try:
        # Try weasyprint first (better Unicode support)
        result = subprocess.run(
            ["weasyprint", tmp_html_path, str(pdf_file)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            return True
        
        # Fallback: try wkhtmltopdf
        result = subprocess.run(
            ["wkhtmltopdf", tmp_html_path, str(pdf_file)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        return result.returncode == 0
        
    except FileNotFoundError:
        # Neither tool available, try pandoc with different engine
        result = subprocess.run(
            [
                "pandoc", tmp_html_path,
                "-o", str(pdf_file),
                "--pdf-engine=weasyprint"
            ],
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0
    finally:
        Path(tmp_html_path).unlink()

def generate_pdf(md_file: Path, pdf_file: Path) -> bool:
    """Generate PDF from markdown."""
    try:
        # Read markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        print(f"  Converting markdown to HTML...")
        html_content = markdown_to_html(md_content)
        
        # Convert HTML to PDF
        print(f"  Converting HTML to PDF...")
        if html_to_pdf(html_content, pdf_file):
            print(f" Created: {pdf_file.name}")
            return True
        else:
            print(f" PDF conversion failed")
            return False
                
    except Exception as e:
        print(f" Error generating {pdf_file.name}: {e}")
        return False

def main():
    """Generate all PDFs."""
    base_dir = Path(__file__).parent
    
    print(" Generating all PDFs from updated markdown sources...")
    print(f" Output directory: {OUTPUT_DIR}")
    print()
    
    success_count = 0
    
    for pdf_name, md_name in SOURCES.items():
        md_file = base_dir / md_name
        pdf_file = OUTPUT_DIR / pdf_name
        
        if not md_file.exists():
            print(f"  Source not found: {md_name}")
            continue
        
        print(f" Generating {pdf_name} from {md_name}...")
        if generate_pdf(md_file, pdf_file):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f" Generated {success_count}/{len(SOURCES)} PDFs successfully")
    print(f" Location: {OUTPUT_DIR}")
    print()
    print("∞ AbëONE ∞")
    
    return 0 if success_count == len(SOURCES) else 1

if __name__ == "__main__":
    sys.exit(main())



