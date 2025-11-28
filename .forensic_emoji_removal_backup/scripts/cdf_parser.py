#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CDF Parser - Convert CDF back to other formats
Bidirectional conversion for maximum flexibility
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class CDFParser:
    """Parse CDF format and convert to other formats."""
    
    def __init__(self):
        self.metadata = {}
    
    def parse_cdf(self, cdf_content: str) -> Dict[str, Any]:
        """Parse CDF content into structured data."""
        lines = cdf_content.split('\n')
        
        # Parse header
        if lines[0].startswith('='):
            # Skip header
            start_idx = 3
        else:
            start_idx = 0
        
        # Parse metadata
        if 'METADATA:' in cdf_content:
            metadata_start = cdf_content.find('METADATA:')
            metadata_lines = cdf_content[metadata_start:].split('\n')[:10]
            for line in metadata_lines:
                if ':' in line and not line.startswith('METADATA'):
                    key, value = line.split(':', 1)
                    self.metadata[key.strip()] = value.strip()
        
        # Parse content
        content_lines = []
        in_section = False
        current_section = None
        
        for i, line in enumerate(lines[start_idx:], start=start_idx):
            # Skip empty lines at start
            if not line.strip() and not content_lines:
                continue
            
            # Section headers
            if line.strip().startswith('=') and len(line.strip()) > 10:
                if current_section:
                    content_lines.append(f"\n## {current_section}\n")
                # Extract section title from next line
                if i + 1 < len(lines):
                    title = lines[i + 1].strip()
                    if title and not title.startswith('='):
                        current_section = title
                        content_lines.append(f"# {title}\n")
                        continue
            
            # Subsection headers
            if line.strip().startswith('-') and len(line.strip()) > 10:
                if i + 1 < len(lines):
                    title = lines[i + 1].strip()
                    if title and not title.startswith('-'):
                        content_lines.append(f"## {title}\n")
                        continue
            
            # Regular content
            if line.strip() and not line.strip().startswith('=') and not line.strip().startswith('-'):
                # Convert lists
                if line.strip().startswith('- '):
                    content_lines.append(line)
                else:
                    content_lines.append(line)
        
        return {
            "metadata": self.metadata,
            "content": "\n".join(content_lines),
            "raw": cdf_content
        }
    
    def cdf_to_markdown(self, cdf_content: str) -> str:
        """Convert CDF to markdown."""
        parsed = self.parse_cdf(cdf_content)
        return parsed["content"]
    
    def cdf_to_html(self, cdf_content: str) -> str:
        """Convert CDF to HTML."""
        markdown = self.cdf_to_markdown(cdf_content)
        
        # Simple markdown to HTML conversion
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.metadata.get('title', 'CDF Document')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        h1 {{ border-bottom: 2px solid #333; padding-bottom: 10px; }}
        h2 {{ border-bottom: 1px solid #ccc; padding-bottom: 5px; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
"""
        
        # Convert markdown to HTML (simple)
        for line in markdown.split('\n'):
            if line.startswith('# '):
                html += f"<h1>{line[2:]}</h1>\n"
            elif line.startswith('## '):
                html += f"<h2>{line[3:]}</h2>\n"
            elif line.startswith('- '):
                html += f"<li>{line[2:]}</li>\n"
            elif line.strip():
                html += f"<p>{line}</p>\n"
            else:
                html += "<br>\n"
        
        html += """
</body>
</html>
"""
        return html
    
    def cdf_to_json(self, cdf_content: str) -> Dict[str, Any]:
        """Convert CDF to JSON."""
        parsed = self.parse_cdf(cdf_content)
        return {
            "cdf_version": "2.0",
            "metadata": parsed["metadata"],
            "content": parsed["content"],
            "genius_index": {
                "technical": 0.0,
                "creative": 0.0,
                "strategic": 0.0
            }
        }


if __name__ == "__main__":
    import sys
    import json
    
    parser = CDFParser()
    
    if len(sys.argv) < 3:
        print("Usage: python cdf_parser.py <input.cdf> <format> [output]")
        print("Formats: markdown, html, json")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    format_type = sys.argv[2].lower()
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    
    cdf_content = input_path.read_text(encoding='utf-8')
    
    if format_type == "markdown":
        result = parser.cdf_to_markdown(cdf_content)
        output_path = output_path or input_path.with_suffix('.md')
        output_path.write_text(result, encoding='utf-8')
        print(f"✅ Converted to markdown: {output_path}")
    
    elif format_type == "html":
        result = parser.cdf_to_html(cdf_content)
        output_path = output_path or input_path.with_suffix('.html')
        output_path.write_text(result, encoding='utf-8')
        print(f"✅ Converted to HTML: {output_path}")
    
    elif format_type == "json":
        result = parser.cdf_to_json(cdf_content)
        output_path = output_path or input_path.with_suffix('.json')
        output_path.write_text(json.dumps(result, indent=2), encoding='utf-8')
        print(f"✅ Converted to JSON: {output_path}")
    
    else:
        print(f"❌ Unknown format: {format_type}")
        sys.exit(1)

