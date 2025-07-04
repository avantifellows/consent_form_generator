#!/usr/bin/env python3
"""
Script to generate PDFs from prefilled markdown consent forms.
Only generates PDFs that don't already exist.
"""

import os
import glob
import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def markdown_to_html(markdown_content):
    """Convert markdown content to HTML with proper styling."""
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['tables', 'fenced_code'])
    html_content = md.convert(markdown_content)
    
    # Wrap in a complete HTML document with styling
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Consent Form</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
                margin-top: 30px;
                margin-bottom: 15px;
            }}
            h1 {{
                text-align: center;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            p {{
                margin-bottom: 15px;
                text-align: justify;
            }}
            ul, ol {{
                margin-bottom: 15px;
                padding-left: 30px;
            }}
            li {{
                margin-bottom: 5px;
            }}
            strong {{
                color: #2c3e50;
            }}
            .signature-line {{
                border-bottom: 1px solid #333;
                display: inline-block;
                min-width: 200px;
                margin: 0 5px;
            }}
            @page {{
                margin: 2cm;
                size: A4;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    return html_template

def convert_markdown_to_pdf(markdown_file_path, pdf_file_path):
    """Convert a markdown file to PDF."""
    try:
        # Read markdown content
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert to HTML
        html_content = markdown_to_html(markdown_content)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(pdf_file_path)
        
        return True
    except Exception as e:
        print(f"Error converting {markdown_file_path} to PDF: {e}")
        return False

def generate_pdfs_from_markdown(input_dir="prefilled_consent_forms", output_dir="consent_form_pdfs"):
    """Generate PDFs from all markdown files in the input directory."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Find all markdown files in the input directory
    markdown_files = glob.glob(os.path.join(input_dir, "*.md"))
    
    if not markdown_files:
        print(f"No markdown files found in {input_dir}")
        return
    
    print(f"Found {len(markdown_files)} markdown files")
    
    generated_count = 0
    skipped_count = 0
    error_count = 0
    
    for md_file in markdown_files:
        # Generate PDF filename
        base_name = os.path.basename(md_file)
        pdf_name = base_name.replace('.md', '.pdf')
        pdf_path = os.path.join(output_dir, pdf_name)
        
        # Check if PDF already exists
        if os.path.exists(pdf_path):
            print(f"PDF already exists, skipping: {pdf_name}")
            skipped_count += 1
            continue
        
        print(f"Generating PDF: {pdf_name}")
        
        # Convert markdown to PDF
        if convert_markdown_to_pdf(md_file, pdf_path):
            print(f"  ✓ Successfully created: {pdf_path}")
            generated_count += 1
        else:
            print(f"  ✗ Failed to create: {pdf_path}")
            error_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"PDF Generation Summary:")
    print(f"  Generated: {generated_count}")
    print(f"  Skipped (already exists): {skipped_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total processed: {len(markdown_files)}")
    print(f"{'='*50}")

def main():
    """Main function to generate PDFs."""
    print("Starting PDF generation from prefilled consent forms...")
    generate_pdfs_from_markdown()
    print("PDF generation completed!")

if __name__ == "__main__":
    main()