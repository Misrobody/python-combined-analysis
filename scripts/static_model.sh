#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: command <outdir> <mode>"
    exit 1
fi

mkdir "bin/$1-sar"
mkdir "bin/$1"

./distrib/oceandsl-tools/bin/sar \
 -o "bin/$1-sar" \
 -E "pyparse" \
 -g $2 \
 -i "data/out" \
 -m module-mode \
 -l "static"

python3 convert.py "bin/$1-sar/type-model.xmi"

######################################

# make the graph
./distrib/oceandsl-tools/bin/mvis \
 -i "bin/$1-sar" \
 -m add-nodes \
 -o "bin/$1" \
 -s all \
 -g dot-component \
 -c num-of-calls op-coupling module-coupling

# convert the graph
cd "bin/$1"
dot -T pdf *.dot -o output.pdf
cd ../..