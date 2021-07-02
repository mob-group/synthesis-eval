#!/usr/bin/env bash

set -eu

ROOT=$(realpath $(dirname "$0"))

INSTALL_DIR="$ROOT/install"
L2_DIR="$ROOT/L2"

if [ -d "$L2_DIR" ]; then
  echo "Removing existing L2 dir..."
  rm -rf "$L2_DIR"
fi

echo "Cloning L2..."

git clone https://github.com/jfeser/L2.git "$L2_DIR"
cd "$L2_DIR"
opam install --deps-only ./l2.opam.locked
git checkout pldi-modernize

echo "Building L2..."

dune external-lib-deps --missing @install
dune build @install

echo "Installing L2..."

mkdir -p "$INSTALL_DIR/bin"
mkdir -p "$INSTALL_DIR/share/L2"

cat >> components/stdlib.ml <<- EOM

let rec newzip = fun xs ys ->
  let rec helper = fun xs ->
    if xs = [] then [] else
      car (car xs) :: helper (cdr xs)
  in map (zip xs ys) helper
EOM

cp _build/default/bin/l2_cli.exe "$INSTALL_DIR/bin/L2"
cp components/* "$INSTALL_DIR/share/L2"
