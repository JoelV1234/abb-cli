#!/bin/bash

# 1. Install system dependencies
echo "Checking system dependencies..."
if [ "$(uname)" = "Linux" ]; then
    echo "Installing system dependencies..."
    sudo apt install -y libxslt1.1 libxml2
else
    echo "Skipping system dependencies install (Linux only)."
fi

# 2. Create the virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# 3. Install dependencies
echo "Installing dependencies from requirements.txt..."
./.venv/bin/pip install -r requirements.txt

# 4. Create the run.sh script automatically
echo "Generating run.sh..."
cat << 'EOF' > run.sh
#!/bin/bash
# Get the directory where this script is located
DIR="$(cd "$(dirname "$0")" && pwd)"

# Run the python script using the venv python binary directly
"$DIR/.venv/bin/python3" "$DIR/main.py"
EOF

# 5. Make the new run.sh executable
chmod +x run.sh

echo "-----------------------------------------------"
echo "Setup complete. Run ./run.sh to start your app."