#!/bin/bash

# Get the directory where this script is located
DIR="$(cd "$(dirname "$0")" && pwd)"

# Run the python script using the python executable INSIDE the venv
# This executes the script WITHIN the venv context without needing 'source activate'
"$DIR/.venv/bin/python3" "$DIR/main.py"