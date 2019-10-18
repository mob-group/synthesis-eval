#!/bin/bash

set -eu

ROOT=$(realpath $(dirname "$0"))

INSTALL_DIR="$ROOT/install"
MSP_DIR="$ROOT/makespeare"

if [ -d "$MSP_DIR" ]; then
  echo "Removing existing makespeare dir..."
  rm -rf "$MSP_DIR"
fi

echo "Cloning makespeare..."

git clone https://github.com/ChristopherRosin/MAKESPEARE.git "$MSP_DIR"
cd "$MSP_DIR"

curl -L --output luajit.tar.gz https://luajit.org/download/LuaJIT-2.1.0-beta3.tar.gz
tar xvf luajit.tar.gz
sed -i 's/^LUAJITDIR.*/LUAJITDIR=..\/LuaJIT-2.1.0-beta3/' code/Makefile

echo "Building makespeare..."
cd code
make

echo "Installing makespeare..."

mkdir -p "$INSTALL_DIR/bin"
cp ./makespeare-x86-64 "$INSTALL_DIR/bin/makespeare"
