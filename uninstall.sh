#!/bin/bash

# 1. Remove Ctrl+P bind from ~/.bashrc
echo "Removing Ctrl+P paste shortcut from ~/.bashrc..."
if [ "$(uname)" = "Darwin" ]; then
    sed -i '' '/pi_clipboard/d' ~/.bashrc
elif [ "$(uname)" = "Linux" ]; then
    sed -i '/pi_clipboard/d' ~/.bashrc
fi

# 2. Remove virtual environment
if [ -d ".venv" ]; then
    echo "Removing virtual environment..."
    rm -rf .venv
fi

# 3. Move out of the directory and delete it
PARENT_DIR=$(dirname "$(pwd)")
CURRENT_DIR=$(basename "$(pwd)")

echo "Removing project folder: $CURRENT_DIR"
cd "$PARENT_DIR" || exit
rm -rf "$CURRENT_DIR"

echo "Cleanup complete."