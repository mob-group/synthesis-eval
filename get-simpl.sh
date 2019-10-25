#!/usr/bin/env bash

set -eu

ROOT=$(realpath $(dirname "$0"))

INSTALL_DIR="$ROOT/install"
SIMPL_DIR="$ROOT/simpl"

if [ -d "$SIMPL_DIR" ]; then
  echo "Removing existing simpl dir..."
  rm -rf "$SIMPL_DIR"
fi

echo "Cloning simpl..."

git clone https://github.com/kupl/SimplPublic.git "$SIMPL_DIR"
cd "$SIMPL_DIR"

echo "Building simpl..."

chmod +x ./build
./build

echo "Installing simpl..."

mkdir -p "$INSTALL_DIR/bin"
cp ./main.native "$INSTALL_DIR/bin/simpl"
