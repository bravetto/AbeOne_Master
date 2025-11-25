#!/usr/bin/env python3
"""
Generate PDFs for Bryan's update documents
Converts simplified markdown to clean PDFs
"""

import os
import sys
from pathlib import Path

def create_html_from_markdown(md_file, html_file):
    """Convert markdown to HTML for PDF conversion."""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple markdown to HTML conversion
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Path(md_file).stem}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #fff;
        }}
        h1 {{
            color: #1f2937;
            border-bottom: 3px solid #a855f7;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            color: #374151;
            margin-top: 30px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #4b5563;
            margin-top: 25px;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        code {{
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background: #f9fafb;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #a855f7;
            padding-left: 20px;
            margin: 20px 0;
            color: #6b7280;
            font-style: italic;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #e5e7eb;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #f9fafb;
            font-weight: 600;
        }}
        .checklist {{
            background: #fef3c7;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #f59e0b;
            margin: 20px 0;
        }}
        .critical {{
            background: #fee2e2;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #ef4444;
            margin: 20px 0;
        }}
        .important {{
            background: #fef3c7;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #f59e0b;
            margin: 20px 0;
        }}
        .optional {{
            background: #f0fdf4;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #22c55e;
            margin: 20px 0;
        }}
        @media print {{
            body {{
                padding: 20px;
            }}
            h1, h2, h3 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
{markdown_to_html(content)}
</body>
</html>
"""
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f" Created HTML: {html_file}")

def markdown_to_html(md_content):
    """Simple markdown to HTML converter."""
    
    html = md_content
    
    # Headers
    html = html.replace('### ', '<h3>').replace('## ', '<h2>').replace('# ', '<h1>')
    html = html.replace('\n### ', '\n</h3>\n<h3>').replace('\n## ', '\n</h2>\n<h2>').replace('\n# ', '\n</h1>\n<h1>')
    
    # Bold
    html = html.replace('**', '<strong>').replace('**', '</strong>')
    
    # Code blocks
    import re
    html = re.sub(r'```([^`]+)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Lists
    lines = html.split('\n')
    in_list = False
    result = []
    
    for line in lines:
        if line.strip().startswith('- [ ]') or line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            line = line.replace('- [ ]', '<li>').replace('- ', '<li>')
            result.append(line + '</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    
    if in_list:
        result.append('</ul>')
    
    html = '\n'.join(result)
    
    # Line breaks
    html = html.replace('\n\n', '</p><p>')
    html = '<p>' + html + '</p>'
    
    return html

def main():
    """Generate PDFs for Bryan's documents."""
    
    base_dir = Path(__file__).parent.parent
    docs = [
        'BRYAN_SIMPLE_CHECKLIST.md',
        'BRYAN_EMAIL_FOLLOWUP.md'
    ]
    
    print(" Generating PDFs for Bryan...")
    print()
    
    for doc in docs:
        md_path = base_dir / doc
        if not md_path.exists():
            print(f"  {doc} not found, skipping...")
            continue
        
        html_path = base_dir / doc.replace('.md', '.html')
        pdf_path = base_dir / doc.replace('.md', '.pdf')
        
        # Create HTML
        create_html_from_markdown(md_path, html_path)
        
        # Try to convert to PDF
        try:
            # Try pandoc
            import subprocess
            result = subprocess.run(
                ['pandoc', str(html_path), '-o', str(pdf_path), '--pdf-engine=wkhtmltopdf'],
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f" Created PDF: {pdf_path}")
            else:
                # Try weasyprint
                result = subprocess.run(
                    ['weasyprint', str(html_path), str(pdf_path)],
                    capture_output=True,
                    timeout=30
                )
                if result.returncode == 0:
                    print(f" Created PDF: {pdf_path}")
                else:
                    print(f"  Could not create PDF. HTML available: {html_path}")
                    print(f"   You can convert HTML to PDF using:")
                    print(f"   - Browser: Open {html_path} and Print to PDF")
                    print(f"   - Online: Use html2pdf.com or similar")
        except Exception as e:
            print(f"  PDF conversion failed: {e}")
            print(f"   HTML available: {html_path}")
            print(f"   You can convert HTML to PDF using:")
            print(f"   - Browser: Open {html_path} and Print to PDF")
            print(f"   - Online: Use html2pdf.com or similar")
    
    print()
    print(" Done! Check the generated files.")

if __name__ == '__main__':
    main()

