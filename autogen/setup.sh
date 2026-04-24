#!/bin/bash

# Setup script for AutoGen Interview Platform Workflow

echo "=========================================="
echo "AutoGen Interview Platform Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python3 not found!"; exit 1; }

# Create virtual environment (optional but recommended)
echo ""
echo "Creating virtual environment..."
python3 -m venv venv || true

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || true

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the workflow:"
echo "  source venv/bin/activate  (if using venv)"
echo "  export OPENAI_API_KEY='your-key-here'"
echo "  python autogen_simple_demo.py"
echo ""
