#!/usr/bin/env python3
# filepath: clean_markdown.py

import re
import os
import sys
import argparse
from pathlib import Path

def clean_markdown_file(file_path, dry_run=False):
    """Remove curly-braced elements from markdown files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Store original content for comparison
        original_content = content
        
        # Replace {{...}} expressions with empty strings
        # Pattern matches {{ followed by any characters (non-greedy) followed by }}
        content = re.sub(r'\{\{\s*([^}]*?)\s*\}\}', '', content)
        
        # Replace {%...%} template tags with empty strings
        content = re.sub(r'\{%[^%]*?%\}', '', content)
        
        # Replace broken links that might result from removing template variables
        # e.g., [network database](%7B%7B%20netdb%20%7D%7D) -> [network database]()
        content = re.sub(r'\]\(%7B%7B[^)]*?%7D%7D\)', ']()', content)
        
        # Handle other URL-encoded template variables
        content = re.sub(r'%7B%7B[^%]*?%7D%7D', '', content)
        
        # Fix escaped backslashes that might appear in code blocks
        content = re.sub(r'\\\\([`*_{}[\]()#+-.!])', r'\1', content)
        
        # Clean up any double spaces created by removals
        content = re.sub(r'  +', ' ', content)
        
        # Only write if content changed and not in dry run mode
        if content != original_content and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned: {file_path}")
            return True
        elif content != original_content and dry_run:
            print(f"Would clean: {file_path} (dry run)")
            return True
        else:
            print(f"No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Clean markdown files by removing template variables and expressions.")
    parser.add_argument("paths", nargs='+', help="Markdown files or directories to process")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without making changes")
    parser.add_argument("--recursive", "-r", action="store_true", help="Process directories recursively")
    args = parser.parse_args()
    
    files_processed = 0
    files_changed = 0
    
    for path in args.paths:
        path_obj = Path(path)
        if path_obj.is_file() and path_obj.suffix.lower() in ['.md', '.markdown']:
            files_processed += 1
            if clean_markdown_file(path_obj, args.dry_run):
                files_changed += 1
        elif path_obj.is_dir():
            if args.recursive:
                for md_file in path_obj.glob('**/*.md'):
                    files_processed += 1
                    if clean_markdown_file(md_file, args.dry_run):
                        files_changed += 1
                for md_file in path_obj.glob('**/*.markdown'):
                    files_processed += 1
                    if clean_markdown_file(md_file, args.dry_run):
                        files_changed += 1
            else:
                for md_file in path_obj.glob('*.md'):
                    files_processed += 1
                    if clean_markdown_file(md_file, args.dry_run):
                        files_changed += 1
                for md_file in path_obj.glob('*.markdown'):
                    files_processed += 1
                    if clean_markdown_file(md_file, args.dry_run):
                        files_changed += 1
        else:
            print(f"Skipping {path}: Not a markdown file or directory")
    
    print(f"\nSummary: Processed {files_processed} files, changed {files_changed} files")

if __name__ == "__main__":
    main()