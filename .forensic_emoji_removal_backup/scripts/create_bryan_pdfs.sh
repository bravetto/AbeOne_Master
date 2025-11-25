#!/bin/bash
# Create clean PDFs for Bryan's documents
# Uses pandoc to convert markdown to HTML, then provides instructions for PDF conversion

cd "$(dirname "$0")/.."

echo "📄 Creating PDF-ready documents for Bryan..."
echo ""

# Create styled HTML versions optimized for PDF printing
for file in BRYAN_SIMPLE_CHECKLIST.md BRYAN_EMAIL_FOLLOWUP.md; do
    if [ -f "$file" ]; then
        html_file="${file%.md}_PRINT.html"
        pdf_file="${file%.md}.pdf"
        
        echo "Processing: $file"
        
        # Create print-optimized HTML
        pandoc "$file" -t html5 -o "$html_file" --standalone \
            --metadata title="${file%.md}" \
            -V geometry:margin=1in \
            --css=<(cat <<'STYLE'
<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 20px;
    background: #fff;
}
h1 {
    color: #1f2937;
    border-bottom: 3px solid #a855f7;
    padding-bottom: 10px;
    margin-top: 0;
}
h2 {
    color: #374151;
    margin-top: 30px;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 5px;
}
h3 {
    color: #4b5563;
    margin-top: 25px;
}
ul, ol {
    margin: 15px 0;
    padding-left: 30px;
}
li {
    margin: 8px 0;
}
code {
    background: #f3f4f6;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Monaco', 'Courier New', monospace;
}
pre {
    background: #f9fafb;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    overflow-x: auto;
}
@media print {
    body { padding: 20px; }
    h1, h2, h3 { page-break-after: avoid; }
    @page { margin: 1in; }
}
</style>
STYLE
        ) 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo "  ✅ Created: $html_file"
            echo "  📄 To create PDF: Open $html_file in browser and Print → Save as PDF"
        else
            echo "  ⚠️  Could not create HTML, using basic conversion"
            pandoc "$file" -t html5 -o "$html_file" --standalone 2>/dev/null
        fi
    fi
done

echo ""
echo "✅ Done!"
echo ""
echo "📋 To create PDFs:"
echo "   1. Open the *_PRINT.html files in your browser"
echo "   2. Press Cmd+P (Mac) or Ctrl+P (Windows)"
echo "   3. Choose 'Save as PDF'"
echo "   4. Save as BRYAN_SIMPLE_CHECKLIST.pdf and BRYAN_EMAIL_FOLLOWUP.pdf"
echo ""
echo "Or use online converter: https://www.html2pdf.com/"

