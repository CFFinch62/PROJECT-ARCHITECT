# Project Architect - Setup Guide

This guide will help you set up Project Architect on each PC/location where you develop. Since you work from multiple locations and different PCs, this ensures consistent setup across all your development environments.

## Prerequisites

### Required Software
- **Python 3.8 or higher** (Python 3.12+ recommended)
- **Git** (for version control)
- **Terminal/Command Prompt** access

### Optional but Recommended
- **GitHub CLI** (`gh`) - for automatic GitHub repository creation
- **VS Code** or **PyCharm** - for development
- **Virtual environment support** (built into Python 3.3+)

## Quick Setup (Automated)

### Linux/Mac
```bash
# Navigate to Project Architect directory
cd "Project Architect"

# Run the setup script
./setup_venv.sh

# Run the application
./run.sh
```

### Windows
```cmd
# Navigate to Project Architect directory
cd "Project Architect"

# Run the setup script
setup_venv.bat

# Run the application
run.bat
```

## Manual Setup (Step by Step)

If you prefer to set up manually or the automated scripts don't work:

### 1. Verify Python Installation
```bash
# Check Python version
python3 --version  # Linux/Mac
python --version   # Windows

# Should show Python 3.8 or higher
```

### 2. Navigate to Project Directory
```bash
cd "Project Architect"
```

### 3. Create Virtual Environment
```bash
# Linux/Mac
python3 -m venv venv

# Windows
python -m venv venv
```

### 4. Activate Virtual Environment
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate.bat
```

### 5. Upgrade pip
```bash
pip install --upgrade pip
```

### 6. Install Dependencies
```bash
pip install -r requirements.txt
```

### 7. Test Installation
```bash
# Linux/Mac
python3 main.py

# Windows
python main.py
```

## Multi-PC Development Workflow

Since you develop from multiple locations, here's the recommended workflow:

### Initial Setup on New PC
1. **Clone/Sync Project**: Get the latest Project Architect files
2. **Run Setup Script**: Use `setup_venv.sh` (Linux/Mac) or `setup_venv.bat` (Windows)
3. **Test Application**: Run `./run.sh` or `run.bat` to verify everything works

### Daily Development Workflow
1. **Sync Files**: Pull latest changes from your sync service (Dropbox, Git, etc.)
2. **Activate Environment**: Use the run scripts or manually activate venv
3. **Develop**: Make your changes
4. **Test**: Run the application to test changes
5. **Sync Changes**: Push/sync your changes for other PCs

### Switching Between PCs
- **Virtual environments are PC-specific** - each PC needs its own venv
- **Source code is shared** - sync via Dropbox, Git, or other service
- **Settings are portable** - stored in `data/` directory
- **Generated projects are portable** - can be opened on any PC

## Directory Structure

```
Project Architect/
├── venv/                    # Virtual environment (PC-specific, don't sync)
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── setup_venv.sh           # Linux/Mac setup script
├── setup_venv.bat          # Windows setup script
├── run.sh                  # Linux/Mac run script
├── run.bat                 # Windows run script
├── project_architect/      # Main application code
├── data/                   # Settings and user data (sync this)
├── logs/                   # Application logs (optional to sync)
└── generated_projects/     # Generated projects (sync if desired)
```

## Troubleshooting

### Common Issues

#### "Python not found"
- **Solution**: Install Python 3.8+ and ensure it's in your PATH
- **Windows**: Download from python.org and check "Add to PATH" during installation
- **Linux**: `sudo apt install python3 python3-venv` (Ubuntu/Debian)
- **Mac**: `brew install python3` (with Homebrew)

#### "Permission denied" on scripts
- **Linux/Mac**: Run `chmod +x setup_venv.sh run.sh`
- **Windows**: Run Command Prompt as Administrator

#### "Module not found" errors
- **Solution**: Ensure virtual environment is activated and dependencies are installed
- **Check**: `pip list` should show all required packages

#### GUI doesn't start
- **Linux**: May need `sudo apt install python3-tk` for tkinter support
- **Check**: Display environment variables (DISPLAY on Linux)

#### Different Python versions between PCs
- **Solution**: Use the same Python version on all PCs when possible
- **Alternative**: Update requirements.txt if needed for compatibility

### Dependency Issues

If you encounter dependency conflicts:

1. **Delete virtual environment**: `rm -rf venv` (Linux/Mac) or `rmdir /s venv` (Windows)
2. **Recreate environment**: Run setup script again
3. **Update requirements**: If needed, update `requirements.txt`

### Performance Issues

If the application runs slowly:

1. **Check Python version**: Newer versions are generally faster
2. **Check available memory**: Close other applications
3. **Check disk space**: Ensure adequate free space

## Development Environment Setup

### VS Code Setup
1. **Install Python extension**
2. **Select interpreter**: Choose the venv Python interpreter
3. **Configure settings**: Use project-specific settings in `.vscode/`

### PyCharm Setup
1. **Configure interpreter**: Point to `venv/bin/python` (Linux/Mac) or `venv\Scripts\python.exe` (Windows)
2. **Enable virtual environment**: PyCharm should auto-detect the venv

## Syncing Between PCs

### What to Sync
- ✅ **Source code** (`project_architect/`, `main.py`, etc.)
- ✅ **Documentation** (`README.md`, `*.md` files)
- ✅ **Configuration** (`requirements.txt`, setup scripts)
- ✅ **User settings** (`data/` directory)
- ✅ **Generated projects** (if you want them on all PCs)

### What NOT to Sync
- ❌ **Virtual environment** (`venv/` directory)
- ❌ **Logs** (`logs/` directory) - optional
- ❌ **Cache files** (`__pycache__/`, `*.pyc`)
- ❌ **IDE files** (`.vscode/`, `.idea/`) - unless you want shared IDE settings

### Recommended .gitignore (if using Git)
```gitignore
# Virtual environment
venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

## Support

If you encounter issues:

1. **Check logs**: Look in `logs/` directory for error messages
2. **Verify setup**: Run the setup script again
3. **Check dependencies**: Ensure all packages in requirements.txt are installed
4. **Test basic functionality**: Try importing modules in Python REPL

## Next Steps

Once Project Architect is set up and running:

1. **Explore the interface**: Familiarize yourself with the GUI
2. **Create a test project**: Try generating a simple desktop GUI project
3. **Customize templates**: Modify existing templates or create new ones
4. **Update existing projects**: Test the project update functionality

Remember: Each PC needs its own virtual environment, but the source code and settings can be shared across all your development locations!
