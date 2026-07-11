"""
Tests for QuestionnaireEngine.

Author: Chuck Finch - Fragillidae Software
"""

import pytest
from pathlib import Path

from project_architect.core.questionnaire import (
    QuestionnaireEngine, QuestionnaireMode, QuestionType
)


class TestQuestionnaireEngine:
    """Tests for QuestionnaireEngine class."""
    
    @pytest.fixture
    def engine(self):
        """Create questionnaire engine instance."""
        return QuestionnaireEngine()
    
    def test_initialization(self, engine):
        """Test engine initializes correctly."""
        assert engine is not None
        assert engine.templates_dir.exists()
    
    def test_load_questionnaire(self, engine):
        """Test loading questionnaire for a project type."""
        success = engine.load_questionnaire('desktop_gui', QuestionnaireMode.NEW_PROJECT)
        assert success is True
        assert len(engine.questions) > 0
    
    def test_get_sections(self, engine):
        """Test getting sections from questionnaire."""
        engine.load_questionnaire('desktop_gui', QuestionnaireMode.NEW_PROJECT)
        sections = engine.get_sections()
        
        assert isinstance(sections, list)
        assert len(sections) > 0
        assert 'project_basics' in sections
    
    def test_get_questions_by_section(self, engine):
        """Test getting questions for a section."""
        engine.load_questionnaire('desktop_gui', QuestionnaireMode.NEW_PROJECT)
        questions = engine.get_questions_by_section('project_basics')
        
        assert isinstance(questions, list)
        assert len(questions) > 0
    
    def test_set_and_get_response(self, engine):
        """Test setting and getting responses."""
        engine.load_questionnaire('desktop_gui', QuestionnaireMode.NEW_PROJECT)
        
        # Set response
        engine.set_response('project_name', 'Test Project')
        
        # Get response
        response = engine.get_response('project_name')
        assert response == 'Test Project'
    
    def test_validate_response_required_field(self, engine):
        """Test validation of required fields."""
        engine.load_questionnaire('desktop_gui', QuestionnaireMode.NEW_PROJECT)
        questions = engine.get_questions_by_section()

        # Find a required question
        required_question = None
        for q in questions:
            if q.required:
                required_question = q
                break
        
        if required_question:
            # Empty value should fail validation
            is_valid, error = engine.validate_response(required_question, '')
            assert is_valid is False
            assert 'required' in error.lower()
    
    def test_is_complete(self, engine):
        """Test questionnaire completion check."""
        engine.load_questionnaire('desktop_gui', QuestionnaireMode.NEW_PROJECT)
        
        # Without responses, should not be complete
        assert engine.is_complete() is False
        
        # Set all required responses
        questions = engine.get_questions_by_section()
        for q in questions:
            if q.required:
                if q.type == QuestionType.TEXT:
                    engine.set_response(q.id, 'test value')
                elif q.type == QuestionType.BOOLEAN:
                    engine.set_response(q.id, True)
                elif q.type == QuestionType.CHOICE:
                    engine.set_response(q.id, q.options[0] if q.options else 'option')
                elif q.default is not None:
                    # Covers VERSION and any other type with a usable default
                    engine.set_response(q.id, q.default)
        
        # Now should be complete
        assert engine.is_complete() is True
    
    def test_get_question_by_id(self, engine):
        """Test getting question by ID."""
        engine.load_questionnaire('desktop_gui', QuestionnaireMode.NEW_PROJECT)
        
        question = engine.get_question_by_id('project_name')
        assert question is not None
        assert question.id == 'project_name'
    
    def test_should_show_question_with_condition(self, engine):
        """Test conditional question showing."""
        engine.load_questionnaire('desktop_gui', QuestionnaireMode.NEW_PROJECT)
        
        # Find a question with conditions
        questions = engine.get_questions_by_section()
        conditional_q = None
        for q in questions:
            if q.depends_on:
                conditional_q = q
                break
        
        if conditional_q:
            # Should evaluate condition properly
            result = engine.should_show_question(conditional_q)
            assert isinstance(result, bool)


class TestQuestionValidation:
    """Tests for question validation logic."""
    
    @pytest.fixture
    def engine(self):
        """Create questionnaire engine instance."""
        engine = QuestionnaireEngine()
        engine.load_questionnaire('desktop_gui', QuestionnaireMode.NEW_PROJECT)
        return engine
    
    def test_email_validation(self, engine):
        """Test email format validation."""
        # Find email question
        email_q = engine.get_question_by_id('author_email')
        if email_q:
            # Valid email
            is_valid, _ = engine.validate_response(email_q, 'test@example.com')
            assert is_valid is True
            
            # Invalid email
            is_valid, error = engine.validate_response(email_q, 'invalid_email')
            assert is_valid is False
    
    def test_version_validation(self, engine):
        """Test version format validation."""
        # Find version question
        version_q = engine.get_question_by_id('project_version')
        if version_q:
            # Valid version
            is_valid, _ = engine.validate_response(version_q, '1.0.0')
            assert is_valid is True
            
            # Invalid version
            is_valid, error = engine.validate_response(version_q, 'invalid')
            assert is_valid is False
