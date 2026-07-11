"""
Project Architect File Operations

Safe file and directory operations for project generation.

Author: Chuck Finch - Fragillidae Software
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime


class FileOperations:
    """File and directory operations with safety checks and backup functionality."""
    
    def __init__(self):
        """Initialize file operations."""
        self.logger = logging.getLogger(__name__)
    
    def create_directory(self, path: Path, parents: bool = True, exist_ok: bool = True) -> bool:
        """
        Create a directory safely.
        
        Args:
            path: Directory path to create
            parents: Create parent directories if needed
            exist_ok: Don't raise error if directory exists
            
        Returns:
            bool: True if successful
        """
        try:
            path = Path(path)
            path.mkdir(parents=parents, exist_ok=exist_ok)
            self.logger.info(f"Created directory: {path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create directory {path}: {e}")
            return False
    
    def write_file(self, path: Path, content: str, backup: bool = True) -> bool:
        """
        Write content to a file safely.
        
        Args:
            path: File path
            content: Content to write
            backup: Create backup if file exists
            
        Returns:
            bool: True if successful
        """
        try:
            path = Path(path)
            
            # Create parent directories
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Backup existing file
            if backup and path.exists():
                self._backup_file(path)
            
            # Write file
            path.write_text(content, encoding='utf-8')
            self.logger.info(f"Wrote file: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to write file {path}: {e}")
            return False
    
    def read_file(self, path: Path) -> Optional[str]:
        """
        Read file content safely.
        
        Args:
            path: File path
            
        Returns:
            File content or None if error
        """
        try:
            path = Path(path)
            content = path.read_text(encoding='utf-8')
            return content
        except Exception as e:
            self.logger.error(f"Failed to read file {path}: {e}")
            return None
    
    def copy_file(self, source: Path, destination: Path, backup: bool = True) -> bool:
        """
        Copy file safely.
        
        Args:
            source: Source file path
            destination: Destination file path
            backup: Create backup if destination exists
            
        Returns:
            bool: True if successful
        """
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                self.logger.error(f"Source file does not exist: {source}")
                return False
            
            # Create parent directories
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Backup existing file
            if backup and destination.exists():
                self._backup_file(destination)
            
            # Copy file
            shutil.copy2(source, destination)
            self.logger.info(f"Copied {source} to {destination}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to copy file: {e}")
            return False
    
    def delete_file(self, path: Path, backup: bool = True) -> bool:
        """
        Delete file safely.
        
        Args:
            path: File path
            backup: Create backup before deleting
            
        Returns:
            bool: True if successful
        """
        try:
            path = Path(path)
            
            if not path.exists():
                self.logger.warning(f"File does not exist: {path}")
                return True
            
            # Backup before deleting
            if backup:
                self._backup_file(path)
            
            path.unlink()
            self.logger.info(f"Deleted file: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete file {path}: {e}")
            return False
    
    def delete_directory(self, path: Path, recursive: bool = False, backup: bool = True) -> bool:
        """
        Delete directory safely.
        
        Args:
            path: Directory path
            recursive: Delete contents recursively
            backup: Create backup before deleting
            
        Returns:
            bool: True if successful
        """
        try:
            path = Path(path)
            
            if not path.exists():
                self.logger.warning(f"Directory does not exist: {path}")
                return True
            
            # Backup before deleting
            if backup:
                self._backup_directory(path)
            
            if recursive:
                shutil.rmtree(path)
            else:
                path.rmdir()
            
            self.logger.info(f"Deleted directory: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete directory {path}: {e}")
            return False
    
    def _backup_file(self, path: Path) -> Optional[Path]:
        """
        Create backup of file.
        
        Args:
            path: File to backup
            
        Returns:
            Backup file path or None if error
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = path.with_suffix(f"{path.suffix}.backup_{timestamp}")
            shutil.copy2(path, backup_path)
            self.logger.info(f"Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return None
    
    def _backup_directory(self, path: Path) -> Optional[Path]:
        """
        Create backup of directory.
        
        Args:
            path: Directory to backup
            
        Returns:
            Backup directory path or None if error
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = path.with_name(f"{path.name}_backup_{timestamp}")
            shutil.copytree(path, backup_path)
            self.logger.info(f"Created directory backup: {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Failed to create directory backup: {e}")
            return None
    
    def validate_path(self, path: str) -> bool:
        """
        Validate a file path for safety.
        
        Args:
            path: Path to validate
            
        Returns:
            bool: True if path is valid and safe
        """
        try:
            path_obj = Path(path)
            
            # Check for directory traversal attempts
            if ".." in path_obj.parts:
                self.logger.warning(f"Path contains directory traversal: {path}")
                return False
            
            # Check for absolute paths that go outside project
            if path_obj.is_absolute():
                # Could add more checks here
                pass
            
            return True
            
        except Exception as e:
            self.logger.error(f"Path validation error: {e}")
            return False
    
    def ensure_directory(self, path: Path) -> bool:
        """
        Ensure directory exists, create if necessary.
        
        Args:
            path: Directory path
            
        Returns:
            bool: True if directory exists or was created
        """
        return self.create_directory(path, parents=True, exist_ok=True)
    
    def list_directory(self, path: Path, pattern: str = "*") -> List[Path]:
        """
        List files in directory.
        
        Args:
            path: Directory path
            pattern: Glob pattern
            
        Returns:
            List of paths
        """
        try:
            path = Path(path)
            if not path.exists():
                return []
            return list(path.glob(pattern))
        except Exception as e:
            self.logger.error(f"Error listing directory {path}: {e}")
            return []
