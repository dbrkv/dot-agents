#!/usr/bin/env python3
"""
Architecture Decision Record Generator

This script generates ADR markdown files using the EdgeX Foundry template structure.
It can create new ADRs from scratch or populate templates with provided information.
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path


class ADRGenerator:
    """Generates Architecture Decision Records using the EdgeX template."""

    def __init__(self, output_dir="docs/adr"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_template(self, title: str, submitters: list = None) -> str:
        """Generate an ADR template with the given title and submitters."""

        if not submitters:
            submitters = ["[Your Name] ([Your Organization])"]

        # Generate filename from title
        filename = self.title_to_filename(title)

        # Current date for initial status
        current_date = datetime.now().strftime("%Y-%m-%d")

        template = f"""# {title}

### Submitters
{chr(10).join(f"*   {submitter}" for submitter in submitters)}

### Change Log
*   [pending](TODO) {current_date}

### Referenced Use Case(s)
*   [Use Case Name](URL)

### Context
TODO: Describe the architectural significance and high-level design approach.
- What problem needs to be solved?
- Why is this decision architecturally significant?
- What is the high-level design approach?

### Proposed Design
TODO: Detail the proposed design without implementation specifics.

**Services/modules to be impacted:**
- Service1: What changes are needed
- Service2: What components are affected

**New services/modules to be added:**
- NewService: Description of new component

**Model and DTO impact:**
- DataModel1: Changes to data structures
- DTO1: API data transfer object modifications

**API impact:**
- API changes: New/modified/deprecated endpoints
- Integration points: How different components interact

**Configuration impact:**
- Configuration sections: New config requirements
- Environment variables: Runtime configuration needs

**DevOps impact:**
- Deployment: Changes to deployment processes
- Monitoring: New monitoring and alerting requirements

### Considerations
TODO: Document alternatives, concerns, and how they were resolved.

**Alternatives considered:**
- Alternative1: Description and why it was rejected
- Alternative2: Description and trade-offs

**Concerns addressed:**
- Concern1: How the issue was resolved
- Concern2: Mitigation strategies implemented

**Issues resolved:**
- Issue1: Resolution approach
- Issue2: How conflicts were managed

### Decision
TODO: Document the final decision and any remaining work.

**Implementation details:**
- Key implementation decisions and caveats
- Future considerations and deferred work

**Requirements not satisfied:**
- Any requirements that cannot be met with this approach
- Limitations and constraints

### Other Related ADRs
*   [Related ADR Title](URL) - Relevance description

### References
*   [Title](URL) - Additional documentation
"""

        return filename, template

    def title_to_filename(self, title: str) -> str:
        """Convert ADR title to filename format."""
        # Convert to lowercase and replace spaces with dashes
        filename = title.lower().replace(' ', '-')
        # Remove special characters except dashes
        filename = ''.join(c for c in filename if c.isalnum() or c == '-')
        # Add .md extension
        return f"{filename}.md"

    def create_adr(self, title: str, submitters: list = None, interactive: bool = False) -> str:
        """Create a new ADR file."""

        filename, template = self.generate_template(title, submitters)
        filepath = self.output_dir / filename

        if interactive:
            print(f"Creating ADR: {title}")
            print(f"Filename: {filename}")
            print(f"Path: {filepath}")
            print()

            # Interactive section completion
            sections = [
                ("Context", "Describe the architectural significance and design approach"),
                ("Referenced Use Case(s)", "List relevant requirements or user stories"),
                ("Considerations", "Document alternatives and concerns"),
                ("Decision", "Document the final decision and remaining work")
            ]

            for section_name, prompt in sections:
                print(f"\n{section_name}:")
                print(f"Prompt: {prompt}")
                print("Enter your text (type 'END' on a new line when finished):")

                lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    lines.append(line)

                if lines:
                    section_text = '\n'.join(lines)
                    # Replace the TODO section with user input
                    template = template.replace(f"TODO: {prompt}", section_text)

        # Write the ADR file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)

        print(f"✅ ADR created: {filepath}")
        return str(filepath)

    def list_adrs(self) -> list:
        """List existing ADR files in the output directory."""
        if not self.output_dir.exists():
            return []

        adrs = []
        for filepath in self.output_dir.glob("*.md"):
            # Extract title from filename
            filename = filepath.stem
            title = filename.replace('-', ' ').title()

            # Get file modification time
            mtime = datetime.fromtimestamp(filepath.stat().st_mtime)

            adrs.append({
                'filename': filepath.name,
                'title': title,
                'path': str(filepath),
                'modified': mtime
            })

        return sorted(adrs, key=lambda x: x['modified'], reverse=True)

    def validate_adr(self, filepath: str) -> list:
        """Validate an ADR file against the EdgeX template requirements."""
        errors = []

        if not os.path.exists(filepath):
            errors.append(f"File does not exist: {filepath}")
            return errors

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Required sections
        required_sections = [
            "### Submitters",
            "### Change Log",
            "### Referenced Use Case(s)",
            "### Context",
            "### Proposed Design",
            "### Considerations",
            "### Decision",
            "### Other Related ADRs",
            "### References"
        ]

        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")

        # Check for TODO items
        if "TODO:" in content:
            errors.append("Contains unfinished TODO items")

        return errors


def main():
    parser = argparse.ArgumentParser(description="Generate Architecture Decision Records")
    parser.add_argument("command", choices=["create", "list", "validate"],
                       help="Command to execute")
    parser.add_argument("--title", help="ADR title (for create command)")
    parser.add_argument("--submitters", nargs="+",
                       help="List of submitters in format 'Name (Organization)'")
    parser.add_argument("--output", default="docs/adr",
                       help="Output directory for ADR files")
    parser.add_argument("--file", help="File to validate (for validate command)")
    parser.add_argument("--interactive", action="store_true",
                       help="Interactive mode for filling sections")

    args = parser.parse_args()

    generator = ADRGenerator(args.output)

    if args.command == "create":
        if not args.title:
            print("Error: --title is required for create command")
            sys.exit(1)

        filepath = generator.create_adr(
            title=args.title,
            submitters=args.submitters,
            interactive=args.interactive
        )

        print(f"\nNext steps:")
        print(f"1. Edit the ADR: {filepath}")
        print(f"2. Fill in all sections and remove TODO items")
        print(f"3. Review with stakeholders")
        print(f"4. Update change log when approved")

    elif args.command == "list":
        adrs = generator.list_adrs()
        if not adrs:
            print(f"No ADRs found in {args.output}")
        else:
            print(f"Architecture Decision Records in {args.output}:")
            print()
            for adr in adrs:
                print(f"📄 {adr['title']}")
                print(f"   File: {adr['filename']}")
                print(f"   Modified: {adr['modified'].strftime('%Y-%m-%d %H:%M')}")
                print(f"   Path: {adr['path']}")
                print()

    elif args.command == "validate":
        if not args.file:
            # Validate all ADRs
            adrs = generator.list_adrs()
            all_valid = True

            for adr in adrs:
                errors = generator.validate_adr(adr['path'])
                if errors:
                    print(f"❌ {adr['filename']}")
                    for error in errors:
                        print(f"   - {error}")
                    all_valid = False
                else:
                    print(f"✅ {adr['filename']}")

            if all_valid:
                print("\nAll ADRs are valid!")
            else:
                print("\nSome ADRs have validation errors.")
        else:
            errors = generator.validate_adr(args.file)
            if errors:
                print(f"❌ Validation errors in {args.file}:")
                for error in errors:
                    print(f"   - {error}")
            else:
                print(f"✅ {args.file} is valid!")


if __name__ == "__main__":
    main()