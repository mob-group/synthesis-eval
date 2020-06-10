#!/bin/bash

builders=( $(find -name gen.py) )

for file in ${builders[@]}; do
	cd $(dirname $file)
	echo $file
	python3 gen.py
	cd ../..
done
