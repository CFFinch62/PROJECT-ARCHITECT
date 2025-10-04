# Project Architect - Testing Guide

This guide covers testing strategies, frameworks, and best practices for Project Architect. It includes unit testing, integration testing, and quality assurance procedures.

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Framework Setup](#test-framework-setup)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [GUI Testing](#gui-testing)
6. [Test Data Management](#test-data-management)
7. [Continuous Testing](#continuous-testing)

## Testing Philosophy

### Testing Pyramid

```
    /\
   /  \     E2E Tests (Few)
  /____\    - Complete workflows
 /      \   - User scenarios
/________\  Integration Tests (Some)
           - Component interactions
           - Template generation
___________
           Unit Tests (Many)
           - Individual functions
           - Business logic
           - Validation rules
```

### Testing Principles

1. **Fast Feedback** - Unit tests run quickly for immediate feedback
2. **Reliable** - Tests produce consistent results
3. **Maintainable** - Tests are easy to understand and modify
4. **Comprehensive** - Critical paths are thoroughly tested
5. **Isolated** - Tests don't depend on external systems

## Test Framework Setup

### Dependencies

```bash
# Core testing framework
pip install pytest>=7.4.0

# Coverage reporting
pip install pytest-cov>=4.1.0

# Mocking and fixtures
pip install pytest-mock>=3.11.0

# Async testing (if needed)
pip install pytest-asyncio>=0.21.0

# GUI testing
pip install pytest-qt>=4.2.0  # For Qt-based testing
```

### Configuration Files

**pytest.ini**:
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test* *Tests
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --tb=short
    --cov=project_architect
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (slower, multiple components)
    gui: GUI tests (require display)
    slow: Slow tests (> 1 second)
    external: Tests requiring external resources
```

**conftest.py** (Global test configuration):
```python
"""Global test configuration and fixtures."""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock

from project_architect.core import QuestionnaireEngine, TemplateEngine
from project_architect.config import Settings


@pytest.fixture(scope="session")
def temp_dir():
    """Create temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = Mock(spec=Settings)
    settings.get.return_value = "default_value"
    return settings


@pytest.fixture
def sample_questionnaire_data():
    """Sample questionnaire data for testing."""
    return {
        "questionnaire": {
            "name": "Test Questionnaire",
            "version": "1.0.0"
        },
        "questions": [
            {
                "id": "project_name",
                "type": "text",
                "prompt": "Project name?",
                "required": True
            },
            {
                "id": "gui_framework",
                "type": "choice",
                "prompt": "GUI framework?",
                "options": ["customtkinter", "tkinter"],
                "default": "customtkinter"
            }
        ]
    }
```

## Unit Testing

### Testing Core Components

#### QuestionnaireEngine Tests

```python
# tests/unit/test_questionnaire.py
import pytest
from project_architect.core import QuestionnaireEngine, QuestionnaireMode
from project_architect.core.questionnaire import Question, QuestionType


class TestQuestionnaireEngine:
    """Test QuestionnaireEngine functionality."""
    
    @pytest.fixture
    def engine(self, temp_dir):
        """Create questionnaire engine for testing."""
        return QuestionnaireEngine(str(temp_dir))
    
    def test_load_questionnaire_success(self, engine, sample_questionnaire_data, temp_dir):
        """Test successful questionnaire loading."""
        # Arrange
        questionnaire_file = temp_dir / "test_questionnaire.json"
        questionnaire_file.write_text(json.dumps(sample_questionnaire_data))
        
        # Act
        result = engine.load_questionnaire("test", QuestionnaireMode.NEW_PROJECT)
        
        # Assert
        assert result is True
        assert len(engine._questions) == 2
        assert "project_name" in engine._questions
    
    def test_load_questionnaire_file_not_found(self, engine):
        """Test questionnaire loading with missing file."""
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            engine.load_questionnaire("nonexistent", QuestionnaireMode.NEW_PROJECT)
    
    def test_set_response_valid(self, engine, sample_questionnaire_data, temp_dir):
        """Test setting valid response."""
        # Arrange
        questionnaire_file = temp_dir / "test_questionnaire.json"
        questionnaire_file.write_text(json.dumps(sample_questionnaire_data))
        engine.load_questionnaire("test", QuestionnaireMode.NEW_PROJECT)
        
        # Act
        result = engine.set_response("project_name", "My Test Project")
        
        # Assert
        assert result is True
        assert engine._responses["project_name"] == "My Test Project"
    
    def test_set_response_invalid(self, engine, sample_questionnaire_data, temp_dir):
        """Test setting invalid response."""
        # Arrange
        questionnaire_file = temp_dir / "test_questionnaire.json"
        questionnaire_file.write_text(json.dumps(sample_questionnaire_data))
        engine.load_questionnaire("test", QuestionnaireMode.NEW_PROJECT)
        
        # Act & Assert
        with pytest.raises(ValidationError):
            engine.set_response("project_name", "")  # Empty string for required field
    
    def test_is_complete_true(self, engine, sample_questionnaire_data, temp_dir):
        """Test questionnaire completion check when complete."""
        # Arrange
        questionnaire_file = temp_dir / "test_questionnaire.json"
        questionnaire_file.write_text(json.dumps(sample_questionnaire_data))
        engine.load_questionnaire("test", QuestionnaireMode.NEW_PROJECT)
        engine.set_response("project_name", "Test Project")
        
        # Act
        result = engine.is_complete()
        
        # Assert
        assert result is True
    
    def test_is_complete_false(self, engine, sample_questionnaire_data, temp_dir):
        """Test questionnaire completion check when incomplete."""
        # Arrange
        questionnaire_file = temp_dir / "test_questionnaire.json"
        questionnaire_file.write_text(json.dumps(sample_questionnaire_data))
        engine.load_questionnaire("test", QuestionnaireMode.NEW_PROJECT)
        
        # Act
        result = engine.is_complete()
        
        # Assert
        assert result is False
```

#### TemplateEngine Tests

```python
# tests/unit/test_template_engine.py
import pytest
from project_architect.core import TemplateEngine


class TestTemplateEngine:
    """Test TemplateEngine functionality."""
    
    @pytest.fixture
    def engine(self, temp_dir):
        """Create template engine for testing."""
        return TemplateEngine(str(temp_dir))
    
    @pytest.fixture
    def sample_template(self, temp_dir):
        """Create sample template file."""
        template_content = """
# {{ project_name }}

Author: {{ author_name }}
Version: {{ version }}

{% if has_database %}
Database: Enabled
{% endif %}
"""
        template_file = temp_dir / "sample.j2"
        template_file.write_text(template_content)
        return template_file
    
    def test_render_template_basic(self, engine, sample_template):
        """Test basic template rendering."""
        # Arrange
        context = {
            "project_name": "Test Project",
            "author_name": "Test Author",
            "version": "1.0.0",
            "has_database": True
        }
        
        # Act
        result = engine.render_template("sample.j2", context)
        
        # Assert
        assert "Test Project" in result
        assert "Test Author" in result
        assert "1.0.0" in result
        assert "Database: Enabled" in result
    
    def test_render_template_with_filters(self, engine, temp_dir):
        """Test template rendering with custom filters."""
        # Arrange
        template_content = "{{ project_name | snake_case }}"
        template_file = temp_dir / "filter_test.j2"
        template_file.write_text(template_content)
        
        context = {"project_name": "My Test Project"}
        
        # Act
        result = engine.render_template("filter_test.j2", context)
        
        # Assert
        assert result.strip() == "my_test_project"
    
    def test_template_not_found(self, engine):
        """Test template rendering with missing template."""
        # Act & Assert
        with pytest.raises(TemplateNotFound):
            engine.render_template("nonexistent.j2", {})
```

### Testing Utilities

#### Validation Tests

```python
# tests/unit/test_validation.py
import pytest
from project_architect.utils.validation import ProjectValidator, ValidationError


class TestProjectValidator:
    """Test validation utilities."""
    
    def test_validate_project_name_valid(self):
        """Test valid project name validation."""
        valid_names = [
            "My Project",
            "Test-App",
            "Project_123",
            "Simple"
        ]
        
        for name in valid_names:
            assert ProjectValidator.validate_project_name(name) is True
    
    def test_validate_project_name_invalid(self):
        """Test invalid project name validation."""
        invalid_names = [
            "",           # Empty
            "   ",        # Whitespace only
            "a" * 101,    # Too long
            "Project/",   # Invalid character
            "Project<>",  # Invalid characters
        ]
        
        for name in invalid_names:
            assert ProjectValidator.validate_project_name(name) is False
    
    def test_validate_email_valid(self):
        """Test valid email validation."""
        valid_emails = [
            "user@example.com",
            "test.email@domain.org",
            "user+tag@example.co.uk"
        ]
        
        for email in valid_emails:
            assert ProjectValidator.validate_email(email) is True
    
    def test_validate_email_invalid(self):
        """Test invalid email validation."""
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user@.com",
            ""
        ]
        
        for email in invalid_emails:
            assert ProjectValidator.validate_email(email) is False
    
    def test_validate_version_valid(self):
        """Test valid version validation."""
        valid_versions = [
            "1.0.0",
            "2.1.3",
            "10.20.30",
            "1.0.0-alpha",
            "2.0.0-beta.1"
        ]
        
        for version in valid_versions:
            assert ProjectValidator.validate_version(version) is True
    
    def test_validate_version_invalid(self):
        """Test invalid version validation."""
        invalid_versions = [
            "1.0",        # Missing patch
            "1",          # Missing minor and patch
            "1.0.0.0",    # Too many parts
            "a.b.c",      # Non-numeric
            ""            # Empty
        ]
        
        for version in invalid_versions:
            assert ProjectValidator.validate_version(version) is False
```

## Integration Testing

### Testing Component Interactions

```python
# tests/integration/test_project_generation.py
import pytest
import json
from pathlib import Path
from project_architect.core import (
    QuestionnaireEngine, 
    TemplateEngine, 
    ProjectGenerator
)


class TestProjectGeneration:
    """Test complete project generation workflow."""
    
    @pytest.fixture
    def setup_templates(self, temp_dir):
        """Set up test templates."""
        template_dir = temp_dir / "templates" / "test_template"
        template_dir.mkdir(parents=True)
        
        # Template configuration
        config = {
            "template": {
                "name": "Test Template",
                "type": "test_template",
                "version": "1.0.0"
            },
            "structure": [
                {"path": "main.py", "type": "file", "template": "main.py.j2"},
                {"path": "README.md", "type": "file", "template": "README.md.j2"}
            ]
        }
        (template_dir / "template.yaml").write_text(yaml.dump(config))
        
        # Questionnaire
        questionnaire = {
            "questions": [
                {
                    "id": "project_name",
                    "type": "text",
                    "prompt": "Project name?",
                    "required": True
                }
            ]
        }
        (template_dir / "questionnaire.json").write_text(json.dumps(questionnaire))
        
        # Template files
        (template_dir / "main.py.j2").write_text(
            '#!/usr/bin/env python3\n'
            '"""{{ project_name }} - Main Application"""\n\n'
            'def main():\n'
            '    print("Hello from {{ project_name }}!")\n\n'
            'if __name__ == "__main__":\n'
            '    main()\n'
        )
        
        (template_dir / "README.md.j2").write_text(
            '# {{ project_name }}\n\n'
            '{{ project_description }}\n'
        )
        
        return template_dir.parent
    
    def test_complete_project_generation(self, setup_templates, temp_dir):
        """Test complete project generation workflow."""
        # Arrange
        questionnaire_engine = QuestionnaireEngine(str(setup_templates))
        template_engine = TemplateEngine(str(setup_templates))
        generator = ProjectGenerator(template_engine)
        
        # Load questionnaire and set responses
        questionnaire_engine.load_questionnaire("test_template")
        questionnaire_engine.set_response("project_name", "Integration Test Project")
        
        output_dir = temp_dir / "generated_project"
        
        # Act
        response = questionnaire_engine.export_responses()
        metadata = generator.generate_project(response, str(output_dir))
        
        # Assert
        assert metadata.name == "Integration Test Project"
        assert (output_dir / "main.py").exists()
        assert (output_dir / "README.md").exists()
        
        # Check file contents
        main_content = (output_dir / "main.py").read_text()
        assert "Integration Test Project" in main_content
        assert "def main():" in main_content
        
        readme_content = (output_dir / "README.md").read_text()
        assert "# Integration Test Project" in readme_content
```

### Testing Project Updates

```python
# tests/integration/test_project_updates.py
import pytest
from project_architect.core import ProjectUpdater, UpdateType


class TestProjectUpdates:
    """Test project update functionality."""
    
    @pytest.fixture
    def existing_project(self, temp_dir):
        """Create existing project for update testing."""
        project_dir = temp_dir / "existing_project"
        project_dir.mkdir()
        
        # Create project metadata
        metadata = {
            "name": "Existing Project",
            "version": "1.0.0",
            "type": "desktop_gui",
            "created_date": "2025-01-01T00:00:00"
        }
        
        project_data_dir = project_dir / ".project_architect"
        project_data_dir.mkdir()
        (project_data_dir / "project_data.json").write_text(json.dumps(metadata))
        
        # Create TECHNICAL_SPECIFICATION.md
        tech_spec = """# Technical Specification

## Version 1.0.0

### Requirements
- Basic GUI application
- Configuration management
"""
        (project_dir / "TECHNICAL_SPECIFICATION.md").write_text(tech_spec)
        
        return project_dir
    
    def test_tech_spec_update(self, existing_project):
        """Test technical specification update."""
        # Arrange
        updater = ProjectUpdater()
        
        # Act
        project_metadata = updater.load_project(str(existing_project))
        updater.start_update_interview(str(existing_project), UpdateType.TECH_SPEC_REVISION)
        
        update_responses = {
            "update_description": "Add database support",
            "new_requirements": ["Database integration", "Data persistence"],
            "modified_requirements": [],
            "removed_requirements": []
        }
        
        update_result = updater.complete_update_interview(update_responses)
        
        # Assert
        assert update_result.update_type == UpdateType.TECH_SPEC_REVISION
        assert update_result.version_after == "1.1.0"
        
        # Check updated technical specification
        tech_spec_content = (existing_project / "TECHNICAL_SPECIFICATION.md").read_text()
        assert "Database integration" in tech_spec_content
        assert "Version 1.1.0" in tech_spec_content
```

## GUI Testing

### Testing GUI Components

```python
# tests/gui/test_main_window.py
import pytest
from unittest.mock import Mock, patch
from project_architect.gui import MainWindow


class TestMainWindow:
    """Test main window functionality."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Mock external dependencies."""
        with patch('project_architect.gui.main_window.QuestionnaireEngine') as mock_qe, \
             patch('project_architect.gui.main_window.TemplateEngine') as mock_te, \
             patch('project_architect.gui.main_window.Settings') as mock_settings:
            
            mock_settings.return_value.load_settings.return_value = Mock()
            yield {
                'questionnaire_engine': mock_qe,
                'template_engine': mock_te,
                'settings': mock_settings
            }
    
    def test_main_window_initialization(self, mock_dependencies):
        """Test main window initializes correctly."""
        # Act
        window = MainWindow()
        
        # Assert
        assert window.title() == "Project Architect"
        assert hasattr(window, '_sidebar')
        assert hasattr(window, '_content_area')
    
    @pytest.mark.gui
    def test_new_project_button_click(self, mock_dependencies):
        """Test new project button functionality."""
        # Arrange
        window = MainWindow()
        
        # Act
        window._start_new_project()
        
        # Assert
        # Verify that questionnaire tab is activated
        assert window._content_area.get() == "Questionnaire"
```

### GUI Test Utilities

```python
# tests/gui/conftest.py
import pytest
import tkinter as tk
from unittest.mock import Mock


@pytest.fixture
def tk_root():
    """Create Tkinter root for GUI testing."""
    root = tk.Tk()
    root.withdraw()  # Hide the window
    yield root
    root.destroy()


@pytest.fixture
def mock_gui_dependencies():
    """Mock GUI dependencies."""
    return {
        'questionnaire_engine': Mock(),
        'template_engine': Mock(),
        'project_generator': Mock(),
        'settings': Mock()
    }
```

## Test Data Management

### Fixtures and Test Data

```python
# tests/fixtures/sample_data.py
"""Sample data for testing."""

SAMPLE_QUESTIONNAIRE = {
    "questionnaire": {
        "name": "Desktop GUI Application",
        "version": "1.0.0"
    },
    "questions": [
        {
            "id": "project_name",
            "type": "text",
            "prompt": "What is the name of your project?",
            "required": True,
            "section": "project_basics"
        },
        {
            "id": "gui_framework",
            "type": "choice",
            "prompt": "Which GUI framework would you like to use?",
            "options": ["customtkinter", "pyqt6", "tkinter"],
            "default": "customtkinter",
            "section": "technical_stack"
        }
    ]
}

SAMPLE_RESPONSES = {
    "project_name": "Test Application",
    "project_description": "A test application for unit testing",
    "author_name": "Test Author",
    "author_email": "test@example.com",
    "gui_framework": "customtkinter",
    "has_database": True,
    "database_type": "sqlite"
}

SAMPLE_TEMPLATE_CONFIG = {
    "template": {
        "name": "Test Template",
        "type": "test_template",
        "version": "1.0.0"
    },
    "structure": [
        {"path": "src", "type": "directory"},
        {"path": "main.py", "type": "file", "template": "main.py.j2"},
        {"path": "requirements.txt", "type": "file", "template": "requirements.txt.j2"}
    ],
    "requirements": {
        "base": ["python>=3.8"],
        "customtkinter": ["customtkinter>=5.2.2"]
    }
}
```

### Test Utilities

```python
# tests/utils.py
"""Testing utilities."""

import json
import yaml
from pathlib import Path
from typing import Dict, Any


def create_test_questionnaire(temp_dir: Path, questionnaire_data: Dict[str, Any]) -> Path:
    """Create test questionnaire file."""
    questionnaire_file = temp_dir / "questionnaire.json"
    questionnaire_file.write_text(json.dumps(questionnaire_data, indent=2))
    return questionnaire_file


def create_test_template_config(temp_dir: Path, config_data: Dict[str, Any]) -> Path:
    """Create test template configuration."""
    config_file = temp_dir / "template.yaml"
    config_file.write_text(yaml.dump(config_data, default_flow_style=False))
    return config_file


def create_test_template_file(temp_dir: Path, filename: str, content: str) -> Path:
    """Create test template file."""
    template_file = temp_dir / filename
    template_file.write_text(content)
    return template_file


def assert_file_contains(file_path: Path, expected_content: str):
    """Assert that file contains expected content."""
    content = file_path.read_text()
    assert expected_content in content, f"Expected '{expected_content}' not found in {file_path}"


def assert_directory_structure(base_dir: Path, expected_structure: Dict[str, Any]):
    """Assert that directory has expected structure."""
    for path, path_type in expected_structure.items():
        full_path = base_dir / path
        if path_type == "directory":
            assert full_path.is_dir(), f"Expected directory {full_path} not found"
        elif path_type == "file":
            assert full_path.is_file(), f"Expected file {full_path} not found"
```

## Continuous Testing

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
      
      - id: coverage
        name: Check coverage
        entry: pytest --cov=project_architect --cov-fail-under=80
        language: system
        pass_filenames: false
        always_run: true
```

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=project_architect --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Test Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=project_architect --cov-report=html

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run tests in parallel
pytest -n auto

# Run tests with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_questionnaire.py::TestQuestionnaireEngine::test_load_questionnaire_success

# Run tests matching pattern
pytest -k "test_validation"

# Run tests and stop on first failure
pytest -x

# Run tests with debugging
pytest --pdb
```

This comprehensive testing guide ensures Project Architect maintains high quality and reliability through thorough automated testing at all levels.
