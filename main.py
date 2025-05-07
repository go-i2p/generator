#!/usr/bin/env python3
"""
Translation Processor

A script to process reStructuredText and HTML files by replacing translation tags
with content from .po files, handling image references, and optionally
converting to markdown.
"""

import argparse
import os
import re
import shutil
import sys
import urllib.parse
from typing import Dict, List, Optional, Tuple

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


def replace_template_vars(content: str) -> str:
    """
    Replace template variables like {{spec_url()}} with their values.
    
    Args:
        content: Content with template variables
        
    Returns:
        Content with template variables replaced
    """
    # Define base URLs for different types of links
    base_urls = {
        'spec_url': 'https://i2p.net/spec/',
        'proposal_url': 'https://i2p.net/spec/proposals/proposal',
        'i2p_url': 'https://i2p.net/',
        'site_url': 'https://i2p.net/',
        'get_url': 'https://i2p.net/'
    }
    
    # Handle {{spec_url("name")}} pattern
    def replace_spec_url(match):
        func_name = match.group(1)
        arg = match.group(2).strip('"\'') if match.group(2) else ""
        
        if func_name in base_urls:
            if func_name == 'proposal_url':
                return f"{base_urls[func_name]}{arg}.html"
            else:
                return f"{base_urls[func_name]}{arg}"
        
        # Handle special cases for other template functions
        if func_name == 'url_for':
            # Extract the filename from patterns like url_for('static', filename='images/...')
            filename_match = re.search(r'filename=[\'"](.*?)[\'"]', arg)
            if filename_match:
                return f"/_static/{filename_match.group(1)}"
        elif func_name == 'i2pconv':
            # For i2p domain conversions, return as is
            return arg
        
        return match.group(0)  # Return unchanged if not recognized
    
    # This pattern matches template functions like {{spec_url("ntcp2")}}
    template_pattern = r'{{([a-zA-Z_]+)\(([^}]*?)\)}}'
    processed_content = re.sub(template_pattern, replace_spec_url, content)
    
    # Handle other simple variable substitutions like {{ _('text') }}
    def replace_simple_var(match):
        var_name = match.group(1).strip()
        # For translation function calls like _('text'), return just the text
        if var_name.startswith("_('") and var_name.endswith("')"):
            return var_name[3:-2]  # Extract the text between quotes
        return match.group(0)  # Return unchanged if not recognized
    
    simple_var_pattern = r'{{([^}]+?)}}'
    return re.sub(simple_var_pattern, replace_simple_var, processed_content)


def replace_translations(content: str, translations: Dict[str, str]) -> str:
    """
    Replace translation tags in the content with translated text.
    
    Args:
        content: Content with translation tags
        translations: Dictionary of translations
        
    Returns:
        Content with translations applied
    """
    # First, handle simple {% trans %}...{% endtrans %} blocks
    def replace_simple_match(match):
        text = match.group(1).strip()
        return translations.get(text, text)
    
    # Match {% trans %}...{% endtrans %} patterns
    simple_pattern = r'{%\s*trans\s*%}(.*?){%\s*endtrans\s*%}'
    content = re.sub(simple_pattern, replace_simple_match, content, flags=re.DOTALL)
    
    # Now handle more complex translation blocks with arguments
    def replace_complex_match(match):
        # Extract parameters if present
        params_str = match.group(1) or ""
        text = match.group(2).strip()
        
        # Process parameters (for future use)
        params = {}
        if params_str:
            param_matches = re.finditer(r'(\w+)=["\'](.*?)["\']', params_str)
            for param_match in param_matches:
                key, value = param_match.groups()
                params[key] = value
                
                # Replace parameter references in the text
                if f"{{{key}}}" in text:
                    text = text.replace(f"{{{key}}}", value)
        
        # Apply translation
        translated = translations.get(text, text)
        
        # If there are parameter values, they need to be maintained in the translation
        for key, value in params.items():
            if f"{{{key}}}" in translated:
                translated = translated.replace(f"{{{key}}}", value)
        
        return translated
    
    # Match {% trans param1="value" -%}...{%- endtrans %} patterns with optional parameters
    complex_pattern = r'{%\s*trans\s*(.*?)-%}(.*?){%-\s*endtrans\s*%}'
    content = re.sub(complex_pattern, replace_complex_match, content, flags=re.DOTALL)
    
    return content


