#!/usr/bin/env sh

#outdir is processed/lang/path to output file
outdir="processed/$LANGUAGE/"$(dirname $1)
# $1 is the input file
input=$1
output=$(basename $1).md
mkdir -p "$outdir"
if [ ! -d "$outdir/_static" ]; then
    cp -r static "processed/_static"
fi
echo python3 "$main" --to-markdown --assets-dir static/ -o "$outdir/$output" "$input" "translations/$LANGUAGE/LC_MESSAGES/$posource"
python3 "$main" --to-markdown --assets-dir static/ -o "$outdir/$output" "$input" "translations/$LANGUAGE/LC_MESSAGES/$posource" 2>> err.$LANGUAGE.log 1>> log.$LANGUAGE.log
python3 clean_markdown.py "$outdir/$output"