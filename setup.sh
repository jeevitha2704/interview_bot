#!/bin/bash

echo "🤖 AI Interview Bot - Setup Script"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env created. Please edit it with your OpenAI API key."
else
    echo "✓ .env file already exists"
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment found"
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

echo ""
echo "📝 Next steps:"
echo "1. Edit .env file and add your OpenAI API key:"
echo "   nano .env"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the application:"
echo "   python app.py"
echo ""
echo "4. Open your browser and go to:"
echo "   http://localhost:5000"
echo ""
