#!/bin/bash

# CrewAI Real API Setup and Run Script
# This script helps you set up and run the CrewAI demo with real API calls

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     CrewAI Multi-Agent Travel Planning - Setup & Run           ║"
echo "║                 (Real API Version)                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY is not set!"
    echo ""
    echo "You have two options:"
    echo ""
    echo "Option 1: Set API key for this session only"
    echo "  export OPENAI_API_KEY='sk-proj-YOUR-KEY-HERE'"
    echo "  python crewai_demo.py"
    echo ""
    echo "Option 2: Set API key permanently"
    echo "  echo 'export OPENAI_API_KEY=\"sk-proj-YOUR-KEY-HERE\"' >> ~/.zshrc"
    echo "  source ~/.zshrc"
    echo "  python crewai_demo.py"
    echo ""
    echo "Get your API key at: https://platform.openai.com/api-keys"
    echo ""
    read -p "Enter your OpenAI API key (or press Enter to skip): " api_key

    if [ ! -z "$api_key" ]; then
        export OPENAI_API_KEY="$api_key"
        echo "✅ API key set for this session!"
    else
        echo "❌ API key not set. Cannot proceed."
        exit 1
    fi
else
    echo "✅ OPENAI_API_KEY is set!"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "Step 1: Checking dependencies..."
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed"
    exit 1
fi

echo "Installing dependencies from requirements.txt..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "Step 2: Verifying setup..."
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if Python file exists
if [ ! -f "crewai_demo.py" ]; then
    echo "❌ crewai_demo.py not found!"
    exit 1
fi

echo "✅ crewai_demo.py found"

# Verify API key again
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY is still not set!"
    exit 1
else
    echo "✅ OPENAI_API_KEY is set"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "Step 3: Running CrewAI Demo..."
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "ℹ️  This will use real OpenAI API calls to research:"
echo "    - Actual flight options and prices"
echo "    - Real hotels with current pricing"
echo "    - Verified attractions and activities"
echo "    - Realistic budget calculations"
echo ""
echo "Estimated API cost: $0.25 - $0.50 USD"
echo "Estimated runtime: 2-5 minutes"
echo ""
read -p "Press Enter to start the demo or Ctrl+C to cancel..."

echo ""
python crewai_demo.py

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "Demo completed!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Output saved to: crewai_output.txt"
echo ""
echo "View the results:"
echo "  cat crewai_output.txt"
echo ""
echo "📊 Check your API usage:"
echo "  https://platform.openai.com/account/usage"
echo ""
echo "💰 View your billing:"
echo "  https://platform.openai.com/account/billing/overview"