def process_rst_images(content: str, base_dir: str, assets_dir: str) -> str:
    """
    Process image references in RST content.
    
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


def process_html_images(content: str, base_dir: str, assets_dir: str) -> str:
    """
    Process image references in HTML content.
    
    Args:
        content: HTML content with image references
        base_dir: Base directory of the input file
        assets_dir: Directory to store images
        
    Returns:
        Content with updated image references
    """
    # Create assets directory if it doesn't exist
    images_dir = os.path.join(assets_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Find image references in HTML
    # This pattern matches <img src="..."> tags
    pattern = r'<img\s+[^>]*src=["\']((?!https?://)[^"\']+)["\'][^>]*>'
    
    def process_match(match):
        img_tag = match.group(0)
        path = match.group(1)
        
        # Skip URLs
        if path.startswith(('http://', 'https://')):
            return img_tag
        
        # Handle templated paths
        if "{{" in path:
            # Extract paths from template expressions like {{ url_for('static', filename='images/file.png') }}
            template_match = re.search(r'filename=[\'"](.*?)[\'"]', path)
            if template_match:
                path = f"/_static/{template_match.group(1)}"
            else:
                return img_tag  # Can't process this template
        
        # Remove leading /_static/ if present
        if path.startswith('/_static/'):
            path = path[9:]  # Remove /_static/ prefix
        
        # Handle relative paths
        if not os.path.isabs(path):
            full_old_path = os.path.join(base_dir, path)
            if not os.path.exists(full_old_path):
                # Try looking in static directory
                full_old_path = os.path.join(base_dir, 'static', path)
        else:
            full_old_path = path
        
        # Extract filename from path
        filename = os.path.basename(path)
        new_rel_path = os.path.join("images", filename)
        new_full_path = os.path.join(assets_dir, new_rel_path)
        
        # Copy the image if it exists
        if os.path.exists(full_old_path):
            try:
                shutil.copy2(full_old_path, new_full_path)
                print(f"Copied image: {full_old_path} -> {new_full_path}")
            except Exception as e:
                print(f"Error copying image {full_old_path}: {e}", file=sys.stderr)
                return img_tag  # Return original if error
        else:
            print(f"Warning: Image file not found: {full_old_path}", file=sys.stderr)
            return img_tag  # Return original if not found
        
        # Return the updated img tag with new path
        return img_tag.replace(match.group(1), f"images/{filename}")
    
    return re.sub(pattern, process_match, content)


def clean_markdown_output(markdown: str) -> str:
    """
    Clean up markdown output by handling URL-encoded template variables.
    
    Args:
        markdown: Markdown content with possible URL-encoded templates
        
    Returns:
        Cleaned markdown content
    """
    # Replace URL-encoded template variables
    def replace_encoded_templates(match):
        # Decode the URL-encoded string
        encoded_text = match.group(0)
        decoded_text = urllib.parse.unquote(encoded_text)
        
        # Extract values from template expressions like {{ url_for('static', filename='images/file.png') }}
        if decoded_text.startswith('{{') and decoded_text.endswith('}}'):
            template_content = decoded_text.strip('{}').strip()
            
            # Handle url_for template function
            if 'url_for' in template_content and 'filename=' in template_content:
                filename_match = re.search(r'filename=[\'"](.*?)[\'"]', template_content)
                if filename_match:
                    return filename_match.group(1)
            
            # Return empty string for other template functions
            return ''
        
        return encoded_text
    
    # Find URL-encoded sequences that might be template variables
    encoded_pattern = r'%7B%7B.*?%7D%7D'
    markdown = re.sub(encoded_pattern, replace_encoded_templates, markdown)
    
    # Clean up any broken image links that might have resulted from template replacements
    # Change ![text](broken_link) to ![text](images/filename.ext) when possible
    def fix_image_links(match):
        alt_text = match.group(1)
        link = match.group(2)
        
        # If link is empty or looks like a broken template
        if not link or link.startswith('%7B') or link.startswith('{{'):
            # Try to extract image filename from alt text or use a placeholder
            filename = alt_text.replace(' ', '-').lower()
            if filename:
                return f"![{alt_text}](images/{filename}.png)"
        
        return match.group(0)  # Return unchanged
    
    # Fix image links
    image_pattern = r'!\[(.*?)\]\((.*?)\)'
    markdown = re.sub(image_pattern, fix_image_links, markdown)
    
    return markdown


def convert_to_markdown(content: str, is_rst: bool = True) -> str:
    """
    Convert content to Markdown.
    
    Args:
        content: Content to convert
        is_rst: Whether the content is RST (True) or HTML (False)
        
    Returns:
        Markdown content
    """
    if not PANDOC_AVAILABLE:
        print("Warning: pypandoc not available. Conversion to Markdown skipped.", file=sys.stderr)
        return content
    
    try:
        if is_rst:
            if not DOCUTILS_AVAILABLE:
                print("Warning: docutils not available. RST to HTML conversion skipped.", file=sys.stderr)
                return content
            
            # Convert RST to HTML
            html = docutils.core.publish_string(
                source=content,
                writer_name='html',
                settings_overrides={'output_encoding': 'unicode'}
            )
            # Convert HTML to Markdown
            markdown = pypandoc.convert_text(html, 'md', format='html')
        else:
            # Convert HTML directly to Markdown
            markdown = pypandoc.convert_text(content, 'md', format='html')
        
        # Post-process markdown to clean up URL-encoded template variables
        markdown = clean_markdown_output(markdown)
        
        return markdown
    except Exception as e:
        print(f"Error converting to markdown: {e}", file=sys.stderr)
        return content


def is_draft(file_path: str) -> bool:
    """
    Check if a file is a draft based on its name.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is a draft, False otherwise
    """
    return '.draft.' in file_path.lower()


def process_file(
    input_path: str,
    po_file_path: str,
    output_path: Optional[str] = None,
    to_markdown: bool = False,
    assets_dir: str = "./assets"
) -> Tuple[bool, str]:
    """
    Process a file by replacing translations and handling images.
    
    Args:
        input_path: Path to input file (RST or HTML)
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
    
    # Determine file type
    is_rst = input_path.lower().endswith('.rst')
    is_html = input_path.lower().endswith(('.html', '.htm'))
    
    if not (is_rst or is_html):
        print(f"Error: Unsupported file type: {input_path}. Only .rst, .html, and .htm files are supported.", 
              file=sys.stderr)
        return False, ""
    
    # Determine output path if not specified
    if not output_path:
        base, ext = os.path.splitext(input_path)
        # Handle .draft.rst/.draft.html case
        if '.draft.' in base.lower():
            base = base.replace('.draft', '')
        
        # Set extension based on conversion type
        if to_markdown:
            out_ext = '.md'
        else:
            out_ext = ext
            
        output_path = f"{base}.translated{out_ext}"
    
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
        
        # Replace template variables
        content = replace_template_vars(content)
        
        # Replace translations
        content = replace_translations(content, translations)
        
        # Process images based on file type
        base_dir = os.path.dirname(os.path.abspath(input_path))
        if is_rst:
            content = process_rst_images(content, base_dir, assets_dir)
        elif is_html:
            content = process_html_images(content, base_dir, assets_dir)
        
        # Convert to markdown if requested
        if to_markdown:
            content = convert_to_markdown(content, is_rst=is_rst)
        
        # Create directory for output file if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Write output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully processed {input_path} -> {output_path}")
        return True, output_path
    
    except Exception as e:
        print(f"Error processing {input_path}: {e}", file=sys.stderr)
        return False, ""


