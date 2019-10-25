#!/bin/bash

set -eu
if [[ $# -ne 1 ]]; then
	echo "Usage $0 <test>"
	exit 1
fi

seed=50105

ROOT=$(realpath $(dirname "$0"))
INSTALL_DIR="$ROOT/install"

IN_FILE="$ROOT/examples/$1/makespeare"

if [ ! -f $IN_FILE ]; then
	echo "Makespeare input file $IN_FILE doesn't exist."
	exit 1
fi

$INSTALL_DIR/bin/makespeare $seed $IN_FILE 2.0 0.0 1.0 0.0 2000000 1
