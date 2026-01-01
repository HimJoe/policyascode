#!/bin/bash

# Quick start script for Policy-to-Code Converter

echo "🚀 Starting Policy-to-Code Converter..."
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Run setup_for_client.sh first."
    exit 1
fi

# Run the converter
echo "📜 Launching Policy-to-Code Converter..."
echo ""
streamlit run policy_to_code_converter.py

# Deactivate when done
deactivate
