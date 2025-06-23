#!/bin/bash

time python3 distrib/pyparse/src/pyparse/pyparse.py \
 -i distrib/UXsim \
 -o data/out \
 -m $1 -e

#/home/dl/.local/lib/python3.10/site-packages/numpy/