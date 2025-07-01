#!/bin/bash

time python3 tools/pyparse/src/pyparse/pyparse.py \
 -i apps/UXsim/ \
 -o data/uxsim/pyparse \
 -m $1 -e -v

#time python3 tools/pyparse/src/pyparse/pyparse.py \
# -i apps/anytree \
# -o data/anytree/pyparse \
# -m $1 -e

#/home/dl/.local/lib/python3.10/site-packages/numpy/