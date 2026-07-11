"""
Project Architect Template Configuration

Template configuration parsing and validation.

Author: Chuck Finch - Fragillidae Software
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


class TemplateConfig:
    """Template configuration management and validation."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize template configuration.
        
        Args:
            config_path: Path to template.yaml file
        """
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path
        self.config_data: Dict[str, Any] = {}
        
        if config_path:
            self.load_config()
    
    def load_config(self, config_path: Optional[Path] = None) -> bool:
        """
        Load template configuration from YAML file.
        
        Args:
            config_path: Path to config file (uses self.config_path if None)
            
        Returns:
            bool: True if successful
        """
        try:
            if config_path:
                self.config_path = config_path
            
            if not self.config_path or not self.config_path.exists():
                self.logger.error(f"Config file not found: {self.config_path}")
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f)
            
            # Validate config structure
            if not self.validate_config():
                return False
            
            self.logger.info(f"Loaded template config from {self.config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading template config: {e}")
            return False
    
    def validate_config(self) -> bool:
        """
        Validate template configuration structure.
        
        Returns:
            bool: True if valid
        """
        try:
            # Check required top-level sections
            required_sections = ['template', 'structure']
            
            for section in required_sections:
                if section not in self.config_data:
                    self.logger.error(f"Missing required section: {section}")
                    return False
            
            # Validate template metadata
            template = self.config_data.get('template', {})
            required_template_fields = ['name', 'type', 'description']
            
            for field in required_template_fields:
                if field not in template:
                    self.logger.error(f"Missing required template field: {field}")
                    return False
            
            # Validate structure
            structure = self.config_data.get('structure', [])
            
            if not isinstance(structure, list):
                self.logger.error("Structure must be a list")
                return False
            
            for i, item in enumerate(structure):
                if not isinstance(item, dict):
                    self.logger.error(f"Structure item {i} must be a dictionary")
                    return False
                
                if 'path' not in item or 'type' not in item:
                    self.logger.error(f"Structure item {i} missing path or type")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating config: {e}")
            return False
    
    def get_template_info(self) -> Dict[str, Any]:
        """
        Get template metadata.
        
        Returns:
            Dict with template info
        """
        return self.config_data.get('template', {})
    
    def get_template_name(self) -> str:
        """Get template name."""
        return self.get_template_info().get('name', 'Unknown')
    
    def get_template_type(self) -> str:
        """Get template type."""
        return self.get_template_info().get('type', 'unknown')
    
    def get_template_description(self) -> str:
        """Get template description."""
        return self.get_template_info().get('description', '')
    
    def get_template_version(self) -> str:
        """Get template version."""
        return self.get_template_info().get('version', '1.0.0')
    
    def get_frameworks(self) -> List[str]:
        """Get supported frameworks."""
        return self.get_template_info().get('frameworks', [])
    
    def get_structure(self) -> List[Dict[str, Any]]:
        """
        Get project structure definition.
        
        Returns:
            List of structure items
        """
        return self.config_data.get('structure', [])
    
    def get_requirements(self) -> Dict[str, List[str]]:
        """
        Get template requirements by framework.
        
        Returns:
            Dict mapping framework to requirements
        """
        return self.config_data.get('requirements', {})
    
    def get_dev_tools(self) -> Dict[str, List[str]]:
        """
        Get development tools configuration.
        
        Returns:
            Dict with dev tool configs
        """
        return self.config_data.get('dev_tools', {})
    
    def get_git_ignore_patterns(self) -> List[str]:
        """
        Get gitignore patterns.
        
        Returns:
            List of patterns for .gitignore
        """
        return self.config_data.get('git_ignore', [])
    
    def get_file_structure_item(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Get structure item by path.
        
        Args:
            path: File/directory path
            
        Returns:
            Structure item dict or None
        """
        structure = self.get_structure()
        
        for item in structure:
            if item.get('path') == path:
                return item
        
        return None
    
    def get_files_by_type(self, item_type: str) -> List[Dict[str, Any]]:
        """
        Get structure items by type.
        
        Args:
            item_type: 'file' or 'directory'
            
        Returns:
            List of matching items
        """
        structure = self.get_structure()
        return [item for item in structure if item.get('type') == item_type]
    
    def get_template_files(self) -> List[str]:
        """
        Get list of template file paths.
        
        Returns:
            List of .j2 template file paths
        """
        templates = []
        structure = self.get_structure()
        
        for item in structure:
            if item.get('type') == 'file' and 'template' in item:
                templates.append(item['template'])
        
        return templates
    
    def validate_template_files_exist(self, template_dir: Path) -> List[str]:
        """
        Validate that all referenced template files exist.
        
        Args:
            template_dir: Directory containing template files
            
        Returns:
            List of missing template files
        """
        missing = []
        template_files = self.get_template_files()
        
        for template_file in template_files:
            full_path = template_dir / template_file
            if not full_path.exists():
                missing.append(template_file)
        
        if missing:
            self.logger.warning(f"Missing template files: {missing}")
        
        return missing
    
    def get_config_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation path.
        
        Args:
            key_path: Dot-separated path (e.g., 'template.name')
            default: Default value if not found
            
        Returns:
            Configuration value or default
        """
        try:
            keys = key_path.split('.')
            value = self.config_data
            
            for key in keys:
                value = value[key]
            
            return value
            
        except (KeyError, TypeError):
            return default
