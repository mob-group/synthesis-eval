#!/bin/bash

ROOT=$(realpath $(dirname "$0"))
INSTALL_DIR="$ROOT/install"

IN_FILE="$ROOT/examples/$1/simpl"

if [ ! -f "$IN_FILE" ]; then
  echo "Simpl input $IN_FILE does not exist"
  exit 1
fi

"$INSTALL_DIR/bin/simpl" -input "$IN_FILE"
