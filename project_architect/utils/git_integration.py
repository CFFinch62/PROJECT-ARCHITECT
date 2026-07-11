"""
Project Architect Git Integration

Git repository operations and management.

Author: Chuck Finch - Fragillidae Software
"""

import subprocess
import logging
from pathlib import Path
from typing import Optional, List, Tuple


class GitIntegration:
    """Git repository operations."""
    
    def __init__(self):
        """Initialize Git integration."""
        self.logger = logging.getLogger(__name__)
    
    def is_git_available(self) -> bool:
        """
        Check if Git is available on the system.
        
        Returns:
            bool: True if Git is available
        """
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Error checking Git availability: {e}")
            return False
    
    def init_repository(self, path: Path) -> bool:
        """
        Initialize a Git repository.
        
        Args:
            path: Repository path
            
        Returns:
            bool: True if successful
        """
        try:
            if not self.is_git_available():
                self.logger.error("Git is not available")
                return False
            
            result = subprocess.run(
                ['git', 'init'],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.logger.info(f"Initialized Git repository at {path}")
                return True
            else:
                self.logger.error(f"Git init failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error initializing repository: {e}")
            return False
    
    def create_gitignore(self, path: Path, content: str) -> bool:
        """
        Create .gitignore file.
        
        Args:
            path: Repository path
            content: Gitignore content
            
        Returns:
            bool: True if successful
        """
        try:
            gitignore_path = path / '.gitignore'
            gitignore_path.write_text(content, encoding='utf-8')
            self.logger.info(f"Created .gitignore at {path}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating .gitignore: {e}")
            return False
    
    def add_files(self, path: Path, files: Optional[List[str]] = None) -> bool:
        """
        Add files to Git staging area.
        
        Args:
            path: Repository path
            files: List of files to add (None for all files)
            
        Returns:
            bool: True if successful
        """
        try:
            if files is None:
                files = ['.']
            
            result = subprocess.run(
                ['git', 'add'] + files,
                cwd=path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.info(f"Added files to Git: {files}")
                return True
            else:
                self.logger.error(f"Git add failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error adding files: {e}")
            return False
    
    def commit(self, path: Path, message: str) -> bool:
        """
        Create a Git commit.
        
        Args:
            path: Repository path
            message: Commit message
            
        Returns:
            bool: True if successful
        """
        try:
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.info(f"Created commit: {message}")
                return True
            else:
                # Check if it's just "nothing to commit"
                if "nothing to commit" in result.stdout:
                    self.logger.info("Nothing to commit")
                    return True
                self.logger.error(f"Git commit failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating commit: {e}")
            return False
    
    def get_status(self, path: Path) -> Optional[str]:
        """
        Get Git repository status.
        
        Args:
            path: Repository path
            
        Returns:
            Status output or None if error
        """
        try:
            result = subprocess.run(
                ['git', 'status'],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting Git status: {e}")
            return None
    
    def is_repository(self, path: Path) -> bool:
        """
        Check if path is a Git repository.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if it's a Git repository
        """
        try:
            git_dir = path / '.git'
            return git_dir.exists() and git_dir.is_dir()
        except Exception as e:
            self.logger.error(f"Error checking repository: {e}")
            return False
    
    def create_branch(self, path: Path, branch_name: str) -> bool:
        """
        Create a new Git branch.
        
        Args:
            path: Repository path
            branch_name: Name of new branch
            
        Returns:
            bool: True if successful
        """
        try:
            result = subprocess.run(
                ['git', 'branch', branch_name],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.logger.info(f"Created branch: {branch_name}")
                return True
            else:
                self.logger.error(f"Git branch failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating branch: {e}")
            return False
    
    def checkout_branch(self, path: Path, branch_name: str) -> bool:
        """
        Checkout a Git branch.
        
        Args:
            path: Repository path
            branch_name: Branch to checkout
            
        Returns:
            bool: True if successful
        """
        try:
            result = subprocess.run(
                ['git', 'checkout', branch_name],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self.logger.info(f"Checked out branch: {branch_name}")
                return True
            else:
                self.logger.error(f"Git checkout failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error checking out branch: {e}")
            return False
    
    def configure_user(self, path: Path, name: str, email: str, global_config: bool = False) -> bool:
        """
        Configure Git user information.
        
        Args:
            path: Repository path
            name: User name
            email: User email
            global_config: Configure globally vs just this repo
            
        Returns:
            bool: True if successful
        """
        try:
            config_flag = '--global' if global_config else '--local'
            
            # Set name
            result = subprocess.run(
                ['git', 'config', config_flag, 'user.name', name],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to set user name: {result.stderr}")
                return False
            
            # Set email
            result = subprocess.run(
                ['git', 'config', config_flag, 'user.email', email],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to set user email: {result.stderr}")
                return False
            
            self.logger.info(f"Configured Git user: {name} <{email}>")
            return True
            
        except Exception as e:
            self.logger.error(f"Error configuring Git user: {e}")
            return False
