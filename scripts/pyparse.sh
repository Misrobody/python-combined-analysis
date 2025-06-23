#!/bin/bash

time python3 tools/pyparse/src/pyparse/pyparse.py \
 -i apps/anytree \
 -o data/out \
 -m $1 -e

#/home/dl/.local/lib/python3.10/site-packages/numpy/