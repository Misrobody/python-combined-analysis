#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: command <indir> <outdir>"
    exit 1
fi

mkdir "bin/$2"

# make the graph
tools/oceandsl-tools/bin/mvis \
 -i "bin/$1" \
 -m add-nodes \
 -o "bin/$2" \
 -s all \
 -g graphml dot-component dot-op
# -c (allen), num-of-calls, op-coupling, module-coupling
# -s all      all-color:[label,...]:[label,...]         diff:[label,...]:[label,...]      subtract:[label,...]    intersect:[label,...]:[label,...]