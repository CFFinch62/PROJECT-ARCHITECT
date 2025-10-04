"""
Project Architect Settings Management

Handles application configuration, user preferences, and settings persistence.
Provides a centralized way to manage all application settings.

Author: Chuck Finch - Fragillidae Software
"""

import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class AppSettings:
    """Application settings data structure."""
    appearance_mode: str = "dark"
    color_theme: str = "blue"
    default_output_dir: str = "generated_projects"
    auto_git_init: bool = True
    auto_venv_create: bool = True
    default_python_version: str = "3.12"
    max_recent_projects: int = 10
    enable_logging: bool = True
    log_level: str = "INFO"
    template_validation: bool = True
    backup_generated_projects: bool = False


class Settings:
    """
    Settings management class for Project Architect.
    
    Handles loading, saving, and managing application settings,
    user preferences, and configuration data.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize settings manager.
        
        Args:
            config_dir: Optional custom configuration directory
        """
        self.logger = logging.getLogger(__name__)
        
        # Set configuration directory
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path(__file__).parent.parent.parent / "data"
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration files
        self.config_file = self.config_dir / "config.yaml"
        self.user_profiles_file = self.config_dir / "user_profiles.json"
        
        # Initialize settings
        self.settings = AppSettings()
        self.user_profiles = {}
        self.current_profile = "default"
        
        self.logger.info(f"Settings initialized with config dir: {self.config_dir}")
    
    def load_settings(self) -> bool:
        """
        Load settings from configuration file.
        
        Returns:
            bool: True if settings loaded successfully, False otherwise
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                
                if config_data:
                    # Update settings with loaded data
                    for key, value in config_data.items():
                        if hasattr(self.settings, key):
                            setattr(self.settings, key, value)
                
                self.logger.info("Settings loaded successfully")
                return True
            else:
                self.logger.info("No config file found, using defaults")
                self.save_settings()  # Create default config file
                return True
                
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            return False
    
    def save_settings(self) -> bool:
        """
        Save current settings to configuration file.
        
        Returns:
            bool: True if settings saved successfully, False otherwise
        """
        try:
            config_data = asdict(self.settings)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
            
            self.logger.info("Settings saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value.
        
        Args:
            key: Setting key
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        return getattr(self.settings, key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set a setting value.
        
        Args:
            key: Setting key
            value: Setting value
            
        Returns:
            bool: True if setting was set successfully
        """
        try:
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
                return True
            else:
                self.logger.warning(f"Unknown setting key: {key}")
                return False
        except Exception as e:
            self.logger.error(f"Error setting {key}: {e}")
            return False
    
    def load_user_profiles(self) -> bool:
        """
        Load user profiles from file.
        
        Returns:
            bool: True if profiles loaded successfully
        """
        try:
            if self.user_profiles_file.exists():
                with open(self.user_profiles_file, 'r', encoding='utf-8') as f:
                    self.user_profiles = json.load(f)
                
                self.logger.info("User profiles loaded successfully")
                return True
            else:
                # Create default profile
                self.user_profiles = {
                    "default": {
                        "name": "Default Profile",
                        "preferred_project_type": "desktop_gui",
                        "default_author": "",
                        "default_email": "",
                        "preferred_gui_framework": "customtkinter",
                        "preferred_testing_framework": "pytest",
                        "include_git_init": True,
                        "include_venv_setup": True,
                        "created_at": "2025-10-04"
                    }
                }
                self.save_user_profiles()
                return True
                
        except Exception as e:
            self.logger.error(f"Error loading user profiles: {e}")
            return False
    
    def save_user_profiles(self) -> bool:
        """
        Save user profiles to file.
        
        Returns:
            bool: True if profiles saved successfully
        """
        try:
            with open(self.user_profiles_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_profiles, f, indent=2)
            
            self.logger.info("User profiles saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving user profiles: {e}")
            return False
    
    def get_profile(self, profile_name: str = None) -> Dict[str, Any]:
        """
        Get user profile data.
        
        Args:
            profile_name: Profile name (uses current if None)
            
        Returns:
            Profile data dictionary
        """
        if profile_name is None:
            profile_name = self.current_profile
        
        return self.user_profiles.get(profile_name, self.user_profiles.get("default", {}))
    
    def set_profile(self, profile_name: str, profile_data: Dict[str, Any]) -> bool:
        """
        Set user profile data.
        
        Args:
            profile_name: Profile name
            profile_data: Profile data dictionary
            
        Returns:
            bool: True if profile set successfully
        """
        try:
            self.user_profiles[profile_name] = profile_data
            return True
        except Exception as e:
            self.logger.error(f"Error setting profile {profile_name}: {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """
        Get all settings as dictionary.
        
        Returns:
            Dictionary of all settings
        """
        return asdict(self.settings)
    
    def reset_to_defaults(self) -> bool:
        """
        Reset all settings to defaults.
        
        Returns:
            bool: True if reset successful
        """
        try:
            self.settings = AppSettings()
            self.save_settings()
            self.logger.info("Settings reset to defaults")
            return True
        except Exception as e:
            self.logger.error(f"Error resetting settings: {e}")
            return False
