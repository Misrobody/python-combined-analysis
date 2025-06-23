#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: command <outdir> <data>"
    exit 1
fi

mkdir "bin/$1"

./distrib/oceandsl-tools/bin/sar \
 -o "bin/$1" \
 -E "ARIELLE" \
 -g call \
 -i "data/$2" \
 -m module-mode \
 -l "toto"

# module-mode file-mode map-mode
# call dataflow both
# "data/sar/results/MITgcm-MLAdjust"