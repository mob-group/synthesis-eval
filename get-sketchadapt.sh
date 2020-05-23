#!/usr/bin/env bash
set -eu

ROOT=$(realpath $(dirname "$0"))
INSTALL_DIR="$ROOT/SketchAdapt"

if [ -d "$INSTALL_DIR"]; then
	echo "Removing existing SketchAdapt dir..."
	rm -rf "INSTALL_DIR"
fi

echo "Installing SketchAdapt..."
git clone https://github.com/j-c-w/neural_sketch

cd neural_sketch
git submodule update --init --recursive
# Get the dependencies
python3 -m virtualenv env
source env/bin/activate

pip3 install torch==1.4.0 numpy dill matplotlib
cd program_synthesis
pip3 install -e
cd ..
