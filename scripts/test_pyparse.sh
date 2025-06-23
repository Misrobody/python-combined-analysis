#!/bin/bash

time python3 tools/pyparse/src/pyparse/pyparse.py \
 -i distrib/UXsim/uxsim \
 -o data/out \
 -m $1 -e

time python3 tools/pyparse/src/pyparse/pyparse.py \
 -i distrib/anytree \
 -o data/out \
 -m $1 -e