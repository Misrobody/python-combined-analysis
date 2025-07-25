#!/bin/bash

# Abort on undefined vars, pipefail, but allow manual exit handling
set -u
set -o pipefail

# Colors
RED='\033[31m'
GREEN='\033[32m'
RESET='\033[0m'

# Usage check
if [ "$#" -ne 3 ]; then
  echo -e "${RED}Usage: $0 <data-dir> <outdir-name> <model-name>${RESET}"
  exit 1
fi

NAME="bin/$2"

MVIS_COMBINED_DIR="$NAME/mvis_combined"

# Clean and prepare directories
rm -rf "$NAME"/*
mkdir -p "$MVIS_COMBINED_DIR"
if [ $? -ne 0 ]; then
  echo -e "${RED}Directory creation failed. Exiting.${RESET}"
  exit 1
fi

echo -e "${GREEN}✔ Directories ready.${RESET}"

# Convert model to graph description
echo -e "${GREEN}▶ Running MVIS...${RESET}"
time tools/oceandsl-tools/bin/mvis \
  -i "$1" \
  -m add-nodes \
  -o "$MVIS_COMBINED_DIR" \
  -s all \
  -g dot-component
if [ $? -ne 0 ]; then
  echo -e "${RED}MVIS command failed. Exiting.${RESET}"
  exit 1
fi

# Visualize graph
echo "$MVIS_COMBINED_DIR/*.dot"
echo -e "${GREEN}▶ Visualizing graph...${RESET}"
time python3 tools/grouped-graph-visualizer/main.py -i "$MVIS_COMBINED_DIR/$3-component.dot" -o "$MVIS_COMBINED_DIR/output.svg" -m "tulip"
if [ $? -ne 0 ]; then
  echo -e "${RED}Visualization failed. Exiting.${RESET}"
  exit 1
fi

cd ../..

echo -e "${GREEN}Done! Output PDF ready at: $MVIS_COMBINED_DIR/output.pdf${RESET}"
