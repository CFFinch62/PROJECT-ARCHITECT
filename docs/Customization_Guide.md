# Project Architect - Customization Guide

This guide explains how to customize Project Architect to meet your specific needs, including creating custom templates, modifying questionnaires, and extending functionality.

## Table of Contents

1. [Overview](#overview)
2. [User Profiles](#user-profiles)
3. [Custom Templates](#custom-templates)
4. [Questionnaire Customization](#questionnaire-customization)
5. [GUI Customization](#gui-customization)
6. [Advanced Customization](#advanced-customization)

## Overview

Project Architect is designed to be highly customizable, allowing you to:

- **Create Custom Templates** - Build templates for your specific project types
- **Modify Questionnaires** - Customize questions and validation rules
- **Configure User Profiles** - Set up different configurations for different contexts
- **Extend Functionality** - Add new features and capabilities
- **Customize GUI** - Modify the user interface to match your preferences

## User Profiles

### Creating User Profiles

User profiles allow you to save different configurations for different contexts (work, personal, client projects, etc.).

#### Profile Configuration

Create profile files in `data/profiles/`:

```yaml
# data/profiles/work_profile.yaml
profile:
  name: "Work Profile"
  description: "Configuration for work projects"
  
defaults:
  author_name: "Your Name"
  author_email: "you@company.com"
  organization: "Your Company"
  license: "Proprietary"
  
preferences:
  default_gui_framework: "customtkinter"
  default_theme: "dark"
  create_github_repo: false
  enable_logging: true
  log_level: "INFO"
  
templates:
  preferred_order:
    - "desktop_gui"
    - "web_app"
    - "cli_tool"
  
quality_settings:
  enable_tests: true
  enable_coverage: true
  enable_linting: true
  enable_formatting: true
  coverage_threshold: 85
```

```yaml
# data/profiles/personal_profile.yaml
profile:
  name: "Personal Profile"
  description: "Configuration for personal projects"
  
defaults:
  author_name: "Your Name"
  author_email: "your.personal@email.com"
  organization: ""
  license: "MIT"
  
preferences:
  default_gui_framework: "customtkinter"
  default_theme: "light"
  create_github_repo: true
  github_visibility: "public"
  
templates:
  preferred_order:
    - "game_dev"
    - "desktop_gui"
    - "data_analysis"
```

#### Using Profiles

```python
# In your customization code
from project_architect.config import Settings

settings = Settings()
profile = settings.load_profile("work_profile")

# Apply profile defaults to questionnaire
questionnaire_engine.apply_profile_defaults(profile)
```

### Profile Management GUI

Add profile selection to the main window:

```python
# Custom profile selector
class ProfileSelector(ctk.CTkFrame):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings
        
        self.profile_var = ctk.StringVar()
        self.profile_dropdown = ctk.CTkComboBox(
            self,
            variable=self.profile_var,
            values=self.settings.get_available_profiles(),
            command=self.on_profile_change
        )
        self.profile_dropdown.pack(pady=10)
    
    def on_profile_change(self, selection):
        profile = self.settings.load_profile(selection)
        self.settings.set_active_profile(profile)
```

## Custom Templates

### Creating a New Template

#### Step 1: Create Template Directory

```bash
mkdir project_architect/templates/my_custom_template
cd project_architect/templates/my_custom_template
```

#### Step 2: Template Configuration

Create `template.yaml`:

```yaml
template:
  name: "My Custom Template"
  type: "my_custom_template"
  description: "Custom template for my specific needs"
  version: "1.0.0"
  author: "Your Name"
  
  # Template metadata
  category: "custom"
  tags: ["custom", "specialized"]
  
  # Minimum requirements
  min_python_version: "3.8"
  supported_platforms: ["windows", "linux", "macos"]

# Project structure definition
structure:
  # Directories
  - path: "src"
    type: "directory"
  - path: "src/core"
    type: "directory"
  - path: "src/utils"
    type: "directory"
  - path: "tests"
    type: "directory"
  - path: "docs"
    type: "directory"
  - path: "config"
    type: "directory"
  
  # Files from templates
  - path: "main.py"
    type: "file"
    template: "main.py.j2"
  - path: "src/__init__.py"
    type: "file"
    template: "src_init.py.j2"
  - path: "src/core/engine.py"
    type: "file"
    template: "core_engine.py.j2"
  - path: "config/settings.yaml"
    type: "file"
    template: "settings.yaml.j2"
  - path: "requirements.txt"
    type: "file"
    template: "requirements.txt.j2"
  
  # Static files (copied as-is)
  - path: ".gitignore"
    type: "static"
    source: "gitignore_template"

# Dependencies based on user choices
requirements:
  base:
    - "python>=3.8"
    - "pyyaml>=6.0"
  
  # Conditional requirements
  database:
    condition: "{{ has_database }}"
    packages:
      - "sqlalchemy>=2.0.0"
      - "alembic>=1.12.0"
  
  web_framework:
    condition: "{{ framework_type == 'web' }}"
    packages:
      - "fastapi>=0.104.0"
      - "uvicorn>=0.24.0"

# Post-generation hooks
hooks:
  post_generation:
    - command: "python -m pip install -e ."
      condition: "{{ install_in_dev_mode }}"
    - command: "git add ."
      condition: "{{ init_git }}"
    - command: "git commit -m 'Initial commit'"
      condition: "{{ init_git }}"
```

#### Step 3: Questionnaire Configuration

Create `questionnaire.json`:

```json
{
  "questionnaire": {
    "name": "My Custom Template Questionnaire",
    "description": "Gather requirements for custom project",
    "version": "1.0.0"
  },
  
  "sections": [
    {
      "id": "project_basics",
      "name": "Project Basics",
      "description": "Basic project information"
    },
    {
      "id": "technical_choices",
      "name": "Technical Choices",
      "description": "Technical configuration options"
    },
    {
      "id": "features",
      "name": "Features",
      "description": "Optional features to include"
    }
  ],
  
  "questions": [
    {
      "id": "project_name",
      "type": "text",
      "prompt": "What is the name of your project?",
      "description": "Enter a descriptive name for your project",
      "required": true,
      "section": "project_basics",
      "order": 1,
      "validation": {
        "min_length": 1,
        "max_length": 100,
        "pattern": "^[a-zA-Z0-9\\s\\-_]+$"
      }
    },
    
    {
      "id": "framework_type",
      "type": "choice",
      "prompt": "What type of framework do you need?",
      "description": "Choose the primary framework type",
      "options": ["desktop", "web", "cli", "library"],
      "default": "desktop",
      "section": "technical_choices",
      "order": 10
    },
    
    {
      "id": "has_database",
      "type": "boolean",
      "prompt": "Do you need database support?",
      "description": "Include database integration capabilities",
      "default": false,
      "section": "features",
      "order": 20
    },
    
    {
      "id": "database_type",
      "type": "choice",
      "prompt": "Which database type?",
      "description": "Select your preferred database",
      "options": ["sqlite", "postgresql", "mysql", "mongodb"],
      "default": "sqlite",
      "section": "features",
      "order": 21,
      "dependencies": ["has_database"],
      "condition": "{{ has_database == true }}"
    },
    
    {
      "id": "custom_feature",
      "type": "multiple_choice",
      "prompt": "Which custom features do you want?",
      "description": "Select all features you want to include",
      "options": [
        "Advanced logging",
        "Configuration management",
        "Plugin system",
        "API integration",
        "Caching layer"
      ],
      "section": "features",
      "order": 30
    }
  ]
}
```

#### Step 4: Template Files

Create template files with `.j2` extension:

**main.py.j2**:
```python
#!/usr/bin/env python3
"""
{{ project_name }} - Main Application

{{ project_description }}

Author: {{ author_name }}
Created: {{ current_date }}
Framework: {{ framework_type | title }}
"""

import logging
{% if has_database %}
from src.core.database import DatabaseManager
{% endif %}
from src.core.engine import {{ project_name | pascal_case }}Engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class {{ project_name | pascal_case }}App:
    """Main application class for {{ project_name }}."""
    
    def __init__(self):
        """Initialize the application."""
        self.name = "{{ project_name }}"
        self.version = "{{ version }}"
        {% if has_database %}
        self.db_manager = DatabaseManager("{{ database_type }}")
        {% endif %}
        self.engine = {{ project_name | pascal_case }}Engine()
        
        logger.info(f"Initialized {self.name} v{self.version}")
    
    def run(self):
        """Run the main application."""
        logger.info("Starting application...")
        
        try:
            {% if framework_type == "desktop" %}
            self._run_desktop_app()
            {% elif framework_type == "web" %}
            self._run_web_app()
            {% elif framework_type == "cli" %}
            self._run_cli_app()
            {% else %}
            self._run_library()
            {% endif %}
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise
        finally:
            self._cleanup()
    
    {% if framework_type == "desktop" %}
    def _run_desktop_app(self):
        """Run desktop application."""
        # Desktop app implementation
        print(f"Running {self.name} as desktop application")
    {% elif framework_type == "web" %}
    def _run_web_app(self):
        """Run web application."""
        # Web app implementation
        print(f"Running {self.name} as web application")
    {% elif framework_type == "cli" %}
    def _run_cli_app(self):
        """Run CLI application."""
        # CLI app implementation
        print(f"Running {self.name} as CLI application")
    {% else %}
    def _run_library(self):
        """Run as library."""
        # Library implementation
        print(f"Running {self.name} as library")
    {% endif %}
    
    def _cleanup(self):
        """Cleanup resources."""
        {% if has_database %}
        if hasattr(self, 'db_manager'):
            self.db_manager.close()
        {% endif %}
        logger.info("Application cleanup completed")


def main():
    """Main entry point."""
    app = {{ project_name | pascal_case }}App()
    app.run()


if __name__ == "__main__":
    main()
```

**requirements.txt.j2**:
```
# {{ project_name }} - Requirements
# Generated on {{ current_date }}

# Base requirements
python>={{ min_python_version | default("3.8") }}
pyyaml>=6.0.1

{% if has_database %}
# Database requirements
{% if database_type == "sqlite" %}
# SQLite is included with Python
{% elif database_type == "postgresql" %}
psycopg2-binary>=2.9.0
{% elif database_type == "mysql" %}
PyMySQL>=1.1.0
{% elif database_type == "mongodb" %}
pymongo>=4.5.0
{% endif %}
sqlalchemy>=2.0.0
alembic>=1.12.0
{% endif %}

{% if framework_type == "web" %}
# Web framework requirements
fastapi>=0.104.0
uvicorn>=0.24.0
jinja2>=3.1.0
{% elif framework_type == "desktop" %}
# Desktop GUI requirements
customtkinter>=5.2.2
pillow>=10.0.0
{% endif %}

{% if "Advanced logging" in custom_feature %}
# Advanced logging
colorlog>=6.7.0
{% endif %}

{% if "Configuration management" in custom_feature %}
# Configuration management
dynaconf>=3.2.0
{% endif %}

{% if "API integration" in custom_feature %}
# API integration
requests>=2.31.0
httpx>=0.25.0
{% endif %}

{% if "Caching layer" in custom_feature %}
# Caching
redis>=5.0.0
{% endif %}

# Development dependencies (install with: pip install -e .[dev])
[dev]
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.9.0
flake8>=6.1.0
mypy>=1.6.0
```

### Advanced Template Features

#### Conditional File Generation

```yaml
# In template.yaml
structure:
  - path: "src/database.py"
    type: "file"
    template: "database.py.j2"
    condition: "{{ has_database }}"
  
  - path: "src/web_routes.py"
    type: "file"
    template: "web_routes.py.j2"
    condition: "{{ framework_type == 'web' }}"
```

#### Dynamic Directory Structure

```yaml
structure:
  {% for model in data_models %}
  - path: "src/models/{{ model.name | snake_case }}.py"
    type: "file"
    template: "model.py.j2"
    context:
      model_name: "{{ model.name }}"
      fields: "{{ model.fields }}"
  {% endfor %}
```

#### Template Inheritance

Create base templates that others can extend:

```yaml
# base_python_template.yaml
template:
  name: "Base Python Template"
  type: "base_python"
  is_base: true

structure:
  - path: "README.md"
    type: "file"
    template: "README.md.j2"
  - path: ".gitignore"
    type: "static"
    source: "python_gitignore"
```

```yaml
# specialized_template.yaml
template:
  name: "Specialized Template"
  type: "specialized"
  extends: "base_python"

structure:
  - path: "specialized.py"
    type: "file"
    template: "specialized.py.j2"
```

## Questionnaire Customization

### Custom Question Types

Create new question types by extending the base system:

```python
# project_architect/core/custom_questions.py
from project_architect.core.questionnaire import Question, QuestionType
from enum import Enum

class CustomQuestionType(Enum):
    COLOR_PICKER = "color_picker"
    FILE_BROWSER = "file_browser"
    DEPENDENCY_SELECTOR = "dependency_selector"

class ColorPickerQuestion(Question):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = CustomQuestionType.COLOR_PICKER
        self.color_format = kwargs.get('color_format', 'hex')  # hex, rgb, hsl
    
    def validate_response(self, response):
        if self.color_format == 'hex':
            return re.match(r'^#[0-9A-Fa-f]{6}$', response) is not None
        # Add other format validations
        return True

class DependencySelectorQuestion(Question):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = CustomQuestionType.DEPENDENCY_SELECTOR
        self.package_registry = kwargs.get('package_registry', 'pypi')
    
    def get_available_packages(self):
        # Fetch available packages from registry
        return ["requests", "flask", "django", "fastapi"]
```

### Dynamic Question Generation

Generate questions based on external data:

```python
def generate_framework_questions(available_frameworks):
    """Generate questions for available frameworks."""
    questions = []
    
    # Main framework selection
    framework_question = {
        "id": "selected_framework",
        "type": "choice",
        "prompt": "Which framework would you like to use?",
        "options": list(available_frameworks.keys()),
        "section": "technical_stack"
    }
    questions.append(framework_question)
    
    # Framework-specific questions
    for framework, config in available_frameworks.items():
        for option in config.get('options', []):
            question = {
                "id": f"{framework}_{option['id']}",
                "type": option['type'],
                "prompt": option['prompt'],
                "condition": f"{{{{ selected_framework == '{framework}' }}}}",
                "section": "framework_config"
            }
            questions.append(question)
    
    return questions
```

### Validation Rules

Create custom validation rules:

```python
# project_architect/utils/custom_validators.py
import re
from typing import Any, Dict

class CustomValidators:
    @staticmethod
    def validate_semantic_version(version: str) -> bool:
        """Validate semantic version format."""
        pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
        return re.match(pattern, version) is not None
    
    @staticmethod
    def validate_python_package_name(name: str) -> bool:
        """Validate Python package name."""
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return re.match(pattern, name) is not None
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format."""
        pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?$'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def validate_license(license_name: str) -> bool:
        """Validate license name against known licenses."""
        known_licenses = [
            "MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause",
            "ISC", "LGPL-2.1", "MPL-2.0", "Unlicense"
        ]
        return license_name in known_licenses
```

## GUI Customization

### Custom Themes

Create custom color schemes:

```python
# project_architect/gui/themes.py
import customtkinter as ctk

class CustomThemes:
    DARK_BLUE = {
        "CTk": {
            "fg_color": ["gray95", "gray10"]
        },
        "CTkToplevel": {
            "fg_color": ["gray95", "gray10"]
        },
        "CTkFrame": {
            "corner_radius": 6,
            "border_width": 0,
            "fg_color": ["gray90", "gray13"],
            "top_fg_color": ["gray85", "gray16"],
            "border_color": ["gray65", "gray28"]
        },
        "CTkButton": {
            "corner_radius": 6,
            "border_width": 0,
            "fg_color": ["#3B8ED0", "#1F6AA5"],
            "hover_color": ["#36719F", "#144870"],
            "border_color": ["#3E454A", "#949A9F"],
            "text_color": ["gray98", "#DCE4EE"],
            "text_color_disabled": ["gray78", "gray68"]
        }
    }
    
    LIGHT_GREEN = {
        # Define light green theme
    }

def apply_custom_theme(theme_name: str):
    """Apply custom theme to the application."""
    if theme_name == "dark_blue":
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme_from_dict(CustomThemes.DARK_BLUE)
    elif theme_name == "light_green":
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme_from_dict(CustomThemes.LIGHT_GREEN)
```

### Custom GUI Components

Create reusable GUI components:

```python
# project_architect/gui/custom_components.py
import customtkinter as ctk
from typing import Callable, List, Optional

class AdvancedProgressBar(ctk.CTkFrame):
    """Advanced progress bar with stages and descriptions."""
    
    def __init__(self, parent, stages: List[str], **kwargs):
        super().__init__(parent, **kwargs)
        
        self.stages = stages
        self.current_stage = 0
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        
        # Stage label
        self.stage_label = ctk.CTkLabel(self, text="")
        self.stage_label.pack(pady=5)
        
        # Stage list
        self.stage_frame = ctk.CTkScrollableFrame(self)
        self.stage_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.stage_labels = []
        for i, stage in enumerate(stages):
            label = ctk.CTkLabel(
                self.stage_frame, 
                text=f"☐ {stage}",
                anchor="w"
            )
            label.pack(fill="x", pady=2)
            self.stage_labels.append(label)
    
    def update_progress(self, stage_index: int, progress: float, message: str = ""):
        """Update progress bar and stage indicators."""
        self.current_stage = stage_index
        self.progress_bar.set(progress)
        
        # Update stage indicators
        for i, label in enumerate(self.stage_labels):
            if i < stage_index:
                label.configure(text=f"✓ {self.stages[i]}")
            elif i == stage_index:
                label.configure(text=f"⟳ {self.stages[i]}")
            else:
                label.configure(text=f"☐ {self.stages[i]}")
        
        # Update current stage label
        if message:
            self.stage_label.configure(text=message)
        else:
            self.stage_label.configure(text=f"Stage {stage_index + 1}: {self.stages[stage_index]}")

class QuestionnaireWidget(ctk.CTkFrame):
    """Advanced questionnaire widget with conditional logic."""
    
    def __init__(self, parent, questionnaire_engine, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.questionnaire_engine = questionnaire_engine
        self.question_widgets = {}
        self.current_section = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the questionnaire UI."""
        # Section selector
        self.section_frame = ctk.CTkFrame(self)
        self.section_frame.pack(fill="x", padx=10, pady=5)
        
        # Questions frame
        self.questions_frame = ctk.CTkScrollableFrame(self)
        self.questions_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Navigation buttons
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(fill="x", padx=10, pady=5)
        
        self.prev_button = ctk.CTkButton(
            self.nav_frame,
            text="Previous",
            command=self._previous_section
        )
        self.prev_button.pack(side="left", padx=5)
        
        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next",
            command=self._next_section
        )
        self.next_button.pack(side="right", padx=5)
    
    def load_questionnaire(self, project_type: str):
        """Load and display questionnaire."""
        self.questionnaire_engine.load_questionnaire(project_type)
        self._create_question_widgets()
        self._show_section(0)
    
    def _create_question_widgets(self):
        """Create widgets for all questions."""
        # Implementation for creating question widgets
        pass
    
    def _show_section(self, section_index: int):
        """Show questions for specific section."""
        # Implementation for showing section
        pass
```

## Advanced Customization

### Plugin System

Create a plugin system for extending functionality:

```python
# project_architect/plugins/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class PluginBase(ABC):
    """Base class for Project Architect plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass
    
    @abstractmethod
    def initialize(self, app_context: Dict[str, Any]) -> None:
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    def get_templates(self) -> List[str]:
        """Get list of templates provided by this plugin."""
        pass
    
    def get_custom_filters(self) -> Dict[str, Callable]:
        """Get custom Jinja2 filters provided by this plugin."""
        return {}
    
    def get_custom_validators(self) -> Dict[str, Callable]:
        """Get custom validators provided by this plugin."""
        return {}

# Example plugin
class GitHubIntegrationPlugin(PluginBase):
    @property
    def name(self) -> str:
        return "GitHub Integration"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def initialize(self, app_context: Dict[str, Any]) -> None:
        self.github_token = app_context.get('github_token')
    
    def get_templates(self) -> List[str]:
        return ["github_actions_template"]
    
    def get_custom_filters(self) -> Dict[str, Callable]:
        return {
            'github_url': self._format_github_url,
            'github_badge': self._create_github_badge
        }
    
    def _format_github_url(self, repo_name: str) -> str:
        return f"https://github.com/{repo_name}"
    
    def _create_github_badge(self, repo_name: str, badge_type: str) -> str:
        return f"![{badge_type}](https://img.shields.io/github/{badge_type}/{repo_name})"
```

### Custom Hooks

Implement hooks for extending the generation process:

```python
# project_architect/hooks/manager.py
from typing import Dict, List, Callable, Any

class HookManager:
    """Manages hooks for extending Project Architect functionality."""
    
    def __init__(self):
        self._hooks: Dict[str, List[Callable]] = {}
    
    def register_hook(self, hook_name: str, callback: Callable):
        """Register a hook callback."""
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        self._hooks[hook_name].append(callback)
    
    def execute_hook(self, hook_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all callbacks for a hook."""
        if hook_name not in self._hooks:
            return context
        
        for callback in self._hooks[hook_name]:
            try:
                context = callback(context) or context
            except Exception as e:
                print(f"Hook {hook_name} failed: {e}")
        
        return context

# Usage example
hook_manager = HookManager()

def add_custom_files(context):
    """Hook to add custom files during generation."""
    if context.get('project_type') == 'web_app':
        context['additional_files'] = [
            {'path': 'docker-compose.yml', 'template': 'docker-compose.yml.j2'}
        ]
    return context

hook_manager.register_hook('pre_generation', add_custom_files)
```

This customization guide provides comprehensive examples for tailoring Project Architect to your specific needs, from simple configuration changes to advanced plugin development.
