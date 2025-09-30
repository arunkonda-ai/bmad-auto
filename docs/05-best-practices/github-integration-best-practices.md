# GitHub Integration Best Practices for BMAD Auto

## Overview

This document provides comprehensive best practices for GitHub integration within the BMAD Auto autonomous system. All agents must follow these guidelines when managing code repositories, pull requests, and development workflows.

## GitHub Setup Best Practices

### Repository Configuration
```yaml
repository_setup:
  organization_structure:
    main_repository: "bmad-auto/autonomous-product-development"
    documentation_repo: "bmad-auto/documentation"
    template_repos: "bmad-auto/project-templates"

  branch_protection:
    main_branch:
      - Require pull request reviews (minimum 2)
      - Require status checks to pass
      - Require branches to be up to date
      - Restrict pushes to main branch
      - Require signed commits for security

  access_control:
    agent_permissions:
      mary: ["read", "create_issues", "comment"]
      john: ["read", "write", "manage_issues", "manage_projects"]
      james: ["read", "write", "create_pr", "review_code"]
      quinn: ["read", "write", "create_pr", "manage_actions"]
      sally: ["read", "create_issues", "comment", "design_reviews"]
      alex: ["admin", "manage_settings", "security_alerts"]
```

### Security Configuration
```yaml
security_setup:
  authentication:
    - Use GitHub Apps for agent authentication
    - Implement fine-grained personal access tokens
    - Enable two-factor authentication for all accounts
    - Use signed commits for code integrity

  secrets_management:
    - Store API keys in GitHub Secrets
    - Use environment-specific secret groups
    - Implement secret rotation policies
    - Monitor secret usage and access

  vulnerability_management:
    - Enable Dependabot security updates
    - Configure CodeQL security scanning
    - Implement SAST/DAST in CI/CD pipeline
    - Monitor security advisories and alerts
```

## Branch Management Best Practices

### Branching Strategy
```yaml
branching_model:
  main_branches:
    main:
      purpose: "Production-ready code"
      protection: "Maximum protection with required reviews"
      auto_deploy: "Production environment"

    develop:
      purpose: "Integration branch for features"
      protection: "Required status checks"
      auto_deploy: "Staging environment"

  feature_branches:
    naming_convention:
      - "feature/agent-name/task-description"
      - "feature/mary/market-research-automation"
      - "feature/james/api-optimization"
      - "feature/quinn/test-automation-suite"

    lifecycle:
      creation: "Branch from develop"
      development: "Regular commits with descriptive messages"
      integration: "Pull request to develop"
      cleanup: "Delete after successful merge"

  release_branches:
    naming_convention: "release/version-number"
    purpose: "Prepare releases and final testing"
    lifecycle: "Branch from develop, merge to main and develop"

  hotfix_branches:
    naming_convention: "hotfix/issue-description"
    purpose: "Critical production fixes"
    lifecycle: "Branch from main, merge to main and develop"
```

### Agent-Specific Branch Practices
```yaml
agent_branch_practices:
  mary_research_branches:
    naming: "research/mary/topic-analysis"
    content: "Research findings, market data, documentation"
    coordination: "Create PR for John's review and strategic input"

  john_coordination_branches:
    naming: "coordination/john/project-management"
    content: "Project plans, roadmaps, strategic documentation"
    coordination: "Coordinate with all agents for input and approval"

  james_development_branches:
    naming: "feature/james/component-name"
    content: "Code implementation, technical documentation"
    coordination: "Request reviews from Alex and Quinn"

  quinn_testing_branches:
    naming: "testing/quinn/test-suite-name"
    content: "Test automation, quality validation scripts"
    coordination: "Coordinate with James for integration testing"

  sally_design_branches:
    naming: "design/sally/ui-component-name"
    content: "Design specifications, UI implementations"
    coordination: "Request feedback through AG UI integration"
```

## Commit Message Best Practices

