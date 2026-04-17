#!/bin/bash
# Get the directory where this script is located
DIR="$(cd "$(dirname "$0")" && pwd)"

# Run the python script using the venv python binary directly
"$DIR/.venv/bin/python3" "$DIR/main.py"
