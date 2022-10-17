#!/bin/bash

echo -n "" > full.json

for f in $(find -name gen.py); do
	dname=$(dirname $f)
	echo "LOokng at $dname"
	cd $dname
	python gen.py
	mv LLM LLM.json
	cat LLM.json >> ../full.json
	echo "" >> ../full.json
	cd ..
done
