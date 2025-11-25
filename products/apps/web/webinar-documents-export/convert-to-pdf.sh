#!/bin/bash
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
        pandoc "$file" -o "$output" -f markdown -t pdf --pdf-engine=wkhtmltopdf 2>/dev/null || \
        pandoc "$file" -o "$output" -f markdown -t pdf 2>/dev/null || \
        echo "⚠️  Could not convert $file - use online converter or Word/Pages"
    fi
done

echo "Done!"
