"""
Project Architect Project Updater

Handles updating existing projects with new requirements, features,
and technical specification modifications through additional interviews.

Author: Chuck Finch - Fragillidae Software
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .questionnaire import QuestionnaireEngine, QuestionnaireMode, QuestionnaireResponse


class UpdateType(Enum):
    """Types of project updates supported."""
    TECH_SPEC_REVISION = "tech_spec_revision"
    FEATURE_ADDITION = "feature_addition"
    ARCHITECTURE_CHANGE = "architecture_change"
    DEPENDENCY_UPDATE = "dependency_update"
    DOCUMENTATION_UPDATE = "documentation_update"
    CONFIGURATION_CHANGE = "configuration_change"


@dataclass
class ProjectUpdate:
    """
    Represents a project update with metadata.
    """
    update_id: str
    update_type: UpdateType
    description: str
    timestamp: str
    changes: Dict[str, Any]
    previous_version: str
    new_version: str
    author: str = ""
    
    def __post_init__(self):
        """Convert string type to enum if needed."""
        if isinstance(self.update_type, str):
            self.update_type = UpdateType(self.update_type)


class ProjectUpdater:
    """
    Manages updates to existing projects through additional interviews
    and technical specification modifications.
    """
    
    def __init__(self, project_path: Path):
        """
        Initialize project updater for a specific project.
        
        Args:
            project_path: Path to the existing project
        """
        self.logger = logging.getLogger(__name__)
        self.project_path = Path(project_path)
        
        # Project metadata paths
        self.project_data_dir = self.project_path / ".project_architect"
        self.project_data_file = self.project_data_dir / "project_data.json"
        self.update_history_file = self.project_data_dir / "update_history.json"
        self.tech_spec_file = self.project_path / "TECHNICAL_SPECIFICATION.md"
        
        # Initialize data structures
        self.project_data: Dict[str, Any] = {}
        self.update_history: List[ProjectUpdate] = []
        self.questionnaire_engine = QuestionnaireEngine()
        
        # Load existing project data
        self._load_project_data()
        self._load_update_history()
        
        self.logger.info(f"ProjectUpdater initialized for {self.project_path}")
    
    def _load_project_data(self) -> bool:
        """
        Load existing project data.
        
        Returns:
            bool: True if data loaded successfully
        """
        try:
            if self.project_data_file.exists():
                with open(self.project_data_file, 'r', encoding='utf-8') as f:
                    self.project_data = json.load(f)
                
                self.logger.info("Project data loaded successfully")
                return True
            else:
                self.logger.warning("No existing project data found")
                # Initialize with minimal data
                self.project_data = {
                    'project_name': self.project_path.name,
                    'project_type': 'unknown',
                    'created_at': datetime.now().isoformat(),
                    'version': '1.0.0',
                    'responses': {}
                }
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading project data: {e}")
            return False
    
    def _load_update_history(self) -> bool:
        """
        Load project update history.
        
        Returns:
            bool: True if history loaded successfully
        """
        try:
            if self.update_history_file.exists():
                with open(self.update_history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                
                self.update_history = [ProjectUpdate(**update) for update in history_data]
                self.logger.info(f"Loaded {len(self.update_history)} project updates")
                return True
            else:
                self.update_history = []
                return True
                
        except Exception as e:
            self.logger.error(f"Error loading update history: {e}")
            return False
    
    def _save_project_data(self) -> bool:
        """
        Save project data to file.
        
        Returns:
            bool: True if saved successfully
        """
        try:
            # Ensure directory exists
            self.project_data_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.project_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.project_data, f, indent=2)
            
            self.logger.info("Project data saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving project data: {e}")
            return False
    
    def _save_update_history(self) -> bool:
        """
        Save update history to file.
        
        Returns:
            bool: True if saved successfully
        """
        try:
            # Ensure directory exists
            self.project_data_dir.mkdir(parents=True, exist_ok=True)
            
            # Convert to dictionaries for JSON serialization
            history_data = []
            for update in self.update_history:
                update_dict = {
                    'update_id': update.update_id,
                    'update_type': update.update_type.value,
                    'description': update.description,
                    'timestamp': update.timestamp,
                    'changes': update.changes,
                    'previous_version': update.previous_version,
                    'new_version': update.new_version,
                    'author': update.author
                }
                history_data.append(update_dict)
            
            with open(self.update_history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2)
            
            self.logger.info("Update history saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving update history: {e}")
            return False
    
    def start_update_interview(self, update_type: UpdateType) -> bool:
        """
        Start an update interview for the specified update type.
        
        Args:
            update_type: Type of update to perform
            
        Returns:
            bool: True if interview started successfully
        """
        try:
            # Determine questionnaire mode based on update type
            if update_type == UpdateType.TECH_SPEC_REVISION:
                mode = QuestionnaireMode.TECH_SPEC_UPDATE
            elif update_type == UpdateType.FEATURE_ADDITION:
                mode = QuestionnaireMode.FEATURE_ADDITION
            else:
                mode = QuestionnaireMode.UPDATE_PROJECT
            
            # Load appropriate questionnaire
            project_type = self.project_data.get('project_type', 'desktop_gui')
            success = self.questionnaire_engine.load_questionnaire(project_type, mode)
            
            if not success:
                self.logger.error(f"Failed to load questionnaire for {project_type} ({mode.value})")
                return False
            
            # Load existing responses
            self.questionnaire_engine.responses = self.project_data.get('responses', {}).copy()
            
            self.logger.info(f"Started {update_type.value} interview")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting update interview: {e}")
            return False
    
    def complete_update_interview(self, update_description: str, author: str = "") -> Optional[ProjectUpdate]:
        """
        Complete the update interview and create an update record.
        
        Args:
            update_description: Description of the update
            author: Author of the update
            
        Returns:
            ProjectUpdate object if successful, None otherwise
        """
        try:
            if not self.questionnaire_engine.is_complete():
                self.logger.error("Questionnaire is not complete")
                return None
            
            # Generate update ID
            update_id = f"update_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Get current version and increment
            current_version = self.project_data.get('version', '1.0.0')
            new_version = self._increment_version(current_version)
            
            # Create update record
            update = ProjectUpdate(
                update_id=update_id,
                update_type=UpdateType.TECH_SPEC_REVISION,  # Default, can be customized
                description=update_description,
                timestamp=datetime.now().isoformat(),
                changes=self._calculate_changes(),
                previous_version=current_version,
                new_version=new_version,
                author=author
            )
            
            # Update project data
            self.project_data['responses'].update(self.questionnaire_engine.responses)
            self.project_data['version'] = new_version
            self.project_data['last_updated'] = update.timestamp
            
            # Add to update history
            self.update_history.append(update)
            
            # Save data
            self._save_project_data()
            self._save_update_history()
            
            self.logger.info(f"Update completed: {update_id}")
            return update
            
        except Exception as e:
            self.logger.error(f"Error completing update interview: {e}")
            return None
    
    def _calculate_changes(self) -> Dict[str, Any]:
        """
        Calculate changes between old and new responses.
        
        Returns:
            Dictionary of changes
        """
        old_responses = self.project_data.get('responses', {})
        new_responses = self.questionnaire_engine.responses
        
        changes = {
            'added': {},
            'modified': {},
            'removed': {}
        }
        
        # Find added and modified
        for key, value in new_responses.items():
            if key not in old_responses:
                changes['added'][key] = value
            elif old_responses[key] != value:
                changes['modified'][key] = {
                    'old': old_responses[key],
                    'new': value
                }
        
        # Find removed
        for key, value in old_responses.items():
            if key not in new_responses:
                changes['removed'][key] = value
        
        return changes
    
    def _increment_version(self, version: str) -> str:
        """
        Increment version number (patch level).
        
        Args:
            version: Current version string
            
        Returns:
            Incremented version string
        """
        try:
            # Parse semantic version (major.minor.patch)
            match = re.match(r'^(\d+)\.(\d+)\.(\d+)(.*)$', version)
            if match:
                major, minor, patch, suffix = match.groups()
                new_patch = int(patch) + 1
                return f"{major}.{minor}.{new_patch}{suffix}"
            else:
                # Fallback: append .1
                return f"{version}.1"
        except Exception:
            return f"{version}.1"
    
    def update_technical_specification(self, update: ProjectUpdate) -> bool:
        """
        Update the technical specification document based on the update.
        
        Args:
            update: ProjectUpdate containing changes
            
        Returns:
            bool: True if updated successfully
        """
        try:
            if not self.tech_spec_file.exists():
                self.logger.warning("Technical specification file not found")
                return False
            
            # Read current tech spec
            with open(self.tech_spec_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add update section
            update_section = self._generate_update_section(update)
            
            # Find insertion point (before "## Future Enhancements" or at end)
            insertion_patterns = [
                r'(## Future Enhancements)',
                r'(## Appendix)',
                r'(\Z)'  # End of file
            ]
            
            inserted = False
            for pattern in insertion_patterns:
                if re.search(pattern, content):
                    content = re.sub(
                        pattern,
                        f"{update_section}\n\n\\1",
                        content,
                        count=1
                    )
                    inserted = True
                    break
            
            if not inserted:
                content += f"\n\n{update_section}"
            
            # Write updated content
            with open(self.tech_spec_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info("Technical specification updated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating technical specification: {e}")
            return False
    
    def _generate_update_section(self, update: ProjectUpdate) -> str:
        """
        Generate markdown section for the update.
        
        Args:
            update: ProjectUpdate to document
            
        Returns:
            Markdown content for the update
        """
        section = f"## Update {update.new_version} - {update.timestamp[:10]}\n\n"
        section += f"**Update Type:** {update.update_type.value.replace('_', ' ').title()}\n"
        section += f"**Description:** {update.description}\n"
        
        if update.author:
            section += f"**Author:** {update.author}\n"
        
        section += f"**Previous Version:** {update.previous_version}\n\n"
        
        # Document changes
        changes = update.changes
        
        if changes.get('added'):
            section += "### New Requirements\n"
            for key, value in changes['added'].items():
                section += f"- **{key}**: {value}\n"
            section += "\n"
        
        if changes.get('modified'):
            section += "### Modified Requirements\n"
            for key, change in changes['modified'].items():
                section += f"- **{key}**: Changed from '{change['old']}' to '{change['new']}'\n"
            section += "\n"
        
        if changes.get('removed'):
            section += "### Removed Requirements\n"
            for key, value in changes['removed'].items():
                section += f"- **{key}**: {value} (removed)\n"
            section += "\n"
        
        return section
    
    def get_update_history(self) -> List[ProjectUpdate]:
        """
        Get the complete update history for the project.
        
        Returns:
            List of ProjectUpdate objects
        """
        return self.update_history.copy()
    
    def get_project_info(self) -> Dict[str, Any]:
        """
        Get current project information.
        
        Returns:
            Dictionary with project information
        """
        return {
            'name': self.project_data.get('project_name', 'Unknown'),
            'type': self.project_data.get('project_type', 'Unknown'),
            'version': self.project_data.get('version', '1.0.0'),
            'created_at': self.project_data.get('created_at', 'Unknown'),
            'last_updated': self.project_data.get('last_updated', 'Never'),
            'update_count': len(self.update_history)
        }
