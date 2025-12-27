#!/bin/bash

# Clash Royale AI - Setup and Run Script

echo "🎯 Clash Royale AI - Setup and Run Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if API token is set
if [ -z "$CLASH_ROYALE_API_TOKEN" ]; then
    echo ""
    echo "⚠️  IMPORTANT: Set your Clash Royale API token"
    echo "   Get it from: https://developer.clashroyale.com/"
    echo ""
    echo "   Run: export CLASH_ROYALE_API_TOKEN='your_token_here'"
    echo ""
fi

echo ""
echo "🚀 Starting servers..."
echo "   - FastAPI backend: http://localhost:8000"
echo "   - Streamlit frontend: http://localhost:8501"
echo ""

# Start FastAPI in background
echo "Starting FastAPI backend..."
python3 api.py &
API_PID=$!

# Wait for API to start
sleep 2

# Start Streamlit
echo "Starting Streamlit frontend..."
streamlit run app.py --server.port=8501

# Cleanup
kill $API_PID
