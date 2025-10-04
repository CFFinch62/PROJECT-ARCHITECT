#!/bin/bash
# Project Architect - Virtual Environment Setup Script (Linux/Mac)
# 
# This script sets up a virtual environment for Project Architect
# Run this script on each PC/location where you develop

echo "🏗️  Project Architect - Virtual Environment Setup"
echo "=================================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Display Python version
PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"

# Check if we're in the Project Architect directory
if [ ! -f "main.py" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the Project Architect directory"
    echo "Expected files: main.py, requirements.txt"
    exit 1
fi

echo "📁 Current directory: $(pwd)"

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo "🗑️  Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    echo "Please check requirements.txt and try again"
    exit 1
fi

# Test the installation
echo "🧪 Testing installation..."
python3 -c "import customtkinter; print('✅ CustomTkinter imported successfully')"
python3 -c "import project_architect; print('✅ Project Architect modules imported successfully')"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To run Project Architect:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the application: python3 main.py"
echo ""
echo "Or use the run script: ./run.sh"
echo ""
echo "💡 Remember to run this setup script on each PC where you develop!"
