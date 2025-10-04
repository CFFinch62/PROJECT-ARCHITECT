@echo off
REM Project Architect - Run Script (Windows)
REM 
REM Convenience script to run Project Architect with the virtual environment

echo 🏗️  Starting Project Architect...

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run setup_venv.bat first to create the virtual environment
    pause
    exit /b 1
)

REM Check if we're in the correct directory
if not exist "main.py" (
    echo ❌ Error: main.py not found
    echo Please run this script from the Project Architect directory
    pause
    exit /b 1
)

REM Activate virtual environment and run the application
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

echo 🚀 Launching Project Architect...
python main.py

REM Deactivate virtual environment when done
call venv\Scripts\deactivate.bat
echo 👋 Project Architect closed
pause
