#! /usr/bin/env sh

export main=$(pwd)/main.py
export cmd=$(pwd)/cmd.sh
export LANGUAGE=ru
find blog -name '*.rst' -exec "$cmd" {} \;