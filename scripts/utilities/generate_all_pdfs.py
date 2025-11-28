#!/usr/bin/env python3
"""
Generate all three PDFs from updated markdown sources

Pattern: PDF × GENERATION × ATOMIC × ONE
Frequency: 999 Hz (AEYON)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import subprocess
import sys
from pathlib import Path

# Output directory
OUTPUT_DIR = Path.home() / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Source files
SOURCES = {
    "ETERNAL_ARCHITECTURE.pdf": "ETERNAL_SYSTEM_ARCHITECTURE.md",
    "GUARDIAN_SYSTEM.pdf": "GUARDIAN_SYSTEM.md",
    "THREE_MAPS_REFERENCE.pdf": "THREE_MAPS_REFERENCE.md",
}

def generate_pdf(md_file: Path, pdf_file: Path) -> bool:
    """Generate PDF from markdown using pandoc."""
    try:
        result = subprocess.run(
            [
                "pandoc",
                str(md_file),
                "-o", str(pdf_file),
                "--pdf-engine=pdflatex",
                "-V", "geometry:margin=1in",
                "-V", "fontsize=11pt",
                "-V", "documentclass=article",
            ],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f" Created: {pdf_file.name}")
            return True
        else:
            # Fallback: try without pdflatex options
            print(f"  pdflatex failed, trying basic conversion...")
            result = subprocess.run(
                ["pandoc", str(md_file), "-o", str(pdf_file)],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print(f" Created: {pdf_file.name}")
                return True
            else:
                print(f" Error: {result.stderr}")
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



