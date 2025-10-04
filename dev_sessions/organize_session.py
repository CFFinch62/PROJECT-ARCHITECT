#!/usr/bin/env python3
"""
Session Organizer Script
Converts raw conversation transcripts into structured session documentation.

Usage:
    python organize_session.py <input_file> [output_file]
    
Example:
    python organize_session.py session2.md session2_organized.md
"""

import sys
import re
from datetime import datetime
from pathlib import Path


class SessionOrganizer:
    """Organizes raw session transcripts into structured documentation."""
    
    def __init__(self, input_file):
        self.input_file = Path(input_file)
        self.raw_content = self.input_file.read_text()
        self.session_data = {
            'date': None,
            'versions': {'start': None, 'end': None},
            'goals': [],
            'files_created': [],
            'files_modified': [],
            'decisions': [],
            'issues': [],
            'deferred': [],
            'tests': [],
            'commits': [],
            'notes': []
        }
    
    def extract_versions(self):
        """Extract version numbers from the transcript."""
        version_pattern = r'v?(\d+\.\d+\.\d+)'
        versions = re.findall(version_pattern, self.raw_content)
        if versions:
            self.session_data['versions']['start'] = versions[0]
            self.session_data['versions']['end'] = versions[-1]
    
    def extract_git_commits(self):
        """Extract git commit messages."""
        # Look for commit patterns
        commit_patterns = [
            r'git commit -m "([^"]+)"',
            r'feat:|fix:|test:|docs:|refactor:',
        ]
        
        # Simple extraction - look for lines that look like commits
        lines = self.raw_content.split('\n')
        for i, line in enumerate(lines):
            if 'git commit' in line.lower() or any(p in line for p in ['feat:', 'fix:', 'test:', 'docs:']):
                # Try to extract the commit message
                if '"' in line:
                    match = re.search(r'"([^"]+)"', line)
                    if match:
                        self.session_data['commits'].append(match.group(1))
    
    def extract_files(self):
        """Extract created and modified files."""
        # Look for file creation patterns
        file_patterns = [
            r'Created?:?\s*\n?\s*-?\s*([a-zA-Z0-9_/\.]+\.py)',
            r'create mode \d+ ([a-zA-Z0-9_/\.]+)',
            r'new file:\s+([a-zA-Z0-9_/\.]+)',
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, self.raw_content)
            self.session_data['files_created'].extend(matches)
        
        # Look for modified files
        modified_patterns = [
            r'Modified?:?\s*\n?\s*-?\s*([a-zA-Z0-9_/\.]+\.py)',
            r'modified:\s+([a-zA-Z0-9_/\.]+)',
        ]
        
        for pattern in modified_patterns:
            matches = re.findall(pattern, self.raw_content)
            self.session_data['files_modified'].extend(matches)
        
        # Remove duplicates
        self.session_data['files_created'] = list(set(self.session_data['files_created']))
        self.session_data['files_modified'] = list(set(self.session_data['files_modified']))
    
    def extract_test_info(self):
        """Extract test information."""
        # Look for test patterns
        test_patterns = [
            r'✅ Test \d+:([^\n]+)',
            r'test_([a-zA-Z0-9_]+)\.py',
            r'(\d+) test cases?',
        ]
        
        for pattern in test_patterns:
            matches = re.findall(pattern, self.raw_content)
            self.session_data['tests'].extend(matches)
    
    def extract_issues(self):
        """Extract issues and solutions."""
        # Look for issue/problem patterns
        issue_keywords = ['Issue', 'Problem', 'Bug', 'Error', 'Failed']
        solution_keywords = ['Solution', 'Fixed', 'Resolved', 'Solved']
        
        lines = self.raw_content.split('\n')
        current_issue = None
        
        for line in lines:
            # Check for issue
            if any(keyword in line for keyword in issue_keywords):
                if ':' in line:
                    current_issue = line.split(':', 1)[1].strip()
                    self.session_data['issues'].append({'problem': current_issue, 'solution': None})
            
            # Check for solution
            elif current_issue and any(keyword in line for keyword in solution_keywords):
                if ':' in line and self.session_data['issues']:
                    self.session_data['issues'][-1]['solution'] = line.split(':', 1)[1].strip()
                    current_issue = None
    
    def generate_organized_doc(self):
        """Generate the organized markdown document."""
        doc = []
        
        # Header
        doc.append(f"# Development Session - Organized")
        doc.append(f"\n**Date:** {datetime.now().strftime('%B %d, %Y')}")
        doc.append(f"**Starting Version:** {self.session_data['versions']['start'] or 'Unknown'}")
        doc.append(f"**Ending Version:** {self.session_data['versions']['end'] or 'Unknown'}")
        doc.append(f"\n---\n")
        
        # Session Goals
        doc.append("## Session Goals\n")
        if self.session_data['goals']:
            for goal in self.session_data['goals']:
                doc.append(f"- {goal}")
        else:
            doc.append("*[Add session goals here]*\n")
        doc.append("\n---\n")
        
        # What Was Built
        doc.append("## What Was Built\n")
        
        if self.session_data['files_created']:
            doc.append("### Files Created\n")
            for file in sorted(self.session_data['files_created']):
                doc.append(f"- `{file}`")
            doc.append("")
        
        if self.session_data['files_modified']:
            doc.append("### Files Modified\n")
            for file in sorted(self.session_data['files_modified']):
                doc.append(f"- `{file}`")
            doc.append("")
        
        doc.append("\n---\n")
        
        # Key Decisions
        doc.append("## Key Technical Decisions\n")
        if self.session_data['decisions']:
            for i, decision in enumerate(self.session_data['decisions'], 1):
                doc.append(f"### {i}. {decision['title']}")
                doc.append(f"**Decision:** {decision['decision']}")
                doc.append(f"**Reasoning:** {decision['reasoning']}\n")
        else:
            doc.append("*[Document key technical decisions made during this session]*\n")
        doc.append("\n---\n")
        
        # Issues Encountered
        doc.append("## Issues Encountered & Solutions\n")
        if self.session_data['issues']:
            for i, issue in enumerate(self.session_data['issues'], 1):
                doc.append(f"### Issue {i}")
                doc.append(f"**Problem:** {issue['problem']}")
                if issue['solution']:
                    doc.append(f"**Solution:** {issue['solution']}")
                doc.append("")
        else:
            doc.append("*[No major issues encountered]*\n")
        doc.append("\n---\n")
        
        # Deferred Items
        doc.append("## Deferred to Future Phases\n")
        if self.session_data['deferred']:
            for item in self.session_data['deferred']:
                doc.append(f"- {item}")
        else:
            doc.append("*[No items deferred]*\n")
        doc.append("\n---\n")
        
        # Test Results
        doc.append("## Test Results\n")
        if self.session_data['tests']:
            doc.append("### Tests Run\n")
            for test in self.session_data['tests']:
                doc.append(f"- {test}")
        else:
            doc.append("*[No tests run this session]*\n")
        doc.append("\n---\n")
        
        # Git Commits
        doc.append("## Git Commit History\n")
        if self.session_data['commits']:
            doc.append("```")
            for commit in self.session_data['commits']:
                doc.append(commit)
            doc.append("```")
        else:
            doc.append("*[No commits made this session]*\n")
        doc.append("\n---\n")
        
        # Next Session
        doc.append("## Next Session Planning\n")
        doc.append("*[Add plans for next session here]*\n")
        doc.append("\n---\n")
        
        # Session Notes
        doc.append("## Session Notes & Observations\n")
        doc.append("*[Add any additional notes or observations here]*\n")
        
        return '\n'.join(doc)
    
    def organize(self, output_file=None):
        """Main method to organize the session."""
        print(f"📖 Reading session file: {self.input_file}")
        
        # Extract information
        print("🔍 Extracting versions...")
        self.extract_versions()
        
        print("🔍 Extracting git commits...")
        self.extract_git_commits()
        
        print("🔍 Extracting files...")
        self.extract_files()
        
        print("🔍 Extracting test information...")
        self.extract_test_info()
        
        print("🔍 Extracting issues...")
        self.extract_issues()
        
        # Generate organized document
        print("📝 Generating organized document...")
        organized_content = self.generate_organized_doc()
        
        # Determine output file
        if output_file is None:
            output_file = self.input_file.stem + '_organized.md'
        
        output_path = Path(output_file)
        
        # Write output
        print(f"💾 Writing to: {output_path}")
        output_path.write_text(organized_content)
        
        print(f"\n✅ Session organized successfully!")
        print(f"📄 Output: {output_path}")
        print(f"\n📊 Summary:")
        print(f"   - Versions: {self.session_data['versions']['start']} → {self.session_data['versions']['end']}")
        print(f"   - Files created: {len(self.session_data['files_created'])}")
        print(f"   - Files modified: {len(self.session_data['files_modified'])}")
        print(f"   - Commits: {len(self.session_data['commits'])}")
        print(f"   - Issues: {len(self.session_data['issues'])}")
        print(f"\n💡 Tip: Review and enhance the generated document with additional context!")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python organize_session.py <input_file> [output_file]")
        print("\nExample:")
        print("  python organize_session.py session2.md")
        print("  python organize_session.py session2.md session2_organized.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(input_file).exists():
        print(f"❌ Error: Input file '{input_file}' not found!")
        sys.exit(1)
    
    organizer = SessionOrganizer(input_file)
    organizer.organize(output_file)


if __name__ == '__main__':
    main()

