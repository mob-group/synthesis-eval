#!/usr/bin/env bash

ROOT=$(realpath $(dirname "$0"))

for example in $(ls "$ROOT/examples"); do
  if [ ! -d "$ROOT/examples/$example" ]; then
    continue
  fi

  IN_PROPS="$ROOT/examples/$example/props"
  IN_C="$ROOT/examples/$example/ref.c"

  if [ -f "$IN_PROPS" ]; then
    continue
  fi

  if [ ! -f "$IN_C" ]; then
    echo "No C implementation to copy: $IN_C"
    exit 1
  fi

  cp "$IN_C" "$IN_PROPS"
done
