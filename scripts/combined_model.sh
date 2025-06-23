#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: command <dar-data-dir> <sar-data-dir>"
    exit 1
fi

NAME="bin"

DAR_INPUT_DIR="$1"
SAR_INPUT_DIR="$2"

DAR_OUTPUT_DIR="$NAME/dar_model"
SAR_OUTPUT_DIR="$NAME/sar_model"
MOP_OUTPUT_DIR="$NAME/mop_model"
MVIS_COMBINED_DIR="$NAME/mvis_combined"

rm -rf "$NAME/*"

mkdir "$DAR_OUTPUT_DIR"
mkdir "$SAR_OUTPUT_DIR"
mkdir "$MOP_OUTPUT_DIR"
mkdir "$MVIS_COMBINED_DIR"

# Dynamic Achitecture Recovery #
tools/oceandsl-tools/bin/dar \
-l dynamic \
-c \
-o "$DAR_OUTPUT_DIR" \
-s java \
-m java-class-mode \
-E "" \
-i "$DAR_INPUT_DIR" \

# Static Architecture Recovery #
tools/oceandsl-tools/bin/sar \
 -l static \
 -o "$SAR_OUTPUT_DIR" \
 -m module-mode \
 -g both \
 -E "" \
 -i "$SAR_INPUT_DIR" \

# Model Conversion
python3 convert.py "$SAR_OUTPUT_DIR/type-model.xmi"

# Combined Model Operations #
tools/oceandsl-tools/bin/mop \
 -i $DAR_OUTPUT_DIR $SAR_OUTPUT_DIR \
 -o  "$MOP_OUTPUT_DIR" \
 -e "" \
 merge

# Model Visualisation and Statistics #
# make the graph
tools/oceandsl-tools/bin/mvis \
 -i "$MOP_OUTPUT_DIR" \
 -m add-nodes \
 -o "$MVIS_COMBINED_DIR" \
 -s all \
 -g dot-component \
 -c num-of-calls op-coupling module-coupling

# convert the graph
cd "$MVIS_COMBINED_DIR"
dot -T pdf *.dot -o output.pdf
cd ../..
