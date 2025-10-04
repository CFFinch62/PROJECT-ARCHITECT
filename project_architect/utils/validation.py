"""
Project Architect Validation Utilities

Provides validation functions for user input, project data, templates,
and configuration. Includes logging setup and error handling utilities.

Author: Chuck Finch - Fragillidae Software
"""

import re
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up application logging with consistent format.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Set up log file if not provided
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = log_dir / f"project_architect_{timestamp}.log"
    
    # Configure logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("ProjectArchitect")
    logger.info(f"Logging initialized - Level: {log_level}, File: {log_file}")
    
    return logger


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class ProjectValidator:
    """
    Validator class for project data and configuration.
    
    Provides methods to validate user input, project names, paths,
    and configuration data.
    """
    
    # Valid project name pattern (alphanumeric, spaces, hyphens, underscores)
    PROJECT_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_]+$')
    
    # Valid identifier pattern (for Python modules, variables, etc.)
    IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    
    # Email validation pattern
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # Version pattern (semantic versioning)
    VERSION_PATTERN = re.compile(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$')
    
    @staticmethod
    def validate_project_name(name: str) -> bool:
        """
        Validate project name.
        
        Args:
            name: Project name to validate
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ValidationError: If name is invalid with details
        """
        if not name or not name.strip():
            raise ValidationError("Project name cannot be empty")
        
        name = name.strip()
        
        if len(name) < 2:
            raise ValidationError("Project name must be at least 2 characters long")
        
        if len(name) > 100:
            raise ValidationError("Project name must be less than 100 characters")
        
        if not ProjectValidator.PROJECT_NAME_PATTERN.match(name):
            raise ValidationError(
                "Project name can only contain letters, numbers, spaces, hyphens, and underscores"
            )
        
        # Check for reserved names
        reserved_names = ['con', 'prn', 'aux', 'nul', 'com1', 'com2', 'com3', 'com4', 
                         'com5', 'com6', 'com7', 'com8', 'com9', 'lpt1', 'lpt2', 'lpt3', 
                         'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9']
        
        if name.lower() in reserved_names:
            raise ValidationError(f"'{name}' is a reserved name and cannot be used")
        
        return True
    
    @staticmethod
    def validate_identifier(identifier: str, field_name: str = "identifier") -> bool:
        """
        Validate Python identifier (module name, variable name, etc.).
        
        Args:
            identifier: Identifier to validate
            field_name: Name of the field being validated (for error messages)
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ValidationError: If identifier is invalid
        """
        if not identifier or not identifier.strip():
            raise ValidationError(f"{field_name} cannot be empty")
        
        identifier = identifier.strip()
        
        if not ProjectValidator.IDENTIFIER_PATTERN.match(identifier):
            raise ValidationError(
                f"{field_name} must be a valid Python identifier "
                "(letters, numbers, underscores; cannot start with number)"
            )
        
        # Check for Python keywords
        python_keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 
            'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import', 
            'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        if identifier in python_keywords:
            raise ValidationError(f"'{identifier}' is a Python keyword and cannot be used")
        
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address.
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ValidationError: If email is invalid
        """
        if not email or not email.strip():
            return True  # Email is optional in most cases
        
        email = email.strip()
        
        if not ProjectValidator.EMAIL_PATTERN.match(email):
            raise ValidationError("Invalid email address format")
        
        return True
    
    @staticmethod
    def validate_version(version: str) -> bool:
        """
        Validate version string (semantic versioning).
        
        Args:
            version: Version string to validate
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ValidationError: If version is invalid
        """
        if not version or not version.strip():
            raise ValidationError("Version cannot be empty")
        
        version = version.strip()
        
        if not ProjectValidator.VERSION_PATTERN.match(version):
            raise ValidationError(
                "Version must follow semantic versioning format (e.g., 1.0.0, 2.1.3-beta)"
            )
        
        return True
    
    @staticmethod
    def validate_path(path: Union[str, Path], must_exist: bool = False, 
                     must_be_dir: bool = False, must_be_writable: bool = False) -> bool:
        """
        Validate file or directory path.
        
        Args:
            path: Path to validate
            must_exist: Whether path must exist
            must_be_dir: Whether path must be a directory
            must_be_writable: Whether path must be writable
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ValidationError: If path is invalid
        """
        if not path:
            raise ValidationError("Path cannot be empty")
        
        path_obj = Path(path)
        
        if must_exist and not path_obj.exists():
            raise ValidationError(f"Path does not exist: {path}")
        
        if must_be_dir and path_obj.exists() and not path_obj.is_dir():
            raise ValidationError(f"Path is not a directory: {path}")
        
        if must_be_writable:
            # Check if parent directory is writable
            parent = path_obj.parent if path_obj.exists() else path_obj.parent
            if not parent.exists():
                try:
                    parent.mkdir(parents=True, exist_ok=True)
                except PermissionError:
                    raise ValidationError(f"Cannot create directory: {parent}")
            
            # Test write permission
            try:
                test_file = parent / ".write_test"
                test_file.touch()
                test_file.unlink()
            except PermissionError:
                raise ValidationError(f"Directory is not writable: {parent}")
        
        return True
    
    @staticmethod
    def validate_questionnaire_data(data: Dict[str, Any]) -> bool:
        """
        Validate questionnaire response data.
        
        Args:
            data: Questionnaire data to validate
            
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ValidationError: If data is invalid
        """
        required_fields = ['project_name', 'project_type', 'author_name']
        
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValidationError(f"Required field missing: {field}")
        
        # Validate specific fields
        ProjectValidator.validate_project_name(data['project_name'])
        
        if 'author_email' in data and data['author_email']:
            ProjectValidator.validate_email(data['author_email'])
        
        if 'version' in data and data['version']:
            ProjectValidator.validate_version(data['version'])
        
        if 'module_name' in data and data['module_name']:
            ProjectValidator.validate_identifier(data['module_name'], 'module_name')
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename by removing invalid characters.
        
        Args:
            filename: Filename to sanitize
            
        Returns:
            Sanitized filename
        """
        # Remove invalid characters for filenames
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remove leading/trailing spaces and dots
        filename = filename.strip(' .')
        
        # Ensure filename is not empty
        if not filename:
            filename = "untitled"
        
        return filename
    
    @staticmethod
    def sanitize_project_name(name: str) -> str:
        """
        Sanitize project name for use as directory name.
        
        Args:
            name: Project name to sanitize
            
        Returns:
            Sanitized project name
        """
        # Replace spaces with underscores
        name = name.replace(' ', '_')
        
        # Remove invalid characters
        name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
        
        # Ensure it starts with a letter or underscore
        if name and name[0].isdigit():
            name = '_' + name
        
        # Ensure it's not empty
        if not name:
            name = 'untitled_project'
        
        return name
