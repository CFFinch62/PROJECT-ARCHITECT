# Project Architect - Architecture Overview

This document provides a comprehensive overview of Project Architect's system architecture, design patterns, and technical implementation details.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Core Components](#core-components)
3. [Design Patterns](#design-patterns)
4. [Data Flow](#data-flow)
5. [Module Dependencies](#module-dependencies)
6. [Extension Points](#extension-points)

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Project Architect                        │
├─────────────────────────────────────────────────────────────┤
│  GUI Layer (CustomTkinter)                                 │
│  ├── MainWindow                                            │
│  ├── QuestionnaireTab                                      │
│  ├── ProjectInfoTab                                        │
│  └── SettingsDialog                                        │
├─────────────────────────────────────────────────────────────┤
│  Core Business Logic                                       │
│  ├── QuestionnaireEngine    ├── ProjectGenerator          │
│  ├── TemplateEngine         ├── ProjectUpdater            │
│  └── ValidationEngine       └── ConfigurationManager      │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                │
│  ├── Template Files (.j2)   ├── Configuration (YAML)     │
│  ├── Questionnaires (JSON)  ├── Project Metadata (JSON)  │
│  └── User Settings (YAML)   └── Update History (JSON)    │
├─────────────────────────────────────────────────────────────┤
│  External Dependencies                                     │
│  ├── Jinja2 (Templates)     ├── PyYAML (Config)          │
│  ├── CustomTkinter (GUI)    ├── GitPython (VCS)          │
│  └── JSONSchema (Validation)└── Pathlib (File System)    │
└─────────────────────────────────────────────────────────────┘
```

### Architectural Principles

1. **Separation of Concerns** - Clear boundaries between GUI, business logic, and data
2. **Modular Design** - Independent, reusable components
3. **Plugin Architecture** - Extensible template and questionnaire system
4. **Configuration-Driven** - Behavior controlled by configuration files
5. **Event-Driven** - Loose coupling through callback mechanisms

## Core Components

### 1. QuestionnaireEngine

**Purpose**: Manages interactive questionnaires for gathering project requirements

**Key Responsibilities**:
- Load questionnaire definitions from JSON files
- Present questions with conditional logic
- Validate user responses
- Export structured response data

**Design Pattern**: Strategy Pattern (different question types)

```python
class QuestionnaireEngine:
    def __init__(self):
        self._questions: Dict[str, Question] = {}
        self._responses: Dict[str, Any] = {}
        self._validators: Dict[QuestionType, Validator] = {}
    
    def load_questionnaire(self, project_type: str, mode: QuestionnaireMode):
        # Load questions based on type and mode
        
    def validate_response(self, question_id: str, response: Any) -> bool:
        # Delegate to appropriate validator
```

### 2. TemplateEngine

**Purpose**: Processes Jinja2 templates to generate project files

**Key Responsibilities**:
- Load and cache template files
- Provide custom filters for text transformation
- Render templates with user context
- Generate complete project structures

**Design Pattern**: Template Method Pattern

```python
class TemplateEngine:
    def __init__(self, templates_dir: str):
        self._jinja_env = Environment(loader=FileSystemLoader(templates_dir))
        self._setup_custom_filters()
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        template = self._jinja_env.get_template(template_name)
        return template.render(**self._enhance_context(context))
```

### 3. ProjectGenerator

**Purpose**: Orchestrates the complete project generation process

**Key Responsibilities**:
- Coordinate questionnaire completion
- Validate project requirements
- Generate project structure using templates
- Set up development environment (venv, git, etc.)

**Design Pattern**: Facade Pattern

```python
class ProjectGenerator:
    def __init__(self, template_engine: TemplateEngine):
        self._template_engine = template_engine
        self._validators = []
        self._generators = []
    
    def generate_project(self, response: QuestionnaireResponse, output_dir: str):
        # Orchestrate the generation process
        self._validate_requirements(response)
        self._create_project_structure(response, output_dir)
        self._setup_development_environment(response, output_dir)
```

### 4. ProjectUpdater

**Purpose**: Manages updates to existing projects through additional interviews

**Key Responsibilities**:
- Load existing project metadata
- Conduct update-specific interviews
- Apply changes to project documentation
- Maintain update history and versioning

**Design Pattern**: Command Pattern (for different update types)

```python
class ProjectUpdater:
    def __init__(self, questionnaire_engine: QuestionnaireEngine):
        self._questionnaire_engine = questionnaire_engine
        self._update_commands: Dict[UpdateType, UpdateCommand] = {}
    
    def apply_update(self, project_path: str, update_type: UpdateType, responses: Dict):
        command = self._update_commands[update_type]
        return command.execute(project_path, responses)
```

### 5. Configuration System

**Purpose**: Manages application settings and user preferences

**Key Responsibilities**:
- Load/save application configuration
- Manage user profiles and preferences
- Provide default values and validation
- Support environment-specific settings

**Design Pattern**: Singleton Pattern

```python
class Settings:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_settings(self) -> AppSettings:
        # Load from YAML configuration file
```

## Design Patterns

### 1. Model-View-Controller (MVC)

- **Model**: Core business logic (QuestionnaireEngine, TemplateEngine, etc.)
- **View**: GUI components (MainWindow, tabs, dialogs)
- **Controller**: Event handlers and coordination logic

### 2. Observer Pattern

Used for progress tracking and status updates:

```python
class ProgressObserver:
    def update(self, progress: int, message: str):
        pass

class ProjectGenerator:
    def __init__(self):
        self._observers: List[ProgressObserver] = []
    
    def add_observer(self, observer: ProgressObserver):
        self._observers.append(observer)
    
    def _notify_progress(self, progress: int, message: str):
        for observer in self._observers:
            observer.update(progress, message)
```

### 3. Factory Pattern

For creating different types of questions and validators:

```python
class QuestionFactory:
    @staticmethod
    def create_question(question_data: Dict) -> Question:
        question_type = QuestionType(question_data['type'])
        
        if question_type == QuestionType.TEXT:
            return TextQuestion(**question_data)
        elif question_type == QuestionType.CHOICE:
            return ChoiceQuestion(**question_data)
        # ... other types
```

### 4. Strategy Pattern

For different validation strategies:

```python
class ValidationStrategy:
    def validate(self, value: Any) -> bool:
        raise NotImplementedError

class EmailValidationStrategy(ValidationStrategy):
    def validate(self, value: str) -> bool:
        return re.match(r'^[^@]+@[^@]+\.[^@]+$', value) is not None

class Validator:
    def __init__(self, strategy: ValidationStrategy):
        self._strategy = strategy
    
    def validate(self, value: Any) -> bool:
        return self._strategy.validate(value)
```

## Data Flow

### Project Generation Flow

```
User Input → Questionnaire → Validation → Template Processing → File Generation → Environment Setup
     ↓              ↓             ↓              ↓                    ↓               ↓
GUI Questions → Response Data → Validated Data → Rendered Files → Project Structure → Ready Project
```

### Detailed Flow

1. **User Interaction**
   - User selects project type
   - GUI loads appropriate questionnaire
   - User answers questions with validation

2. **Data Processing**
   - Responses collected and validated
   - Context variables generated
   - Template configuration loaded

3. **Template Processing**
   - Jinja2 templates rendered with context
   - File contents generated
   - Directory structure created

4. **Project Assembly**
   - Files written to target directory
   - Virtual environment created
   - Git repository initialized
   - Dependencies installed

5. **Finalization**
   - Project metadata saved
   - Success confirmation
   - Project ready for development

### Update Flow

```
Existing Project → Load Metadata → Update Interview → Apply Changes → Update History
       ↓               ↓              ↓               ↓              ↓
Project Directory → Current State → New Requirements → Modified Files → Version Increment
```

## Module Dependencies

### Dependency Graph

```
MainWindow
    ├── QuestionnaireEngine
    │   ├── Question (dataclass)
    │   ├── QuestionnaireResponse (dataclass)
    │   └── ValidationEngine
    ├── TemplateEngine
    │   ├── Jinja2
    │   └── Custom Filters
    ├── ProjectGenerator
    │   ├── TemplateEngine
    │   ├── ValidationEngine
    │   └── FileSystemUtils
    ├── ProjectUpdater
    │   ├── QuestionnaireEngine
    │   ├── ProjectMetadata
    │   └── VersionManager
    └── Settings
        ├── AppSettings (dataclass)
        └── UserProfiles
```

### External Dependencies

- **CustomTkinter**: Modern GUI framework
- **Jinja2**: Template processing engine
- **PyYAML**: Configuration file parsing
- **GitPython**: Git repository management
- **JSONSchema**: JSON validation
- **Pathlib**: Cross-platform path handling
- **Dataclasses**: Structured data containers

## Extension Points

### 1. Custom Question Types

Add new question types by extending the base Question class:

```python
class CustomQuestion(Question):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = QuestionType.CUSTOM
    
    def validate_response(self, response: Any) -> bool:
        # Custom validation logic
        return True
```

### 2. Template Filters

Add custom Jinja2 filters:

```python
def custom_filter(text: str) -> str:
    # Custom text transformation
    return text.upper()

# Register in TemplateEngine
template_engine.add_filter('custom_filter', custom_filter)
```

### 3. Update Commands

Implement new update types:

```python
class CustomUpdateCommand(UpdateCommand):
    def execute(self, project_path: str, responses: Dict) -> ProjectUpdate:
        # Custom update logic
        return ProjectUpdate(...)

# Register in ProjectUpdater
updater.register_update_command(UpdateType.CUSTOM, CustomUpdateCommand())
```

### 4. Validation Strategies

Add custom validation:

```python
class CustomValidationStrategy(ValidationStrategy):
    def validate(self, value: Any) -> bool:
        # Custom validation logic
        return True
```

### 5. Progress Observers

Implement custom progress tracking:

```python
class CustomProgressObserver(ProgressObserver):
    def update(self, progress: int, message: str):
        # Custom progress handling
        print(f"Progress: {progress}% - {message}")
```

## Performance Considerations

### 1. Template Caching

Templates are cached after first load to improve performance:

```python
class TemplateEngine:
    def __init__(self):
        self._template_cache: Dict[str, Template] = {}
    
    def get_template(self, name: str) -> Template:
        if name not in self._template_cache:
            self._template_cache[name] = self._jinja_env.get_template(name)
        return self._template_cache[name]
```

### 2. Lazy Loading

Questionnaires and templates are loaded only when needed:

```python
class QuestionnaireEngine:
    def load_questionnaire(self, project_type: str):
        if project_type not in self._loaded_questionnaires:
            self._load_questionnaire_file(project_type)
```

### 3. Asynchronous Operations

Long-running operations use progress callbacks to maintain UI responsiveness:

```python
def generate_project_async(self, response: QuestionnaireResponse, 
                          progress_callback: Callable):
    # Perform generation with periodic progress updates
    for step, total in enumerate(generation_steps):
        progress_callback(int((step / total) * 100), f"Step {step}")
```

## Security Considerations

### 1. Path Validation

All file paths are validated to prevent directory traversal:

```python
def validate_path(path: str) -> bool:
    resolved = Path(path).resolve()
    return resolved.is_relative_to(ALLOWED_BASE_PATH)
```

### 2. Template Sandboxing

Jinja2 templates run in a sandboxed environment:

```python
from jinja2.sandbox import SandboxedEnvironment

env = SandboxedEnvironment(loader=FileSystemLoader(templates_dir))
```

### 3. Input Sanitization

All user inputs are sanitized before processing:

```python
def sanitize_input(value: str) -> str:
    # Remove potentially dangerous characters
    return re.sub(r'[<>"|&]', '', value)
```

This architecture provides a solid foundation for Project Architect's functionality while maintaining flexibility for future enhancements and extensions.
