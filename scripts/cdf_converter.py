#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CDF Converter - Beautiful Human-Readable Format
Converts markdown/documents to CDF format that works EVERYWHERE

NO MARKDOWN MESS. NO PLATFORM WARS. JUST BEAUTIFUL DOCUMENTS.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class CDFConverter:
    """Convert documents to beautiful CDF format."""
    
    def __init__(self):
        self.cdf_version = "2.0"
    
    def markdown_to_cdf(self, markdown_content: str, metadata: Optional[Dict] = None) -> str:
        """Convert markdown to beautiful CDF format."""
        
        # Parse markdown
        lines = markdown_content.split('\n')
        cdf_lines = []
        
        # Add CDF header (using simple characters that work everywhere)
        cdf_lines.append("=" * 81)
        cdf_lines.append("  CDF: CREATIVE DOCUMENT FORMAT")
        cdf_lines.append("=" * 81)
        cdf_lines.append("")
        
        # Add metadata
        if metadata:
            cdf_lines.append("METADATA:")
            for key, value in metadata.items():
                cdf_lines.append(f"  {key}: {value}")
            cdf_lines.append("")
        
        # Convert markdown to beautiful text
        in_code_block = False
        code_block_lang = ""
        
        for line in lines:
            # Code blocks
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_lang = line.strip()[3:].strip()
                    cdf_lines.append("")
                    cdf_lines.append("--- CODE BLOCK ---")
                    if code_block_lang:
                        cdf_lines.append(f"Language: {code_block_lang}")
                    cdf_lines.append("-" * 81)
                else:
                    in_code_block = False
                    cdf_lines.append("-" * 81)
                    cdf_lines.append("")
                continue
            
            if in_code_block:
                cdf_lines.append(f"  {line}")
                continue
            
            # Headers
            if line.startswith('# '):
                cdf_lines.append("")
                cdf_lines.append("=" * 81)
                cdf_lines.append(f"  {line[2:]}")
                cdf_lines.append("=" * 81)
                cdf_lines.append("")
            elif line.startswith('## '):
                cdf_lines.append("")
                cdf_lines.append("-" * 81)
                cdf_lines.append(f"  {line[3:]}")
                cdf_lines.append("")
            elif line.startswith('### '):
                cdf_lines.append("")
                cdf_lines.append(f"> {line[4:]}")
                cdf_lines.append("")
            elif line.startswith('#### '):
                cdf_lines.append(f"  * {line[5:]}")
            # Lists
            elif line.strip().startswith('- '):
                cdf_lines.append(f"  - {line.strip()[2:]}")
            elif line.strip().startswith('* '):
                cdf_lines.append(f"  - {line.strip()[2:]}")
            # Bold/italic (remove markdown, keep plain text)
            elif '**' in line:
                line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)  # Remove bold markers
                cdf_lines.append(line)
            elif '*' in line and not line.strip().startswith('*'):
                line = re.sub(r'\*(.+?)\*', r'\1', line)  # Remove italic markers
                cdf_lines.append(line)
            # Links
            elif '[' in line and '](' in line:
                line = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1 → \2', line)
                cdf_lines.append(line)
            # Horizontal rules
            elif line.strip() == '---':
                cdf_lines.append("")
                cdf_lines.append("" * 81)
                cdf_lines.append("")
            # Empty lines
            elif not line.strip():
                cdf_lines.append("")
            # Regular text
            else:
                cdf_lines.append(line)
        
        return '\n'.join(cdf_lines)
    
    def convert_file(self, input_file: Path, output_file: Optional[Path] = None) -> Path:
        """Convert a markdown file to CDF format."""
        content = input_file.read_text(encoding='utf-8')
        
        metadata = {
            "title": input_file.stem,
            "created": datetime.now().isoformat(),
            "source": str(input_file)
        }
        
        cdf_content = self.markdown_to_cdf(content, metadata)
        
        if not output_file:
            output_file = input_file.parent / f"{input_file.stem}.cdf"
        
        output_file.write_text(cdf_content, encoding='utf-8')
        return output_file


if __name__ == "__main__":
    import sys
    
    converter = CDFConverter()
    
    if len(sys.argv) < 2:
        print("Usage: python cdf_converter.py <input.md> [output.cdf]")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    result = converter.convert_file(input_path, output_path)
    print(f" Converted to: {result}")

