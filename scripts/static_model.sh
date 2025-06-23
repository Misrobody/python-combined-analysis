#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: command <input-dir> <mode> <out-name>"
    exit 1
fi

######################################

NAME="bin/$3-static-model-$2"

SAR_OUTPUT_DIR="$NAME/sar"
MVIS_OUTPUT_DIR="$NAME/mvis"

mkdir -p "$NAME"
mkdir -p "$SAR_OUTPUT_DIR"
mkdir -p "$MVIS_OUTPUT_DIR"

if [ $? -ne 0 ]; then
  echo "Directory Creation failed. Exiting."
  exit 1
fi

######################################

# make the architecture model
echo "make the architecture model"
./tools/oceandsl-tools/bin/sar \
 -o "$SAR_OUTPUT_DIR" \
 -E "pyparse" \
 -g "$2" \
 -i "$1" \
 -m module-mode \
 -l "static"

if [ $? -ne 0 ]; then
  echo "SAR command failed. Exiting."
  exit 1
fi

######################################

# tweak the model
echo "tweak the model"
python3 python/convert.py "bin/$1-sar/type-model.xmi"

if [ $? -ne 0 ]; then
  echo "Convert command failed. Exiting."
  exit 1
fi

######################################

# make the graph
echo "make the graph"
./tools/oceandsl-tools/bin/mvis \
 -i "$SAR_OUTPUT_DIR" \
 -m add-nodes \
 -o "$MVIS_OUTPUT_DIR" \
 -s all \
 -g dot-component \
 -c num-of-calls op-coupling module-coupling

if [ $? -ne 0 ]; then
  echo "MVIS command failed. Exiting."
  exit 1
fi

######################################

# convert the graph
echo "convert the graph"
cd "$MVIS_OUTPUT_DIR"
dot -T pdf *.dot -o output.pdf
cd ../..

if [ $? -ne 0 ]; then
  echo "DOT command failed. Exiting."
  exit 1
fi