### Conventional Commits
```yaml
commit_standards:
  format: "type(scope): description [Linear-ID]"

  types:
    feat: "New feature implementation"
    fix: "Bug fix or issue resolution"
    docs: "Documentation updates"
    style: "Code style changes (formatting, etc.)"
    refactor: "Code refactoring without feature changes"
    test: "Test additions or modifications"
    chore: "Maintenance tasks and build changes"

  examples:
    - "feat(api): add user authentication endpoint [BMAD-123]"
    - "fix(database): resolve connection pool timeout [BMAD-124]"
    - "docs(api): update endpoint documentation [BMAD-125]"
    - "test(integration): add API endpoint tests [BMAD-126]"

  agent_specific_scopes:
    mary: "(research)", "(analysis)", "(market)"
    john: "(coordination)", "(strategy)", "(roadmap)"
    james: "(api)", "(backend)", "(frontend)", "(integration)"
    quinn: "(testing)", "(quality)", "(automation)"
    sally: "(ux)", "(design)", "(accessibility)"
    alex: "(infra)", "(deployment)", "(security)"
```

### Co-Authored Commits
```yaml
collaboration_commits:
  format: |
    feat(component): implement feature description

    Detailed description of changes and coordination.

    Co-authored-by: John PM <john@bmad-auto.com>
    Co-authored-by: James Dev <james@bmad-auto.com>

  usage_scenarios:
    cross_agent_development:
      - Features requiring multiple agent coordination
      - Complex implementations with shared responsibility
      - Knowledge transfer and collaborative problem solving

    pair_programming:
      - James and Alex on infrastructure features
      - Quinn and James on test automation
      - Sally and John on user experience features
```

## Pull Request Best Practices

### PR Creation Standards
```yaml
pr_standards:
  title_format: "[Agent] Feature/Fix Description [Linear-ID]"

  description_template: |
    ## Summary
    Brief description of changes and their purpose.

    ## Agent Coordination
    - **Primary Agent**: [Agent Name]
    - **Collaborating Agents**: [List of involved agents]
    - **Linear Issue**: [Link to Linear issue]

    ## Changes Made
    - [ ] Feature implementation
    - [ ] Test coverage added
    - [ ] Documentation updated
    - [ ] Quality checks passed

    ## Testing Strategy
    - Unit tests: [Status]
    - Integration tests: [Status]
    - Quality validation: [Status]
    - Performance testing: [Status]

    ## Agent Review Requirements
    - [ ] Technical review (James/Alex)
    - [ ] Quality review (Quinn)
    - [ ] UX review (Sally) - if applicable
    - [ ] Strategic review (John) - if applicable

    ## Deployment Notes
    - Database migrations: [Yes/No]
    - Configuration changes: [Yes/No]
    - Infrastructure updates: [Yes/No]
    - Feature flags: [Yes/No]

  size_guidelines:
    small: "< 100 lines changed (preferred)"
    medium: "100-500 lines changed (acceptable)"
    large: "> 500 lines changed (requires justification)"
```

### Review Process
```yaml
review_workflow:
  automatic_reviewers:
    code_changes:
      - "james" (technical review)
      - "alex" (architecture review if infrastructure)
      - "quinn" (quality review)

    documentation_changes:
      - "john" (strategic alignment)
      - relevant_agent (domain expertise)

    design_changes:
      - "sally" (ux review)
      - "john" (business alignment)

  review_requirements:
    mandatory_approvals:
      - At least 2 approvals for feature PRs
      - 1 approval for documentation PRs
      - 1 approval for test-only PRs
      - Alex approval for infrastructure changes

    quality_gates:
      - All CI/CD checks must pass
      - Code coverage must meet minimum threshold
      - Security scans must pass
      - Performance benchmarks must be met

  agent_review_responsibilities:
    james_technical_review:
      focus: "Code quality, architecture, maintainability"
      checklist:
        - [ ] Code follows established patterns
        - [ ] Proper error handling implemented
        - [ ] Performance considerations addressed
        - [ ] Security best practices followed

    quinn_quality_review:
      focus: "Testing, quality assurance, reliability"
      checklist:
        - [ ] Adequate test coverage provided
        - [ ] Edge cases considered and tested
        - [ ] Quality metrics maintained or improved
        - [ ] No regression in existing functionality

    alex_infrastructure_review:
      focus: "System architecture, scalability, security"
      checklist:
        - [ ] Infrastructure changes properly planned
        - [ ] Scalability considerations addressed
        - [ ] Security implications evaluated
        - [ ] Deployment strategy documented

    sally_ux_review:
      focus: "User experience, accessibility, design consistency"
      checklist:
        - [ ] User experience improved or maintained
        - [ ] Accessibility standards met
        - [ ] Design system consistency preserved
        - [ ] User feedback incorporated appropriately
```

