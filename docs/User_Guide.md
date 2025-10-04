# Project Architect - User Guide

Welcome to Project Architect, a comprehensive project template system that generates well-structured, documented, and AI-friendly development projects. This guide will walk you through all the features and capabilities of the system.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating New Projects](#creating-new-projects)
3. [Updating Existing Projects](#updating-existing-projects)
4. [Working with Templates](#working-with-templates)
5. [Project Types](#project-types)
6. [Advanced Features](#advanced-features)
7. [Best Practices](#best-practices)

## Getting Started

### First Launch

When you first launch Project Architect, you'll see the welcome screen with:
- **Quick Start section** with available project types
- **Recent Projects** (empty initially)
- **Sidebar** with main actions

### Main Interface

The interface consists of:
- **Header** - Application title and settings button
- **Sidebar** - Main navigation and actions
- **Content Area** - Tabbed interface for different views
- **Status Bar** - Progress indicators and status messages

## Creating New Projects

### Step 1: Choose Project Type

Click **"🆕 Start New Project"** or select a project type from the welcome screen:

- **Desktop GUI Application** - CustomTkinter, PyQt6, Tkinter, or Kivy
- **Web Application** - Node.js/HTML-based web projects
- **CLI Tool/Utility** - Command-line applications
- **Game Development** - Game projects with appropriate structure
- **Marine Electronics Tool** - Specialized marine electronics applications
- **Educational Software** - Learning and educational applications
- **Data Analysis/Visualization** - Data science and analysis projects

### Step 2: Complete the Questionnaire

The questionnaire is organized into sections:

#### Project Basics
- **Project Name** - Descriptive name for your application
- **Description** - Brief description of what the project does
- **Version** - Initial version number (defaults to 1.0.0)
- **Author Information** - Your name and email
- **Organization** - Company or organization name (optional)

#### Technical Stack
- **GUI Framework** - Choose your preferred framework
- **Theme Settings** - Dark/light theme and color scheme
- **Window Properties** - Resizable, minimum resolution
- **Database Requirements** - SQLite, PostgreSQL, MySQL, MongoDB

#### Features
- **Configuration Files** - JSON, YAML, INI, or TOML format
- **Logging** - Comprehensive logging with configurable levels
- **User Interface Elements** - Menu bar, toolbar, status bar
- **Additional Features** - Based on project type

#### Quality Assurance
- **Testing Framework** - pytest with coverage reporting
- **Code Quality Tools** - Black formatting, flake8/pylint linting
- **Type Checking** - MyPy static type analysis

#### Development Setup
- **Virtual Environment** - Automatic venv creation
- **Git Repository** - Initialize with initial commit
- **GitHub Integration** - Create repository with GitHub CLI

### Step 3: Generate Project

1. **Review Answers** - Check your responses for accuracy
2. **Select Output Directory** - Choose where to create the project
3. **Generate** - Click generate to create the project structure

### What Gets Generated

Every project includes:

#### Core Structure
```
YourProject/
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── setup.py                   # Package setup
├── src/                       # Source code
│   ├── __init__.py
│   ├── main_window.py         # Main GUI window
│   ├── config.py              # Configuration management
│   └── utils.py               # Utility functions
├── tests/                     # Unit tests
├── docs/                      # Documentation
└── dev_sessions/              # Development session logs
```

#### Documentation Suite
- **README.md** - Project overview and setup instructions
- **CHANGELOG.md** - Version history tracking
- **IMPLEMENTATION_PLAN.md** - Development roadmap
- **TECHNICAL_SPECIFICATION.md** - Detailed requirements
- **AI_CONTEXT.md** - AI assistant collaboration guide
- **CODING_STANDARDS.md** - Project-specific coding guidelines
- **DEV_RULES.md** - Development rules and best practices
- **DEV_PROCESS.md** - Standardized development workflow

#### Development Tools
- **Virtual Environment** - Isolated Python environment
- **Git Repository** - Version control with initial commit
- **Quality Tools** - Linting, formatting, and testing setup
- **IDE Configuration** - VS Code and PyCharm settings

## Updating Existing Projects

Project Architect's unique feature is the ability to update existing projects through additional interviews.

### Opening a Project

1. Click **"📂 Open Project"**
2. Select the project directory
3. Project Architect loads the project metadata and history

### Types of Updates

#### Technical Specification Updates
- **Purpose** - Modify project requirements and specifications
- **Process** - Guided interview focusing on requirement changes
- **Output** - Updated TECHNICAL_SPECIFICATION.md with change history

#### Feature Addition
- **Purpose** - Add new features to existing projects
- **Process** - Detailed feature specification interview
- **Output** - Updated documentation and implementation plan

#### Architecture Changes
- **Purpose** - Modify project architecture or technology stack
- **Process** - Architecture-focused questionnaire
- **Output** - Updated technical documentation and migration plan

### Update Process

1. **Load Project** - Open existing project to load current state
2. **Select Update Type** - Choose the type of update needed
3. **Complete Interview** - Answer questions about the changes
4. **Review Changes** - See what will be modified
5. **Apply Updates** - Generate updated documentation

### Version Management

- **Automatic Versioning** - Increments version numbers automatically
- **Change Tracking** - Complete audit trail of all modifications
- **Update History** - Detailed history of all project updates
- **Rollback Support** - Ability to see previous versions

## Working with Templates

### Understanding Templates

Templates define:
- **Project Structure** - Directories and files to create
- **File Contents** - Template files with variable substitution
- **Dependencies** - Required Python packages
- **Configuration** - Development tools and settings

### Template Components

#### Template Configuration (template.yaml)
```yaml
template:
  name: "Desktop GUI Application"
  type: "desktop_gui"
  description: "Professional desktop application"
  
structure:
  - path: "src"
    type: "directory"
  - path: "main.py"
    type: "file"
    template: "main.py.j2"
```

#### Questionnaire (questionnaire.json)
```json
{
  "questions": [
    {
      "id": "project_name",
      "type": "text",
      "prompt": "What is the name of your project?",
      "required": true
    }
  ]
}
```

#### Template Files (.j2 files)
Jinja2 templates with variable substitution:
```python
# {{ project_name }} - Main Application
# Author: {{ author_name }}
# Created: {{ current_date }}

class {{ project_name_pascal }}App:
    def __init__(self):
        self.name = "{{ project_name }}"
```

### Available Variables

Templates have access to:
- **User Responses** - All questionnaire answers
- **Derived Variables** - project_name_snake, project_name_pascal, etc.
- **Date/Time** - current_date, current_year, etc.
- **System Info** - Platform-specific information

## Project Types

### Desktop GUI Application

**Best For**: Desktop applications with graphical interfaces

**Features**:
- Multiple GUI frameworks (CustomTkinter, PyQt6, Tkinter, Kivy)
- Professional window management
- Theme and styling support
- Database integration options
- Comprehensive testing setup

**Generated Structure**:
- Modern GUI architecture
- Configuration management
- Logging system
- Quality assurance tools

### Web Application

**Best For**: Web-based applications and services

**Features**:
- Node.js/Express backend
- HTML/CSS/JavaScript frontend
- Database integration
- API development support
- Responsive design

### CLI Tool/Utility

**Best For**: Command-line applications and utilities

**Features**:
- Argument parsing
- Configuration file support
- Logging and error handling
- Cross-platform compatibility
- Package distribution setup

### Game Development

**Best For**: Game projects and interactive applications

**Features**:
- Game engine integration
- Asset management
- Scene/level organization
- Input handling
- Performance optimization

### Marine Electronics Tool

**Best For**: Specialized marine electronics applications

**Features**:
- Marine-specific libraries
- Data acquisition support
- Instrument communication
- Chart and navigation support
- Real-time data processing

### Educational Software

**Best For**: Learning and educational applications

**Features**:
- User progress tracking
- Content management
- Assessment tools
- Accessibility features
- Multi-user support

### Data Analysis/Visualization

**Best For**: Data science and analysis projects

**Features**:
- Scientific computing libraries
- Data visualization tools
- Jupyter notebook integration
- Statistical analysis support
- Report generation

## Advanced Features

### AI-Friendly Documentation

Every generated project includes:
- **AI_CONTEXT.md** - Project context optimized for AI assistants
- **Structured Documentation** - Consistent format for AI parsing
- **Clear Architecture** - Well-documented code organization
- **Development Patterns** - Standardized coding patterns

### Quality Assurance Integration

- **Automated Testing** - pytest with coverage reporting
- **Code Formatting** - Black for consistent code style
- **Linting** - flake8 and pylint for code quality
- **Type Checking** - MyPy for static type analysis
- **Pre-commit Hooks** - Automated quality checks

### Development Workflow

- **Session Tracking** - Development session documentation
- **Progress Monitoring** - Implementation plan tracking
- **Change Management** - Comprehensive change history
- **Documentation Updates** - Automatic documentation maintenance

## Best Practices

### Project Creation

1. **Plan First** - Think through requirements before starting
2. **Choose Appropriate Type** - Select the template that best fits your needs
3. **Complete Questionnaire Thoroughly** - Provide detailed, accurate information
4. **Review Generated Structure** - Understand the created project layout
5. **Customize as Needed** - Modify templates for specific requirements

### Project Updates

1. **Regular Updates** - Keep project documentation current
2. **Document Changes** - Use the update system for all modifications
3. **Version Consistently** - Follow semantic versioning practices
4. **Track Dependencies** - Monitor and update dependencies regularly
5. **Maintain Quality** - Run tests and quality checks regularly

### Multi-PC Development

1. **Sync Source Code** - Keep code synchronized across PCs
2. **Individual Environments** - Each PC should have its own virtual environment
3. **Consistent Setup** - Use the setup scripts on each PC
4. **Share Settings** - Sync the data/ directory for consistent settings
5. **Document Environment** - Note any PC-specific requirements

### Template Customization

1. **Start with Existing** - Modify existing templates rather than creating from scratch
2. **Test Thoroughly** - Test templates with various input combinations
3. **Document Changes** - Document any template modifications
4. **Version Templates** - Track template versions and changes
5. **Share Improvements** - Consider contributing improvements back

## Troubleshooting

### Common Issues

**Application Won't Start**
- Check Python version (3.8+ required)
- Verify virtual environment is activated
- Ensure all dependencies are installed

**Template Not Found**
- Check template directory structure
- Verify template.yaml exists and is valid
- Check questionnaire.json format

**Generation Fails**
- Review questionnaire responses for errors
- Check output directory permissions
- Verify template files are accessible

**Update Process Fails**
- Ensure project has Project Architect metadata
- Check project directory structure
- Verify write permissions

### Getting Help

1. **Check Logs** - Look in logs/ directory for error details
2. **Review Documentation** - Check relevant documentation sections
3. **Verify Setup** - Run setup scripts again if needed
4. **Test Basic Functionality** - Try creating a simple test project

## Next Steps

After mastering the basics:

1. **Explore Advanced Features** - Try project updates and customization
2. **Create Custom Templates** - Develop templates for your specific needs
3. **Integrate with Workflow** - Incorporate into your development process
4. **Share and Collaborate** - Use with team members and share improvements

Project Architect is designed to grow with your needs and streamline your development process. The more you use it, the more time you'll save on project setup and maintenance!
