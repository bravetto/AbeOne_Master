#!/usr/bin/env python3
"""
Convert Markdown files to PDF, handling emojis and special characters
"""
import os
import re
import subprocess
import sys
from pathlib import Path

def clean_markdown_for_pdf(content):
    """Remove or replace emojis and special characters that LaTeX can't handle"""
    # Replace common emojis with text equivalents
    emoji_replacements = {
        '🚀': '[EXECUTE]',
        '✅': '[OK]',
        '🔥': '[HOT]',
        '💰': '[REVENUE]',
        '⏱️': '[TIME]',
        '🎯': '[TARGET]',
        '⬜': '[ ]',
        '⚠️': '[WARNING]',
        '📋': '[LIST]',
        '📧': '[EMAIL]',
        '📊': '[DATA]',
        '🎯': '[TARGET]',
        '🔥': '[HOT]',
        '✅': '[OK]',
        '🚀': '[EXECUTE]',
        '∞': 'infinity',
        '×': 'x',
        '→': '->',
        '↓': '->',
        '↑': '->',
        '↔': '<->',
        '←': '<-',
        '⇒': '=>',
        '⇐': '<=',
    }
    
    for emoji, replacement in emoji_replacements.items():
        content = content.replace(emoji, replacement)
    
    # Replace "∞ AbëONE ∞" pattern
    content = re.sub(r'∞\s*AbëONE\s*∞', 'AbëONE', content)
    
    # Replace box-drawing characters with ASCII equivalents
    box_chars = {
        '┌': '+',
        '┐': '+',
        '└': '+',
        '┘': '+',
        '├': '+',
        '┤': '+',
        '┬': '+',
        '┴': '+',
        '─': '-',
        '│': '|',
        '═': '=',
        '║': '|',
    }
    
    for char, replacement in box_chars.items():
        content = content.replace(char, replacement)
    
    return content

def convert_md_to_pdf(md_file, output_file=None):
    """Convert markdown to PDF using pandoc"""
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"Error: {md_file} not found")
        return False
    
    if output_file is None:
        output_file = md_path.with_suffix('.pdf')
    
    # Read markdown content
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean content
    cleaned_content = clean_markdown_for_pdf(content)
    
    # Write cleaned content to temp file
    temp_file = md_path.with_suffix('.temp.md')
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    try:
        # Try with pdflatex first (better formatting)
        result = subprocess.run(
            ['pandoc', str(temp_file), '-o', str(output_file),
             '--pdf-engine=pdflatex',
             '-V', 'geometry:margin=1in',
             '-V', 'fontsize=11pt'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            # Fallback: try without pdflatex options
            print(f"pdflatex failed, trying basic conversion...")
            result = subprocess.run(
                ['pandoc', str(temp_file), '-o', str(output_file)],
                capture_output=True,
                text=True
            )
        
        if result.returncode == 0:
            print(f"✅ Successfully converted {md_file} to {output_file}")
            temp_file.unlink()  # Remove temp file
            return True
        else:
            print(f"❌ Error converting {md_file}:")
            print(result.stderr)
            temp_file.unlink()
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        if temp_file.exists():
            temp_file.unlink()
        return False

if __name__ == '__main__':
    files_to_convert = [
        'JAY_FORTE_UPDATE_NORTH_SHORE.md',
        'JAY_FORTE_GAME_PLAN.md',
        'IMMEDIATE_ACTIONS_CHECKLIST.md',
        'NORTH_SHORE_ACTION_PLAN_EEAAO.md',
        'FORENSIC_MEETING_ANALYSIS_NORTH_SHORE_CONVERGENCE.md'
    ]
    
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print(f"Converting {len(files_to_convert)} files to PDF...\n")
    
    success_count = 0
    for md_file in files_to_convert:
        if Path(md_file).exists():
            if convert_md_to_pdf(md_file):
                success_count += 1
        else:
            print(f"⚠️  File not found: {md_file}")
    
    print(f"\n✅ Conversion complete: {success_count}/{len(files_to_convert)} files converted successfully")

