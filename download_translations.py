#!/usr/bin/env python3

import json
import requests
import os
from urllib.parse import urlparse

def download_google_doc_as_markdown(doc_url):
    """Download a Google Doc as markdown"""
    if not doc_url:
        return None
    
    # Convert Google Docs URL to export URL
    if '/edit' in doc_url:
        export_url = doc_url.replace('/edit', '/export?format=md')
    else:
        export_url = doc_url + '/export?format=md'
    
    try:
        response = requests.get(export_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {doc_url}: {e}")
        return None

def main():
    # Read the languages JSON file
    with open('languages.json', 'r') as f:
        languages = json.load(f)
    
    # Create markdown files directory if it doesn't exist
    os.makedirs('markdown', exist_ok=True)
    
    for lang_data in languages:
        lang_code = lang_data['lang']
        lang_name = lang_data['lang_name']
        source_link = lang_data['source_link']
        
        print(f"Processing {lang_name} ({lang_code})...")
        
        if not source_link:
            print(f"  No source link found for {lang_name}, skipping...")
            continue
        
        # Download markdown content
        markdown_content = download_google_doc_as_markdown(source_link)
        
        if markdown_content:
            # Save to markdown file
            output_file = f"markdown/{lang_code}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"  Saved {output_file}")
        else:
            print(f"  Failed to download content for {lang_name}")

if __name__ == "__main__":
    main()