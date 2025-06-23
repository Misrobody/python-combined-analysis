#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: command <indir> <outdir>"
    exit 1
fi

mkdir "bin/$2"

# make the graph
distrib/oceandsl-tools/bin/mvis \
 -i "bin/$1" \
 -m add-nodes \
 -o "bin/$2" \
 -s all \
 -g dot-component \
 -c num-of-calls op-coupling module-coupling

# convert the graph
cd "bin/$2"
dot -T pdf *.dot -o output.pdf
cd ../..

# -c (allen), num-of-calls, op-coupling, module-coupling
# -s all      all-color:[label,...]:[label,...]         diff:[label,...]:[label,...]      subtract:[label,...]    intersect:[label,...]:[label,...]