#!/usr/bin/env bash

if [ -f './env.sh' ]; then
  source './env.sh'
fi

if [ -z "$IDL_ROOT" ]; then
  echo "No IDL installation supplied; can't build baseline"
  exit 1
else
  IDL_DIR="$IDL_ROOT/lib/cmake/llvm"
  if [ ! -d "$IDL_DIR" ]; then
    echo "Not a valid IDL install location: $IDL_DIR"
    exit 2
  fi
fi

ROOT=$(realpath $(dirname "$0"))

INSTALL_DIR="$ROOT/install"
BASELINE_DIR="$ROOT/baseline"

if [ -d "$BASELINE_DIR" ]; then
  echo "Removing existing baseline dir..."
  rm -rf "$BASELINE_DIR"
fi

echo "Cloning baseline..."

git clone git@github.com:Baltoli/accsynt.git "$BASELINE_DIR"
cd "$BASELINE_DIR"

echo "Building baseline..."

git checkout baseline
mkdir build
cd build

cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" \
  -DLLVM_DIR="$IDL_DIR" \
  -DCMAKE_C_COMPILER=gcc-8 \
  -DCMAKE_CXX_COMPILER=g++-8 \
  ../src

make -j$(nproc)
make install

mv "$INSTALL_DIR/bin/synth" "$INSTALL_DIR/bin/baseline"
