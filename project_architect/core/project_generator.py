"""
Project Architect Project Generator

Orchestrates the complete project generation process, including directory
structure creation, file generation, and development environment setup.

Author: Chuck Finch - Fragillidae Software
"""

import logging
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable

from .questionnaire import QuestionnaireResponse
from .template_engine import TemplateEngine
from ..utils.validation import ProjectValidator


class ProjectGenerator:
    """
    Main project generator that orchestrates the complete project creation process.
    
    Handles directory structure creation, file generation from templates,
    virtual environment setup, Git initialization, and dependency installation.
    """
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize project generator.
        
        Args:
            templates_dir: Directory containing project templates
        """
        self.logger = logging.getLogger(__name__)
        
        # Initialize template engine
        self.template_engine = TemplateEngine(templates_dir)
        
        # Progress tracking
        self.progress_callback: Optional[Callable[[int, int, str], None]] = None
        self.current_step = 0
        self.total_steps = 0
        
        self.logger.info("ProjectGenerator initialized")
    
    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """
        Set callback for progress updates.
        
        Args:
            callback: Function that receives (current_step, total_steps, message)
        """
        self.progress_callback = callback
    
    def _update_progress(self, message: str):
        """
        Update progress and call callback if set.
        
        Args:
            message: Progress message
        """
        if self.progress_callback:
            self.progress_callback(self.current_step, self.total_steps, message)
        
        self.logger.info(f"Progress ({self.current_step}/{self.total_steps}): {message}")
        self.current_step += 1
    
    def generate_project(self, responses: QuestionnaireResponse, output_dir: Path) -> bool:
        """
        Generate a complete project from questionnaire responses.
        
        Args:
            responses: Questionnaire responses containing project requirements
            output_dir: Directory where project should be generated
            
        Returns:
            bool: True if project generated successfully
        """
        try:
            self.logger.info(f"Starting project generation: {responses.project_name}")
            
            # Calculate total steps
            self._calculate_total_steps(responses)
            self.current_step = 0
            
            # Validate inputs
            self._update_progress("Validating project requirements")
            if not self._validate_project_requirements(responses, output_dir):
                return False
            
            # Create project directory
            project_path = output_dir / responses.project_name
            self._update_progress(f"Creating project directory: {project_path}")
            if not self._create_project_directory(project_path):
                return False
            
            # Generate project structure from template
            self._update_progress("Generating project structure from template")
            if not self.template_engine.generate_project_structure(
                responses.project_type, project_path, responses
            ):
                return False
            
            # Setup virtual environment if requested
            if responses.responses.get('create_venv', True):
                self._update_progress("Creating virtual environment")
                if not self._create_virtual_environment(project_path):
                    self.logger.warning("Failed to create virtual environment")
            
            # Install dependencies if virtual environment was created
            if responses.responses.get('create_venv', True):
                self._update_progress("Installing project dependencies")
                if not self._install_dependencies(project_path):
                    self.logger.warning("Failed to install dependencies")
            
            # Initialize Git repository if requested
            if responses.responses.get('init_git', True):
                self._update_progress("Initializing Git repository")
                if not self._initialize_git_repository(project_path):
                    self.logger.warning("Failed to initialize Git repository")
            
            # Create GitHub repository if requested
            if responses.responses.get('create_github_repo', False):
                self._update_progress("Creating GitHub repository")
                if not self._create_github_repository(project_path, responses):
                    self.logger.warning("Failed to create GitHub repository")
            
            # Final validation
            self._update_progress("Performing final validation")
            if not self._validate_generated_project(project_path):
                self.logger.warning("Generated project validation failed")
            
            self._update_progress(f"Project '{responses.project_name}' generated successfully!")
            self.logger.info(f"Project generation completed: {project_path}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating project: {e}")
            return False
    
    def _calculate_total_steps(self, responses: QuestionnaireResponse):
        """
        Calculate total number of steps for progress tracking.
        
        Args:
            responses: Questionnaire responses
        """
        self.total_steps = 4  # Base steps: validate, create dir, generate structure, final validation
        
        if responses.responses.get('create_venv', True):
            self.total_steps += 2  # Create venv + install dependencies
        
        if responses.responses.get('init_git', True):
            self.total_steps += 1  # Initialize Git
        
        if responses.responses.get('create_github_repo', False):
            self.total_steps += 1  # Create GitHub repo
    
    def _validate_project_requirements(self, responses: QuestionnaireResponse, output_dir: Path) -> bool:
        """
        Validate project requirements before generation.
        
        Args:
            responses: Questionnaire responses
            output_dir: Output directory
            
        Returns:
            bool: True if requirements are valid
        """
        try:
            # Validate project name
            ProjectValidator.validate_project_name(responses.project_name)
            
            # Validate output directory
            ProjectValidator.validate_path(output_dir, must_exist=True, must_be_dir=True)
            
            # Check if project directory already exists
            project_path = output_dir / responses.project_name
            if project_path.exists():
                self.logger.error(f"Project directory already exists: {project_path}")
                return False
            
            # Validate template exists
            available_templates = self.template_engine.list_available_templates()
            if responses.project_type not in available_templates:
                self.logger.error(f"Template not found: {responses.project_type}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return False
    
    def _create_project_directory(self, project_path: Path) -> bool:
        """
        Create the main project directory.
        
        Args:
            project_path: Path to project directory
            
        Returns:
            bool: True if directory created successfully
        """
        try:
            project_path.mkdir(parents=True, exist_ok=False)
            self.logger.info(f"Created project directory: {project_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating project directory: {e}")
            return False
    
    def _create_virtual_environment(self, project_path: Path) -> bool:
        """
        Create a virtual environment for the project.
        
        Args:
            project_path: Path to project directory
            
        Returns:
            bool: True if virtual environment created successfully
        """
        try:
            venv_path = project_path / "venv"
            
            # Create virtual environment
            result = subprocess.run(
                [sys.executable, "-m", "venv", str(venv_path)],
                capture_output=True,
                text=True,
                cwd=project_path
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to create virtual environment: {result.stderr}")
                return False
            
            self.logger.info(f"Created virtual environment: {venv_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating virtual environment: {e}")
            return False
    
    def _install_dependencies(self, project_path: Path) -> bool:
        """
        Install project dependencies in the virtual environment.
        
        Args:
            project_path: Path to project directory
            
        Returns:
            bool: True if dependencies installed successfully
        """
        try:
            venv_path = project_path / "venv"
            requirements_file = project_path / "requirements.txt"
            
            if not venv_path.exists():
                self.logger.warning("Virtual environment not found, skipping dependency installation")
                return False
            
            if not requirements_file.exists():
                self.logger.warning("requirements.txt not found, skipping dependency installation")
                return True
            
            # Determine pip executable path
            if sys.platform == "win32":
                pip_executable = venv_path / "Scripts" / "pip.exe"
            else:
                pip_executable = venv_path / "bin" / "pip"
            
            if not pip_executable.exists():
                self.logger.error(f"Pip executable not found: {pip_executable}")
                return False
            
            # Install dependencies
            result = subprocess.run(
                [str(pip_executable), "install", "-r", "requirements.txt"],
                capture_output=True,
                text=True,
                cwd=project_path
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to install dependencies: {result.stderr}")
                return False
            
            self.logger.info("Dependencies installed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error installing dependencies: {e}")
            return False
    
    def _initialize_git_repository(self, project_path: Path) -> bool:
        """
        Initialize a Git repository for the project.
        
        Args:
            project_path: Path to project directory
            
        Returns:
            bool: True if Git repository initialized successfully
        """
        try:
            # Initialize Git repository
            result = subprocess.run(
                ["git", "init"],
                capture_output=True,
                text=True,
                cwd=project_path
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to initialize Git repository: {result.stderr}")
                return False
            
            # Add all files
            result = subprocess.run(
                ["git", "add", "."],
                capture_output=True,
                text=True,
                cwd=project_path
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to add files to Git: {result.stderr}")
                return False
            
            # Create initial commit
            result = subprocess.run(
                ["git", "commit", "-m", "Initial commit - Project generated by Project Architect"],
                capture_output=True,
                text=True,
                cwd=project_path
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to create initial commit: {result.stderr}")
                return False
            
            self.logger.info("Git repository initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing Git repository: {e}")
            return False
    
    def _create_github_repository(self, project_path: Path, responses: QuestionnaireResponse) -> bool:
        """
        Create a GitHub repository for the project.
        
        Args:
            project_path: Path to project directory
            responses: Questionnaire responses
            
        Returns:
            bool: True if GitHub repository created successfully
        """
        try:
            # Check if GitHub CLI is available
            result = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.logger.error("GitHub CLI (gh) not found. Please install it to create GitHub repositories.")
                return False
            
            # Get repository visibility
            visibility = responses.responses.get('github_visibility', 'private')
            visibility_flag = "--private" if visibility == "private" else "--public"
            
            # Create GitHub repository
            result = subprocess.run(
                ["gh", "repo", "create", responses.project_name, visibility_flag, "--source=.", "--push"],
                capture_output=True,
                text=True,
                cwd=project_path
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to create GitHub repository: {result.stderr}")
                return False
            
            self.logger.info(f"GitHub repository created successfully: {responses.project_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating GitHub repository: {e}")
            return False
    
    def _validate_generated_project(self, project_path: Path) -> bool:
        """
        Validate the generated project structure.
        
        Args:
            project_path: Path to project directory
            
        Returns:
            bool: True if project structure is valid
        """
        try:
            # Check if main files exist
            required_files = [
                "README.md",
                "CHANGELOG.md",
                "IMPLEMENTATION_PLAN.md",
                "TECHNICAL_SPECIFICATION.md"
            ]
            
            for file_name in required_files:
                file_path = project_path / file_name
                if not file_path.exists():
                    self.logger.warning(f"Required file missing: {file_name}")
                    return False
            
            # Check if main directories exist
            required_dirs = [
                "src",
                "tests",
                "docs",
                "dev_sessions"
            ]
            
            for dir_name in required_dirs:
                dir_path = project_path / dir_name
                if not dir_path.exists():
                    self.logger.warning(f"Required directory missing: {dir_name}")
                    return False
            
            self.logger.info("Project structure validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating project structure: {e}")
            return False
