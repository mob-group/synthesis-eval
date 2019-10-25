#!/usr/bin/env bash

ROOT=$(realpath $(dirname "$0"))
INSTALL_DIR="$ROOT/install"

IN_FILE="$ROOT/examples/$1/L2.json"

if [ ! -f "$IN_FILE" ]; then
  echo "L2 input $IN_FILE does not exist"
  exit 1
fi

"$INSTALL_DIR/bin/L2" synth -l      \
  "$INSTALL_DIR/share/L2/stdlib.ml" \
  -dd higher_order,input_ctx        \
  "$ROOT/examples/$1/L2.json"
