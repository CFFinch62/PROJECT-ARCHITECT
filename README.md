# Project Architect

A comprehensive project template system that generates well-structured, documented, and AI-friendly development projects based on proven best practices and organizational patterns.

## Overview

Project Architect helps developers create new projects with consistent structure, comprehensive documentation, and built-in quality assurance tools. Based on the successful patterns from the Service Center project, it ensures every new project starts with professional organization and AI-friendly documentation.

## Features

### Core Functionality
- **Interactive Questionnaire** - Guided prompts to gather project requirements
- **Multiple Project Templates** - Pre-configured templates for different project types
- **Comprehensive Documentation Generation** - Auto-generates all essential project documents
- **AI-Friendly Structure** - Optimized for AI assistant collaboration
- **Quality Assurance Integration** - Built-in testing frameworks and code quality tools

### Project Types Supported
1. **Desktop GUI Application** - CustomTkinter/PyQt-based applications
2. **Web Application** - Node.js/HTML-based web projects
3. **CLI Tool/Utility** - Command-line applications and utilities
4. **Game Development** - Game projects with appropriate structure
5. **Marine Electronics Tool** - Specialized marine electronics applications
6. **Educational Software** - Learning and educational applications
7. **Data Analysis/Visualization** - Data science and analysis projects

### Generated Documentation
- **README.md** - Project overview and setup instructions
- **CHANGELOG.md** - Version history tracking
- **IMPLEMENTATION_PLAN.md** - Phase-based development roadmap
- **TECHNICAL_SPECIFICATION.md** - Comprehensive technical requirements
- **AI_CONTEXT.md** - Project context for AI assistants
- **CODING_STANDARDS.md** - Project-specific coding guidelines
- **DEV_RULES.md** - Development rules and best practices
- **DEV_PROCESS.md** - Standardized development workflow

## Technology Stack

- **Language**: Python 3.12+
- **GUI Framework**: CustomTkinter 5.2.2
- **Template Engine**: Jinja2 3.1.2
- **Configuration**: YAML/JSON-based templates
- **Version Control**: Git integration
- **Platform**: Cross-platform (Windows, Mac, Linux)

## Project Structure

```
Project Architect/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── project_architect/               # Main application package
│   ├── core/                        # Core functionality
│   │   ├── questionnaire.py         # Interactive questionnaire system
│   │   ├── template_engine.py       # Template processing engine
│   │   ├── project_generator.py     # Project structure generation
│   │   └── documentation_builder.py # Documentation generation
│   ├── templates/                   # Project templates
│   │   ├── desktop_gui/             # Desktop GUI application template
│   │   ├── web_app/                 # Web application template
│   │   ├── cli_tool/                # CLI tool template
│   │   ├── game/                    # Game development template
│   │   ├── marine_electronics/      # Marine electronics template
│   │   ├── educational/             # Educational software template
│   │   └── data_analysis/           # Data analysis template
│   ├── gui/                         # GUI components
│   │   ├── main_window.py           # Main application window
│   │   ├── questionnaire_dialog.py  # Questionnaire interface
│   │   └── project_browser.py       # Project template browser
│   ├── config/                      # Configuration management
│   │   ├── settings.py              # Application settings
│   │   ├── user_profiles.py         # User profile management
│   │   └── template_config.py       # Template configuration
│   └── utils/                       # Utility functions
│       ├── file_operations.py       # File and directory operations
│       ├── git_integration.py       # Git repository management
│       └── validation.py            # Input validation
├── tests/                           # Unit tests
├── docs/                            # Documentation
├── dev_sessions/                    # Development session logs
├── data/                            # Application data
│   ├── user_profiles.json           # User profile storage
│   └── project_history.json         # Generated project history
└── assets/                          # Application assets
    ├── icons/                       # Application icons
    └── templates/                   # Document templates
```

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Git (for repository initialization)
- pip (Python package manager)

### Installation

1. **Navigate to Project Architect directory**
2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   ```
3. **Activate virtual environment**:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run Project Architect**:
   ```bash
   python main.py
   ```

## Usage

1. **Launch Project Architect**
2. **Select Project Type** from available templates
3. **Complete Interactive Questionnaire** with project details
4. **Choose Output Directory** for new project
5. **Generate Project** - creates complete project structure
6. **Review Generated Files** and begin development

## Generated Project Features

### Standard Structure
- Organized folder hierarchy (src/, tests/, docs/, dev_sessions/)
- Professional documentation suite
- Git repository initialization
- Virtual environment setup
- Requirements management

### Quality Assurance
- Pre-configured testing framework
- Code quality tools (linting, formatting)
- Pre-commit hooks
- Continuous integration templates

### AI-Friendly Design
- Comprehensive context documentation
- Clear architecture descriptions
- Standardized coding patterns
- Detailed technical specifications

## Development

### Adding New Templates
1. Create template directory in `project_architect/templates/`
2. Define template configuration in YAML
3. Create template files with Jinja2 placeholders
4. Add questionnaire questions for template-specific data
5. Test template generation

### Customization
- User profiles for preferred configurations
- Custom template creation
- Configurable documentation styles
- Extensible questionnaire system

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Current Status

**Version**: 1.0.0 (In Development)
**Status**: Initial Implementation Phase
**Next Steps**: Core functionality development

## License

Proprietary - All rights reserved

## Support

For questions or issues, please contact the development team.
