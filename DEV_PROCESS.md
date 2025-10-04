# Development Process

This document outlines the development workflow and best practices for software projects. Following this process ensures consistency, maintainability, and quality across all development sessions.

---

## Table of Contents

1. [Pre-Session Preparation](#pre-session-preparation)
2. [Session Startup](#session-startup)
3. [Development Workflow](#development-workflow)
4. [Testing Process](#testing-process)
5. [Session Wrap-Up](#session-wrap-up)
6. [Post-Session Documentation](#post-session-documentation)
7. [Quality Checklist](#quality-checklist)

---

## Pre-Session Preparation

### Before Starting Development

1. **Review Previous Session**
   - Read the last session's organized documentation (`dev_sessions/sessionN_organized.md`)
   - Review "Next Session Planning" section
   - Check for any deferred items or follow-ups

2. **Check Project Status**
   - Review current version number in main module
   - Check IMPLEMENTATION_PLAN.md for current phase/task
   - Review CHANGELOG.md for recent changes
   - Run `git status` to ensure clean working directory

3. **Set Session Goals**
   - Define 1-3 specific goals for this session
   - Identify which tasks from IMPLEMENTATION_PLAN.md to tackle
   - Note any dependencies or blockers
   - Write goals down for later documentation

4. **Environment Check**
   ```bash
   # Activate virtual environment
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   
   # Verify dependencies
   pip list
   
   # Test application startup
   python main.py
   ```

---

## Session Startup

### Starting a New Development Session

1. **Create Session Transcript File**
   ```bash
   # Create new session file with date
   touch dev_sessions/sessionN_MM-DD-YY.md
   ```

2. **Review Development Rules**
   - Quickly scan DEV_RULES.md
   - Remember: 300-line target, 500-line hard limit
   - Ask before coding, don't remove code without consultation

3. **Pull Latest Changes** (if using version control)
   ```bash
   git pull origin main
   ```

4. **Start AI Assistant Session**
   - Share DEV_RULES.md with AI
   - Share current task from IMPLEMENTATION_PLAN.md
   - Share relevant specification sections
   - Establish session goals

---

## Development Workflow

### Step-by-Step Development Process

#### 1. Information Gathering (Before Coding)

**Always gather information first!**

- Use codebase exploration tools to understand existing code
- Search for references and patterns in the codebase
- Read relevant files and documentation
- Check database schema if working with data
- Review similar implementations in the codebase
- Look at version control history for similar features

**Rule:** Never start coding without understanding the context!

#### 2. Planning

- Break down the task into smaller, manageable pieces
- Identify files that need to be created or modified
- Plan the order of implementation
- Consider dependencies and integration points
- Estimate complexity and potential issues

#### 3. Implementation

**File Size Management:**
- Monitor file sizes during development
- If approaching 300 lines, consider refactoring
- If approaching 500 lines, STOP and discuss splitting the file
- Keep functions and classes focused and single-purpose

**Code Quality:**
- Write clean, readable code
- Add appropriate comments and docstrings
- Follow consistent naming conventions
- Remove dead code as you go
- Clean up debug code after fixing issues

#### 4. Integration Testing

- Test new functionality as you implement it
- Verify integration with existing code
- Check for regressions in existing functionality
- Test edge cases and error conditions

---

## Testing Process

### Testing Guidelines

1. **Unit Testing**
   - Write tests for new functions and classes
   - Update existing tests when modifying code
   - Aim for good test coverage of critical functionality

2. **Integration Testing**
   - Test how new code works with existing systems
   - Verify database operations if applicable
   - Test user interface interactions

3. **Manual Testing**
   - Test the application end-to-end
   - Verify user workflows work correctly
   - Check for UI/UX issues
   - Test on different screen resolutions (minimum 1366x768)

4. **Running Tests**
   ```bash
   # Run unit tests
   python -m pytest tests/
   
   # Run with coverage
   python -m pytest --cov=project_name tests/
   
   # Run specific test file
   python -m pytest tests/test_specific.py
   ```

---

## Session Wrap-Up

### End of Session Checklist

1. **Code Review**
   - Review all changes made during the session
   - Remove any debug code or temporary changes
   - Ensure code follows project standards
   - Check for unused imports or variables

2. **Testing**
   - Run all tests to ensure nothing is broken
   - Perform manual testing of new functionality
   - Verify the application starts and runs correctly

3. **Documentation Updates**
   - Update relevant documentation files
   - Add or update code comments
   - Update API documentation if interfaces changed

4. **Version Control**
   ```bash
   # Stage changes
   git add .
   
   # Commit with descriptive message
   git commit -m "feat: implement [feature description]"
   
   # Push changes (if using remote repository)
   git push origin main
   ```

---

## Post-Session Documentation

### Documentation Requirements

1. **Update CHANGELOG.md**
   - Add entry for current version
   - List all changes made in the session
   - Note any breaking changes or important updates

2. **Update Session Log**
   - Document what was accomplished
   - Note any issues encountered and how they were resolved
   - List any deferred items or follow-ups needed
   - Plan priorities for next session

3. **Update Implementation Plan**
   - Mark completed tasks as done
   - Update task status and progress
   - Add any new tasks discovered during development
   - Adjust timeline estimates if needed

---

## Quality Checklist

### Before Completing Any Task

- [ ] Code follows project style guidelines
- [ ] All files are under 500 lines (preferably under 300)
- [ ] No dead or commented-out code remains
- [ ] All functions have appropriate docstrings
- [ ] Error handling is implemented where needed
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Changes are committed with clear messages
- [ ] Application runs without errors
- [ ] UI elements fit within 1366x768 resolution
- [ ] No security vulnerabilities introduced
- [ ] Performance is acceptable for intended use

### Code Quality Standards

- **Readability:** Code should be self-documenting
- **Maintainability:** Easy to modify and extend
- **Testability:** Functions should be easy to test
- **Performance:** Efficient for the intended use case
- **Security:** No obvious security vulnerabilities
- **Compatibility:** Works across target platforms

---

## Best Practices and Common Pitfalls

### Best Practices

1. **Start Small:** Implement the simplest version first
2. **Test Early:** Don't wait until the end to test
3. **Document Decisions:** Record why you made certain choices
4. **Ask Questions:** When in doubt, ask for clarification
5. **Stay Organized:** Keep files and code well-structured

### Common Pitfalls to Avoid

1. **Coding Without Understanding:** Always gather context first
2. **Ignoring File Size Limits:** Monitor line counts regularly
3. **Skipping Tests:** Tests save time in the long run
4. **Poor Commit Messages:** Write clear, descriptive commits
5. **Forgetting Documentation:** Update docs as you code

### Tools and Commands Reference

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependencies
pip install -r requirements.txt
pip freeze > requirements.txt

# Testing
python -m pytest
python -m pytest --cov=project_name

# Code quality
black .                   # Code formatting
flake8 .                 # Linting
pylint project_name      # Static analysis

# Git workflow
git status
git add .
git commit -m "message"
git push origin main
```

---

## Continuous Improvement

### Session Retrospectives

After each major milestone:
- Review what worked well
- Identify areas for improvement
- Update this process document if needed
- Share learnings with the team

### Process Updates

This document should be updated when:
- New tools are adopted
- Better practices are discovered
- Common issues are identified
- Team feedback suggests improvements

---

**Remember:** This process is designed to help maintain quality and consistency. Follow it as a guide, but adapt as needed for specific situations. When in doubt, prioritize quality over speed and communication over assumptions.
