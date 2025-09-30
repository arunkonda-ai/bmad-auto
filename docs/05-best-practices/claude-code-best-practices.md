# Claude Code Best Practices for BMAD Auto

## Overview

This document provides comprehensive best practices for Claude Code usage within the BMAD Auto autonomous system. All agents must follow these guidelines when interacting with Claude Code for optimal performance and quality outcomes.

**CRITICAL PRINCIPLE: ASK DON'T ASSUME**
- **OBVIOUS** (use general knowledge): Basic programming patterns, common frameworks, standard practices
- **NON-OBVIOUS** (must ask): Business rules, domain-specific requirements, project-specific constraints, user workflows
- **Always Ask For**: Business logic, validation rules, user experience flows, integration specifics, performance requirements
- **Never Assume**: Requirements, priorities, user needs, business constraints, technical specifications beyond obvious patterns

## Core Principles

### 1. ASK DON'T ASSUME Protocol
- **Never assume project-specific information** - always ask for non-obvious details
- **Distinguish Obvious vs Non-Obvious**:
  - **OBVIOUS**: Basic programming patterns, common frameworks, standard practices
  - **NON-OBVIOUS**: Business rules, domain requirements, project specifics, user workflows
- **Always ask for**: Business logic, validation rules, user experience flows, integration specifics
- **Agent-to-Agent communication**: Apply same principle when coordinating with other agents

### 2. Concise Communication
- **Keep responses under 4 lines** unless user explicitly requests detail
- **Answer directly** without unnecessary preamble or postamble
- **One word answers are best** when appropriate
- **Avoid explaining code** unless specifically requested

### 3. Tool Usage Efficiency
- **Batch tool calls** when multiple independent operations needed
- **Use TodoWrite tool** for complex multi-step tasks (3+ steps)
- **Prefer Read tool** for specific file paths over search tools
- **Use Task tool** for open-ended searches requiring multiple rounds

### 4. Code Quality Standards
- **Follow existing conventions** in the codebase
- **Check library availability** before using any framework
- **Never add comments** unless explicitly requested
- **Keep files under 300 lines** for maintainability
- **Use async/await patterns** with proper error handling

## Agent-Specific Best Practices

### Mary (Business Analyst)
```yaml
claude_usage:
  research_tasks:
    - Use WebSearch for market research with specific queries
    - Batch multiple search operations in single response
    - Use Read tool for analyzing competitor documentation
    - WebFetch for competitor website analysis

  documentation:
    - Keep research findings concise and actionable
    - Use TodoWrite for multi-step research projects
    - Structure findings in clear sections
    - Include data sources and confidence levels

  linear_integration:
    - Create issues with proper labels and priorities
    - Link research findings to strategic requirements
    - Update issue status based on research progress
    - Use Linear webhooks for real-time coordination
```

### John (Product Manager & PM Coordinator)
```yaml
claude_usage:
  coordination_tasks:
    - Use TodoWrite for managing agent assignments
    - Batch coordination commands in single response
    - Use Linear MCP for project management operations
    - Monitor all agent progress through structured updates
    - Apply ASK DON'T ASSUME when coordinating between agents

  strategic_planning:
    - Keep PRDs concise and actionable
    - Use AG UI for strategic approval workflows
    - Document decisions with clear rationale
    - Update project status in real-time
    - Ask for clarification on non-obvious business requirements

  quality_orchestration:
    - Coordinate cross-agent quality validation
    - Use batch processing for efficiency
    - Escalate to human approval when needed
    - Maintain audit trail of all decisions
    - Use 6W framework for all decisions (What, Why, Where, When, How, Who)

  pm_hub_coordination:
    - Central coordination for all 10 agents
    - Context distribution based on relevance filtering
    - Batch processing for agent updates
    - Command simulation oversight for .bmad-core preservation
```

### James (Developer)
```yaml
claude_usage:
  development_tasks:
    - Follow size compliance (under 300 lines per file)
    - Use Read tool before any file modifications
    - Batch related code changes in single response
    - Never add comments unless requested

  github_integration:
    - Create feature branches with descriptive names
    - Use conventional commit messages
    - Request PR reviews from relevant agents
    - Monitor CI/CD pipeline status

  code_quality:
    - Run linting and type checking before commits
    - Use proper async/await patterns
    - Follow existing code conventions
    - Implement proper error handling
```

### Quinn (QA Engineer)
```yaml
claude_usage:
  testing_tasks:
    - Use TodoWrite for comprehensive test planning
    - Batch test execution commands
    - Use Playwright MCP for browser automation
    - Document test results clearly

  quality_validation:
    - Cross-validate with other agents
    - Use automated testing tools
    - Report issues with clear reproduction steps
    - Maintain test coverage metrics

  performance_monitoring:
    - Monitor system performance metrics
    - Use diagnostic tools for troubleshooting
    - Escalate performance issues promptly
    - Document optimization recommendations
```

### Sally (UX Designer)
```yaml
claude_usage:
  design_tasks:
    - Use AG UI for human collaboration on designs
    - Create interactive prototypes for validation
    - Document design decisions with user impact
    - Maintain design system consistency

  accessibility:
    - Follow WCAG guidelines strictly
    - Test with screen readers and accessibility tools
    - Document accessibility considerations
    - Validate with diverse user groups

  user_research:
    - Use structured research methodologies
    - Document user feedback systematically
    - Translate insights into actionable recommendations
    - Coordinate with Mary on user data analysis
```

