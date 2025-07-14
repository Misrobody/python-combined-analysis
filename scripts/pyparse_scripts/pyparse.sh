#!/bin/bash

time python3 tools/pyparse/src/pyparse/pyparse.py \
 -i ~/OtktDSL-examples/apps/numpy \
 -o data/numpy/pyparse-newest \
 -m both -e -v

#time python3 tools/pyparse/src/pyparse/pyparse.py \
# -i apps/anytree \
# -o data/anytree/pyparse \
# -m $1 -e

#/home/dl/.local/lib/python3.10/site-packages/numpy/