#!/usr/bin/env python3
"""
Script to update consent forms with child names and roll numbers from Google Sheets.
"""

import gspread
import os
import glob
from pathlib import Path

def authenticate_google_sheets():
    """Authenticate with Google Sheets API using service account credentials."""
    try:
        gc = gspread.service_account(filename='google_secret.json')
        return gc
    except Exception as e:
        print(f"Error authenticating with Google Sheets: {e}")
        return None

def read_sheet_data(gc, sheet_id):
    """Read data from Google Sheet and return as list of dictionaries."""
    try:
        sheet = gc.open_by_key(sheet_id)
        worksheet = sheet.worksheet("School Data")  # Use the "School Data" sheet
        
        # Get all records (assumes first row contains headers)
        records = worksheet.get_all_records()
        print(f"Found {len(records)} records in the 'School Data' sheet")
        
        # Print column names for debugging
        if records:
            print("Available columns:", list(records[0].keys()))
        
        return records
    except Exception as e:
        print(f"Error reading sheet data: {e}")
        return []

def update_markdown_files(records, consent_forms_dir="consent_forms", output_dir="prefilled_consent_forms"):
    """Update markdown files with child names and roll numbers."""
    if not records:
        print("No records found to process")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Get all markdown files in the consent_forms directory
    markdown_files = glob.glob(os.path.join(consent_forms_dir, "*.md"))
    
    if not markdown_files:
        print(f"No markdown files found in {consent_forms_dir} directory")
        return
    
    print(f"Found {len(markdown_files)} markdown files to update")
    
    # Process each record
    successful_count = 0
    for i, record in enumerate(records):
        # Extract child name, roll number, and language from the record
        # Using the actual column names from the Google Sheet
        child_name = record.get('Student Name', '')
        roll_number = record.get('10th CBSE Roll Number', '')
        additional_language = record.get('Additional Language', '')
        
        if not child_name or not roll_number or not additional_language:
            print(f"Record {i+1}: Missing child name, roll number, or language, skipping...")
            continue
            
        # Map language names to file codes
        language_map = {
            'English': 'en',
            'Kannada': 'kn', 
            'Hindi': 'hi',
            'Tamil': 'ta',
            'Telugu': 'te',
            'Marati': 'mr',
            'Odia': 'or',
            'Assamese': 'as',
            'Gujarati': 'gu',
            'Malayalam': 'ml',
            'Bengali': 'bn'
        }
        
        language_code = language_map.get(additional_language)
        if not language_code:
            print(f"Record {i+1}: Unknown language '{additional_language}', skipping...")
            continue
            
        print(f"Processing record {i+1}: {child_name} (Roll: {roll_number}, Language: {additional_language} -> {language_code})")
        
        # Find the specific markdown file for this language
        language_file = None
        for md_file in markdown_files:
            if f"/{language_code}.md" in md_file:
                language_file = md_file
                break
        
        if not language_file:
            print(f"  No markdown file found for language: {additional_language}")
            continue
        
        try:
            # Read the original file
            with open(language_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace placeholders with actual values
            updated_content = content.replace("{{CHILD_NAME}}", child_name)
            updated_content = updated_content.replace("{{CHILD_10_ROLL_NUMBER}}", str(roll_number))
            
            # Create output filename with child's name
            base_name = os.path.basename(language_file)
            name_part = base_name.replace('.md', '')
            output_filename = f"{name_part}_{child_name.replace(' ', '_')}_prefilled.md"
            output_path = os.path.join(output_dir, output_filename)
            
            # Write the updated content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
                
            print(f"  Created: {output_path}")
            
        except Exception as e:
            print(f"  Error updating {language_file}: {e}")
        
        successful_count += 1
    
    print(f"Processed {successful_count} records successfully.")

def main():
    """Main function to orchestrate the process."""
    SHEET_ID = "1LyKfZoq5v9Evx0uHKQpFkjoIGjNVL_UbNkdNKegEbXc"
    
    print("Starting consent form update process...")
    
    # Authenticate with Google Sheets
    gc = authenticate_google_sheets()
    if not gc:
        print("Failed to authenticate with Google Sheets")
        return
    
    # Read data from the sheet
    records = read_sheet_data(gc, SHEET_ID)
    if not records:
        print("No data found in the sheet")
        return
    
    # Update markdown files
    update_markdown_files(records)
    
    print("Process completed!")

if __name__ == "__main__":
    main()