# Development Rules

**BEFORE ANY CODING IS DONE THIS LIST MUST BE REVIEWED!**

## Pre-Development Review
- Review the following files immediately:
  - CHANGELOG.md
  - IMPLEMENTATION_PLAN.md
  - TECHNICAL_SPECIFICATION.md
  - README.md

## Project Standards

### Cross-Platform Compatibility
- Project is intended to be cross-platform (Windows, Mac, Linux)
- Test on multiple platforms when possible
- Use cross-platform libraries and approaches
- Avoid platform-specific code unless absolutely necessary

### Modular Design
- Project will be modular for better organization and maintenance
- Each module should have a single, well-defined responsibility
- Keep dependencies between modules minimal and well-documented
- Use clear interfaces between modules

### File Size Limits
- When possible, all files will be 300 lines of code or less with a 500 line hard limit
- If, when editing a file, it is anticipated that the number of lines will exceed 500, editing should pause and we should discuss how to break the file into multiple files
- Once we agree on a plan, then continue editing
- Prioritize readability and maintainability over arbitrary line limits

### Code Quality
- We MUST cleanup code as we go
- Don't just add code without regard to code it may be replacing that no longer needs to exist
- Any replaced code, if no longer valid, should be deleted
- After a debug session, once we agree the problem is fixed we MUST cleanup all debug code added during the session
- Remove unused imports, variables, and functions regularly
- Maintain consistent code formatting and style

## User Interface Standards

### Screen Resolution Requirements
- All GUI work must be done with a minimum screen size of 1366x768 in mind
- All windows and dialogs must fully fit within minimum resolution of 1366x768
- All windows must scale properly when maximized and/or returned to normal size
- All windows should have every element visible with little to no scrolling required at the minimum resolution
- All windows and dialogs must limit wasted space as much as possible

### Responsive Design
- Interfaces should adapt gracefully to different screen sizes
- Use appropriate layout managers and responsive design principles
- Test interface at different resolutions and scaling factors
- Ensure accessibility for users with different display configurations

## Development Workflow

### Session Management
After every coding session, and during if requested, we shall do the following:
- Review codebase for unused/dead code and remove it
- Make a development commit with clear commit message
- Update all relevant documentation
- Make a documentation commit
- Update CHANGELOG.md with changes made
- Review and update task progress in IMPLEMENTATION_PLAN.md

### Version Control
- Make frequent, small commits with descriptive messages
- Use conventional commit message format when possible
- Keep commits focused on single changes or features
- Update documentation in separate commits when possible
- Tag releases with semantic versioning

### Documentation
- Keep all documentation up to date with code changes
- Document any architectural decisions or design choices
- Include code comments for complex logic
- Update API documentation when interfaces change
- Maintain user-facing documentation for any UI changes

## Communication and Collaboration

### Asking for Help
- **If you do not know the answer to a question, or are not sure how to proceed, please ask for help**
- **Please DO NOT make guesses or assumptions that lead you to add code I am not aware you will be adding**
- **Please DO NOT remove code I have added without consulting me first**
- **PLEASE ASK BEFORE YOU START CODING**

### Decision Making
- Discuss architectural changes before implementing
- Get approval for major refactoring efforts
- Confirm understanding of requirements before coding
- Review design decisions with stakeholders when needed

### Code Review
- All significant changes should be reviewed
- Focus on correctness, maintainability, and adherence to standards
- Check for potential security issues or performance problems
- Ensure changes align with project goals and architecture

## Testing and Quality Assurance

### Testing Requirements
- Write unit tests for new functionality
- Update existing tests when modifying code
- Run all tests before committing changes
- Maintain high test coverage for critical functionality

### Quality Checks
- Use linting tools to maintain code quality
- Run static analysis tools when available
- Check for security vulnerabilities in dependencies
- Validate that changes don't break existing functionality

### Performance Considerations
- Profile performance-critical code
- Optimize for the common use case
- Consider memory usage and resource consumption
- Test with realistic data sizes and scenarios

## Error Handling and Logging

### Error Handling
- Implement proper error handling for all user-facing operations
- Provide meaningful error messages to users
- Log errors appropriately for debugging
- Gracefully handle edge cases and unexpected inputs

### Logging
- Use appropriate logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Include relevant context in log messages
- Avoid logging sensitive information
- Configure logging appropriately for different environments

## Security Considerations

### Data Protection
- Protect sensitive user data
- Use secure methods for storing credentials
- Validate all user inputs
- Follow security best practices for the technology stack

### Dependencies
- Keep dependencies up to date
- Review security advisories for used libraries
- Use dependency scanning tools when available
- Minimize the number of external dependencies

## Final Reminders

- **Quality over speed** - Take time to do things right
- **Communication is key** - Ask questions and clarify requirements
- **Document decisions** - Future you (and others) will thank you
- **Test thoroughly** - Bugs found early are easier to fix
- **Stay organized** - Keep the codebase clean and well-structured

**PLEASE CREATE A MEMORY OF THESE RULES.**
