# Project Architect - Template Guide

This guide explains how to understand, use, and customize Project Architect templates. Templates are the foundation of the project generation system, defining the structure, content, and configuration of generated projects.

## Table of Contents

1. [Understanding Templates](#understanding-templates)
2. [Template Structure](#template-structure)
3. [Using Existing Templates](#using-existing-templates)
4. [Customizing Templates](#customizing-templates)
5. [Creating New Templates](#creating-new-templates)
6. [Template Variables](#template-variables)
7. [Advanced Features](#advanced-features)

## Understanding Templates

### What is a Template?

A template is a blueprint that defines:
- **Project Structure** - Directories and files to create
- **File Contents** - Template files with variable substitution
- **Dependencies** - Required packages and tools
- **Configuration** - Development environment setup
- **Questions** - Interactive questionnaire for customization

### Template Components

Each template consists of:
1. **template.yaml** - Template configuration and structure definition
2. **questionnaire.json** - Interactive questions for user input
3. **Template Files (.j2)** - Jinja2 templates for file generation
4. **Static Files** - Files copied as-is without modification

## Template Structure

### Directory Layout

```
project_architect/templates/desktop_gui/
├── template.yaml           # Template configuration
├── questionnaire.json      # User questionnaire
├── main.py.j2             # Main application template
├── README.md.j2           # README template
├── requirements.txt.j2    # Dependencies template
├── src/
│   ├── main_window.py.j2  # GUI window template
│   ├── config.py.j2       # Configuration template
│   └── utils.py.j2        # Utilities template
├── tests/
│   └── test_main.py.j2    # Test template
└── docs/
    └── API_Reference.md.j2 # Documentation template
```

### Template Configuration (template.yaml)

```yaml
template:
  name: "Desktop GUI Application"
  type: "desktop_gui"
  description: "Professional desktop application with modern GUI"
  version: "1.0.0"
  author: "Project Architect"

# Project structure definition
structure:
  - path: "src"
    type: "directory"
  - path: "main.py"
    type: "file"
    template: "main.py.j2"
  - path: "requirements.txt"
    type: "file"
    template: "requirements.txt.j2"

# Framework-specific requirements
requirements:
  base:
    - "python>=3.8"
  customtkinter:
    - "customtkinter>=5.2.2"
    - "pillow>=10.0.0"
  testing:
    - "pytest>=7.4.0"
    - "pytest-cov>=4.1.0"
```

### Questionnaire Configuration (questionnaire.json)

```json
{
  "questionnaire": {
    "name": "Desktop GUI Application Questionnaire",
    "description": "Gather requirements for desktop application",
    "version": "1.0.0"
  },
  "questions": [
    {
      "id": "project_name",
      "type": "text",
      "prompt": "What is the name of your project?",
      "description": "Enter a descriptive name",
      "required": true,
      "section": "project_basics",
      "order": 1
    },
    {
      "id": "gui_framework",
      "type": "choice",
      "prompt": "Which GUI framework?",
      "options": ["customtkinter", "pyqt6", "tkinter"],
      "default": "customtkinter",
      "section": "technical_stack",
      "order": 10
    }
  ]
}
```

## Using Existing Templates

### Available Templates

Project Architect includes these built-in templates:

#### Desktop GUI Application
- **Purpose** - Desktop applications with graphical interfaces
- **Frameworks** - CustomTkinter, PyQt6, Tkinter, Kivy
- **Features** - Modern GUI, database support, configuration management
- **Best For** - Business applications, utilities, tools

#### Web Application (Coming Soon)
- **Purpose** - Web-based applications and services
- **Frameworks** - Node.js, Express, HTML/CSS/JavaScript
- **Features** - RESTful APIs, database integration, responsive design
- **Best For** - Web services, dashboards, online tools

#### CLI Tool (Coming Soon)
- **Purpose** - Command-line applications and utilities
- **Features** - Argument parsing, configuration files, cross-platform
- **Best For** - System utilities, automation scripts, data processing

### Selecting Templates

When creating a new project:
1. **Browse Available Templates** - View all installed templates
2. **Read Descriptions** - Understand what each template provides
3. **Check Requirements** - Ensure you have necessary dependencies
4. **Consider Project Needs** - Match template features to your requirements

### Template Customization During Generation

Templates can be customized through:
- **Questionnaire Responses** - Your answers shape the generated project
- **Conditional Logic** - Questions appear based on previous answers
- **Framework Selection** - Choose specific technologies within templates
- **Feature Toggles** - Enable/disable optional features

## Customizing Templates

### Modifying Existing Templates

#### 1. Locate Template Files
```bash
cd project_architect/templates/desktop_gui/
```

#### 2. Edit Template Configuration
Modify `template.yaml` to:
- Add new file/directory structures
- Change default requirements
- Update template metadata

#### 3. Customize Questionnaire
Edit `questionnaire.json` to:
- Add new questions
- Modify existing questions
- Change question order or sections

#### 4. Update Template Files
Modify `.j2` files to:
- Change generated code structure
- Add new functionality
- Customize documentation

### Example: Adding a New Feature

Let's add logging configuration to the desktop GUI template:

#### 1. Add Question to questionnaire.json
```json
{
  "id": "log_level",
  "type": "choice",
  "prompt": "Default logging level?",
  "options": ["DEBUG", "INFO", "WARNING", "ERROR"],
  "default": "INFO",
  "section": "features",
  "order": 25
}
```

#### 2. Update Template File
In `src/config.py.j2`:
```python
import logging

class AppConfig:
    def __init__(self):
        self.log_level = logging.{{ log_level }}
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(level=self.log_level)
```

#### 3. Add to Structure
In `template.yaml`:
```yaml
structure:
  - path: "logs"
    type: "directory"
```

## Creating New Templates

### Step 1: Create Template Directory

```bash
mkdir project_architect/templates/my_template
cd project_architect/templates/my_template
```

### Step 2: Create Configuration Files

#### template.yaml
```yaml
template:
  name: "My Custom Template"
  type: "my_template"
  description: "Custom template for my specific needs"
  version: "1.0.0"

structure:
  - path: "src"
    type: "directory"
  - path: "main.py"
    type: "file"
    template: "main.py.j2"

requirements:
  base:
    - "python>=3.8"
```

#### questionnaire.json
```json
{
  "questionnaire": {
    "name": "My Template Questionnaire",
    "version": "1.0.0"
  },
  "questions": [
    {
      "id": "project_name",
      "type": "text",
      "prompt": "Project name?",
      "required": true
    }
  ]
}
```

### Step 3: Create Template Files

#### main.py.j2
```python
#!/usr/bin/env python3
"""
{{ project_name }} - Main Application

{{ project_description }}

Author: {{ author_name }}
Created: {{ current_date }}
"""

def main():
    print("Hello from {{ project_name }}!")

if __name__ == "__main__":
    main()
```

### Step 4: Test Your Template

1. **Restart Project Architect** - Templates are loaded at startup
2. **Create Test Project** - Use your new template
3. **Verify Output** - Check generated project structure
4. **Iterate** - Refine based on results

## Template Variables

### Built-in Variables

Templates have access to these variables:

#### User Input
- `{{ project_name }}` - Project name from questionnaire
- `{{ project_description }}` - Project description
- `{{ author_name }}` - Author name
- `{{ author_email }}` - Author email
- All questionnaire responses by ID

#### Derived Variables
- `{{ project_name_snake }}` - snake_case version
- `{{ project_name_pascal }}` - PascalCase version
- `{{ project_name_camel }}` - camelCase version
- `{{ project_name_kebab }}` - kebab-case version

#### Date/Time
- `{{ current_date }}` - Current date (YYYY-MM-DD)
- `{{ current_time }}` - Current time (HH:MM:SS)
- `{{ current_year }}` - Current year
- `{{ current_month }}` - Current month name

#### System Information
- `{{ python_version }}` - Python version
- `{{ platform }}` - Operating system platform

### Custom Filters

Templates support custom Jinja2 filters:

```python
# Convert to different cases
{{ "my project" | snake_case }}     # my_project
{{ "my project" | pascal_case }}    # MyProject
{{ "my project" | camel_case }}     # myProject
{{ "my project" | kebab_case }}     # my-project

# Date formatting
{{ current_date | date_format("%B %d, %Y") }}  # October 04, 2025

# Text manipulation
{{ long_text | indent(4) }}         # Indent by 4 spaces
{{ text | title_case }}             # Title Case
```

### Conditional Logic

Use Jinja2 conditionals for dynamic content:

```python
{% if gui_framework == "customtkinter" %}
import customtkinter as ctk
{% elif gui_framework == "pyqt6" %}
from PyQt6.QtWidgets import QApplication
{% endif %}

{% if has_database %}
import sqlite3
{% endif %}

# List iteration
{% for feature in selected_features %}
# Enable {{ feature }}
{% endfor %}
```

## Advanced Features

### Template Inheritance

Create base templates that others can extend:

#### base_template.yaml
```yaml
template:
  name: "Base Template"
  type: "base"
  
structure:
  - path: "README.md"
    type: "file"
    template: "README.md.j2"
```

#### specialized_template.yaml
```yaml
template:
  name: "Specialized Template"
  type: "specialized"
  extends: "base"
  
structure:
  - path: "specialized.py"
    type: "file"
    template: "specialized.py.j2"
```

### Dynamic Requirements

Generate requirements based on user choices:

```yaml
requirements:
  base:
    - "python>=3.8"
  
  # Conditional requirements
  "{{ gui_framework }}":
    - "customtkinter>=5.2.2"  # if gui_framework == "customtkinter"
    - "PyQt6>=6.5.0"          # if gui_framework == "pyqt6"
  
  {% if has_database %}
  database:
    - "sqlalchemy>=2.0.0"
  {% endif %}
```

### Multi-file Templates

Create complex file structures:

```yaml
structure:
  - path: "src/models"
    type: "directory"
  
  {% for model in data_models %}
  - path: "src/models/{{ model.name | snake_case }}.py"
    type: "file"
    template: "model.py.j2"
    context:
      model_name: "{{ model.name }}"
      fields: "{{ model.fields }}"
  {% endfor %}
```

### Template Validation

Add validation to ensure template integrity:

```python
# In template.yaml
validation:
  required_questions:
    - "project_name"
    - "author_name"
  
  file_checks:
    - path: "main.py"
      must_exist: true
    - path: "requirements.txt"
      must_contain: "python"
```

## Best Practices

### Template Design

1. **Keep It Simple** - Start with basic functionality
2. **Make It Flexible** - Use questionnaires for customization
3. **Follow Conventions** - Use standard project structures
4. **Document Everything** - Include comprehensive documentation
5. **Test Thoroughly** - Test with various input combinations

### File Organization

1. **Logical Structure** - Group related files together
2. **Clear Naming** - Use descriptive file and directory names
3. **Consistent Patterns** - Follow naming conventions
4. **Separate Concerns** - Keep templates focused on specific aspects

### Variable Usage

1. **Meaningful Names** - Use descriptive variable names
2. **Consistent Casing** - Use appropriate case for context
3. **Default Values** - Provide sensible defaults
4. **Validation** - Validate user input appropriately

### Maintenance

1. **Version Templates** - Track template versions
2. **Update Regularly** - Keep dependencies current
3. **Backward Compatibility** - Consider existing projects
4. **Document Changes** - Maintain change logs

## Troubleshooting

### Common Issues

**Template Not Found**
- Check template directory exists
- Verify template.yaml is present and valid
- Restart Project Architect after adding templates

**Generation Fails**
- Check Jinja2 syntax in template files
- Verify all referenced variables exist
- Check file permissions

**Missing Variables**
- Ensure questionnaire provides all needed variables
- Check variable names match exactly
- Use default values for optional variables

**Invalid YAML/JSON**
- Validate configuration files
- Check indentation and syntax
- Use online validators if needed

### Debugging Templates

1. **Check Logs** - Look in logs/ directory for errors
2. **Test Variables** - Add debug output to templates
3. **Validate Syntax** - Check Jinja2 and YAML/JSON syntax
4. **Incremental Testing** - Test small changes at a time

Templates are the heart of Project Architect's power and flexibility. Master them, and you'll be able to generate exactly the projects you need, every time!