def find_files(directory: str, include_drafts: bool = False) -> List[str]:
    """
    Find all RST and HTML files in a directory recursively.
    
    Args:
        directory: Directory to search
        include_drafts: Whether to include draft files
        
    Returns:
        List of file paths
    """
    result_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.rst', '.html', '.htm')):
                # Skip draft files if not included
                if not include_drafts and '.draft.' in file.lower():
                    continue
                result_files.append(os.path.join(root, file))
    return result_files


def process_directory(
    input_dir: str,
    po_file_path: str,
    output_dir: Optional[str] = None,
    to_markdown: bool = False,
    assets_dir: str = "./assets",
    include_drafts: bool = False
) -> bool:
    """
    Process all RST and HTML files in a directory.
    
    Args:
        input_dir: Directory containing files
        po_file_path: Path to .po file with translations
        output_dir: Directory to write output files (default: add .translated suffix)
        to_markdown: Whether to convert to markdown
        assets_dir: Directory to store assets
        include_drafts: Whether to include draft files
        
    Returns:
        True if all files were processed successfully, False otherwise
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory does not exist: {input_dir}", file=sys.stderr)
        return False
    
    # Find all RST and HTML files in the directory
    input_files = find_files(input_dir, include_drafts)
    if not input_files:
        print(f"No RST or HTML files found in {input_dir}", file=sys.stderr)
        return False
    
    success = True
    for input_file in input_files:
        # Determine output path based on relative path from input_dir
        rel_path = os.path.relpath(input_file, input_dir)
        if output_dir:
            out_path = os.path.join(output_dir, rel_path)
            # Adjust extension if converting to markdown
            if to_markdown:
                out_path = os.path.splitext(out_path)[0] + '.md'
            # Remove .draft from path if present
            if '.draft.' in out_path:
                out_path = out_path.replace('.draft', '')
        else:
            out_path = None
        
        # Process the file
        file_success, _ = process_file(
            input_file,
            po_file_path,
            out_path,
            to_markdown,
            assets_dir
        )
        
        if not file_success:
            success = False
    
    return success


def main():
    """Parse arguments and run the script."""
    # Fix for locale/gettext issues by forcing English locale
    import locale
    import os
    # Force 'C' locale to avoid gettext issues
    os.environ['LC_ALL'] = 'C'
    locale.setlocale(locale.LC_ALL, 'C')
    
    parser = argparse.ArgumentParser(
        description='Process RST and HTML files by replacing translations and handling images'
    )
    parser.add_argument('input_path', help='Path to input file or directory')
    parser.add_argument('po_file_path', help='Path to .po file with translations')
    parser.add_argument('-o', '--output-path', help='Path to write output file or directory')
    parser.add_argument('--to-markdown', action='store_true', help='Convert output to markdown')
    parser.add_argument('--assets-dir', default='./assets', help='Directory to store assets (default: ./assets)')
    parser.add_argument('--include-drafts', action='store_true', help='Process draft files (ending in .draft.rst or .draft.html)')
    parser.add_argument('--recursive', action='store_true', help='Process directories recursively')
    
    args = parser.parse_args()
    
    if args.to_markdown and not PANDOC_AVAILABLE:
        print("Warning: Markdown conversion requires pypandoc package.", file=sys.stderr)
        print("Install it with: pip install pypandoc", file=sys.stderr)
    
    # Check if input path is a directory
    if os.path.isdir(args.input_path):
        if args.recursive:
            success = process_directory(
                args.input_path,
                args.po_file_path,
                args.output_path,
                args.to_markdown,
                args.assets_dir,
                args.include_drafts
            )
        else:
            print("Error: Input path is a directory. Use --recursive to process it.", file=sys.stderr)
            success = False
    else:
        # Process a single file
        success, _ = process_file(
            args.input_path,
            args.po_file_path,
            args.output_path,
            args.to_markdown,
            args.assets_dir
        )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()