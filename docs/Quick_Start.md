# Project Architect - Quick Start Guide

Get up and running with Project Architect in just a few minutes! This guide will walk you through creating your first project.

## Prerequisites

- Python 3.8 or higher
- 10 minutes of your time
- A project idea (or use our example)

## Step 1: Setup (2 minutes)

### Automated Setup

**Linux/Mac:**
```bash
cd "Project Architect"
./setup_venv.sh
```

**Windows:**
```cmd
cd "Project Architect"
setup_venv.bat
```

### Manual Setup (if automated fails)
```bash
# Create virtual environment
python3 -m venv venv  # Linux/Mac
python -m venv venv   # Windows

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Launch Project Architect (30 seconds)

**Using run scripts:**
```bash
./run.sh     # Linux/Mac
run.bat      # Windows
```

**Manual launch:**
```bash
# Activate venv first, then:
python3 main.py  # Linux/Mac
python main.py   # Windows
```

## Step 3: Create Your First Project (5 minutes)

### Example Project: Task Manager

Let's create a simple desktop task manager application.

1. **Click "🆕 Start New Project"** or select "Desktop Gui" from the welcome screen

2. **Fill out the questionnaire:**

   **Project Basics:**
   - Project Name: `My Task Manager`
   - Description: `A simple desktop task management application`
   - Version: `1.0.0` (default)
   - Author Name: `Your Name`
   - Author Email: `your.email@example.com` (optional)

   **Technical Stack:**
   - GUI Framework: `customtkinter` (recommended)
   - App Theme: `dark`
   - Color Scheme: `blue`
   - Window Resizable: `Yes`
   - Minimum Resolution: `1366x768`

   **Features:**
   - Database: `Yes` → SQLite
   - Configuration Files: `Yes` → JSON
   - Logging: `Yes` → INFO level
   - Menu Bar: `Yes`
   - Toolbar: `Yes`
   - Status Bar: `Yes`

   **Quality Assurance:**
   - Unit Testing: `Yes`
   - Test Coverage: `Yes`
   - Code Linting: `Yes`
   - Code Formatting: `Yes`
   - Type Checking: `Yes`

   **Development Setup:**
   - Create Virtual Environment: `Yes`
   - Initialize Git: `Yes`
   - Create GitHub Repo: `No` (for now)

3. **Select Output Directory:**
   - Choose where you want the project created
   - Click "Generate Project"

4. **Wait for Generation:**
   - Watch the progress bar
   - Generation typically takes 30-60 seconds

## Step 4: Explore Your Generated Project (2 minutes)

Navigate to your project directory. You'll find:

```
My Task Manager/
├── main.py                     # 🚀 Run this to start your app
├── requirements.txt            # 📦 Dependencies
├── README.md                   # 📖 Project documentation
├── TECHNICAL_SPECIFICATION.md  # 📋 Detailed requirements
├── src/                        # 💻 Your source code
│   ├── main_window.py         # 🖼️ Main GUI window
│   ├── config.py              # ⚙️ Configuration management
│   └── utils.py               # 🔧 Utility functions
├── tests/                      # 🧪 Unit tests
├── docs/                       # 📚 Documentation
├── dev_sessions/              # 📝 Development logs
└── venv/                      # 🐍 Virtual environment
```

## Step 5: Run Your New Application (1 minute)

```bash
cd "My Task Manager"

# Activate the project's virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run your application
python3 main.py  # Linux/Mac
python main.py   # Windows
```

**🎉 Congratulations!** You should see your new Task Manager application window open.

## What You Get Out of the Box

### Professional Application Structure
- ✅ Modern GUI with CustomTkinter
- ✅ Configuration management
- ✅ Logging system
- ✅ Database integration ready
- ✅ Error handling

### Complete Documentation
- ✅ README with setup instructions
- ✅ Technical specification
- ✅ Implementation plan
- ✅ AI-friendly documentation
- ✅ Development workflow guides

### Quality Assurance
- ✅ Unit testing framework (pytest)
- ✅ Code formatting (Black)
- ✅ Linting (flake8, pylint)
- ✅ Type checking (MyPy)
- ✅ Test coverage reporting

### Development Tools
- ✅ Virtual environment
- ✅ Git repository with initial commit
- ✅ IDE configuration (VS Code, PyCharm)
- ✅ Development session tracking

## Next Steps

### Immediate (5 minutes)
1. **Explore the Code** - Look at `src/main_window.py` to see the GUI structure
2. **Read the README** - Understand the project structure and features
3. **Run Tests** - Execute `pytest` to see the testing framework
4. **Check Documentation** - Review the generated technical specification

### Short Term (30 minutes)
1. **Customize the GUI** - Modify `main_window.py` to add your features
2. **Add Database Models** - Create your task data structures
3. **Implement Core Features** - Add task creation, editing, deletion
4. **Write Tests** - Add tests for your new functionality

### Long Term (ongoing)
1. **Use Update System** - When requirements change, use Project Architect's update feature
2. **Maintain Documentation** - Keep the technical specification current
3. **Track Development** - Use the dev_sessions folder for progress tracking
4. **Share and Collaborate** - Use the AI-friendly documentation for team collaboration

## Common First-Time Issues

### "Python not found"
**Solution:** Install Python 3.8+ and ensure it's in your PATH

### "Permission denied" on scripts
**Linux/Mac:** Run `chmod +x setup_venv.sh run.sh`
**Windows:** Run Command Prompt as Administrator

### "Module not found" errors
**Solution:** Ensure virtual environment is activated and dependencies installed

### GUI doesn't appear
**Linux:** May need `sudo apt install python3-tk`
**Check:** Display environment variables

## Quick Commands Reference

```bash
# Setup (run once per PC)
./setup_venv.sh          # Linux/Mac
setup_venv.bat           # Windows

# Daily usage
./run.sh                 # Linux/Mac
run.bat                  # Windows

# Manual activation
source venv/bin/activate # Linux/Mac
venv\Scripts\activate    # Windows

# Run tests
pytest

# Format code
black .

# Check code quality
flake8 .
pylint src/
```

## Example Projects to Try

### Beginner Projects
1. **Todo List** - Simple task management
2. **Note Taker** - Text editor with save/load
3. **Calculator** - Basic arithmetic calculator
4. **File Organizer** - Organize files by type/date

### Intermediate Projects
1. **Expense Tracker** - Personal finance management
2. **Inventory System** - Track items and quantities
3. **Contact Manager** - Address book application
4. **Time Tracker** - Log time spent on activities

### Advanced Projects
1. **Project Manager** - Full project management suite
2. **Data Visualizer** - Charts and graphs from data
3. **System Monitor** - Display system performance
4. **Network Tool** - Network diagnostics and monitoring

## Getting Help

- **Documentation** - Check the `docs/` folder for detailed guides
- **Logs** - Look in `logs/` directory for error messages
- **Examples** - Study the generated code structure
- **Templates** - Examine template files in `project_architect/templates/`

## Pro Tips

1. **Start Simple** - Begin with basic functionality, add complexity later
2. **Use the Update System** - When requirements change, use Project Architect's update feature
3. **Follow the Structure** - The generated structure is optimized for maintainability
4. **Document Changes** - Use the dev_sessions folder to track your progress
5. **Test Early** - Run tests frequently to catch issues early

**Ready to build something amazing? Your professional development environment is just a few clicks away!** 🚀
