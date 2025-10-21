# ADR Examples

This document contains example ADRs for different types of architectural decisions.

## Example 1: Software Architecture - Database Selection

```markdown
# choose-database-technology

### Submitters
*   John Doe (TechCorp)
*   Jane Smith (TechCorp)

### Change Log
*   [approved](https://github.com/techcorp/project/pull/123) 2024-01-15

### Referenced Use Case(s)
*   [User Data Management](https://github.com/techcorp/requirements/blob/main/user-data.md)

### Context
Our application requires a robust database solution to handle user data, session management, and analytics. The current file-based approach is becoming unsustainable as user traffic grows. This decision is architecturally significant as it will affect all data persistence layers and establish patterns for future data storage decisions.

### Proposed Design
We will adopt PostgreSQL as our primary database technology with the following impacts:

**Services/modules to be impacted:**
- UserService: Migration from file storage to database
- AnalyticsService: Implementation of structured data storage
- SessionManager: Database-based session storage

**Model and DTO impact:**
- User entity with proper relational structure
- Analytics event schema with time-series optimization
- Session entity with security considerations

**API impact:**
- User CRUD operations with proper error handling
- Analytics endpoints with pagination support
- Session validation endpoints

**Configuration impact:**
- Database connection settings
- Connection pool configuration
- Migration scripts and versioning

**DevOps impact:**
- Database provisioning and backups
- Monitoring and alerting setup
- Migration deployment procedures

### Considerations
**Alternatives considered:**
- MongoDB: Better for unstructured data but less established in organization
- MySQL: Similar to PostgreSQL but with fewer advanced features
- SQLite: Simple but not suitable for production scale

**Concerns addressed:**
- Team PostgreSQL experience vs. MongoDB learning curve
- Performance requirements for analytics queries
- Data consistency and ACID compliance

**Resolved issues:**
- Migration strategy designed to minimize downtime
- Backup procedures established for data safety

### Decision
PostgreSQL was chosen due to:
- Strong team experience and organizational support
- Robust feature set including JSON support for flexibility
- Excellent tooling and monitoring capabilities
- Proven reliability in production environments

Remaining work:
- Implement migration scripts with rollback capability
- Set up monitoring and alerting
- Train team on PostgreSQL best practices

### Other Related ADRs
*   [implement-caching-layer](https://github.com/techcorp/adrs/002-cache.md) - Database query optimization
*   [design-apis](https://github.com/techcorp/adrs/001-apis.md) - API design patterns affecting database interactions

### References
*   [PostgreSQL Documentation](https://www.postgresql.org/docs/)
*   [Database Migration Guide](https://github.com/techcorp/wiki/blob/main/migrations.md)
*   [Performance Benchmarks](https://techcorp.internal/benchmarks/database/)
```

## Example 2: Infrastructure - Cloud Provider Selection

```markdown
# choose-cloud-provider

### Submitters
*   Sarah Wilson (DevOps Team)
*   Mike Chen (Infrastructure Team)

### Change Log
*   [approved](https://github.com/company/infra/pull/456) 2024-02-20

### Referenced Use Case(s)
*   [Production Hosting Requirements](https://github.com/company/requirements/blob/main/hosting.md)
*   [Disaster Recovery Plan](https://github.com/company/security/blob/main/dr-plan.md)

### Context
As we scale our operations, hosting applications on-premise is becoming increasingly complex and expensive. This decision to move to a cloud provider is architecturally significant as it will affect our entire infrastructure strategy, deployment processes, and operational procedures.

### Proposed Design
We will migrate our infrastructure to AWS with the following service selections:

**Services/modules to be impacted:**
- All application services: Containerized deployment
- Database team: RDS migration from on-premise
- Monitoring team: CloudWatch integration

**New services/modules to be added:**
- AWS EKS for container orchestration
- RDS for managed database services
- CloudFront for CDN and static content
- Lambda for serverless functions

**Model and DTO impact:**
- Infrastructure as Code using Terraform
- Environment configuration management
- Service discovery and load balancing

**API impact:**
- Internal service endpoints for cloud services
- External API gateway configuration
- Security group and VPC configuration

**Configuration impact:**
- Cloud provider credentials and IAM roles
- Environment-specific configurations
- Auto-scaling policies and thresholds

**DevOps impact:**
- CI/CD pipeline updates for cloud deployment
- Monitoring and logging integration
- Cost management and optimization

### Considerations
**Alternatives considered:**
- Google Cloud Platform: Strong Kubernetes support but less mature enterprise features
- Microsoft Azure: Good enterprise integration but higher learning curve
- Multi-cloud: Maximum flexibility but increased complexity

**Concerns addressed:**
- Vendor lock-in risks mitigated by using managed services with standard interfaces
- Data sovereignty compliance verified with regional deployments
- Cost optimization through reserved instances and auto-scaling

**Resolved issues:**
- Migration timeline established with phased approach
- Training program implemented for DevOps team
- Monitoring and alerting configured for cloud environment

### Decision
AWS was selected based on:
- Largest service portfolio and feature set
- Strong enterprise support and SLAs
- Extensive documentation and community
- Competitive pricing for our workload patterns
- Strong local support presence

Remaining work:
- Complete migration of all services
- Implement cost monitoring and optimization
- Develop disaster recovery procedures for cloud

### Other Related ADRs
*   [implement-containers](https://github.com/company/adrs/003-containers.md) - Containerization strategy
*   [design-disaster-recovery](https://github.com/company/adrs/004-dr.md) - Cloud-based disaster recovery

### References
*   [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
*   [Cloud Migration Strategy](https://github.com/company/wiki/blob/main/cloud-migration.md)
*   [Cost Analysis](https://company.internal/reports/cloud-cost-analysis/)
```

