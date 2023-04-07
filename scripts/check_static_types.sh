#!/bin/bash

set -o errexit

echo "Removing old mypy cache"
rm -rf .mypy_cache 

for file in "run.py" "tests/"; do
    echo "Running mypy on $file"
    python -m mypy "$file"
done
