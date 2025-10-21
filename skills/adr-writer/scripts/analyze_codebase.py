#!/usr/bin/env python3
"""
Codebase Analyzer for ADR Creation

This script helps analyze existing code to understand design decisions
and generate draft ADRs documenting the rationale behind implementations.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
import subprocess


class CodebaseAnalyzer:
    """Analyzes codebase to infer architectural decisions."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.git_available = self._check_git_available()

    def _check_git_available(self) -> bool:
        """Check if git is available and this is a git repository."""
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            subprocess.run(['git', 'rev-parse', '--git-dir'],
                         cwd=self.repo_path, capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def get_git_history(self, file_pattern: str = "*", limit: int = 50) -> List[Dict]:
        """Get git history for files matching the pattern."""
        if not self.git_available:
            return []

        cmd = [
            'git', 'log', '--oneline', '--grep="architecture\\|design\\|decision\\|refactor"',
            f'--{limit}', '--', file_pattern
        ]

        try:
            result = subprocess.run(cmd, cwd=self.repo_path,
                                  capture_output=True, text=True, check=True)
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        commits.append({
                            'hash': parts[0],
                            'message': parts[1]
                        })
            return commits
        except subprocess.CalledProcessError:
            return []

    def analyze_file_patterns(self) -> Dict[str, List[str]]:
        """Analyze file patterns to infer architectural decisions."""

        patterns = {
            'database': [
                '**/*.sql', '**/migrations/**', '**/schema.sql',
                '**/database/**', '**/db/**', '**/*model*.py'
            ],
            'api': [
                '**/api/**', '**/routes/**', '**/controllers/**',
                '**/*router*.py', '**/*endpoint*.py', '**/swagger/**'
            ],
            'config': [
                '**/config/**', '**/*.env*', '**/settings/**',
                '**/*config*.py', '**/properties/**'
            ],
            'infrastructure': [
                '**/docker*', '**/k8s/**', '**/helm/**',
                '**/terraform/**', '**/cloudformation/**'
            ],
            'authentication': [
                '**/auth/**', '**/security/**', '**/*auth*.py',
                '**/*login*.py', '**/*token*.py'
            ]
        }

        findings = {}

        for category, file_patterns in patterns.items():
            findings[category] = []
            for pattern in file_patterns:
                files = list(self.repo_path.glob(pattern))
                findings[category].extend([str(f.relative_to(self.repo_path))
                                         for f in files if f.is_file()])

        return findings

    def detect_technology_stack(self) -> Dict[str, List[str]]:
        """Detect the technology stack from files and dependencies."""

        stack = {
            'languages': [],
            'frameworks': [],
            'databases': [],
            'build_tools': [],
            'package_managers': []
        }

        # Language detection
        language_patterns = {
            'Python': ['**/*.py', 'requirements*.txt', 'setup.py', 'pyproject.toml'],
            'JavaScript': ['**/*.js', '**/*.ts', 'package*.json', 'tsconfig.json'],
            'Java': ['**/*.java', 'pom.xml', 'build.gradle'],
            'Go': ['**/*.go', 'go.mod', 'go.sum'],
            'Ruby': ['**/*.rb', 'Gemfile', 'gemspec'],
            'C#': ['**/*.cs', '*.csproj', '*.sln'],
            'PHP': ['**/*.php', 'composer.json']
        }

        for lang, patterns in language_patterns.items():
            for pattern in patterns:
                if list(self.repo_path.glob(pattern)):
                    if lang not in stack['languages']:
                        stack['languages'].append(lang)

        # Framework detection
        framework_indicators = {
            'Django': ['settings.py', '**/urls.py', '**/wsgi.py'],
            'Flask': ['app.py', 'wsgi.py', '**/__init__.py'],
            'Spring': ['**/application.properties', '**/spring-*.xml'],
            'Express': ['**/express*.js', '**/app.js'],
            'React': ['**/package.json', '**/jsx', '**/tsx'],
            'Angular': ['**/angular.json', '**/app.module.ts'],
            'Vue': ['**/vue.config.js', '**/main.js']
        }

        for framework, patterns in framework_indicators.items():
            for pattern in patterns:
                if list(self.repo_path.glob(pattern)):
                    if framework not in stack['frameworks']:
                        stack['frameworks'].append(framework)

        # Database detection
        db_indicators = {
            'PostgreSQL': ['postgresql', 'postgres', 'psycopg2'],
            'MySQL': ['mysql', 'mysqldb', 'pymysql'],
            'MongoDB': ['mongodb', 'pymongo', 'mongoose'],
            'Redis': ['redis', 'predis'],
            'SQLite': ['sqlite3', 'sqlite']
        }

        # Search in requirements files and code
        for db, indicators in db_indicators.items():
            for indicator in indicators:
                # Check requirements files
                for req_file in list(self.repo_path.glob('**/requirements*.txt')):
                    if req_file.exists():
                        with open(req_file, 'r') as f:
                            if indicator in f.read().lower():
                                if db not in stack['databases']:
                                    stack['databases'].append(db)

                # Check package.json
                for package_file in list(self.repo_path.glob('**/package.json')):
                    if package_file.exists():
                        with open(package_file, 'r') as f:
                            if indicator in f.read().lower():
                                if db not in stack['databases']:
                                    stack['databases'].append(db)

        return stack

    def extract_design_patterns(self) -> List[Dict[str, str]]:
        """Extract design patterns from code structure."""

        patterns = []

        # Look for common design patterns in file structure
        pattern_indicators = {
            'MVC': ['**/models/**', '**/views/**', '**/controllers/**'],
            'Repository': ['**/repositories/**', '**/*repository*.py'],
            'Factory': ['**/*factory*.py', '**/factories/**'],
            'Observer': ['**/*observer*.py', '**/*event*.py', '**/*listener*.py'],
            'Singleton': ['**/*singleton*.py'],
            'Strategy': ['**/*strategy*.py', '**/strategies/**'],
            'Adapter': ['**/*adapter*.py', '**/adapters/**'],
            'Proxy': ['**/*proxy*.py', '**/proxies/**']
        }

        for pattern, file_patterns in pattern_indicators.items():
            for pattern_file in file_patterns:
                files = list(self.repo_path.glob(pattern_file))
                if files:
                    patterns.append({
                        'pattern': pattern,
                        'files': [str(f.relative_to(self.repo_path)) for f in files],
                        'description': self._get_pattern_description(pattern)
                    })

        return patterns

    def _get_pattern_description(self, pattern: str) -> str:
        """Get description for design pattern."""
        descriptions = {
            'MVC': 'Model-View-Controller pattern separating data, presentation, and logic',
            'Repository': 'Repository pattern abstracting data access logic',
            'Factory': 'Factory pattern for object creation with loose coupling',
            'Observer': 'Observer pattern for event-driven communication',
            'Singleton': 'Singleton pattern ensuring single instance of a class',
            'Strategy': 'Strategy pattern for algorithm selection and interchangeability',
            'Adapter': 'Adapter pattern for interface compatibility',
            'Proxy': 'Proxy pattern for controlled access to objects'
        }
        return descriptions.get(pattern, 'Design pattern implementation found')

    def generate_adr_draft(self, topic: str) -> str:
        """Generate a draft ADR based on codebase analysis."""

        # Analyze the codebase
        file_patterns = self.analyze_file_patterns()
        tech_stack = self.detect_technology_stack()
        design_patterns = self.extract_design_patterns()
        git_history = self.get_git_history()

        # Generate the draft
        draft = f"""# {topic}

### Submitters
*   [Your Name] ([Your Organization])

### Change Log
*   [pending](TODO) {self._get_current_date()}

### Referenced Use Case(s)
*   [Use Case Name](URL)

### Context
This ADR documents the architectural decision regarding {topic}.
The analysis of the existing codebase reveals the following context:

**Technology Stack Detected:**
- Languages: {', '.join(tech_stack['languages']) if tech_stack['languages'] else 'None detected'}
- Frameworks: {', '.join(tech_stack['frameworks']) if tech_stack['frameworks'] else 'None detected'}
- Databases: {', '.join(tech_stack['databases']) if tech_stack['databases'] else 'None detected'}

**Key File Patterns:**
{self._format_file_patterns(file_patterns)}

**Design Patterns Identified:**
{self._format_design_patterns(design_patterns)}

This decision is architecturally significant because it affects the overall system structure and maintainability.

### Proposed Design
Based on the current implementation, the following design approach has been adopted:

TODO: Detail the specific design decisions made
- How the current implementation addresses the requirements
- Key architectural patterns and principles followed
- Integration points with other system components

### Considerations
**Alternatives considered:**
TODO: Document what other approaches were evaluated
- Alternative1: Description and why it was not chosen
- Alternative2: Description of trade-offs

**Current Implementation Analysis:**
- Strengths identified in the existing code
- Potential areas for improvement
- Technical debt or constraints observed

### Decision
TODO: Document the final decision and rationale

**Implementation Details:**
- Key architectural choices made
- How this decision aligns with system goals
- Performance and scalability considerations

**Future Considerations:**
- Potential evolution of this approach
- When this decision might need reconsideration
- Related architectural decisions that may be needed

### Other Related ADRs
*   [Related ADR Title](URL) - Relevance description

### References
*   [Technology Documentation](URL)
*   [Design Pattern References](URL)
"""

        return draft

    def _get_current_date(self) -> str:
        """Get current date in YYYY-MM-DD format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def _format_file_patterns(self, patterns: Dict[str, List[str]]) -> str:
        """Format file patterns for the ADR draft."""
        formatted = []
        for category, files in patterns.items():
            if files:
                formatted.append(f"- {category.title()}: {', '.join(files[:3])}")
                if len(files) > 3:
                    formatted.append(f"  ... and {len(files) - 3} more files")
        return '\n'.join(formatted) if formatted else "- No significant patterns detected"

    def _format_design_patterns(self, patterns: List[Dict]) -> str:
        """Format design patterns for the ADR draft."""
        if not patterns:
            return "- No specific design patterns identified"

        formatted = []
        for pattern in patterns:
            formatted.append(f"- {pattern['pattern']}: {pattern['description']}")
        return '\n'.join(formatted)

    def analyze_commit_message(self, commit_hash: str) -> Dict[str, Any]:
        """Analyze a specific commit for architectural insights."""
        if not self.git_available:
            return {}

        try:
            # Get commit details
            result = subprocess.run(
                ['git', 'show', '--format=%B%n%an%n%ad', '--name-only', commit_hash],
                cwd=self.repo_path, capture_output=True, text=True, check=True
            )

            output = result.stdout.split('\n')
            message = output[0]
            author = output[1] if len(output) > 1 else "Unknown"
            date = output[2] if len(output) > 2 else "Unknown"

            files_changed = [line for line in output[3:] if line.strip()]

            return {
                'hash': commit_hash,
                'message': message,
                'author': author,
                'date': date,
                'files_changed': files_changed,
                'is_architectural': any(keyword in message.lower()
                                       for keyword in ['architecture', 'design', 'refactor', 'decision'])
            }
        except subprocess.CalledProcessError:
            return {}


def main():
    parser = argparse.ArgumentParser(description="Analyze codebase for ADR creation")
    parser.add_argument("--path", default=".", help="Path to codebase directory")
    parser.add_argument("--topic", help="Topic for ADR generation")
    parser.add_argument("--output", help="Output file for generated ADR")
    parser.add_argument("--analyze", choices=['stack', 'patterns', 'history', 'all'],
                       default='all', help="What to analyze")
    parser.add_argument("--commit", help="Analyze specific commit")

    args = parser.parse_args()

    analyzer = CodebaseAnalyzer(args.path)

    if args.commit:
        commit_info = analyzer.analyze_commit_message(args.commit)
        if commit_info:
            print(f"Commit Analysis:")
            print(f"Hash: {commit_info['hash']}")
            print(f"Message: {commit_info['message']}")
            print(f"Author: {commit_info['author']}")
            print(f"Date: {commit_info['date']}")
            print(f"Files changed: {', '.join(commit_info['files_changed'])}")
            print(f"Architectural: {commit_info['is_architectural']}")
        else:
            print("Commit not found or git not available")
        return

    if args.analyze in ['stack', 'all']:
        print("Technology Stack Analysis:")
        stack = analyzer.detect_technology_stack()
        for category, items in stack.items():
            if items:
                print(f"  {category.replace('_', ' ').title()}: {', '.join(items)}")
        print()

    if args.analyze in ['patterns', 'all']:
        print("Design Patterns Analysis:")
        patterns = analyzer.extract_design_patterns()
        for pattern in patterns:
            print(f"  {pattern['pattern']}: {len(pattern['files'])} files")
            for file in pattern['files'][:3]:
                print(f"    - {file}")
            if len(pattern['files']) > 3:
                print(f"    ... and {len(pattern['files']) - 3} more files")
        print()

    if args.analyze in ['history', 'all']:
        print("Architectural Commit History:")
        history = analyzer.get_git_history()
        for commit in history[:10]:
            print(f"  {commit['hash']}: {commit['message']}")
        print()

    if args.topic:
        draft = analyzer.generate_adr_draft(args.topic)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(draft)
            print(f"ADR draft written to: {args.output}")
        else:
            print("Generated ADR Draft:")
            print("=" * 50)
            print(draft)


if __name__ == "__main__":
    main()