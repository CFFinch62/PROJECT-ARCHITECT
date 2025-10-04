"""
Project Architect - A comprehensive project template system

This package provides tools for generating well-structured, documented,
and AI-friendly development projects based on proven organizational patterns.

Author: Chuck Finch - Fragillidae Software
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Chuck Finch"
__email__ = "chuckcodes4cash@gmail.com"
__description__ = "A comprehensive project template system for generating professional development projects"

# Package metadata
PACKAGE_NAME = "Project Architect"
COMPANY = "Fragillidae Software"
COPYRIGHT = "© 2025 Fragillidae Software. All rights reserved."

# Application constants
DEFAULT_TEMPLATE_DIR = "templates"
DEFAULT_OUTPUT_DIR = "generated_projects"
CONFIG_FILE = "config.yaml"
USER_PROFILES_FILE = "user_profiles.json"
PROJECT_HISTORY_FILE = "project_history.json"

# Supported project types
PROJECT_TYPES = [
    "desktop_gui",
    "web_app", 
    "cli_tool",
    "game",
    "marine_electronics",
    "educational",
    "data_analysis"
]

# File size limits (following Service Center patterns)
MAX_FILE_LINES = 300
HARD_LIMIT_LINES = 500

# Import main classes for easy access
try:
    from .core.questionnaire import QuestionnaireEngine
    from .core.template_engine import TemplateEngine
    from .core.project_generator import ProjectGenerator
    from .core.documentation_builder import DocumentationBuilder
    from .config.settings import Settings
    
    __all__ = [
        'QuestionnaireEngine',
        'TemplateEngine', 
        'ProjectGenerator',
        'DocumentationBuilder',
        'Settings',
        'PROJECT_TYPES',
        '__version__'
    ]
    
except ImportError:
    # Handle case where modules aren't created yet
    __all__ = [
        'PROJECT_TYPES',
        '__version__'
    ]
