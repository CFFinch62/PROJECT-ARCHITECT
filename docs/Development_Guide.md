# Project Architect - Development Guide

This guide is for developers who want to contribute to Project Architect or extend its functionality. It covers the development environment setup, coding standards, testing procedures, and contribution guidelines.

## Table of Contents

1. [Development Environment](#development-environment)
2. [Project Structure](#project-structure)
3. [Coding Standards](#coding-standards)
4. [Testing Guidelines](#testing-guidelines)
5. [Contributing](#contributing)
6. [Release Process](#release-process)

## Development Environment

### Prerequisites

- **Python 3.8+** (Python 3.12+ recommended)
- **Git** for version control
- **IDE**: VS Code or PyCharm recommended
- **GitHub CLI** (optional, for repository management)

### Setup for Development

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd "Project Architect"
   ```

2. **Create Development Environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv_dev
   
   # Activate virtual environment
   source venv_dev/bin/activate  # Linux/Mac
   venv_dev\Scripts\activate     # Windows
   
   # Install development dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If exists
   ```

3. **Install Development Tools**
   ```bash
   # Code formatting
   pip install black isort
   
   # Linting
   pip install flake8 pylint mypy
   
   # Testing
   pip install pytest pytest-cov pytest-mock
   
   # Documentation
   pip install sphinx sphinx-rtd-theme
   ```

4. **IDE Configuration**

   **VS Code (.vscode/settings.json)**:
   ```json
   {
     "python.defaultInterpreterPath": "./venv_dev/bin/python",
     "python.formatting.provider": "black",
     "python.linting.enabled": true,
     "python.linting.flake8Enabled": true,
     "python.linting.pylintEnabled": true,
     "python.testing.pytestEnabled": true,
     "python.testing.pytestArgs": ["tests/"],
     "files.exclude": {
       "**/__pycache__": true,
       "**/*.pyc": true
     }
   }
   ```

   **PyCharm**:
   - Set interpreter to `venv_dev/bin/python`
   - Enable Black formatting
   - Configure pytest as test runner
   - Set up flake8 and pylint inspections

## Project Structure

### Directory Organization

```
Project Architect/
├── project_architect/          # Main application package
│   ├── __init__.py            # Package initialization
│   ├── core/                  # Core business logic
│   │   ├── __init__.py
│   │   ├── questionnaire.py   # Questionnaire engine
│   │   ├── template_engine.py # Template processing
│   │   ├── project_generator.py # Project generation
│   │   └── project_updater.py # Project updates
│   ├── gui/                   # User interface
│   │   ├── __init__.py
│   │   ├── main_window.py     # Main application window
│   │   ├── components/        # Reusable GUI components
│   │   └── dialogs/           # Dialog windows
│   ├── config/                # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py        # Settings handling
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── validation.py      # Input validation
│   │   └── file_utils.py      # File system utilities
│   └── templates/             # Project templates
│       ├── desktop_gui/       # Desktop GUI template
│       ├── web_app/           # Web application template
│       └── cli_tool/          # CLI tool template
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   ├── fixtures/              # Test fixtures
│   └── conftest.py            # Pytest configuration
├── docs/                      # Documentation
├── dev_sessions/              # Development session logs
├── logs/                      # Application logs
├── data/                      # Configuration and user data
├── main.py                    # Application entry point
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── setup.py                   # Package setup
├── pytest.ini                # Pytest configuration
├── .flake8                    # Flake8 configuration
├── pyproject.toml             # Black and other tool config
└── README.md                  # Project overview
```

### Module Guidelines

1. **File Size Limits**
   - Target: 300 lines per file
   - Hard limit: 500 lines per file
   - Split larger files into logical modules

2. **Import Organization**
   ```python
   # Standard library imports
   import os
   import sys
   from pathlib import Path
   
   # Third-party imports
   import customtkinter as ctk
   from jinja2 import Environment
   
   # Local imports
   from project_architect.core import QuestionnaireEngine
   from project_architect.utils import validate_path
   ```

3. **Module Structure**
   ```python
   """Module docstring describing purpose and usage."""
   
   # Imports
   
   # Constants
   DEFAULT_TIMEOUT = 30
   
   # Type definitions
   ResponseDict = Dict[str, Any]
   
   # Classes
   class MainClass:
       """Class docstring."""
       pass
   
   # Functions
   def utility_function():
       """Function docstring."""
       pass
   
   # Main execution (if applicable)
   if __name__ == "__main__":
       main()
   ```

## Coding Standards

### Python Style Guide

Follow PEP 8 with these specific guidelines:

1. **Line Length**: 88 characters (Black default)
2. **Indentation**: 4 spaces
3. **Quotes**: Double quotes for strings, single quotes for string literals in code
4. **Naming Conventions**:
   - Classes: `PascalCase`
   - Functions/methods: `snake_case`
   - Constants: `UPPER_SNAKE_CASE`
   - Private members: `_leading_underscore`

### Documentation Standards

1. **Docstrings**: Use Google-style docstrings
   ```python
   def process_questionnaire(responses: Dict[str, Any]) -> QuestionnaireResult:
       """Process questionnaire responses and generate result.
       
       Args:
           responses: Dictionary of question IDs to user responses
           
       Returns:
           QuestionnaireResult: Processed questionnaire data
           
       Raises:
           ValidationError: If responses fail validation
           ProcessingError: If processing fails
       """
   ```

2. **Type Hints**: Use type hints for all public functions
   ```python
   from typing import Dict, List, Optional, Union
   
   def validate_responses(responses: Dict[str, Any]) -> List[str]:
       """Validate questionnaire responses."""
       errors: List[str] = []
       return errors
   ```

3. **Comments**: Use comments sparingly, prefer self-documenting code
   ```python
   # Good: Explain why, not what
   # Use exponential backoff to handle rate limiting
   time.sleep(2 ** attempt)
   
   # Bad: Explain what the code does
   # Increment the counter by 1
   counter += 1
   ```

### Error Handling

1. **Custom Exceptions**
   ```python
   class ProjectArchitectError(Exception):
       """Base exception for Project Architect."""
       pass
   
   class ValidationError(ProjectArchitectError):
       """Raised when validation fails."""
       pass
   ```

2. **Exception Handling**
   ```python
   try:
       result = risky_operation()
   except SpecificError as e:
       logger.error(f"Operation failed: {e}")
       raise ProcessingError(f"Failed to process: {e}") from e
   except Exception as e:
       logger.exception("Unexpected error occurred")
       raise
   ```

3. **Logging**
   ```python
   import logging
   
   logger = logging.getLogger(__name__)
   
   def process_data(data):
       logger.info("Starting data processing")
       try:
           result = complex_operation(data)
           logger.debug(f"Processing result: {result}")
           return result
       except Exception as e:
           logger.error(f"Processing failed: {e}")
           raise
   ```

## Testing Guidelines

### Test Structure

```
tests/
├── unit/                      # Unit tests (fast, isolated)
│   ├── test_questionnaire.py
│   ├── test_template_engine.py
│   └── test_validation.py
├── integration/               # Integration tests (slower, multiple components)
│   ├── test_project_generation.py
│   └── test_project_updates.py
├── fixtures/                  # Test data and fixtures
│   ├── sample_questionnaires/
│   ├── sample_templates/
│   └── sample_projects/
└── conftest.py               # Shared test configuration
```

### Writing Tests

1. **Test Naming**
   ```python
   def test_questionnaire_loads_valid_json():
       """Test that questionnaire loads from valid JSON file."""
   
   def test_questionnaire_raises_error_on_invalid_json():
       """Test that questionnaire raises error for invalid JSON."""
   ```

2. **Test Structure (Arrange-Act-Assert)**
   ```python
   def test_template_engine_renders_simple_template():
       # Arrange
       engine = TemplateEngine("test_templates/")
       context = {"name": "Test Project", "version": "1.0.0"}
       
       # Act
       result = engine.render_template("simple.j2", context)
       
       # Assert
       assert "Test Project" in result
       assert "1.0.0" in result
   ```

3. **Fixtures**
   ```python
   # conftest.py
   import pytest
   from project_architect.core import QuestionnaireEngine
   
   @pytest.fixture
   def questionnaire_engine():
       """Create questionnaire engine for testing."""
       return QuestionnaireEngine("tests/fixtures/questionnaires/")
   
   @pytest.fixture
   def sample_responses():
       """Sample questionnaire responses."""
       return {
           "project_name": "Test Project",
           "author_name": "Test Author",
           "gui_framework": "customtkinter"
       }
   ```

4. **Mocking**
   ```python
   from unittest.mock import Mock, patch
   
   def test_project_generator_creates_venv(mock_subprocess):
       with patch('subprocess.run') as mock_run:
           mock_run.return_value.returncode = 0
           
           generator = ProjectGenerator()
           generator.create_virtual_environment("/test/path")
           
           mock_run.assert_called_once()
   ```

### Test Categories

1. **Unit Tests** - Test individual functions/methods in isolation
2. **Integration Tests** - Test component interactions
3. **End-to-End Tests** - Test complete workflows
4. **Performance Tests** - Test performance characteristics
5. **UI Tests** - Test GUI components (limited, focus on logic)

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=project_architect --cov-report=html

# Run specific test file
pytest tests/unit/test_questionnaire.py

# Run tests matching pattern
pytest -k "test_validation"

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x
```

### Test Configuration

**pytest.ini**:
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --disable-warnings
    --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
    gui: GUI tests
```

## Contributing

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-template-type
   ```

2. **Make Changes**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation

3. **Run Quality Checks**
   ```bash
   # Format code
   black .
   isort .
   
   # Check linting
   flake8 .
   pylint project_architect/
   
   # Type checking
   mypy project_architect/
   
   # Run tests
   pytest --cov=project_architect
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new template type for data analysis projects"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/new-template-type
   # Create pull request through GitHub
   ```

### Commit Message Format

Use conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

**Examples**:
```
feat(templates): add web application template
fix(questionnaire): handle empty responses gracefully
docs(api): update API reference for new methods
```

### Code Review Guidelines

1. **Review Checklist**
   - [ ] Code follows style guidelines
   - [ ] Tests are included and pass
   - [ ] Documentation is updated
   - [ ] No breaking changes (or properly documented)
   - [ ] Performance impact considered

2. **Review Process**
   - All code must be reviewed before merging
   - Address all review comments
   - Ensure CI/CD checks pass
   - Squash commits before merging

## Release Process

### Version Management

Use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Prepare Release**
   ```bash
   # Update version in __init__.py
   # Update CHANGELOG.md
   # Run full test suite
   pytest --cov=project_architect
   ```

2. **Create Release Branch**
   ```bash
   git checkout -b release/v1.2.0
   git commit -m "chore: prepare release v1.2.0"
   ```

3. **Tag Release**
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

4. **Build Distribution**
   ```bash
   python setup.py sdist bdist_wheel
   ```

5. **Deploy** (if applicable)
   ```bash
   # Deploy to package repository
   twine upload dist/*
   ```

### Quality Gates

Before any release:

- [ ] All tests pass
- [ ] Code coverage > 80%
- [ ] No linting errors
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated

## Development Best Practices

1. **Test-Driven Development**
   - Write tests before implementation
   - Keep tests simple and focused
   - Maintain high test coverage

2. **Continuous Integration**
   - Run tests on every commit
   - Check code quality automatically
   - Prevent broken code from merging

3. **Documentation**
   - Keep documentation current
   - Include examples in docstrings
   - Document design decisions

4. **Performance**
   - Profile code for bottlenecks
   - Use appropriate data structures
   - Cache expensive operations

5. **Security**
   - Validate all inputs
   - Use secure defaults
   - Keep dependencies updated

This development guide ensures consistent, high-quality contributions to Project Architect while maintaining a productive development environment.
