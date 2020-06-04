#!/usr/bin/env bash

set -eu

ROOT=$(realpath $(dirname "$0"))
INSTALL_DIR="$ROOT/neural_sketch"

IN_FILE="$ROOT/examples/$1/SketchAdapt"

if [[ ! -f "$IN_FILE" ]]; then
	echo "SketchAdapt input $IN_FILE does not exist"
	exit 1
fi

# Now run the algorithm
cd $INSTALL_DIR
source env/bin/activate

# And get the pypy installation
export PATH=$PATH:pypy3.6-v7.3.1-linux64/bin

python3 eval/evaluate_deepcoder.py --precomputed_data_file $IN_FILE
