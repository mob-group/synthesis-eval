#!/bin/bash

set -eu
if [[ $# -ne 1 ]]; then
	echo "Usage $0 <test>"
	exit 1
fi

source utils.sh

ROOT=$(realpath $(dirname "$0"))
INSTALL_DIR="$ROOT/install"

IN_FILE="$ROOT/examples/$1/makespeare"

if [ ! -f $IN_FILE ]; then
	echo "Makespeare input file $IN_FILE doesn't exist."
	exit 1
fi

num_seeds=$(get_config_value makespeare_seeds)

typeset -a seeds
seeds=( $(seq 50000 $(( 50000 + $num_seeds - 1 ))) )
if [[ ${#seeds[@]} == 0 ]]; then
	echo "Found no seeds!  Try setting some non-zero number of seeds in the config"
	exit 1
fi
parallel $INSTALL_DIR/bin/makespeare {} $IN_FILE 2.0 0.0 1.0 0.0 2000000 9 ::: ${seeds[@]}