## CI/CD Integration Best Practices

### Automated Workflows
```yaml
github_actions:
  quality_checks:
    code_quality:
      - name: "Code Linting and Formatting"
        triggers: ["pull_request", "push_to_main"]
        tools: ["eslint", "prettier", "black", "ruff"]

      - name: "Type Checking"
        triggers: ["pull_request", "push_to_main"]
        tools: ["typescript", "mypy", "pyright"]

    testing:
      - name: "Unit Tests"
        triggers: ["pull_request", "push_to_main"]
        coverage_requirement: "80%"
        failure_action: "block_merge"

      - name: "Integration Tests"
        triggers: ["pull_request", "push_to_main"]
        environment: "testing"
        dependencies: ["database", "redis", "external_apis"]

      - name: "End-to-End Tests"
        triggers: ["pull_request_to_main"]
        environment: "staging"
        tools: ["playwright", "cypress"]

    security:
      - name: "Security Scanning"
        triggers: ["pull_request", "push_to_main", "schedule"]
        tools: ["codeql", "snyk", "trivy"]
        failure_action: "create_issue"

      - name: "Dependency Check"
        triggers: ["pull_request", "push_to_main", "schedule"]
        tools: ["dependabot", "safety", "audit"]

  deployment_workflows:
    staging_deployment:
      trigger: "push_to_develop"
      environment: "staging"
      steps:
        - "build_and_test"
        - "deploy_to_staging"
        - "run_smoke_tests"
        - "notify_agents"

    production_deployment:
      trigger: "push_to_main"
      environment: "production"
      steps:
        - "build_and_test"
        - "security_scan"
        - "deploy_to_production"
        - "run_health_checks"
        - "notify_stakeholders"
```

### Agent-Triggered Actions
```yaml
agent_automation:
  mary_research_automation:
    trigger: "push_to_research_branch"
    actions:
      - "validate_research_format"
      - "update_research_index"
      - "notify_john_for_review"
      - "create_linear_research_issue"

  james_development_automation:
    trigger: "push_to_feature_branch"
    actions:
      - "run_code_quality_checks"
      - "execute_unit_tests"
      - "update_api_documentation"
      - "request_quinn_quality_review"

  quinn_testing_automation:
    trigger: "push_to_testing_branch"
    actions:
      - "execute_test_suite"
      - "generate_coverage_report"
      - "update_quality_metrics"
      - "create_quality_assessment_issue"

  sally_design_automation:
    trigger: "push_to_design_branch"
    actions:
      - "validate_design_specs"
      - "check_accessibility_compliance"
      - "update_design_system"
      - "request_ux_review_via_agui"
```

## Issue and Project Management

### GitHub Issues Integration
```yaml
issue_management:
  issue_templates:
    bug_report:
      title: "[Bug] Issue Description"
      labels: ["bug", "agent:assigned"]
      assignees: ["relevant_agent"]
      projects: ["Bug Tracking"]

    feature_request:
      title: "[Feature] Feature Description"
      labels: ["enhancement", "agent:assigned"]
      assignees: ["john", "relevant_agent"]
      projects: ["Feature Development"]

    agent_coordination:
      title: "[Coordination] Task Description"
      labels: ["coordination", "agent:multiple"]
      assignees: ["john"]
      projects: ["Agent Coordination"]

  automation_rules:
    issue_triage:
      - Auto-assign issues based on labels
      - Create Linear issue for tracking
      - Notify relevant agents
      - Add to appropriate project boards

    status_sync:
      - Update GitHub issue status from Linear
      - Sync labels and milestones bidirectionally
      - Maintain cross-platform consistency
      - Generate status reports
```

