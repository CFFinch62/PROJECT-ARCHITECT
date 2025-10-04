"""
Project Architect Template Engine

Handles template processing, variable substitution, and file generation
for both new projects and project updates.

Author: Chuck Finch - Fragillidae Software
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import json
import yaml

from jinja2 import Environment, FileSystemLoader, Template, TemplateError
from jinja2.exceptions import TemplateNotFound, TemplateSyntaxError

from .questionnaire import QuestionnaireResponse


class TemplateEngine:
    """
    Template processing engine using Jinja2 for generating project files
    and documentation from questionnaire responses.
    """
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize template engine.
        
        Args:
            templates_dir: Directory containing project templates
        """
        self.logger = logging.getLogger(__name__)
        
        # Set templates directory
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            self.templates_dir = Path(__file__).parent.parent / "templates"
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        
        # Add custom filters
        self._add_custom_filters()
        
        # Template cache
        self.template_cache: Dict[str, Template] = {}
        
        self.logger.info(f"TemplateEngine initialized with templates from {self.templates_dir}")
    
    def _add_custom_filters(self):
        """Add custom Jinja2 filters for project generation."""
        
        def snake_case(text: str) -> str:
            """Convert text to snake_case."""
            # Replace spaces and hyphens with underscores
            text = re.sub(r'[-\s]+', '_', str(text))
            # Insert underscores before capital letters
            text = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
            return text.lower()
        
        def pascal_case(text: str) -> str:
            """Convert text to PascalCase."""
            # Split on spaces, hyphens, and underscores
            words = re.split(r'[-_\s]+', str(text))
            return ''.join(word.capitalize() for word in words if word)
        
        def camel_case(text: str) -> str:
            """Convert text to camelCase."""
            pascal = pascal_case(text)
            return pascal[0].lower() + pascal[1:] if pascal else ""
        
        def kebab_case(text: str) -> str:
            """Convert text to kebab-case."""
            # Replace spaces and underscores with hyphens
            text = re.sub(r'[_\s]+', '-', str(text))
            # Insert hyphens before capital letters
            text = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', text)
            return text.lower()
        
        def title_case(text: str) -> str:
            """Convert text to Title Case."""
            return str(text).title()
        
        def current_date(format_str: str = "%Y-%m-%d") -> str:
            """Get current date in specified format."""
            return datetime.now().strftime(format_str)
        
        def current_year() -> str:
            """Get current year."""
            return str(datetime.now().year)
        
        def indent_text(text: str, spaces: int = 4) -> str:
            """Indent text by specified number of spaces."""
            lines = str(text).split('\n')
            indent = ' ' * spaces
            return '\n'.join(indent + line if line.strip() else line for line in lines)
        
        # Register filters
        self.jinja_env.filters['snake_case'] = snake_case
        self.jinja_env.filters['pascal_case'] = pascal_case
        self.jinja_env.filters['camel_case'] = camel_case
        self.jinja_env.filters['kebab_case'] = kebab_case
        self.jinja_env.filters['title_case'] = title_case
        self.jinja_env.filters['current_date'] = current_date
        self.jinja_env.filters['current_year'] = current_year
        self.jinja_env.filters['indent'] = indent_text
    
    def load_template_config(self, project_type: str) -> Optional[Dict[str, Any]]:
        """
        Load template configuration for a project type.
        
        Args:
            project_type: Type of project template
            
        Returns:
            Template configuration dictionary or None if not found
        """
        try:
            config_file = self.templates_dir / project_type / "template.yaml"
            
            if not config_file.exists():
                # Try JSON format as fallback
                config_file = self.templates_dir / project_type / "template.json"
                
                if not config_file.exists():
                    self.logger.error(f"Template configuration not found for {project_type}")
                    return None
            
            # Load configuration
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.suffix == '.yaml':
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
            
            self.logger.info(f"Loaded template configuration for {project_type}")
            return config
            
        except Exception as e:
            self.logger.error(f"Error loading template configuration for {project_type}: {e}")
            return None
    
    def get_template(self, template_path: str) -> Optional[Template]:
        """
        Get a Jinja2 template, using cache if available.
        
        Args:
            template_path: Path to template file relative to templates directory
            
        Returns:
            Jinja2 Template object or None if not found
        """
        try:
            # Check cache first
            if template_path in self.template_cache:
                return self.template_cache[template_path]
            
            # Load template
            template = self.jinja_env.get_template(template_path)
            
            # Cache template
            self.template_cache[template_path] = template
            
            return template
            
        except TemplateNotFound:
            self.logger.error(f"Template not found: {template_path}")
            return None
        except TemplateSyntaxError as e:
            self.logger.error(f"Template syntax error in {template_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error loading template {template_path}: {e}")
            return None
    
    def render_template(self, template_path: str, context: Dict[str, Any]) -> Optional[str]:
        """
        Render a template with the given context.
        
        Args:
            template_path: Path to template file
            context: Template context variables
            
        Returns:
            Rendered template content or None if error
        """
        try:
            template = self.get_template(template_path)
            if not template:
                return None
            
            # Add common context variables
            enhanced_context = self._enhance_context(context)
            
            # Render template
            content = template.render(**enhanced_context)
            
            return content
            
        except TemplateError as e:
            self.logger.error(f"Template rendering error for {template_path}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error rendering template {template_path}: {e}")
            return None
    
    def _enhance_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance template context with additional variables.
        
        Args:
            context: Original context
            
        Returns:
            Enhanced context with additional variables
        """
        enhanced = context.copy()
        
        # Add current date/time information
        now = datetime.now()
        enhanced.update({
            'current_date': now.strftime('%Y-%m-%d'),
            'current_time': now.strftime('%H:%M:%S'),
            'current_datetime': now.isoformat(),
            'current_year': str(now.year),
            'current_month': now.strftime('%B'),
            'current_day': str(now.day)
        })
        
        # Add project name variations if project_name exists
        if 'project_name' in context:
            project_name = str(context['project_name'])
            enhanced.update({
                'project_name_snake': self.jinja_env.filters['snake_case'](project_name),
                'project_name_pascal': self.jinja_env.filters['pascal_case'](project_name),
                'project_name_camel': self.jinja_env.filters['camel_case'](project_name),
                'project_name_kebab': self.jinja_env.filters['kebab_case'](project_name),
                'project_name_title': self.jinja_env.filters['title_case'](project_name)
            })
        
        # Add author information if available
        if 'author_name' in context:
            enhanced['author'] = context['author_name']
        if 'author_email' in context:
            enhanced['email'] = context['author_email']
        
        return enhanced
    
    def generate_file_from_template(self, template_path: str, output_path: Path, 
                                  context: Dict[str, Any], backup: bool = True) -> bool:
        """
        Generate a file from a template.
        
        Args:
            template_path: Path to template file
            output_path: Path where generated file should be saved
            context: Template context variables
            backup: Whether to backup existing file
            
        Returns:
            bool: True if file generated successfully
        """
        try:
            # Render template
            content = self.render_template(template_path, context)
            if content is None:
                return False
            
            # Create backup if file exists and backup is requested
            if backup and output_path.exists():
                backup_path = output_path.with_suffix(f"{output_path.suffix}.backup")
                output_path.rename(backup_path)
                self.logger.info(f"Created backup: {backup_path}")
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write generated content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Generated file: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating file {output_path}: {e}")
            return False
    
    def generate_project_structure(self, project_type: str, output_dir: Path, 
                                 responses: QuestionnaireResponse) -> bool:
        """
        Generate complete project structure from template.
        
        Args:
            project_type: Type of project template
            output_dir: Directory where project should be generated
            responses: Questionnaire responses
            
        Returns:
            bool: True if project generated successfully
        """
        try:
            # Load template configuration
            config = self.load_template_config(project_type)
            if not config:
                return False
            
            # Prepare context from responses
            context = responses.responses.copy()
            context.update({
                'project_type': project_type,
                'questionnaire_mode': responses.mode.value,
                'generation_timestamp': responses.timestamp
            })
            
            # Get project structure definition
            structure = config.get('structure', [])
            
            # Generate each item in the structure
            success_count = 0
            total_count = len(structure)
            
            for item in structure:
                if self._generate_structure_item(item, output_dir, context, project_type):
                    success_count += 1
                else:
                    self.logger.warning(f"Failed to generate structure item: {item}")
            
            # Generate project metadata
            self._generate_project_metadata(output_dir, responses, config)
            
            self.logger.info(f"Generated {success_count}/{total_count} structure items")
            return success_count == total_count
            
        except Exception as e:
            self.logger.error(f"Error generating project structure: {e}")
            return False
    
    def _generate_structure_item(self, item: Dict[str, Any], output_dir: Path, 
                                context: Dict[str, Any], project_type: str) -> bool:
        """
        Generate a single structure item (file or directory).
        
        Args:
            item: Structure item definition
            output_dir: Output directory
            context: Template context
            project_type: Project type for template path resolution
            
        Returns:
            bool: True if item generated successfully
        """
        try:
            item_path = Path(item['path'])
            item_type = item.get('type', 'file')
            
            # Resolve output path
            output_path = output_dir / item_path
            
            if item_type == 'directory':
                # Create directory
                output_path.mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"Created directory: {output_path}")
                return True
            
            elif item_type == 'file':
                # Generate file from template
                template_path = item.get('template')
                
                if template_path:
                    # Use specified template
                    full_template_path = f"{project_type}/{template_path}"
                    return self.generate_file_from_template(
                        full_template_path, output_path, context, backup=False
                    )
                else:
                    # Create empty file or use content
                    content = item.get('content', '')
                    
                    # Ensure directory exists
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Write content
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    self.logger.debug(f"Created file: {output_path}")
                    return True
            
            else:
                self.logger.error(f"Unknown structure item type: {item_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error generating structure item {item}: {e}")
            return False
    
    def _generate_project_metadata(self, output_dir: Path, responses: QuestionnaireResponse, 
                                 config: Dict[str, Any]) -> bool:
        """
        Generate project metadata files.
        
        Args:
            output_dir: Project output directory
            responses: Questionnaire responses
            config: Template configuration
            
        Returns:
            bool: True if metadata generated successfully
        """
        try:
            # Create .project_architect directory
            metadata_dir = output_dir / ".project_architect"
            metadata_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate project data file
            project_data = {
                'project_name': responses.project_name,
                'project_type': responses.project_type,
                'created_at': responses.timestamp,
                'version': responses.version,
                'responses': responses.responses,
                'template_config': config,
                'generator_version': '1.0.0'
            }
            
            project_data_file = metadata_dir / "project_data.json"
            with open(project_data_file, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2)
            
            # Initialize empty update history
            update_history_file = metadata_dir / "update_history.json"
            with open(update_history_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
            
            self.logger.info("Generated project metadata")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating project metadata: {e}")
            return False
    
    def list_available_templates(self) -> List[str]:
        """
        List all available project templates.
        
        Returns:
            List of template names
        """
        try:
            templates = []
            
            for item in self.templates_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if it has a template configuration
                    config_files = [
                        item / "template.yaml",
                        item / "template.json"
                    ]
                    
                    if any(f.exists() for f in config_files):
                        templates.append(item.name)
            
            return sorted(templates)
            
        except Exception as e:
            self.logger.error(f"Error listing templates: {e}")
            return []
