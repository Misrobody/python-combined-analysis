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
  echo -e "${RED}Usage: $0 <input-dir> <mode> <out-name>${RESET}"
  exit 1
fi

INPUT_DIR="$1"
MODE="$2"
OUT_NAME="$3"

NAME="bin/${OUT_NAME}-static-model-${MODE}"
SAR_OUTPUT_DIR="$NAME/sar"
MVIS_OUTPUT_DIR="$NAME/mvis"

# Clean and prepare directories
rm -rf "$NAME"/*
mkdir -p "$SAR_OUTPUT_DIR" "$MVIS_OUTPUT_DIR"
if [ $? -ne 0 ]; then
  echo -e "${RED}Directory creation failed. Exiting.${RESET}"
  exit 1
fi

echo -e "${GREEN}✔ Directories ready.${RESET}"

# Run SAR
echo -e "${GREEN}▶ Running SAR...${RESET}"
time ./tools/oceandsl-tools/bin/sar \
  -o "$SAR_OUTPUT_DIR" \
  -E "pyparse" \
  -g "$MODE" \
  -i "$INPUT_DIR" \
  -m module-mode \
  -l "static"
if [ $? -ne 0 ]; then
  echo -e "${RED}SAR command failed. Exiting.${RESET}"
  exit 1
fi

# Convert model
echo -e "${GREEN}▶ Converting model...${RESET}"
time python3 python/convert.py "$SAR_OUTPUT_DIR/type-model.xmi"
if [ $? -ne 0 ]; then
  echo -e "${RED}Conversion failed. Exiting.${RESET}"
  exit 1
fi

# Visualize with MVIS
echo -e "${GREEN}▶ Running MVIS...${RESET}"
time ./tools/oceandsl-tools/bin/mvis \
  -i "$SAR_OUTPUT_DIR" \
  -m add-nodes \
  -o "$MVIS_OUTPUT_DIR" \
  -s all \
  -g dot-component \
  -c num-of-calls op-coupling module-coupling
if [ $? -ne 0 ]; then
  echo -e "${RED}MVIS command failed. Exiting.${RESET}"
  exit 1
fi

# Group graph
echo -e "${GREEN}▶ Grouping graph...${RESET}"
time python3 python/table.py "$MVIS_OUTPUT_DIR/sar-component.dot" "$MVIS_OUTPUT_DIR/output.dot"
if [ $? -ne 0 ]; then
  echo -e "${RED}Grouping failed. Exiting.${RESET}"
  exit 1
fi

# Convert .dot to PDF
echo -e "${GREEN}▶ Generating PDF from .dot files...${RESET}"
cd "$MVIS_OUTPUT_DIR"
time fdp -Tpdf -o output.pdf -v output.dot 
if [ $? -ne 0 ]; then
  echo -e "${RED}FDP conversion failed. Exiting.${RESET}"
  exit 1
fi
cd ../..

echo -e "${GREEN}Done! Output PDF ready at: $MVIS_OUTPUT_DIR/output.pdf${RESET}"
