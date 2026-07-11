"""
Tests for utility modules.

Author: Chuck Finch - Fragillidae Software
"""

import pytest
from pathlib import Path
import json

from project_architect.utils.file_operations import FileOperations
from project_architect.utils.git_integration import GitIntegration
from project_architect.utils.user_profiles import UserProfile
from project_architect.utils.template_config import TemplateConfig


class TestFileOperations:
    """Tests for FileOperations class."""
    
    @pytest.fixture
    def file_ops(self):
        """Create FileOperations instance."""
        return FileOperations()
    
    def test_create_directory(self, file_ops, tmp_path):
        """Test directory creation."""
        test_dir = tmp_path / "test_dir"
        success = file_ops.create_directory(test_dir)
        
        assert success is True
        assert test_dir.exists()
        assert test_dir.is_dir()
    
    def test_write_and_read_file(self, file_ops, tmp_path):
        """Test file writing and reading."""
        test_file = tmp_path / "test.txt"
        content = "Hello, World!"
        
        # Write file
        success = file_ops.write_file(test_file, content, backup=False)
        assert success is True
        assert test_file.exists()
        
        # Read file
        read_content = file_ops.read_file(test_file)
        assert read_content == content
    
    def test_copy_file(self, file_ops, tmp_path):
        """Test file copying."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        
        # Create source file
        source.write_text("Test content")
        
        # Copy
        success = file_ops.copy_file(source, dest, backup=False)
        assert success is True
        assert dest.exists()
        assert dest.read_text() == "Test content"
    
    def test_delete_file(self, file_ops, tmp_path):
        """Test file deletion."""
        test_file = tmp_path / "delete_me.txt"
        test_file.write_text("Delete this")
        
        success = file_ops.delete_file(test_file, backup=False)
        assert success is True
        assert not test_file.exists()
    
    def test_validate_path(self, file_ops):
        """Test path validation."""
        # Safe path
        assert file_ops.validate_path("project/file.txt") is True
        
        # Unsafe path with directory traversal
        assert file_ops.validate_path("../../../etc/passwd") is False


class TestGitIntegration:
    """Tests for GitIntegration class."""
    
    @pytest.fixture
    def git(self):
        """Create GitIntegration instance."""
        return GitIntegration()
    
    def test_is_git_available(self, git):
        """Test Git availability check."""
        # Should return True or False, not error
        result = git.is_git_available()
        assert isinstance(result, bool)
    
    @pytest.mark.skipif(not GitIntegration().is_git_available(), 
                       reason="Git not available")
    def test_init_repository(self, git, tmp_path):
        """Test Git repository initialization."""
        success = git.init_repository(tmp_path)
        assert success is True
        assert (tmp_path / '.git').exists()
    
    @pytest.mark.skipif(not GitIntegration().is_git_available(),
                       reason="Git not available")
    def test_create_gitignore(self, git, tmp_path):
        """Test .gitignore creation."""
        content = "*.pyc\n__pycache__/"
        success = git.create_gitignore(tmp_path, content)
        
        assert success is True
        assert(tmp_path / '.gitignore').exists()
        assert (tmp_path / '.gitignore').read_text() == content
    
    @pytest.mark.skipif(not GitIntegration().is_git_available(),
                       reason="Git not available")
    def test_is_repository(self, git, tmp_path):
        """Test repository detection."""
        # Not a repo initially
        assert git.is_repository(tmp_path) is False
        
        # Initialize repo
        git.init_repository(tmp_path)
        
        # Now is a repo
        assert git.is_repository(tmp_path) is True


class TestUserProfile:
    """Tests for UserProfile class."""
    
    @pytest.fixture
    def profile(self, tmp_path):
        """Create UserProfile instance with temp path."""
        profile_path = tmp_path / "profile.json"
        return UserProfile(profile_path)
    
    def test_initialization(self, profile):
        """Test profile initialization."""
        assert profile is not None
        assert profile.profile_data is not None
        assert 'user_info' in profile.profile_data
        assert 'preferences' in profile.profile_data
    
    def test_set_and_get_user_info(self, profile):
        """Test setting and getting user info."""
        profile.set_user_info('name', 'Test User')
        
        name = profile.get_user_info('name')
        assert name == 'Test User'
    
    def test_set_and_get_preference(self, profile):
        """Test setting and getting preferences."""
        profile.set_preference('default_template', 'web_app')
        
        template = profile.get_preference('default_template')
        assert template == 'web_app'
    
    def test_add_recent_project(self, profile):
        """Test adding recent project."""
        success = profile.add_recent_project(
            '/path/to/project',
            'Test Project',
            'desktop_gui'
        )
        
        assert success is True
        
        recent = profile.get_recent_projects()
        assert len(recent) == 1
        assert recent[0]['name'] == 'Test Project'
    
    def test_remove_recent_project(self, profile):
        """Test removing recent project."""
        # Add project
        profile.add_recent_project('/path/to/project', 'Test', 'desktop_gui')
        
        # Remove it
        success = profile.remove_recent_project('/path/to/project')
        assert success is True
        
        # Should be empty
        recent = profile.get_recent_projects()
        assert len(recent) == 0
    
    def test_export_import_profile(self, profile, tmp_path):
        """Test profile export and import."""
        # Set some data
        profile.set_user_info('name', 'Test User')
        profile.set_preference('theme', 'light')
        
        # Export
        export_path = tmp_path / "export.json"
        success = profile.export_profile(export_path)
        assert success is True
        assert export_path.exists()
        
        # Create new profile and import
        profile2_path = tmp_path / "profile2.json"
        profile2 = UserProfile(profile2_path)
        success = profile2.import_profile(export_path)
        
        assert success is True
        assert profile2.get_user_info('name') == 'Test User'
        assert profile2.get_preference('theme') == 'light'


class TestTemplateConfig:
    """Tests for TemplateConfig class."""
    
    @pytest.fixture
    def config(self):
        """Create TemplateConfig for desktop_gui."""
        templates_dir = Path(__file__).parent.parent / 'project_architect' / 'templates'
        config_path = templates_dir / 'desktop_gui' / 'template.yaml'
        return TemplateConfig(config_path)
    
    def test_load_config(self, config):
        """Test loading configuration."""
        assert config.config_data is not None
        assert 'template' in config.config_data
        assert 'structure' in config.config_data
    
    def test_validate_config(self, config):
        """Test configuration validation."""
        is_valid = config.validate_config()
        assert is_valid is True
    
    def test_get_template_info(self, config):
        """Test getting template metadata."""
        info = config.get_template_info()
        
        assert 'name' in info
        assert 'type' in info
        assert 'description' in info
        assert info['type'] == 'desktop_gui'
    
    def test_get_template_name(self, config):
        """Test getting template name."""
        name = config.get_template_name()
        assert name is not None
        assert len(name) > 0
    
    def test_get_structure(self, config):
        """Test getting project structure."""
        structure = config.get_structure()
        
        assert isinstance(structure, list)
        assert len(structure) > 0
    
    def test_get_template_files(self, config):
        """Test getting template file list."""
        templates = config.get_template_files()
        
        assert isinstance(templates, list)
        assert len(templates) > 0
        # Should include main.py.j2
        assert 'main.py.j2' in templates
    
    def test_validate_template_files_exist(self, config):
        """Test validating template files exist."""
        templates_dir = Path(__file__).parent.parent / 'project_architect' / 'templates' / 'desktop_gui'
        
        missing = config.validate_template_files_exist(templates_dir)
        
        # After Phase 1, should have no missing files
        assert len(missing) == 0
    
    def test_get_config_value(self, config):
        """Test dot-notation config access."""
        template_type = config.get_config_value('template.type')
        assert template_type == 'desktop_gui'
        
        # Non-existent key
        result = config.get_config_value('nonexistent.key', 'default')
        assert result == 'default'
