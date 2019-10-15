#!/bin/bash

ROOT=$(realpath $(dirname "$0"))

INSTALL_DIR="$ROOT/install"
L2_DIR="$ROOT/L2"

if [ -d "$L2_DIR" ]; then
  echo "Removing existing L2 dir..."
  rm -rf "$L2_DIR"
fi

echo "Cloning L2..."

git clone git@github.com:jfeser/L2.git "$L2_DIR"
cd "$L2_DIR"

echo "Building L2..."

jbuilder external-lib-deps --missing @install
jbuilder build @install

echo "Installing L2..."

mkdir -p "$INSTALL_DIR/bin"
mkdir -p "$INSTALL_DIR/share/L2"

cp _build/default/bin/l2_cli.exe "$INSTALL_DIR/bin/L2"
cp components/* "$INSTALL_DIR/share/L2"
