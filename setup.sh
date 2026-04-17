#!/bin/bash

# 1. Create the virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# 2. Install dependencies
echo "Installing dependencies from requirements.txt..."
./.venv/bin/pip install -r requirements.txt

# 3. Create the run.sh script automatically
echo "Generating run.sh..."
cat << 'EOF' > run.sh
#!/bin/bash
# Get the directory where this script is located
DIR="$(cd "$(dirname "$0")" && pwd)"

# Run the python script using the venv python binary directly
"$DIR/.venv/bin/python3" "$DIR/main.py"
EOF

# 4. Make the new run.sh executable
chmod +x run.sh
chmod +x uninstall.sh

echo "-----------------------------------------------"
echo "Setup complete. Run ./run.sh to start your app."