### Project Boards
```yaml
project_management:
  board_structure:
    agent_coordination_board:
      columns: ["Backlog", "In Progress", "Review", "Done"]
      automation: "Move cards based on PR status"
      visibility: "Organization"

    feature_development_board:
      columns: ["Planning", "Development", "Testing", "Release"]
      automation: "Move cards based on Linear status"
      filters: "By agent, priority, milestone"

    quality_assurance_board:
      columns: ["Pending", "Testing", "Review", "Approved"]
      automation: "Move cards based on test results"
      metrics: "Quality trends and improvements"

  milestone_management:
    sprint_milestones:
      duration: "2 weeks"
      planning: "John coordinates with all agents"
      tracking: "Daily progress updates"
      retrospective: "End-of-sprint review and improvements"

    release_milestones:
      duration: "1 month"
      planning: "Monthly roadmap coordination"
      tracking: "Weekly progress reviews"
      delivery: "Staged deployment with quality validation"
```

## Monitoring and Analytics

### Repository Health Metrics
```yaml
health_monitoring:
  code_quality_metrics:
    - Code coverage percentage
    - Cyclomatic complexity trends
    - Technical debt indicators
    - Security vulnerability counts

  collaboration_metrics:
    - Pull request review times
    - Agent contribution distribution
    - Cross-agent collaboration frequency
    - Knowledge sharing effectiveness

  performance_metrics:
    - Build and test execution times
    - Deployment frequency and success rates
    - Issue resolution times
    - Feature delivery velocity

  integration_health:
    - API usage and rate limits
    - Webhook delivery success rates
    - Sync accuracy with Linear
    - Automation failure rates
```

### Reporting and Dashboards
```yaml
reporting_setup:
  agent_performance_reports:
    individual_metrics:
      - Commits and PRs per sprint
      - Code review participation
      - Issue resolution efficiency
      - Quality contribution scores

    collaboration_metrics:
      - Cross-agent PR reviews
      - Coordination effectiveness
      - Knowledge sharing contributions
      - Process improvement initiatives

  system_health_dashboards:
    repository_overview:
      - Active branches and PRs
      - Build status and trends
      - Security alert status
      - Dependency health

    integration_status:
      - Linear sync health
      - CI/CD pipeline performance
      - External service integrations
      - Automation effectiveness
```

## Security and Compliance

### Security Best Practices
```yaml
security_practices:
  code_security:
    - Never commit secrets or credentials
    - Use environment variables for configuration
    - Implement proper input validation
    - Follow secure coding guidelines

  access_management:
    - Principle of least privilege
    - Regular access reviews
    - MFA enforcement
    - Session management

  vulnerability_management:
    - Automated security scanning
    - Rapid response to critical vulnerabilities
    - Regular dependency updates
    - Security awareness training

  compliance_requirements:
    - Code review audit trails
    - Change management documentation
    - Security scanning evidence
    - Compliance reporting automation
```

### Backup and Recovery
```yaml
disaster_recovery:
  repository_backup:
    - Daily automated backups
    - Multiple geographic locations
    - Version history preservation
    - Recovery testing procedures

  configuration_backup:
    - Repository settings and rules
    - Workflow and action configurations
    - Security and access policies
    - Integration configurations

  recovery_procedures:
    - Documented recovery processes
    - RTO and RPO targets
    - Emergency contact procedures
    - Business continuity planning
```

---

*These GitHub integration best practices ensure optimal code management, collaboration, and quality assurance across the BMAD Auto autonomous system, enabling efficient development workflows and high-quality software delivery.*