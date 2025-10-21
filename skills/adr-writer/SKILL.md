---
name: adr-writer
description: This skill should be used when creating Architecture Decision Records (ADRs) for software development projects. Use it for documenting technical decisions related to software architecture, infrastructure choices, technology stack selection, and cost-driven technical decisions. The skill helps create ADRs from scratch, generate decisions for new technical choices, and document rationale for existing implementations.
---

# Architecture Decision Record Writer

## Overview

This skill enables the creation of comprehensive Architecture Decision Records (ADRs) using the EdgeX Foundry template. It supports the complete ADR lifecycle: identifying when ADRs are needed, researching alternatives, documenting decisions, and managing updates for software development projects.

## Workflow Decision Tree

### Identify if an ADR is Needed
Ask these questions to determine if an ADR should be created:

1. **Is this decision architecturally significant?**
   - Affects system structure or behavior
   - Impacts multiple components or teams
   - Difficult to reverse once implemented
   - Sets precedent for future decisions

2. **Does this decision have long-term consequences?**
   - Affects maintainability, scalability, or performance
   - Creates technical debt or constraints
   - Requires significant investment to change later

3. **Are there multiple viable alternatives?**
   - More than one technical approach exists
   - Trade-offs need to be evaluated
   - Stakeholders need to understand the rationale

If any answer is "yes", create an ADR. If all are "no", proceed without an ADR.

## ADR Creation Workflow

### Step 1: Decision Analysis
Before writing the ADR, gather the necessary information:

1. **Identify the Context:**
   - What problem needs solving?
   - Why is this decision needed now?
   - What are the constraints and requirements?
   - Who are the stakeholders?

2. **Research Alternatives:**
   - List all viable options
   - Evaluate pros and cons of each
   - Consider technical, business, and operational factors
   - Document cost implications where relevant

3. **Consult Stakeholders:**
   - Gather input from development teams
   - Get feedback from architecture committees
   - Consider future maintainer perspectives

### Step 2: ADR Document Creation
Use the EdgeX template structure to create the ADR:

1. **Title:** Use present tense imperative verb phrase (e.g., "choose-database", "implement-caching")
2. **Submitters:** List all contributors with their organizations
3. **Change Log:** Track status changes with dates and pull request URLs
4. **Referenced Use Cases:** Link to relevant requirements or user stories
5. **Context:** Explain architectural significance and high-level approach
6. **Proposed Design:** Detail technical specifications without implementation specifics
7. **Considerations:** Document alternatives, concerns, and resolved issues
8. **Decision:** Document final implementation details and any unsatisfied requirements
9. **Related ADRs:** Link to related architectural decisions
10. **References:** List additional documentation and resources

### Step 3: Review and Approval
Simple team workflow:

1. **Create Draft:** Write ADR and commit to git repository
2. **Team Review:** Team members review asynchronously
3. **Team Discussion:** Review decisions in team calls
4. **Update Status:** Modify ADR based on team consensus
5. **Store All Versions:** Keep all variants in git for historical reference

### Step 4: Lifecycle Management
Maintain the ADR throughout its lifecycle:

1. **Implementation Tracking:** Monitor progress during implementation
2. **Amendments:** Add changes with timestamps and rationale
3. **Status Updates:** Track from pending → approved → amended → deprecated
4. **Periodic Review:** Reevaluate annually or when circumstances change

## ADR Templates and Examples

### Software Architecture Decisions
Use for decisions about:
- System design patterns
- Component architecture
- Data model design
- API design and contracts
- Integration patterns

### Infrastructure Decisions
Use for decisions about:
- Cloud provider selection
- Deployment strategies
- Containerization approaches
- Network architecture
- Security infrastructure

### Technology Stack Decisions
Use for decisions about:
- Programming language selection
- Framework choices
- Database technologies
- Third-party libraries
- Development tools

### Cost Optimization Decisions
Use when technical choices are driven by cost:
- Cloud resource optimization
- Licensing decisions
- Open source vs. commercial solutions
- Performance vs. cost trade-offs
- Scalability approaches

## Code Analysis for Existing ADRs

When documenting decisions for existing code:

1. **Analyze the Implementation:**
   - Identify the technical approach chosen
   - Look for evidence of rejected alternatives
   - Note any workarounds or compensating patterns

2. **Infer the Rationale:**
   - Consider the project context when written
   - Identify constraints that may have influenced the decision
   - Look for performance or scalability requirements

3. **Validate with Team:**
   - Consult original developers if available
   - Review commit messages and pull requests
   - Cross-reference with documentation

4. **Document Current State:**
   - Record what was implemented and why
   - Note any changes or evolution since implementation
   - Identify any emerging issues or technical debt

## Resources

This skill includes specialized resources for ADR creation and management:

### scripts/
**`generate_adr.py`** - Python script for generating ADR files using the EdgeX template:
- Creates new ADRs with proper structure
- Validates existing ADRs for completeness
- Lists and manages ADR collection
- Interactive mode for guided section completion
- Command-line interface for automation

**`analyze_codebase.py`** - Python script for analyzing existing code to create ADRs:
- Detects technology stack and design patterns
- Analyzes git history for architectural decisions
- Generates draft ADRs based on codebase analysis
- Identifies file patterns suggesting architectural choices

### references/
**`edgex_template.md`** - Complete EdgeX template documentation:
- Field-by-field explanations
- Required sections and content guidelines
- Format and structure requirements
- Best practices for each section

**`decision_framework.md`** - Comprehensive decision-making framework:
- How to identify architecturally significant decisions
- Evaluation criteria and trade-off analysis
- Alternative analysis matrix
- Consensus building and stakeholder management
- Decision quality checklist

**`adr_examples.md`** - Real-world ADR examples:
- Software architecture decisions
- Infrastructure choices
- Technology stack selections
- Cost optimization scenarios
- Complete examples with realistic content

### assets/templates/
**`software_architecture.md`** - Template for software design decisions:
- System design patterns
- Component architecture
- API design and contracts
- Integration patterns

**`infrastructure_decision.md`** - Template for infrastructure decisions:
- Cloud provider selection
- Deployment strategies
- Containerization approaches
- Network and security architecture

**`cost_optimization.md`** - Template for cost-driven technical decisions:
- Cost-benefit analysis frameworks
- Performance vs. cost trade-offs
- Implementation ROI calculations
- Risk assessment and mitigation

## Usage Examples

### Creating a New ADR
To create a new ADR for a database selection decision:
```bash
python scripts/generate_adr.py create --title "choose-primary-database" --interactive
```

### Analyzing Existing Code
To generate an ADR for an existing authentication system:
```bash
python scripts/analyze_codebase.py --topic "authentication-architecture" --output auth-adr.md
```

### Validating ADR Collection
To check all ADRs for completeness:
```bash
python scripts/generate_adr.py validate
```

These resources work together to provide comprehensive ADR creation and management capabilities, from initial decision identification through documentation and lifecycle management.
