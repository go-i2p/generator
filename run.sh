#! /usr/bin/env sh

main=$(pwd)/main.py
LANGUAGE=ar
find blog -name '*.rst' -exec python3 "$main" --to-markdown --assets-dir static/ -o processed/{}.md {} "translations/$LANGUAGE/LC_MESSAGES/docs.po" \;