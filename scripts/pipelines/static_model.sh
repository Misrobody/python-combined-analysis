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


# Group graph
echo -e "${GREEN}▶ Grouping graph...${RESET}"
time python3 python/dot_visualization/ClusteredDotGraph.py "$MVIS_OUTPUT_DIR/sar-component.dot" "$MVIS_OUTPUT_DIR/output.dot"
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
