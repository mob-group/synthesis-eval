#!/bin/bash

for f in $(find -name gen.py); do
	dname=$(dirname $f)
	echo "LOokng at $dname"
	cd $dname
	python gen.py
	mv LLM LLM.json
	cd ..
done
