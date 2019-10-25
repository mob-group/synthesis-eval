#!/usr/bin/env bash

ROOT=$(realpath $(dirname "$0"))
INSTALL_DIR="$ROOT/install"

IN_PROPS="$ROOT/examples/$1/props"
IN_LIB="$ROOT/examples/$1/ref.so"

./compile-ref "$1"

if [ ! -f "$IN_PROPS" ]; then
  echo "Baseline input $IN_PROPS does not exist"
  exit 1
fi

if [ ! -f "$IN_LIB" ]; then
  echo "Baseline input $IN_LIB does not exist"
  exit 1
fi

"$INSTALL_DIR/bin/pldi" \
  -dump-control \
  -count \
  "$IN_PROPS" "$IN_LIB"