### Alex (Infrastructure Architect)
```yaml
claude_usage:
  infrastructure_tasks:
    - Preserve .bmad-core infrastructure absolutely
    - Monitor system health continuously
    - Use proper deployment patterns
    - Document architecture decisions

  bmad_core_preservation:
    - Never modify .bmad-core files
    - Monitor command simulation accuracy
    - Validate infrastructure integrity
    - Escalate preservation issues immediately

  performance_optimization:
    - Monitor resource utilization
    - Implement efficient scaling patterns
    - Optimize database performance
    - Maintain security best practices
```

## Tool-Specific Best Practices

### Linear Integration
```yaml
linear_best_practices:
  issue_management:
    - Use consistent labeling system
    - Set proper priorities and estimates
    - Link related issues appropriately
    - Update status in real-time

  project_coordination:
    - Create clear project milestones
    - Track progress against deadlines
    - Use custom fields for agent assignments
    - Maintain clean project hierarchy

  automation:
    - Use webhooks for real-time updates
    - Implement status sync with workflow states
    - Automate issue creation from agent tasks
    - Monitor API rate limits
```

### GitHub Integration
```yaml
github_best_practices:
  branch_management:
    - Use feature branch workflow
    - Follow naming conventions (feature/agent-task)
    - Keep branches focused and small
    - Delete merged branches promptly

  commit_practices:
    - Use conventional commit messages
    - Keep commits atomic and focused
    - Include issue references in commits
    - Use co-authored commits for agent collaboration

  pull_requests:
    - Request reviews from relevant agents
    - Use PR templates for consistency
    - Ensure CI/CD passes before merge
    - Document breaking changes clearly

  security:
    - Never commit secrets or keys
    - Use environment variables for configuration
    - Scan for vulnerabilities regularly
    - Follow security review processes
```

### AG UI Integration
```yaml
agui_best_practices:
  human_collaboration:
    - Use time-bounded approval workflows
    - Provide clear context for decisions
    - Enable back-and-forth discussion
    - Document approval rationale

  strategic_decisions:
    - Escalate architecture changes
    - Require approval for resource allocation
    - Validate business impact decisions
    - Maintain decision audit trail

  real_time_coordination:
    - Use WebSocket for live updates
    - Provide progress indicators
    - Handle disconnection gracefully
    - Maintain session state
```

### Database Context Management
```yaml
database_best_practices:
  context_distribution:
    - Filter context by agent relevance
    - Use vector embeddings for semantic search
    - Implement efficient batch processing
    - Maintain context versioning

  performance:
    - Use connection pooling
    - Implement proper indexing
    - Monitor query performance
    - Optimize vector operations

  data_integrity:
    - Use transactions for consistency
    - Implement proper backup strategies
    - Validate data before storage
    - Handle schema migrations carefully
```

## Error Handling Best Practices

### Agent Error Recovery
```yaml
error_recovery:
  agent_failures:
    - Implement graceful degradation
    - Use fallback coordination patterns
    - Escalate to PM coordination hub
    - Maintain operation continuity

  external_service_failures:
    - Use MCP with direct API fallback
    - Implement retry with exponential backoff
    - Monitor service health continuously
    - Document service dependencies

  quality_gate_failures:
    - Escalate to human approval
    - Document failure reasons clearly
    - Implement corrective actions
    - Prevent regression
```

### Command Simulation Error Handling
```yaml
command_simulation_errors:
  bmad_core_preservation:
    - Validate .bmad-core integrity continuously
    - Never proceed if preservation fails
    - Escalate preservation issues immediately
    - Maintain rollback capabilities

  database_translation:
    - Validate command translation accuracy
    - Implement transaction rollback
    - Monitor translation performance
    - Log all command operations
```

## Performance Optimization

### PM Coordination Efficiency
```yaml
pm_optimization:
  batch_processing:
    - Group related agent updates
    - Process context distribution efficiently
    - Use async operations for coordination
    - Monitor coordination latency

  context_management:
    - Implement intelligent filtering
    - Use vector similarity for relevance
    - Cache frequently accessed context
    - Optimize embedding operations
```

### Agent Coordination Patterns
```yaml
coordination_optimization:
  handoff_protocols:
    - Minimize context transfer overhead
    - Use structured handoff formats
    - Validate handoff completeness
    - Monitor handoff success rates

  parallel_processing:
    - Identify independent agent tasks
    - Coordinate parallel execution
    - Aggregate results efficiently
    - Handle dependencies properly
```

## Monitoring and Observability

### Agent Performance Metrics
```yaml
monitoring_best_practices:
  agent_metrics:
    - Track response times
    - Monitor success rates
    - Measure quality scores
    - Analyze coordination efficiency

  system_health:
    - Monitor resource utilization
    - Track external service health
    - Measure workflow completion rates
    - Analyze error patterns

  quality_metrics:
    - Track quality gate success rates
    - Monitor human approval patterns
    - Measure user satisfaction
    - Analyze improvement opportunities
```

## Security Best Practices

### Agent Security
```yaml
security_guidelines:
  access_control:
    - Implement role-based permissions
    - Use secure authentication methods
    - Monitor agent access patterns
    - Audit sensitive operations

  data_protection:
    - Encrypt sensitive data
    - Use secure communication channels
    - Implement data retention policies
    - Handle PII appropriately

  integration_security:
    - Secure API credentials
    - Use OAuth where available
    - Monitor for security vulnerabilities
    - Implement security scanning
```

---

*These best practices ensure optimal Claude Code usage across the BMAD Auto autonomous system, enabling efficient, high-quality, and secure agent operations.*