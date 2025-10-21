# EdgeX Foundry ADR Template

This is the EdgeX Foundry ADR template structure with field explanations.

## Template Structure

```markdown
# [ADR Title]

### Submitters
*   Name (Organization)

### Change Log
*   [Status](URL) YYYY-MM-DD

### Referenced Use Case(s)
*   [Use Case Name](URL)

### Context
*   Architectural significance
*   High-level design approach

### Proposed Design
*   Services/modules impacted
*   New services/modules added
*   Model and DTO impact
*   API impact
*   Configuration impact
*   DevOps impact

### Considerations
*   Alternatives considered
*   Concerns addressed
*   Issues resolved

### Decision
*   Implementation details
*   Remaining issues
*   Unsatisfied requirements

### Other Related ADRs
*   [ADR Title](URL) - Relevance

### References
*   [Title](URL)
```

## Field Explanations

### Submitters
List all contributors to the ADR with their organizations in the format:
*   John Doe (Acme Corporation)
*   Jane Smith (Tech Startup Inc.)

### Change Log
Track all changes to the ADR with status, date, and pull request:
*   **Status**: pending, approved, amended, deprecated
*   **Date**: ISO 8601 format (YYYY-MM-DD)
*   **URL**: Link to pull request with details

### Referenced Use Case(s)
Link to requirements documents, user stories, or use cases that justify the ADR.

### Context
Explain why this decision is architecturally significant:
- What problem needs solving
- Why this requires an ADR (vs. simple issue/PR)
- High-level approach overview
- Architectural impact scope

### Proposed Design
Detail the technical design without implementation specifics:
- **Services/Modules**: Which existing components will change
- **New Components**: What new services/modules will be added
- **Data Models**: Changes to data structures, DTOs
- **APIs**: New/modified/deprecated endpoints
- **Configuration**: New config sections, environment variables
- **DevOps**: Impact on deployment, monitoring, operations

### Considerations
Document the decision-making process:
- Alternative approaches considered
- Concerns that arose during discussion
- How issues were resolved or mitigated
- Trade-offs evaluated

### Decision
Document the final agreed approach:
- Implementation details and caveats
- Future considerations or deferred work
- Requirements that cannot be satisfied
- Constraints or limitations

### Related ADRs
Link to other relevant ADRs:
- Sub-component decisions
- Deprecated designs
- Prerequisite decisions

### References
Additional documentation and resources relevant to the decision.