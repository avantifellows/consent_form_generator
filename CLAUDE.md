# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based consent form generator for Avanti Fellows that integrates with Google Sheets to create personalized consent forms in multiple languages. The system reads student data from Google Sheets, generates prefilled consent forms using markdown templates, and converts them to PDFs.

## Key Commands

**Setup and Installation:**
```bash
uv sync                              # Install dependencies
```

**Main Workflow:**
```bash
uv run python update_consent_forms.py    # Generate prefilled forms from Google Sheets
uv run python generate_pdfs.py          # Convert markdown forms to PDFs
uv run python download_translations.py  # Download latest translations from Google Docs
```

**Development Commands:**
```bash
python -m pip install -e .         # Install in development mode
python update_consent_forms.py     # Run directly with system Python
```

## Architecture

**Core Components:**
- `update_consent_forms.py`: Main script that fetches student data from Google Sheets and generates personalized consent forms
- `generate_pdfs.py`: Converts markdown files to styled PDFs using weasyprint
- `download_translations.py`: Downloads translated consent forms from Google Docs
- `languages.json`: Configuration file mapping language codes to template files and source documents

**Data Flow:**
1. Google Sheets "School Data" worksheet contains student information
2. `update_consent_forms.py` reads sheet data and fills templates with student names/roll numbers
3. Personalized markdown files are generated in `prefilled_consent_forms/`
4. `generate_pdfs.py` converts markdown files to PDFs with professional styling
5. Final PDFs are saved in `consent_form_pdfs/`

**Directory Structure:**
- `consent_forms/`: Language-specific markdown templates (en.md, hi.md, kn.md, etc.)
- `prefilled_consent_forms/`: Generated personalized forms (gitignored)
- `consent_form_pdfs/`: Final PDF outputs (gitignored)
- `google_secret.json`: Google service account credentials (gitignored)

## Configuration Details

**Google Sheets Integration:**
- Hard-coded sheet ID: `1LyKfZoq5v9Evx0uHKQpFkjoIGjNVL_UbNkdNKegEbXc`
- Expected worksheet name: "School Data"
- Required columns: "Student Name", "10th CBSE Roll Number", "Additional Language"

**Language Support:**
The system supports 11 languages with specific mappings:
- English (en), Hindi (hi), Kannada (kn), Tamil (ta), Telugu (te)
- Marathi (mr), Odia (or), Assamese (as), Gujarati (gu), Malayalam (ml), Bengali (bn)

**Template System:**
- Templates use `{{CHILD_NAME}}` and `{{CHILD_10_ROLL_NUMBER}}` as placeholders
- Files are named using pattern: `{language_code}_{student_name}_prefilled.md`
- PDF generation includes professional styling with Arial font, centered headers, and proper margins

## Dependencies

- `gspread`: Google Sheets API integration
- `weasyprint`: HTML to PDF conversion with CSS styling
- `markdown`: Markdown to HTML conversion with table/code support
- `requests`: HTTP client for downloading Google Docs translations

## Security Notes

- `google_secret.json` contains sensitive service account credentials
- Student data in `prefilled_consent_forms/` and `consent_form_pdfs/` contains PII
- All sensitive files are gitignored to prevent accidental commits
- The system processes real student data for consent form generation

## Data Processing Logic

- Only processes students with populated "Additional Language" fields
- Skips records missing required fields (name, roll number, language)
- PDF generation skips existing files to avoid overwriting
- Error handling includes detailed logging for debugging