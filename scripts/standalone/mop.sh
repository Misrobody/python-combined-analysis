#!/bin/bash

set -u
set -o pipefail

# Colors
RED='\033[31m'
GREEN='\033[32m'
RESET='\033[0m'

# Usage check
if [ "$#" -ne 3 ]; then
  echo -e "${RED}Usage: $0 <indir1> <indir2> <outdir>${RESET}"
  exit 1
fi

INDIR1="bin/$1"
INDIR2="bin/$2"
OUTDIR="bin/$3"

# Create output directory
mkdir -p "$OUTDIR"
if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to create output directory: $OUTDIR${RESET}"
  exit 1
fi

# Run MOP
echo -e "${GREEN}▶ Merging models...${RESET}"
tools/oceandsl-tools/bin/mop \
  -i "$INDIR1" "$INDIR2" \
  -o "$OUTDIR" \
  -e "mop" \
  merge
if [ $? -ne 0 ]; then
  echo -e "${RED}MOP command failed. Exiting.${RESET}"
  exit 1
fi

echo -e "${GREEN}MOP merge completed successfully! Output in: $OUTDIR${RESET}"
