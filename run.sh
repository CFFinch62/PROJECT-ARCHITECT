#!/bin/bash
# Project Architect - Run Script (Linux/Mac)
# 
# Convenience script to run Project Architect with the virtual environment

echo "🏗️  Starting Project Architect..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup_venv.sh first to create the virtual environment"
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found"
    echo "Please run this script from the Project Architect directory"
    exit 1
fi

# Activate virtual environment and run the application
echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo "🚀 Launching Project Architect..."
python3 main.py

# Deactivate virtual environment when done
deactivate
echo "👋 Project Architect closed"
