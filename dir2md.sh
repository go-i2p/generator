#!/bin/sh

# Usage function for help
usage() {
    cat << EOF
Usage: $(basename "$0") [directory] [output.md]
Generate a markdown-formatted directory listing with file links.

Arguments:
    directory   : Directory to scan (default: current directory)
    output.md   : Output markdown file (default: directory_listing.md)
EOF
    exit 1
}

# Set default values
target_dir="${1:-.}"
output_file="${2:-directory_listing.md}"

# Validate directory
if [ ! -d "$target_dir" ]; then
    echo "Error: Directory '$target_dir' does not exist." >&2
    usage
fi

# Create or truncate the output file
: > "$output_file"

# Get absolute paths
target_dir=$(cd "$target_dir" && pwd)
output_dir=$(cd "$(dirname "$output_file")" && pwd)
output_name=$(basename "$output_file")

# Write header to the markdown file
{
    echo "# Directory Listing: $target_dir"
    echo "Generated on: $(date)"
    echo
} >> "$output_file"

# Function to calculate the depth of a path
get_depth() {
    printf "%s" "$1" | tr -c -d '/' | wc -c
}

# Function to create a relative path between two absolute paths
make_relative_path() {
    # $1 is the path to the markdown file directory
    # $2 is the path to the target file
    
    # Start with both paths
    common_path="$1"
    target="$2"
    
    # Initialize relative path
    rel_path=""
    
    # Find the common prefix
    while [ "${target#$common_path/}" = "$target" ] && [ -n "$common_path" ]; do
        common_path="${common_path%/*}"
        rel_path="../$rel_path"
    done
    
    # If there's no common path left, we've gone up as far as we need to
    if [ -z "$common_path" ]; then
        rel_path="/$target"
    else
        # Remove the common prefix and prepend the relative path
        rel_path="${rel_path}${target#$common_path/}"
    fi
    
    printf "%s" "$rel_path"
}

# Main function to generate the listing
generate_listing() {
    find "$target_dir" -print | sort | while read -r item; do
        # Skip the target directory itself
        [ "$item" = "$target_dir" ] && continue
        
        # Calculate relative path and depth
        rel_path="${item#$target_dir/}"
        depth=$(get_depth "$rel_path")
        
        # Calculate indentation (2 spaces per level)
        indent=""
        i=0
        while [ $i -lt "$depth" ]; do
            indent="$indent  "
            i=$((i + 1))
        done
        
        # Get the basename of the item
        base_name=$(basename "$item")
        
        # Create relative link path from output file to target
        link_path=$(make_relative_path "$output_dir" "$item")
        
        # Generate the markdown line
        if [ -d "$item" ]; then
            # Directory: add trailing slash and make it bold
            echo "${indent}- **[${base_name}/](${link_path}/)**" >> "$output_file"
        else
            # Regular file: create a link
            echo "${indent}- [${base_name}](${link_path})" >> "$output_file"
        fi
    done
}

# Generate the listing
generate_listing

echo "Directory listing has been saved to: $output_file"