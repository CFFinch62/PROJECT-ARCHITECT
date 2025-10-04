# Project Architect - Troubleshooting Guide

This guide helps you diagnose and resolve common issues with Project Architect. It covers installation problems, runtime errors, template issues, and performance problems.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Application Startup Problems](#application-startup-problems)
3. [Template and Generation Issues](#template-and-generation-issues)
4. [GUI Problems](#gui-problems)
5. [Performance Issues](#performance-issues)
6. [Platform-Specific Issues](#platform-specific-issues)
7. [Debugging Tools](#debugging-tools)

## Installation Issues

### Python Version Problems

**Problem**: "Python not found" or version compatibility errors

**Solutions**:
```bash
# Check Python version
python3 --version  # Should be 3.8 or higher

# If Python 3 not found on Linux/Mac
sudo apt install python3 python3-pip python3-venv  # Ubuntu/Debian
brew install python3  # macOS with Homebrew

# If Python 3 not found on Windows
# Download from python.org and ensure "Add to PATH" is checked
```

**Verification**:
```bash
python3 -c "import sys; print(sys.version)"
```

### Virtual Environment Issues

**Problem**: Virtual environment creation fails

**Solutions**:
```bash
# Ensure venv module is available
python3 -m venv --help

# If venv module missing (Ubuntu/Debian)
sudo apt install python3-venv

# Alternative: use virtualenv
pip install virtualenv
virtualenv venv

# Windows: Ensure execution policy allows scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Problem**: Virtual environment activation fails

**Solutions**:
```bash
# Linux/Mac - check shell
echo $SHELL
# Use appropriate activation script
source venv/bin/activate      # bash/zsh
source venv/bin/activate.fish # fish
source venv/bin/activate.csh  # csh/tcsh

# Windows - check PowerShell vs Command Prompt
venv\Scripts\activate.bat     # Command Prompt
venv\Scripts\Activate.ps1     # PowerShell
```

### Dependency Installation Problems

**Problem**: Package installation fails

**Solutions**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output to see errors
pip install -v -r requirements.txt

# If specific package fails, try individual installation
pip install customtkinter
pip install jinja2
pip install pyyaml

# Clear pip cache if corrupted
pip cache purge

# Use different index if default fails
pip install -i https://pypi.org/simple/ -r requirements.txt
```

**Problem**: Permission denied during installation

**Solutions**:
```bash
# Use user installation (recommended)
pip install --user -r requirements.txt

# Or fix permissions (Linux/Mac)
sudo chown -R $USER ~/.local/lib/python3.*/site-packages/

# Windows: Run Command Prompt as Administrator
```

## Application Startup Problems

### Import Errors

**Problem**: "ModuleNotFoundError" when starting application

**Diagnostic Steps**:
```bash
# Check if virtual environment is activated
which python  # Should point to venv/bin/python

# Verify package installation
pip list | grep customtkinter
pip list | grep jinja2

# Test imports manually
python3 -c "import customtkinter; print('CustomTkinter OK')"
python3 -c "import project_architect; print('Project Architect OK')"
```

**Solutions**:
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"

# Ensure you're in the correct directory
pwd  # Should be in Project Architect directory
ls   # Should see main.py and project_architect/ folder
```

### Configuration Issues

**Problem**: Settings or configuration errors

**Diagnostic Steps**:
```bash
# Check configuration directory
ls -la data/
ls -la logs/

# Check permissions
ls -la data/settings.yaml
```

**Solutions**:
```bash
# Reset configuration
rm -rf data/settings.yaml
# Application will recreate with defaults

# Fix permissions
chmod 755 data/
chmod 644 data/settings.yaml

# Check disk space
df -h .
```

### Logging Problems

**Problem**: No log files created or permission errors

**Solutions**:
```bash
# Create logs directory if missing
mkdir -p logs/

# Fix permissions
chmod 755 logs/

# Check log file
tail -f logs/project_architect_$(date +%Y%m%d).log

# Test logging manually
python3 -c "
import logging
logging.basicConfig(filename='test.log', level=logging.INFO)
logging.info('Test message')
print('Check test.log file')
"
```

## Template and Generation Issues

### Template Loading Problems

**Problem**: "Template not found" errors

**Diagnostic Steps**:
```bash
# Check template directory structure
ls -la project_architect/templates/
ls -la project_architect/templates/desktop_gui/

# Verify template files
ls -la project_architect/templates/desktop_gui/template.yaml
ls -la project_architect/templates/desktop_gui/questionnaire.json
```

**Solutions**:
```bash
# Verify template.yaml syntax
python3 -c "
import yaml
with open('project_architect/templates/desktop_gui/template.yaml') as f:
    yaml.safe_load(f)
print('YAML syntax OK')
"

# Verify questionnaire.json syntax
python3 -c "
import json
with open('project_architect/templates/desktop_gui/questionnaire.json') as f:
    json.load(f)
print('JSON syntax OK')
"

# Check file permissions
chmod 644 project_architect/templates/desktop_gui/*
```

### Project Generation Failures

**Problem**: Project generation stops or fails

**Diagnostic Steps**:
```bash
# Check available disk space
df -h .

# Check output directory permissions
ls -la /path/to/output/directory/

# Enable debug logging
export PYTHONPATH=.
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# Run generation with debug output
"
```

**Solutions**:
```bash
# Ensure output directory exists and is writable
mkdir -p /path/to/output/
chmod 755 /path/to/output/

# Try generation in temporary directory
python3 -c "
import tempfile
temp_dir = tempfile.mkdtemp()
print(f'Try generating in: {temp_dir}')
"

# Check for long path issues (Windows)
# Use shorter output paths or enable long path support
```

### Template Rendering Errors

**Problem**: Jinja2 template errors

**Common Errors and Solutions**:

```python
# UndefinedError: 'variable_name' is undefined
# Solution: Check questionnaire provides all required variables

# TemplateSyntaxError: unexpected 'end of template'
# Solution: Check for unmatched {% %} blocks

# TemplateRuntimeError: division by zero
# Solution: Add conditional checks in templates
{% if denominator != 0 %}
{{ numerator / denominator }}
{% endif %}
```

**Debug Template Rendering**:
```python
# Test template manually
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('project_architect/templates/desktop_gui/'))
template = env.get_template('main.py.j2')
result = template.render(project_name='Test', author_name='Test Author')
print(result)
```

## GUI Problems

### Display Issues

**Problem**: GUI doesn't appear or appears corrupted

**Linux Solutions**:
```bash
# Check display environment
echo $DISPLAY

# Install tkinter if missing
sudo apt install python3-tk

# Test basic tkinter
python3 -c "
import tkinter as tk
root = tk.Tk()
root.title('Test')
tk.Label(root, text='Test').pack()
root.mainloop()
"

# For headless systems, use virtual display
sudo apt install xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
```

**macOS Solutions**:
```bash
# Install tkinter via Homebrew Python
brew install python-tk

# Check macOS version compatibility
sw_vers
```

**Windows Solutions**:
```cmd
# Ensure Python was installed with tkinter
python -c "import tkinter; print('Tkinter available')"

# Check display scaling settings
# Right-click desktop > Display settings > Scale
# Try 100% scaling if having issues
```

### CustomTkinter Issues

**Problem**: CustomTkinter-specific errors

**Solutions**:
```bash
# Update to latest version
pip install --upgrade customtkinter

# Check version compatibility
python3 -c "
import customtkinter as ctk
print(f'CustomTkinter version: {ctk.__version__}')
"

# Test basic CustomTkinter
python3 -c "
import customtkinter as ctk
ctk.set_appearance_mode('dark')
app = ctk.CTk()
app.title('Test')
app.geometry('400x300')
app.mainloop()
"
```

### Theme and Appearance Problems

**Problem**: Theme not loading or appearance issues

**Solutions**:
```python
# Reset appearance settings
import customtkinter as ctk
ctk.set_appearance_mode("system")  # or "dark" or "light"
ctk.set_default_color_theme("blue")  # or "green" or "dark-blue"

# Check theme files
import customtkinter
print(customtkinter.__file__)  # Check installation directory
```

## Performance Issues

### Slow Startup

**Problem**: Application takes long time to start

**Diagnostic Steps**:
```bash
# Profile startup time
time python3 main.py

# Check import times
python3 -X importtime main.py 2> import_times.log
# Analyze import_times.log for slow imports
```

**Solutions**:
```bash
# Optimize Python startup
export PYTHONDONTWRITEBYTECODE=1  # Skip .pyc files
export PYTHONUNBUFFERED=1         # Unbuffered output

# Check for antivirus interference (Windows)
# Add Project Architect directory to antivirus exclusions

# Use SSD instead of HDD if possible
# Close other resource-intensive applications
```

### Slow Project Generation

**Problem**: Project generation is very slow

**Solutions**:
```python
# Enable progress callbacks to see where time is spent
def progress_callback(progress, message):
    print(f"{progress}%: {message}")

# Use the callback in generation
generator.generate_project(response, output_dir, progress_callback)

# Check disk I/O
# Use faster storage
# Close file indexing services temporarily
```

### Memory Issues

**Problem**: High memory usage or out of memory errors

**Solutions**:
```bash
# Monitor memory usage
python3 -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"

# Reduce template caching if needed
# Process templates in smaller batches
# Close unnecessary applications
```

## Platform-Specific Issues

### Windows Issues

**Problem**: Path length limitations

**Solutions**:
```cmd
# Enable long path support (Windows 10+)
# Run as Administrator:
reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1

# Or use shorter paths
# Generate projects closer to root directory
```

**Problem**: PowerShell execution policy

**Solutions**:
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single script
powershell -ExecutionPolicy Bypass -File setup_venv.ps1
```

### Linux Issues

**Problem**: Missing system dependencies

**Solutions**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-dev python3-pip python3-venv python3-tk

# CentOS/RHEL/Fedora
sudo yum install python3-devel python3-pip python3-tkinter
# or
sudo dnf install python3-devel python3-pip python3-tkinter

# Arch Linux
sudo pacman -S python python-pip tk
```

### macOS Issues

**Problem**: Homebrew Python vs system Python conflicts

**Solutions**:
```bash
# Use Homebrew Python consistently
brew install python3
which python3  # Should show /usr/local/bin/python3 or /opt/homebrew/bin/python3

# Update PATH in shell profile
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Or use pyenv for Python version management
brew install pyenv
pyenv install 3.12.0
pyenv global 3.12.0
```

## Debugging Tools

### Enable Debug Logging

```python
# Add to main.py or create debug_main.py
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

# Run with debug output
python3 debug_main.py
```

### Check System Information

```python
# Create system_info.py
import sys
import platform
import customtkinter
import jinja2
import yaml

print("=== System Information ===")
print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Architecture: {platform.architecture()}")
print(f"CustomTkinter version: {customtkinter.__version__}")
print(f"Jinja2 version: {jinja2.__version__}")
print(f"PyYAML version: {yaml.__version__}")
print(f"Python path: {sys.executable}")
print(f"Working directory: {os.getcwd()}")
```

### Test Individual Components

```python
# Test questionnaire engine
from project_architect.core import QuestionnaireEngine
engine = QuestionnaireEngine()
print("QuestionnaireEngine: OK")

# Test template engine
from project_architect.core import TemplateEngine
template_engine = TemplateEngine("project_architect/templates")
print("TemplateEngine: OK")

# Test GUI components
import customtkinter as ctk
app = ctk.CTk()
app.withdraw()  # Don't show window
print("GUI components: OK")
app.destroy()
```

### Performance Profiling

```python
# Create profile_app.py
import cProfile
import pstats
from main import main

# Profile the application
cProfile.run('main()', 'profile_stats')

# Analyze results
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

### Network Diagnostics

```bash
# Test GitHub connectivity (for repository creation)
curl -I https://github.com

# Test PyPI connectivity (for package installation)
curl -I https://pypi.org

# Check DNS resolution
nslookup github.com
nslookup pypi.org
```

## Getting Additional Help

### Log Analysis

When reporting issues, include:

1. **System Information**: OS, Python version, package versions
2. **Error Messages**: Complete error messages and stack traces
3. **Log Files**: Contents of log files from `logs/` directory
4. **Steps to Reproduce**: Exact steps that cause the issue
5. **Configuration**: Relevant configuration files

### Useful Commands for Support

```bash
# Generate system report
python3 -c "
import sys, platform, os
print('Python:', sys.version)
print('Platform:', platform.platform())
print('Working Dir:', os.getcwd())
print('Python Path:', sys.executable)
"

# Check package versions
pip list | grep -E "(customtkinter|jinja2|pyyaml)"

# Check file permissions
ls -la main.py project_architect/

# Check recent log entries
tail -20 logs/project_architect_$(date +%Y%m%d).log
```

### Common Solutions Summary

1. **Always activate virtual environment** before running
2. **Check Python version** (3.8+ required)
3. **Verify file permissions** for templates and output directories
4. **Check disk space** before project generation
5. **Update dependencies** if experiencing issues
6. **Use debug logging** to identify specific problems
7. **Test components individually** to isolate issues

Most issues can be resolved by following the systematic diagnostic steps outlined in this guide. If problems persist, the debugging tools and system information commands will help identify the root cause.
