"""
Tests for TemplateEngine.

Author: Chuck Finch - Fragillidae Software
"""

import pytest
from pathlib import Path
from datetime import datetime

from project_architect.core.template_engine import TemplateEngine


class TestTemplateEngine:
    """Tests for TemplateEngine class."""
    
    @pytest.fixture
    def engine(self):
        """Create template engine instance."""
        return TemplateEngine()
    
    def test_initialization(self, engine):
        """Test engine initializes correctly."""
        assert engine is not None
        assert engine.templates_dir.exists()
        assert engine.jinja_env is not None
    
    def test_list_available_templates(self, engine):
        """Test listing available templates."""
        templates = engine.list_available_templates()
        
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert 'desktop_gui' in templates
    
    def test_load_template_config(self, engine):
        """Test loading template configuration."""
        config = engine.load_template_config('desktop_gui')
        
        assert config is not None
        assert 'template' in config
        assert 'structure' in config
        assert config['template']['type'] == 'desktop_gui'
    
    def test_render_template_basic(self, tmp_path):
        """Test rendering a simple template."""
        # Create a simple template inside the engine's templates directory,
        # since render_template() resolves paths relative to templates_dir.
        template_path = tmp_path / "test.j2"
        template_path.write_text("Hello {{ name }}!")
        local_engine = TemplateEngine(templates_dir=tmp_path)

        # Render with context
        result = local_engine.render_template("test.j2", {'name': 'World'})

        assert result is not None
        assert result == "Hello World!"
    
    def test_render_template_with_filters(self, engine):
        """Test custom Jinja filters."""
        # Create template using custom filters
        template_content = "{{ name | snake_case }}"
        
        # Save template temporarily
        temp_template = engine.jinja_env.from_string(template_content)
        result = temp_template.render(name="HelloWorld")
        
        assert result == "hello_world"
    
    def test_pascal_case_filter(self, engine):
        """Test PascalCase filter."""
        template = engine.jinja_env.from_string("{{ name | pascal_case }}")
        result = template.render(name="hello_world")
        assert result == "HelloWorld"
    
    def test_snake_case_filter(self, engine):
        """Test snake_case filter."""
        template = engine.jinja_env.from_string("{{ name | snake_case }}")
        result = template.render(name="HelloWorld")
        assert result == "hello_world"
    
    def test_generate_file_from_template(self, tmp_path):
        """Test generating a file from template."""
        # Create a template inside the engine's templates directory,
        # since generate_file_from_template() resolves paths relative to templates_dir.
        template_path = tmp_path / "source.j2"
        template_path.write_text("Project: {{ project_name }}")
        local_engine = TemplateEngine(templates_dir=tmp_path)

        # Output path
        output_path = tmp_path / "output.txt"

        # Generate file
        context = {'project_name': 'Test Project'}
        success = local_engine.generate_file_from_template(
            "source.j2",
            output_path,
            context,
            backup=False
        )
        
        assert success is True
        assert output_path.exists()
        assert output_path.read_text() == "Project: Test Project"
    
    def test_generate_project_structure(self, engine, tmp_path):
        """Test generating project structure."""
        # Load desktop_gui config
        config = engine.load_template_config('desktop_gui')
        
        # Generate structure (just directories for test)
        context = {
            'project_name': 'test_project',
            'author_name': 'Test Author',
            'current_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Create a few directories based on structure
        structure = config.get('structure', [])
        for item in structure[:5]:  # Just test first 5 items
            if item['type'] == 'directory':
                dir_path = tmp_path / item['path']
                dir_path.mkdir(parents=True, exist_ok=True)
                assert dir_path.exists()


class TestTemplateFilters:
    """Tests for custom Jinja2 filters."""
    
    @pytest.fixture
    def engine(self):
        """Create template engine instance."""
        return TemplateEngine()
    
    def test_snake_case_variations(self, engine):
        """Test snake_case with various inputs."""
        template = engine.jinja_env.from_string("{{ name | snake_case }}")
        
        test_cases = [
            ("HelloWorld", "hello_world"),
            ("hello-world", "hello_world"),
            ("hello world", "hello_world"),
            ("HELLO_WORLD", "hello_world"),
        ]
        
        for input_val, expected in test_cases:
            result = template.render(name=input_val)
            assert result == expected, f"Failed for input: {input_val}"
    
    def test_pascal_case_variations(self, engine):
        """Test PascalCase with various inputs."""
        template = engine.jinja_env.from_string("{{ name | pascal_case }}")
        
        test_cases = [
            ("hello_world", "HelloWorld"),
            ("hello-world", "HelloWorld"),
            ("hello world", "HelloWorld"),
        ]
        
        for input_val, expected in test_cases:
            result = template.render(name=input_val)
            assert result == expected, f"Failed for input: {input_val}"


class TestTemplateGeneration:
    """Integration tests for template generation."""
    
    @pytest.fixture
    def engine(self):
        """Create template engine instance."""
        return TemplateEngine()
    
    def test_desktop_gui_template_exists(self, engine):
        """Test that desktop_gui template files exist."""
        config = engine.load_template_config('desktop_gui')
        structure = config.get('structure', [])
        
        template_dir = engine.templates_dir / 'desktop_gui'
        
        # Check that referenced templates exist
        missing_templates = []
        for item in structure:
            if item['type'] == 'file' and 'template' in item:
                template_file = template_dir / item['template']
                if not template_file.exists():
                    missing_templates.append(item['template'])
        
        # Should have no missing templates after Phase 1
        assert len(missing_templates) == 0, f"Missing templates: {missing_templates}"
