"""
Project Architect Questionnaire Engine

Handles interactive questionnaires for gathering project requirements,
including initial project creation and subsequent project updates.

Author: Chuck Finch - Fragillidae Software
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class QuestionType(Enum):
    """Types of questions supported by the questionnaire system."""
    TEXT = "text"
    EMAIL = "email"
    CHOICE = "choice"
    MULTIPLE_CHOICE = "multiple_choice"
    BOOLEAN = "boolean"
    FILE_PATH = "file_path"
    DIRECTORY_PATH = "directory_path"
    VERSION = "version"
    IDENTIFIER = "identifier"


class QuestionnaireMode(Enum):
    """Modes for running questionnaires."""
    NEW_PROJECT = "new_project"
    UPDATE_PROJECT = "update_project"
    FEATURE_ADDITION = "feature_addition"
    TECH_SPEC_UPDATE = "tech_spec_update"


@dataclass
class Question:
    """
    Represents a single question in the questionnaire.
    """
    id: str
    type: QuestionType
    prompt: str
    description: str = ""
    required: bool = True
    default: Any = None
    options: List[str] = None
    validation_pattern: str = None
    depends_on: str = None
    depends_value: Any = None
    section: str = "general"
    order: int = 0
    
    def __post_init__(self):
        """Convert string type to enum if needed."""
        if isinstance(self.type, str):
            self.type = QuestionType(self.type)


@dataclass
class QuestionnaireResponse:
    """
    Stores responses to questionnaire questions.
    """
    project_name: str
    project_type: str
    mode: QuestionnaireMode
    responses: Dict[str, Any]
    timestamp: str
    version: str = "1.0.0"
    
    def __post_init__(self):
        """Convert string mode to enum if needed."""
        if isinstance(self.mode, str):
            self.mode = QuestionnaireMode(self.mode)


class QuestionnaireEngine:
    """
    Main questionnaire engine for gathering project requirements.
    
    Supports both initial project creation and subsequent project updates
    through additional interviews.
    """
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize questionnaire engine.
        
        Args:
            templates_dir: Directory containing questionnaire templates
        """
        self.logger = logging.getLogger(__name__)
        
        # Set templates directory
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            self.templates_dir = Path(__file__).parent.parent / "templates"
        
        # Initialize questionnaire data
        self.questions: List[Question] = []
        self.responses: Dict[str, Any] = {}
        self.current_section = "general"
        self.mode = QuestionnaireMode.NEW_PROJECT
        
        # Callbacks for UI integration
        self.progress_callback: Optional[Callable[[int, int], None]] = None
        self.validation_callback: Optional[Callable[[str, Any], bool]] = None
        
        self.logger.info("QuestionnaireEngine initialized")
    
    def load_questionnaire(self, project_type: str, mode: QuestionnaireMode = QuestionnaireMode.NEW_PROJECT) -> bool:
        """
        Load questionnaire for specified project type and mode.
        
        Args:
            project_type: Type of project (desktop_gui, web_app, etc.)
            mode: Questionnaire mode (new_project, update_project, etc.)
            
        Returns:
            bool: True if questionnaire loaded successfully
        """
        try:
            self.mode = mode
            questionnaire_file = self.templates_dir / project_type / "questionnaire.json"
            
            if not questionnaire_file.exists():
                self.logger.error(f"Questionnaire file not found: {questionnaire_file}")
                return False
            
            with open(questionnaire_file, 'r', encoding='utf-8') as f:
                questionnaire_data = json.load(f)
            
            # Load base questions
            self.questions = []
            for q_data in questionnaire_data.get('questions', []):
                question = Question(**q_data)
                self.questions.append(question)
            
            # Load mode-specific questions
            mode_questions = questionnaire_data.get(f'{mode.value}_questions', [])
            for q_data in mode_questions:
                question = Question(**q_data)
                self.questions.append(question)
            
            # Sort questions by order and section
            self.questions.sort(key=lambda q: (q.section, q.order))
            
            self.logger.info(f"Loaded {len(self.questions)} questions for {project_type} ({mode.value})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading questionnaire: {e}")
            return False
    
    def load_existing_responses(self, project_path: Path) -> bool:
        """
        Load existing responses from a project for update mode.
        
        Args:
            project_path: Path to existing project
            
        Returns:
            bool: True if responses loaded successfully
        """
        try:
            # Look for existing project data
            project_data_file = project_path / ".project_architect" / "project_data.json"
            
            if not project_data_file.exists():
                self.logger.warning(f"No existing project data found at {project_data_file}")
                return False
            
            with open(project_data_file, 'r', encoding='utf-8') as f:
                project_data = json.load(f)
            
            # Load previous responses
            self.responses = project_data.get('responses', {})
            
            self.logger.info(f"Loaded {len(self.responses)} existing responses")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading existing responses: {e}")
            return False
    
    def get_questions_by_section(self, section: str = None) -> List[Question]:
        """
        Get questions for a specific section.
        
        Args:
            section: Section name (None for all questions)
            
        Returns:
            List of questions for the section
        """
        if section is None:
            return self.questions
        
        return [q for q in self.questions if q.section == section]
    
    def get_sections(self) -> List[str]:
        """
        Get all unique sections in the questionnaire.
        
        Returns:
            List of section names
        """
        sections = list(set(q.section for q in self.questions))
        return sorted(sections)
    
    def should_show_question(self, question: Question) -> bool:
        """
        Determine if a question should be shown based on dependencies.

        Args:
            question: Question to check

        Returns:
            bool: True if question should be shown
        """
        if not question.depends_on:
            return True

        # Get the dependency value - check responses first, then fall back to default
        if question.depends_on in self.responses:
            dependency_value = self.responses[question.depends_on]
        else:
            # Check if the parent question has a default value
            parent_question = self.get_question_by_id(question.depends_on)
            if parent_question is None:
                return False
            dependency_value = parent_question.default

        if question.depends_value is None:
            # Just check if dependency has any value
            return bool(dependency_value)

        # Check if dependency matches expected value
        return dependency_value == question.depends_value

    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """
        Get a question by its ID.

        Args:
            question_id: ID of the question to find

        Returns:
            Question object or None if not found
        """
        for question in self.questions:
            if question.id == question_id:
                return question
        return None
    
    def validate_response(self, question: Question, value: Any) -> tuple[bool, str]:
        """
        Validate a response to a question.
        
        Args:
            question: Question being answered
            value: Response value
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Import validation here to avoid circular imports
            from ..utils.validation import ProjectValidator
            
            # Check required fields
            if question.required and (value is None or value == ""):
                return False, f"{question.prompt} is required"
            
            # Skip validation for empty optional fields
            if not question.required and (value is None or value == ""):
                return True, ""
            
            # Type-specific validation
            if question.type == QuestionType.EMAIL:
                ProjectValidator.validate_email(str(value))
            elif question.type == QuestionType.VERSION:
                ProjectValidator.validate_version(str(value))
            elif question.type == QuestionType.IDENTIFIER:
                ProjectValidator.validate_identifier(str(value), question.id)
            elif question.type == QuestionType.FILE_PATH:
                ProjectValidator.validate_path(value, must_exist=False)
            elif question.type == QuestionType.DIRECTORY_PATH:
                ProjectValidator.validate_path(value, must_exist=False, must_be_dir=True)
            elif question.type == QuestionType.CHOICE:
                if question.options and str(value) not in question.options:
                    return False, f"Value must be one of: {', '.join(question.options)}"
            elif question.type == QuestionType.MULTIPLE_CHOICE:
                if question.options and isinstance(value, list):
                    for item in value:
                        if str(item) not in question.options:
                            return False, f"All values must be from: {', '.join(question.options)}"
            
            # Custom validation callback
            if self.validation_callback:
                if not self.validation_callback(question.id, value):
                    return False, "Custom validation failed"
            
            return True, ""
            
        except Exception as e:
            return False, str(e)
    
    def set_response(self, question_id: str, value: Any) -> bool:
        """
        Set response for a question.
        
        Args:
            question_id: ID of the question
            value: Response value
            
        Returns:
            bool: True if response was set successfully
        """
        try:
            # Find the question
            question = next((q for q in self.questions if q.id == question_id), None)
            if not question:
                self.logger.error(f"Question not found: {question_id}")
                return False
            
            # Validate response
            is_valid, error_msg = self.validate_response(question, value)
            if not is_valid:
                self.logger.error(f"Validation failed for {question_id}: {error_msg}")
                return False
            
            # Store response
            self.responses[question_id] = value
            
            # Update progress callback
            if self.progress_callback:
                answered = len([q for q in self.questions if q.id in self.responses and self.should_show_question(q)])
                total = len([q for q in self.questions if self.should_show_question(q)])
                self.progress_callback(answered, total)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting response for {question_id}: {e}")
            return False
    
    def get_response(self, question_id: str, default: Any = None) -> Any:
        """
        Get response for a question.
        
        Args:
            question_id: ID of the question
            default: Default value if not found
            
        Returns:
            Response value or default
        """
        return self.responses.get(question_id, default)
    
    def is_complete(self) -> bool:
        """
        Check if questionnaire is complete.
        
        Returns:
            bool: True if all required questions are answered
        """
        for question in self.questions:
            if not self.should_show_question(question):
                continue
            
            if question.required and question.id not in self.responses:
                return False
        
        return True
    
    def get_completion_percentage(self) -> float:
        """
        Get completion percentage of questionnaire.
        
        Returns:
            Completion percentage (0.0 to 100.0)
        """
        visible_questions = [q for q in self.questions if self.should_show_question(q)]
        if not visible_questions:
            return 100.0
        
        answered_questions = [q for q in visible_questions if q.id in self.responses]
        return (len(answered_questions) / len(visible_questions)) * 100.0
    
    def export_responses(self) -> QuestionnaireResponse:
        """
        Export responses as a structured object.
        
        Returns:
            QuestionnaireResponse object
        """
        return QuestionnaireResponse(
            project_name=self.responses.get('project_name', 'Untitled Project'),
            project_type=self.responses.get('project_type', 'desktop_gui'),
            mode=self.mode,
            responses=self.responses.copy(),
            timestamp=datetime.now().isoformat(),
            version="1.0.0"
        )
    
    def save_responses(self, file_path: Path) -> bool:
        """
        Save responses to file.
        
        Args:
            file_path: Path to save responses
            
        Returns:
            bool: True if saved successfully
        """
        try:
            response_obj = self.export_responses()
            
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(response_obj), f, indent=2)
            
            self.logger.info(f"Responses saved to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving responses: {e}")
            return False
    
    def set_progress_callback(self, callback: Callable[[int, int], None]):
        """Set callback for progress updates."""
        self.progress_callback = callback
    
    def set_validation_callback(self, callback: Callable[[str, Any], bool]):
        """Set callback for custom validation."""
        self.validation_callback = callback
