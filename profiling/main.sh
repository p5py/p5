#!/bin/bash

FILES=*.py
for f in $FILES
do
    if [[ "$f" != "main.py" ]]; then
        echo "Running $f"
        timeout 3 python $f
        echo "Finished $f"
    fi
done
