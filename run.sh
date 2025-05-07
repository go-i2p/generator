#! /usr/bin/env sh

export main=$(pwd)/main.py
export cmd=$(pwd)/cmd.sh


export LANGUAGES="ar az ca cs da de el es es_AR et_EE fa fi fr gl he hu id it ja ko mg nb nl pl pt pt_BR ro ru sk sl sq sv tr uk zh zh_TW"
# produce translated files for all languages and all directories
for lang in $LANGUAGES; do
    export LANGUAGE=$lang
    export dir=pages
    export posource=docs.po
    export ext=html
    echo "Processing $lang in $dir for $ext"
    find "$dir" -name "*.$ext" -exec "$cmd" {} \;
done

for lang in $LANGUAGES; do
    export LANGUAGE=$lang
    export dir=pages
    export posource=blog.po
    export ext=rst
    echo "Processing $lang in $dir for $ext"
    find "$dir" -name "*.$ext" -exec "$cmd" {} \;
done
