#!/bin/bash

if [ -f './env.sh' ]; then
  source './env.sh'
fi

if [ -z "$IDL_ROOT" ]; then
  echo "No IDL installation supplied; can't build pldi"
  exit 1
else
  IDL_DIR="$IDL_ROOT/install/lib/cmake/llvm"
  if [ ! -d "$IDL_DIR" ]; then
    echo "Not a valid IDL install location: $IDL_DIR"
    exit 2
  fi
fi

ROOT=$(realpath $(dirname "$0"))

INSTALL_DIR="$ROOT/install"
PLDI_DIR="$ROOT/pldi"

if [ -d "$PLDI_DIR" ]; then
  echo "Removing existing pldi dir..."
  rm -rf "$PLDI_DIR"
fi

echo "Cloning pldi..."

git clone git@github.com:Baltoli/accsynt.git "$PLDI_DIR"
cd "$PLDI_DIR"

echo "Building pldi..."

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

mv "$INSTALL_DIR/bin/synth" "$INSTALL_DIR/bin/pldi"