## Example 3: Technology Stack - Frontend Framework

```markdown
# choose-frontend-framework

### Submitters
*   Alex Kumar (Frontend Team)
*   Emma Rodriguez (Product Team)

### Change Log
*   [approved](https://github.com/company/frontend/pull/789) 2024-03-10

### Referenced Use Case(s)
*   [User Interface Requirements](https://github.com/company/requirements/blob/main/ui-requirements.md)
*   [Mobile Responsiveness](https://github.com/company/requirements/blob/main/mobile.md)

### Context
Our current frontend stack uses jQuery and vanilla JavaScript, which is becoming difficult to maintain and extend as our application grows. This decision to adopt a modern frontend framework is architecturally significant as it will affect our entire frontend development process, team skill requirements, and user experience.

### Proposed Design
We will adopt React as our primary frontend framework with the following approach:

**Services/modules to be impacted:**
- User Interface components: Complete rewrite using React
- Dashboard application: Migration from server-side rendering
- Mobile web experience: Responsive redesign
- Form handling: Standardized form management

**New services/modules to be added:**
- Component library for reusable UI elements
- State management using Redux Toolkit
- Routing with React Router
- Testing framework with Jest and React Testing Library

**Model and DTO impact:**
- Component prop interfaces and TypeScript definitions
- State management schema and data flow patterns
- API integration with proper error handling

**API impact:**
- RESTful API consumption patterns
- WebSocket integration for real-time features
- Authentication and authorization in frontend

**Configuration impact:**
- Build system configuration with Webpack/Vite
- Development environment setup
- CI/CD pipeline for frontend deployments

**DevOps impact:**
- Frontend deployment pipeline
- Bundle optimization and caching strategies
- Performance monitoring integration

### Considerations
**Alternatives considered:**
- Vue.js: Simpler learning curve but smaller ecosystem
- Angular: More opinionated but steeper learning curve
- Svelte: Better performance but less mature ecosystem

**Concerns addressed:**
- Team learning curve mitigated by gradual migration approach
- Performance concerns addressed with proper optimization techniques
- Legacy system integration through component-by-component migration

**Resolved issues:**
- Training schedule established for React development
- Component library design system created
- Performance benchmarks established for migration targets

### Decision
React was chosen because:
- Largest ecosystem and community support
- Strong TypeScript integration
- Extensive third-party library availability
- Good performance with proper optimization
- Strong team experience with similar frameworks

Remaining work:
- Build reusable component library
- Migrate critical user-facing components first
- Implement comprehensive testing strategy
- Establish performance monitoring

### Other Related ADRs
*   [implement-typescript](https://github.com/company/adrs/005-typescript.md) - Type safety in frontend
*   [design-component-library](https://github.com/company/adrs/006-components.md) - Reusable UI components

### References
*   [React Documentation](https://react.dev/)
*   [Frontend Development Guidelines](https://github.com/company/wiki/blob/main/frontend-standards.md)
*   [Performance Benchmarks](https://company.internal/performance/frontend/)
```