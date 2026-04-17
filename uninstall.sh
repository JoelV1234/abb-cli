#!/bin/bash

# 1. Uninstall python packages
if [ -f "requirements.txt" ]; then
    echo "Uninstalling dependencies..."
    pip uninstall -r requirements.txt -y
else
    echo "requirements.txt not found, skipping pip uninstall."
fi

# 2. Move out of the directory and delete it
PARENT_DIR=$(dirname "$(pwd)")
CURRENT_DIR=$(basename "$(pwd)")

echo "Removing project folder: $CURRENT_DIR"
cd "$PARENT_DIR" || exit
rm -rf "$CURRENT_DIR"

echo "Cleanup complete."