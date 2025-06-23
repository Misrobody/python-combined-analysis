#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: command <outdir>"
    exit 1
fi

mkdir  "bin/$1"

distrib/oceandsl-tools/bin/mop \
 -i bin/new bin/dar_output \
 -o  "bin/$1" \
 -e anytree \
 merge