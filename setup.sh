#!/bin/bash
# Quick Start Script for AML System

echo "=========================================="
echo "AML System - Sprint 1 Quick Start"
echo "=========================================="
echo ""

# Check Python installation
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application, run:"
echo "   python app.py"
echo ""
echo "Then open your browser and go to:"
echo "   http://localhost:5000"
echo ""
echo "Demo Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "=========================================="
