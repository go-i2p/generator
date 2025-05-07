#!/bin/sh

# Usage function for help
usage() {
    cat << EOF
Usage: $(basename "$0") [directory] [output.md]
Generate a markdown-formatted directory listing.

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

# Write header to the markdown file
{
    echo "# Directory Listing: $(cd "$target_dir" && pwd)"
    echo "Generated on: $(date)"
    echo
} >> "$output_file"

# Function to calculate the depth of a path
get_depth() {
    printf "%s" "$1" | tr -c -d '/' | wc -c
}

# Main function to generate the listing
generate_listing() {
    # Use find to get all files and directories, sort them
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
        
        # Generate the markdown line
        if [ -d "$item" ]; then
            # Directory: add trailing slash and make it bold
            echo "${indent}- **${base_name}/**" >> "$output_file"
        else
            # Regular file
            echo "${indent}- ${base_name}" >> "$output_file"
        fi
    done
}

# Generate the listing
generate_listing

echo "Directory listing has been saved to: $output_file"