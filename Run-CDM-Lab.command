#!/bin/bash
# Move to the script's directory
cd "$(dirname "$0")"

echo "=========================================="
echo " 🛡️ Cyber Defense Matrix: AI Automation Lab"
echo "=========================================="
echo "Initializing local environment..."

# 1. Create virtual environment if missing
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Install or update dependencies quietly
echo "Checking dependencies..."
pip install -r requirements.txt --quiet

# 4. Launch Streamlit
echo ""
echo "🚀 Launching dashboard in your browser..."
echo "Close this terminal window to stop the application."
echo "=========================================="
streamlit run app.py