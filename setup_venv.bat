@echo off
REM Project Architect - Virtual Environment Setup Script (Windows)
REM 
REM This script sets up a virtual environment for Project Architect
REM Run this script on each PC/location where you develop

echo 🏗️  Project Architect - Virtual Environment Setup
echo ==================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Found: %PYTHON_VERSION%

REM Check if we're in the Project Architect directory
if not exist "main.py" (
    echo ❌ Error: Please run this script from the Project Architect directory
    echo Expected files: main.py, requirements.txt
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ Error: Please run this script from the Project Architect directory
    echo Expected files: main.py, requirements.txt
    pause
    exit /b 1
)

echo 📁 Current directory: %CD%

REM Remove existing virtual environment if it exists
if exist "venv" (
    echo 🗑️  Removing existing virtual environment...
    rmdir /s /q venv
)

REM Create new virtual environment
echo 🔧 Creating virtual environment...
python -m venv venv

if %errorlevel% neq 0 (
    echo ❌ Error: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📦 Installing dependencies from requirements.txt...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Error: Failed to install dependencies
    echo Please check requirements.txt and try again
    pause
    exit /b 1
)

REM Test the installation
echo 🧪 Testing installation...
python -c "import customtkinter; print('✅ CustomTkinter imported successfully')"
python -c "import project_architect; print('✅ Project Architect modules imported successfully')"

echo.
echo 🎉 Setup completed successfully!
echo.
echo To run Project Architect:
echo   1. Activate the virtual environment: venv\Scripts\activate.bat
echo   2. Run the application: python main.py
echo.
echo Or use the run script: run.bat
echo.
echo 💡 Remember to run this setup script on each PC where you develop!
pause
