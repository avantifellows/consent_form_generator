# Consent Form Generator

A Python tool to generate personalized consent forms from Google Sheets data and convert them to PDFs.

## Features

- 📊 **Google Sheets Integration**: Read student data from Google Sheets
- 🌐 **Multi-language Support**: Generate forms in 11 languages (English, Hindi, Kannada, Tamil, Telugu, Marathi, Odia, Assamese, Gujarati, Malayalam, Bengali)
- 📝 **Template System**: Markdown-based consent form templates with placeholders
- 🎯 **Smart Processing**: Only processes students with specified language preferences
- 📄 **PDF Generation**: Convert filled forms to professional PDFs
- ♻️ **Efficient**: Skips already generated files to avoid duplication

## Setup

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd consent_form_generator
```

2. Install dependencies:
```bash
uv sync
```

3. Add your Google Service Account credentials:
   - Place your `google_secret.json` file in the project root
   - Ensure your service account has access to the Google Sheet

## Usage

### 1. Generate Prefilled Consent Forms

```bash
uv run python update_consent_forms.py
```

This script:
- Reads student data from the "School Data" sheet
- Processes students with populated "Additional Language" fields
- Generates personalized markdown forms in `prefilled_consent_forms/`

### 2. Generate PDFs

```bash
uv run python generate_pdfs.py
```

This script:
- Converts all markdown files in `prefilled_consent_forms/` to PDF
- Saves PDFs to `consent_form_pdfs/`
- Skips already existing PDFs

## File Structure

```
consent_form_generator/
├── consent_forms/          # Template markdown files
│   ├── en.md               # English template
│   ├── hi.md               # Hindi template
│   └── ...                 # Other language templates
├── prefilled_consent_forms/ # Generated personalized forms (gitignored)
├── consent_form_pdfs/      # Generated PDF files (gitignored)
├── update_consent_forms.py # Main generation script
├── generate_pdfs.py        # PDF conversion script
├── google_secret.json     # Service account credentials (gitignored)
└── pyproject.toml          # Project dependencies
```

## Configuration

### Google Sheet Structure

The script expects a sheet named "School Data" with these columns:
- `Student Name`: Full name of the student
- `10th CBSE Roll Number`: Student's board roll number
- `Additional Language`: Language preference (English, Hindi, Kannada, etc.)

### Adding New Languages

1. Create a new template file in `consent_forms/` (e.g., `ur.md` for Urdu)
2. Add the language mapping in `update_consent_forms.py`:
   ```python
   language_map = {
       # ... existing mappings
       'Urdu': 'ur',
   }
   ```

### Template Placeholders

Use these placeholders in your markdown templates:
- `{{CHILD_NAME}}`: Replaced with student's name
- `{{CHILD_10_ROLL_NUMBER}}`: Replaced with student's roll number

## Security

⚠️ **Important**: Never commit sensitive files to version control:
- `google_secret.json` contains service account credentials
- `prefilled_consent_forms/` contains student personal information
- These are automatically excluded via `.gitignore`

## Dependencies

- `gspread`: Google Sheets API client
- `markdown`: Markdown to HTML conversion
- `weasyprint`: HTML to PDF conversion
- `requests`: HTTP client for API calls

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]