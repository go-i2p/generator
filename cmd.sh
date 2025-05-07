#!/usr/bin/env sh

#outdir is processed+path to output file
outdir=processed/$(dirname $1)
mkdir -p "$outdir"
# $1 is the input file
input=$1
output=$(basename $1 .rst).md
python3 "$main" --to-markdown --assets-dir static/ -o "$outdir/$output" "$input" "translations/$LANGUAGE/LC_MESSAGES/blog.po"