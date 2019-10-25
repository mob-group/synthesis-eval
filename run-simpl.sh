#!/usr/bin/env bash

set -eu

if [[ $# -ne 1 ]]; then
	echo "Usage: $0 <test name>"
	echo "See examples folder for a list of the examples"
	exit 1
fi

ROOT=$(realpath $(dirname "$0"))
INSTALL_DIR="$ROOT/install"

IN_FILE="$ROOT/examples/$1/simpl"

if [ ! -f "$IN_FILE" ]; then
  echo "Simpl input $IN_FILE does not exist"
  exit 1
fi

"$INSTALL_DIR/bin/simpl" -input "$IN_FILE"
