# Project TODOs: Google Drive Integration

## Architecture Overview

### Enhanced Data Flow
```
1. Google Sheets "School Data" → Read student data (name, roll, language, school, grade)
2. Generate personalized consent forms → prefilled_consent_forms/
3. Convert to PDFs → consent_form_pdfs/
4. Upload PDFs to Google Drive → DRIVE_FOLDER_ID/SCHOOL/GRADE/
5. Log missing school/grade data → missing_data.csv
```

### Google Drive Folder Structure
```
DRIVE_FOLDER_ID/
├── School A/
│   ├── 11/
│   │   ├── en_Student1_prefilled.pdf
│   │   └── hi_Student2_prefilled.pdf
│   └── 12/
│       └── kn_Student3_prefilled.pdf
└── School B/
    ├── 11/
    └── 12/
```

## Prerequisites (Your Tasks)

### 1. Google Service Account Setup
- [ ] Create/use existing Google service account
- [ ] Enable Google Drive API for the service account
- [ ] Download service account JSON credentials
- [ ] Grant the service account access to your target Google Drive folder
- [ ] Get the DRIVE_FOLDER_ID from the Google Drive URL

### 2. Google Sheets Structure
- [ ] Ensure your "School Data" sheet has columns: "School Name" and "Grade"
- [ ] Verify existing columns: "Student Name", "10th CBSE Roll Number", "Additional Language"

## Development Tasks (Implementation)

### High Priority
- [ ] **Research current Google Sheets data structure** - ✅ COMPLETED
- [ ] **Design Google Drive folder structure validation and creation logic** - ✅ COMPLETED
- [ ] **Create drive_integration.py module** with functions:
  - `authenticate_drive()`: Initialize Google Drive client
  - `find_or_create_folder()`: Check if folder exists, create if not
  - `upload_file_to_folder()`: Upload PDF to specific folder
  - `get_folder_structure()`: Navigate DRIVE_FOLDER_ID/SCHOOL/GRADE hierarchy

### Medium Priority
- [ ] **Implement missing data logging system**:
  - Create CSV logger for records missing school/grade data
  - Headers: timestamp, student_name, roll_number, language, missing_fields

- [ ] **Update update_consent_forms.py**:
  - Extract school and grade data from Google Sheets
  - Pass school/grade info to PDF generation process
  - Handle missing school/grade data gracefully

- [ ] **Modify generate_pdfs.py**:
  - Add Google Drive upload after successful PDF generation
  - Include school/grade folder navigation
  - Add error handling for upload failures

- [ ] **Create configuration system**:
  - Add DRIVE_FOLDER_ID to configuration
  - Environment variable support for sensitive data
  - Validation for required configuration values

- [ ] **Implement error handling and retry logic**:
  - Retry logic for Google Drive operations
  - Detailed logging for debugging
  - Graceful handling of API rate limits

### Low Priority
- [ ] **Add Google Drive API dependencies** to pyproject.toml
- [ ] **Update CLAUDE.md** with new architecture and Google Drive integration details

## Expected New Commands

```bash
# Setup (after getting service account credentials)
uv run python setup_drive_access.py    # Validate Drive access and folder structure

# Enhanced workflow
uv run python update_consent_forms.py  # Now extracts school/grade data
uv run python generate_pdfs.py         # Now uploads to Google Drive
uv run python validate_uploads.py      # Verify uploaded files

# Utilities
uv run python check_missing_data.py    # Review missing_data.csv
uv run python cleanup_drive.py         # Remove test files from Drive
```

## Configuration Requirements

### New Files Needed
- **drive_config.json**: Configuration file with:
  - DRIVE_FOLDER_ID
  - Retry settings
  - Upload preferences
- **missing_data.csv**: Log file for records with missing school/grade data

### Environment Variables
- For sensitive configuration that shouldn't be in version control

## New Components

### drive_integration.py
Core Google Drive operations module with functions for:
- Authentication with Google Drive API
- Folder creation and navigation
- File upload with error handling
- Folder structure validation

### Enhanced Error Handling
- Retry logic for API operations
- Comprehensive logging
- Missing data tracking
- Upload failure recovery

## Implementation Notes

- Maintain existing workflow compatibility
- Add robust error handling and logging
- Ensure data privacy and security
- Validate all folder operations before file uploads
- Handle API rate limits gracefully

## Testing Strategy

1. **Unit Tests**: Test individual functions in drive_integration.py
2. **Integration Tests**: Test full workflow with test data
3. **Manual Testing**: Verify folder creation and file uploads
4. **Data Validation**: Ensure missing data logging works correctly

## Ready to Implement

When ready to proceed, tasks can be implemented in the following order:
1. Add Google Drive API dependencies
2. Create drive_integration.py module
3. Implement missing data logging
4. Update existing scripts with new functionality
5. Add configuration system
6. Implement error handling and retry logic
7. Update documentation