#!/bin/bash

for d in ./*; do
	if [[ -d $d ]]; then
		if [[ $(cat $d/ref.c) == *void* ]]; then
		vim -O $d/gen.py $d/ref.c 
		fi
	fi
done
