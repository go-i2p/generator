#!/usr/bin/env python3
"""
RST Translation Processor

A script to process reStructuredText files by replacing translation tags
with content from .po files, handling image references, and optionally
converting to markdown.
"""

import argparse
import os
import re
import shutil
import sys
from typing import Dict, Optional, Tuple

import polib

# Optional dependency for markdown conversion
try:
    import docutils.core
    DOCUTILS_AVAILABLE = True
except ImportError:
    DOCUTILS_AVAILABLE = False

try:
    import pypandoc
    PANDOC_AVAILABLE = True
except ImportError:
    PANDOC_AVAILABLE = False


def load_translations(po_file_path: str) -> Dict[str, str]:
    """
    Load translations from a .po file into a dictionary.
    
    Args:
        po_file_path: Path to the .po file
        
    Returns:
        Dictionary mapping original text to translated text
    """
    try:
        po = polib.pofile(po_file_path)
        translations = {}
        for entry in po:
            if entry.msgstr and entry.msgid:  # Only include entries with translations
                translations[entry.msgid] = entry.msgstr
        return translations
    except Exception as e:
        print(f"Error loading translations from {po_file_path}: {e}", file=sys.stderr)
        return {}


def replace_translations(content: str, translations: Dict[str, str]) -> str:
    """
    Replace translation tags in the content with translated text.
    
    Args:
        content: RST content with translation tags
        translations: Dictionary of translations
        
    Returns:
        Content with translations applied
    """
    def replace_match(match):
        text = match.group(1).strip()
        return translations.get(text, text)
    
    # Match {% trans %}...{% endtrans %} patterns
    pattern = r'{%\s*trans\s*%}(.*?){%\s*endtrans\s*%}'
    return re.sub(pattern, replace_match, content, flags=re.DOTALL)


def process_images(content: str, base_dir: str, assets_dir: str) -> str:
    """
    Process image references in the content.
    
    Args:
        content: RST content with image references
        base_dir: Base directory of the input file
        assets_dir: Directory to store images
        
    Returns:
        Content with updated image references
    """
    # Create assets directory if it doesn't exist
    images_dir = os.path.join(assets_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Find image references
    # This pattern matches both basic image directives and figure directives
    pattern = r'\.\.\s+(image|figure)::\s+([\S]+)'
    
    def process_match(match):
        directive_type = match.group(1)  # image or figure
        old_path = match.group(2).strip()
        
        # Handle relative paths
        if not os.path.isabs(old_path):
            full_old_path = os.path.join(base_dir, old_path)
        else:
            full_old_path = old_path
        
        # Extract filename from path
        filename = os.path.basename(old_path)
        new_rel_path = os.path.join("images", filename)
        new_full_path = os.path.join(assets_dir, new_rel_path)
        
        # Copy the image if it exists
        if os.path.exists(full_old_path):
            try:
                shutil.copy2(full_old_path, new_full_path)
                print(f"Copied image: {full_old_path} -> {new_full_path}")
            except Exception as e:
                print(f"Error copying image {full_old_path}: {e}", file=sys.stderr)
        else:
            print(f"Warning: Image file not found: {full_old_path}", file=sys.stderr)
        
        # Return the updated directive
        return f".. {directive_type}:: {new_rel_path}"
    
    return re.sub(pattern, process_match, content)


def convert_to_markdown(rst_content: str) -> str:
    """
    Convert RST content to Markdown.
    
    Args:
        rst_content: RST content to convert
        
    Returns:
        Markdown content
    """
    if not DOCUTILS_AVAILABLE:
        print("Warning: docutils not available. RST to HTML conversion skipped.", file=sys.stderr)
        return rst_content
    
    if not PANDOC_AVAILABLE:
        print("Warning: pypandoc not available. HTML to Markdown conversion skipped.", file=sys.stderr)
        return rst_content
    
    try:
        # Convert RST to HTML
        html = docutils.core.publish_string(
            source=rst_content,
            writer_name='html',
            settings_overrides={'output_encoding': 'unicode'}
        )
        
        # Convert HTML to Markdown
        markdown = pypandoc.convert_text(html, 'md', format='html')
        return markdown
    except Exception as e:
        print(f"Error converting to markdown: {e}", file=sys.stderr)
        return rst_content


def process_rst_file(
    input_path: str,
    po_file_path: str,
    output_path: Optional[str] = None,
    to_markdown: bool = False,
    assets_dir: str = "./assets"
) -> Tuple[bool, str]:
    """
    Process an RST file by replacing translations and handling images.
    
    Args:
        input_path: Path to input RST file
        po_file_path: Path to .po file with translations
        output_path: Path to write output (default: add .translated suffix)
        to_markdown: Whether to convert to markdown
        assets_dir: Directory to store assets
        
    Returns:
        Tuple of (success: bool, output_path: str)
    """
    # Check that input files exist
    if not os.path.exists(input_path):
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        return False, ""
    
    if not os.path.exists(po_file_path):
        print(f"Error: PO file does not exist: {po_file_path}", file=sys.stderr)
        return False, ""
    
    # Determine output path if not specified
    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}.translated{'.md' if to_markdown else ext}"
    
    # Create assets directory
    os.makedirs(assets_dir, exist_ok=True)
    
    try:
        # Load translations
        translations = load_translations(po_file_path)
        if not translations:
            print("Warning: No translations found in the .po file", file=sys.stderr)
        
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace translations
        content = replace_translations(content, translations)
        
        # Process images
        base_dir = os.path.dirname(os.path.abspath(input_path))
        content = process_images(content, base_dir, assets_dir)
        
        # Convert to markdown if requested
        if to_markdown:
            content = convert_to_markdown(content)
        
        # Write output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully processed {input_path} -> {output_path}")
        return True, output_path
    
    except Exception as e:
        print(f"Error processing {input_path}: {e}", file=sys.stderr)
        return False, ""


def main():
    """Parse arguments and run the script."""
    parser = argparse.ArgumentParser(
        description='Process RST files by replacing translations and handling images'
    )
    parser.add_argument('input_path', help='Path to input RST file')
    parser.add_argument('po_file_path', help='Path to .po file with translations')
    parser.add_argument('-o', '--output-path', help='Path to write output file')
    parser.add_argument('--to-markdown', action='store_true', help='Convert output to markdown')
    parser.add_argument('--assets-dir', default='./assets', help='Directory to store assets (default: ./assets)')
    
    args = parser.parse_args()
    
    if args.to_markdown and not (DOCUTILS_AVAILABLE and PANDOC_AVAILABLE):
        print("Warning: Markdown conversion requires docutils and pypandoc packages.", file=sys.stderr)
        print("Install them with: pip install docutils pypandoc", file=sys.stderr)
    
    success, output_path = process_rst_file(
        args.input_path,
        args.po_file_path,
        args.output_path,
        args.to_markdown,
        args.assets_dir
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()