#!/usr/bin/env bash

ROOT=$(realpath $(dirname "$0"))
INSTALL_DIR="$ROOT/install"

valid=()
invalid=()

for example in $(ls "$ROOT/examples"); do
  if [ ! -d "$ROOT/examples/$example" ]; then
    continue
  fi

  IN_PROPS="$ROOT/examples/$example/props"
  IN_LIB="$ROOT/examples/$example/ref.so"

  ./compile-ref "$example"

  if [ ! -f "$IN_PROPS" ]; then
    invalid+=("$example")
    continue
  fi

  if [ ! -f "$IN_LIB" ]; then
    invalid+=("$example")
    continue
  fi

  sh -c "$INSTALL_DIR/bin/pldi -dry-run $IN_PROPS $IN_LIB" >/dev/null 2>&1

  if [ $? -eq 0 ]; then
    valid+=("$example")
  else
    invalid+=("$example")
  fi
done

BOLD='\e[1m'
GREEN='\e[32m'
RED='\e[31m'
RESET='\e[0m'

echo -e "${BOLD}${GREEN}✔ Done${RESET}"
for val_ex in ${valid[@]}; do
  echo "$val_ex"
done

echo -e "\n${BOLD}${RED}✘ Not Done${RESET}"
for inval_ex in ${invalid[@]}; do
  echo "$inval_ex"
done
