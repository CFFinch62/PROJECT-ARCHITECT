"""
Project Architect User Profiles

User profile management for storing preferences and recent projects.

Author: Chuck Finch - Fragillidae Software
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class UserProfile:
    """User profile with preferences and project history."""
    
    def __init__(self, profile_path: Optional[Path] = None):
        """
        Initialize user profile.
        
        Args:
            profile_path: Path to profile file (default: ~/.project_architect/profile.json)
        """
        self.logger = logging.getLogger(__name__)
        
        if profile_path is None:
            profile_path = Path.home() /".project_architect" / "profile.json"
        
        self.profile_path = Path(profile_path)
        self.profile_data: Dict[str, Any] = {}
        
        # Load existing profile
        self.load_profile()
    
    def load_profile(self) -> bool:
        """
        Load user profile from disk.
        
        Returns:
            bool: True if successful
        """
        try:
            if not self.profile_path.exists():
                # Create default profile
                self._create_default_profile()
                return True
            
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                self.profile_data = json.load(f)
            
            self.logger.info(f"Loaded profile from {self.profile_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading profile: {e}")
            self._create_default_profile()
            return False
    
    def save_profile(self) -> bool:
        """
        Save user profile to disk.
        
        Returns:
            bool: True if successful
        """
        try:
            # Ensure directory exists
            self.profile_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write profile
            with open(self.profile_path, 'w', encoding='utf-8') as f:
                json.dump(self.profile_data, f, indent=2)
            
            self.logger.info(f"Saved profile to {self.profile_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving profile: {e}")
            return False
    
    def _create_default_profile(self):
        """Create default profile data."""
        self.profile_data = {
            "user_info": {
                "name": "",
                "email": "",
                "organization": ""
            },
            "preferences": {
                "default_template": "desktop_gui",
                "auto_git_init": True,
                "auto_create_venv": True,
                "default_python_version": "3.12",
                "editor": "",
                "theme": "dark"
            },
            "recent_projects": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        # Save default profile
        self.save_profile()
    
    def get_user_info(self, key: str, default: Any = None) -> Any:
        """
        Get user information.
        
        Args:
            key: Info key (name, email, organization)
            default: Default value if not found
            
        Returns:
            User info value
        """
        return self.profile_data.get("user_info", {}).get(key, default)
    
    def set_user_info(self, key: str, value: Any) -> bool:
        """
        Set user information.
        
        Args:
            key: Info key
            value: Value to set
            
        Returns:
            bool: True if successful
        """
        try:
            if "user_info" not in self.profile_data:
                self.profile_data["user_info"] = {}
            
            self.profile_data["user_info"][key] = value
            self.profile_data["last_updated"] = datetime.now().isoformat()
            
            return self.save_profile()
            
        except Exception as e:
            self.logger.error(f"Error setting user info: {e}")
            return False
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Get user preference.
        
        Args:
            key: Preference key
            default: Default value if not found
            
        Returns:
            Preference value
        """
        return self.profile_data.get("preferences", {}).get(key, default)
    
    def set_preference(self, key: str, value: Any) -> bool:
        """
        Set user preference.
        
        Args:
            key: Preference key
            value: Value to set
            
        Returns:
            bool: True if successful
        """
        try:
            if "preferences" not in self.profile_data:
                self.profile_data["preferences"] = {}
            
            self.profile_data["preferences"][key] = value
            self.profile_data["last_updated"] = datetime.now().isoformat()
            
            return self.save_profile()
            
        except Exception as e:
            self.logger.error(f"Error setting preference: {e}")
            return False
    
    def add_recent_project(self, project_path: str, project_name: str, 
                          project_type: str, max_recent: int = 10) -> bool:
        """
        Add project to recent projects list.
        
        Args:
            project_path: Path to project
            project_name: Project name
            project_type: Project type
            max_recent: Maximum number of recent projects to keep
            
        Returns:
            bool: True if successful
        """
        try:
            if "recent_projects" not in self.profile_data:
                self.profile_data["recent_projects"] = []
            
            # Create project entry
            project_entry = {
                "path": str(project_path),
                "name": project_name,
                "type": project_type,
                "last_accessed": datetime.now().isoformat()
            }
            
            # Remove duplicate if exists
            recent = self.profile_data["recent_projects"]
            recent = [p for p in recent if p["path"] != str(project_path)]
            
            # Add to front
            recent.insert(0, project_entry)
            
            # Limit to max_recent
            self.profile_data["recent_projects"] = recent[:max_recent]
            self.profile_data["last_updated"] = datetime.now().isoformat()
            
            return self.save_profile()
            
        except Exception as e:
            self.logger.error(f"Error adding recent project: {e}")
            return False
    
    def get_recent_projects(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get list of recent projects.
        
        Args:
            limit: Maximum number of projects to return
            
        Returns:
            List of recent project entries
        """
        recent = self.profile_data.get("recent_projects", [])
        
        if limit:
            return recent[:limit]
        
        return recent
    
    def remove_recent_project(self, project_path: str) -> bool:
        """
        Remove project from recent list.
        
        Args:
            project_path: Path to project to remove
            
        Returns:
            bool: True if successful
        """
        try:
            if "recent_projects" not in self.profile_data:
                return True
            
            recent = self.profile_data["recent_projects"]
            recent = [p for p in recent if p["path"] != str(project_path)]
            self.profile_data["recent_projects"] = recent
            self.profile_data["last_updated"] = datetime.now().isoformat()
            
            return self.save_profile()
            
        except Exception as e:
            self.logger.error(f"Error removing recent project: {e}")
            return False
    
    def export_profile(self, export_path: Path) -> bool:
        """
        Export profile to file.
        
        Args:
            export_path: Path to export to
            
        Returns:
            bool: True if successful
        """
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.profile_data, f, indent=2)
            
            self.logger.info(f"Exported profile to {export_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting profile: {e}")
            return False
    
    def import_profile(self, import_path: Path) -> bool:
        """
        Import profile from file.
        
        Args:
            import_path: Path to import from
            
        Returns:
            bool: True if successful
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                self.profile_data = json.load(f)
            
            self.profile_data["last_updated"] = datetime.now().isoformat()
            
            self.logger.info(f"Imported profile from {import_path}")
            return self.save_profile()
            
        except Exception as e:
            self.logger.error(f"Error importing profile: {e}")
            return False
