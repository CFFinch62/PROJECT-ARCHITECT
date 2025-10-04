# Project Architect - API Reference

This document provides comprehensive API documentation for Project Architect's core modules and classes. Use this reference when extending or integrating with Project Architect.

## Table of Contents

1. [Core Modules](#core-modules)
2. [QuestionnaireEngine](#questionnaireengine)
3. [TemplateEngine](#templateengine)
4. [ProjectGenerator](#projectgenerator)
5. [ProjectUpdater](#projectupdater)
6. [Configuration](#configuration)
7. [Utilities](#utilities)

## Core Modules

### project_architect.core

Main package containing core functionality:

```python
from project_architect.core import (
    QuestionnaireEngine,
    TemplateEngine,
    ProjectGenerator,
    ProjectUpdater,
    QuestionnaireMode,
    UpdateType
)
```

## QuestionnaireEngine

Interactive questionnaire system for gathering project requirements.

### Class: QuestionnaireEngine

```python
class QuestionnaireEngine:
    """Manages interactive questionnaires for project generation."""
    
    def __init__(self, templates_dir: str = None, logger: logging.Logger = None)
```

#### Methods

##### load_questionnaire()
```python
def load_questionnaire(self, project_type: str, mode: QuestionnaireMode = QuestionnaireMode.NEW_PROJECT) -> bool:
    """
    Load questionnaire for specified project type and mode.
    
    Args:
        project_type: Type of project template
        mode: Questionnaire mode (NEW_PROJECT, UPDATE_PROJECT, etc.)
    
    Returns:
        bool: True if questionnaire loaded successfully
    
    Raises:
        FileNotFoundError: If questionnaire file not found
        ValueError: If questionnaire format is invalid
    """
```

##### get_question()
```python
def get_question(self, question_id: str) -> Optional[Question]:
    """
    Get question by ID.
    
    Args:
        question_id: Unique question identifier
    
    Returns:
        Question object or None if not found
    """
```

##### set_response()
```python
def set_response(self, question_id: str, response: Any) -> bool:
    """
    Set response for a question with validation.
    
    Args:
        question_id: Question identifier
        response: User response
    
    Returns:
        bool: True if response is valid and set
    
    Raises:
        ValidationError: If response fails validation
    """
```

##### is_complete()
```python
def is_complete(self) -> bool:
    """
    Check if all required questions have been answered.
    
    Returns:
        bool: True if questionnaire is complete
    """
```

##### export_responses()
```python
def export_responses(self) -> QuestionnaireResponse:
    """
    Export all responses as structured data.
    
    Returns:
        QuestionnaireResponse: Complete response data
    """
```

### Data Classes

#### Question
```python
@dataclass
class Question:
    id: str
    type: QuestionType
    prompt: str
    description: str = ""
    required: bool = True
    default: Any = None
    options: List[str] = field(default_factory=list)
    validation: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    section: str = "general"
    order: int = 0
```

#### QuestionnaireResponse
```python
@dataclass
class QuestionnaireResponse:
    project_type: str
    mode: QuestionnaireMode
    responses: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: datetime
    version: str
```

### Enums

#### QuestionnaireMode
```python
class QuestionnaireMode(Enum):
    NEW_PROJECT = "new_project"
    UPDATE_PROJECT = "update_project"
    FEATURE_ADDITION = "feature_addition"
    TECH_SPEC_UPDATE = "tech_spec_update"
```

#### QuestionType
```python
class QuestionType(Enum):
    TEXT = "text"
    EMAIL = "email"
    CHOICE = "choice"
    MULTIPLE_CHOICE = "multiple_choice"
    BOOLEAN = "boolean"
    FILE_PATH = "file_path"
    DIRECTORY_PATH = "directory_path"
    VERSION = "version"
    IDENTIFIER = "identifier"
```

## TemplateEngine

Jinja2-based template processing system.

### Class: TemplateEngine

```python
class TemplateEngine:
    """Handles template loading, processing, and file generation."""
    
    def __init__(self, templates_dir: str, logger: logging.Logger = None)
```

#### Methods

##### load_template_config()
```python
def load_template_config(self, template_type: str) -> Dict[str, Any]:
    """
    Load template configuration from template.yaml.
    
    Args:
        template_type: Template type identifier
    
    Returns:
        dict: Template configuration
    
    Raises:
        FileNotFoundError: If template config not found
        yaml.YAMLError: If config format is invalid
    """
```

##### render_template()
```python
def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
    """
    Render template with provided context.
    
    Args:
        template_name: Name of template file
        context: Variables for template rendering
    
    Returns:
        str: Rendered template content
    
    Raises:
        TemplateNotFound: If template file not found
        TemplateError: If template rendering fails
    """
```

##### generate_project_structure()
```python
def generate_project_structure(self, 
                             template_type: str, 
                             output_dir: str, 
                             context: Dict[str, Any],
                             progress_callback: Callable = None) -> ProjectMetadata:
    """
    Generate complete project structure from template.
    
    Args:
        template_type: Type of template to use
        output_dir: Directory to create project in
        context: Template variables
        progress_callback: Optional progress callback function
    
    Returns:
        ProjectMetadata: Information about generated project
    
    Raises:
        TemplateError: If generation fails
        OSError: If file system operations fail
    """
```

##### list_available_templates()
```python
def list_available_templates(self) -> List[Dict[str, Any]]:
    """
    Get list of all available templates.
    
    Returns:
        List of template information dictionaries
    """
```

### Custom Filters

The template engine provides these custom Jinja2 filters:

```python
# Case conversion filters
{{ "my project" | snake_case }}     # my_project
{{ "my project" | pascal_case }}    # MyProject
{{ "my project" | camel_case }}     # myProject
{{ "my project" | kebab_case }}     # my-project

# Date/time filters
{{ current_date | date_format("%Y-%m-%d") }}
{{ current_time | time_format("%H:%M:%S") }}

# Text manipulation
{{ text | indent(4) }}              # Indent by 4 spaces
{{ text | title_case }}             # Title Case
{{ text | upper_case }}             # UPPER CASE
{{ text | lower_case }}             # lower case
```

## ProjectGenerator

Orchestrates complete project generation process.

### Class: ProjectGenerator

```python
class ProjectGenerator:
    """Manages the complete project generation workflow."""
    
    def __init__(self, 
                 template_engine: TemplateEngine,
                 logger: logging.Logger = None)
```

#### Methods

##### generate_project()
```python
def generate_project(self,
                    questionnaire_response: QuestionnaireResponse,
                    output_dir: str,
                    progress_callback: Callable = None) -> ProjectMetadata:
    """
    Generate complete project from questionnaire responses.
    
    Args:
        questionnaire_response: User responses and project requirements
        output_dir: Directory to create project in
        progress_callback: Optional progress callback
    
    Returns:
        ProjectMetadata: Generated project information
    
    Raises:
        GenerationError: If project generation fails
        ValidationError: If requirements validation fails
    """
```

##### validate_requirements()
```python
def validate_requirements(self, response: QuestionnaireResponse) -> List[str]:
    """
    Validate project requirements before generation.
    
    Args:
        response: Questionnaire responses to validate
    
    Returns:
        List of validation error messages (empty if valid)
    """
```

### Data Classes

#### ProjectMetadata
```python
@dataclass
class ProjectMetadata:
    name: str
    type: str
    version: str
    author: str
    description: str
    created_date: datetime
    project_path: str
    template_version: str
    dependencies: List[str]
    features: List[str]
    configuration: Dict[str, Any]
```

## ProjectUpdater

Manages updates to existing projects through additional interviews.

### Class: ProjectUpdater

```python
class ProjectUpdater:
    """Handles updating existing projects with new requirements."""
    
    def __init__(self, 
                 questionnaire_engine: QuestionnaireEngine,
                 logger: logging.Logger = None)
```

#### Methods

##### load_project()
```python
def load_project(self, project_path: str) -> ProjectMetadata:
    """
    Load existing project metadata and history.
    
    Args:
        project_path: Path to project directory
    
    Returns:
        ProjectMetadata: Current project information
    
    Raises:
        FileNotFoundError: If project metadata not found
        ValueError: If project format is invalid
    """
```

##### start_update_interview()
```python
def start_update_interview(self, 
                          project_path: str, 
                          update_type: UpdateType) -> bool:
    """
    Begin update interview for existing project.
    
    Args:
        project_path: Path to project directory
        update_type: Type of update to perform
    
    Returns:
        bool: True if interview started successfully
    
    Raises:
        ProjectNotFoundError: If project not found or invalid
    """
```

##### complete_update_interview()
```python
def complete_update_interview(self, 
                            responses: Dict[str, Any]) -> ProjectUpdate:
    """
    Complete update interview and apply changes.
    
    Args:
        responses: User responses to update questions
    
    Returns:
        ProjectUpdate: Information about applied update
    
    Raises:
        UpdateError: If update application fails
    """
```

##### get_update_history()
```python
def get_update_history(self, project_path: str) -> List[ProjectUpdate]:
    """
    Get complete update history for project.
    
    Args:
        project_path: Path to project directory
    
    Returns:
        List of ProjectUpdate objects in chronological order
    """
```

### Enums

#### UpdateType
```python
class UpdateType(Enum):
    TECH_SPEC_REVISION = "tech_spec_revision"
    FEATURE_ADDITION = "feature_addition"
    ARCHITECTURE_CHANGE = "architecture_change"
    DEPENDENCY_UPDATE = "dependency_update"
    DOCUMENTATION_UPDATE = "documentation_update"
    CONFIGURATION_CHANGE = "configuration_change"
```

### Data Classes

#### ProjectUpdate
```python
@dataclass
class ProjectUpdate:
    update_id: str
    update_type: UpdateType
    timestamp: datetime
    version_before: str
    version_after: str
    description: str
    changes: Dict[str, Any]
    author: str
    responses: Dict[str, Any]
```

## Configuration

Configuration management system.

### Class: Settings

```python
class Settings:
    """Manages application configuration and user preferences."""
    
    def __init__(self, config_dir: str = None)
```

#### Methods

##### load_settings()
```python
def load_settings(self) -> AppSettings:
    """Load application settings from file."""
```

##### save_settings()
```python
def save_settings(self, settings: AppSettings) -> bool:
    """Save application settings to file."""
```

##### get()
```python
def get(self, key: str, default: Any = None) -> Any:
    """Get configuration value by key."""
```

##### set()
```python
def set(self, key: str, value: Any) -> None:
    """Set configuration value."""
```

## Utilities

### Validation

```python
class ProjectValidator:
    """Static methods for validating project data."""
    
    @staticmethod
    def validate_project_name(name: str) -> bool:
        """Validate project name format."""
    
    @staticmethod
    def validate_identifier(identifier: str) -> bool:
        """Validate Python identifier format."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address format."""
    
    @staticmethod
    def validate_version(version: str) -> bool:
        """Validate semantic version format."""
    
    @staticmethod
    def validate_path(path: str, must_exist: bool = False) -> bool:
        """Validate file system path."""
```

### Exceptions

```python
class ProjectArchitectError(Exception):
    """Base exception for Project Architect."""

class ValidationError(ProjectArchitectError):
    """Raised when validation fails."""

class TemplateError(ProjectArchitectError):
    """Raised when template processing fails."""

class GenerationError(ProjectArchitectError):
    """Raised when project generation fails."""

class UpdateError(ProjectArchitectError):
    """Raised when project update fails."""
```

## Usage Examples

### Basic Project Generation

```python
from project_architect.core import QuestionnaireEngine, TemplateEngine, ProjectGenerator

# Initialize components
questionnaire = QuestionnaireEngine()
template_engine = TemplateEngine("templates/")
generator = ProjectGenerator(template_engine)

# Load questionnaire and collect responses
questionnaire.load_questionnaire("desktop_gui")
questionnaire.set_response("project_name", "My App")
questionnaire.set_response("author_name", "John Doe")

# Generate project
if questionnaire.is_complete():
    response = questionnaire.export_responses()
    metadata = generator.generate_project(response, "/path/to/output")
    print(f"Generated project: {metadata.name}")
```

### Project Update

```python
from project_architect.core import ProjectUpdater, UpdateType

# Initialize updater
updater = ProjectUpdater(questionnaire_engine)

# Load existing project
project = updater.load_project("/path/to/project")

# Start update interview
updater.start_update_interview(project.project_path, UpdateType.FEATURE_ADDITION)

# Complete update
responses = {"feature_name": "User Authentication", "feature_priority": "High"}
update = updater.complete_update_interview(responses)
print(f"Applied update: {update.description}")
```

### Custom Template

```python
from project_architect.core import TemplateEngine

# Initialize template engine
engine = TemplateEngine("my_templates/")

# Render custom template
context = {
    "project_name": "My Project",
    "author": "Jane Doe",
    "features": ["logging", "config", "database"]
}

content = engine.render_template("custom_main.py.j2", context)
print(content)
```

This API reference provides the foundation for extending and integrating with Project Architect. All classes include comprehensive error handling and logging for robust operation.
