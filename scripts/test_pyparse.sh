#!/bin/bash

OUTDIR="bin/pyparse-test-output"
mkdir "$OUTDIR"

time python3 tools/pyparse/src/pyparse/pyparse.py \
 -i apps/UXsim/uxsim \
 -o "$OUTDIR" \
 -m $1 -e

time python3 tools/pyparse/src/pyparse/pyparse.py \
 -i apps/anytree \
 -o "$OUTDIR" \
 -m $1 -e