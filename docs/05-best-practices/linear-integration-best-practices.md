# Linear Integration Best Practices for BMAD Auto

## Overview

This document provides comprehensive best practices for Linear project management integration within the BMAD Auto autonomous system. All agents must follow these guidelines when creating, updating, and managing Linear issues and projects.

## Linear Setup Best Practices

### Initial Configuration
```yaml
linear_setup:
  workspace_configuration:
    - Create dedicated BMAD Auto team
    - Set up custom issue templates for each agent
    - Configure automation rules for status updates
    - Establish labeling taxonomy for agent coordination

  integration_settings:
    - Enable API access with proper scopes
    - Configure webhook endpoints for real-time updates
    - Set up MCP integration as primary method
    - Configure direct API fallback for reliability

  security_configuration:
    - Use environment variables for API keys
    - Implement rate limiting protection
    - Set up monitoring for API usage
    - Configure audit logging for all operations
```

### Team Structure Setup
```yaml
team_organization:
  bmad_auto_team:
    name: "BMAD Auto - Autonomous Development"
    identifier: "BMAD"
    description: "AI-powered autonomous product development"

  agent_roles:
    - name: "Mary - Business Analyst"
      permissions: ["create_issues", "update_issues", "comment"]
      focus_areas: ["research", "market-analysis", "user-research"]

    - name: "John - Product Manager"
      permissions: ["create_issues", "update_issues", "assign", "manage_projects"]
      focus_areas: ["strategy", "coordination", "roadmap"]

    - name: "James - Developer"
      permissions: ["create_issues", "update_issues", "link_to_github"]
      focus_areas: ["development", "technical", "implementation"]

    - name: "Quinn - QA Engineer"
      permissions: ["create_issues", "update_issues", "quality_validation"]
      focus_areas: ["testing", "quality", "validation"]

    - name: "Sally - UX Designer"
      permissions: ["create_issues", "update_issues", "design_review"]
      focus_areas: ["ux", "design", "accessibility"]
```

## Issue Management Best Practices

### Issue Creation Standards
```yaml
issue_creation:
  title_conventions:
    research: "[Research] {Topic} - {Agent}"
    development: "[Dev] {Feature} - {Component}"
    quality: "[QA] {Test Type} - {Feature}"
    design: "[UX] {Design Task} - {Component}"
    coordination: "[PM] {Coordination Task} - {Scope}"

  required_fields:
    - Clear, actionable title
    - Detailed description with acceptance criteria
    - Appropriate labels for categorization
    - Priority level (Urgent, High, Medium, Low)
    - Estimated effort (Story points or time)
    - Assigned agent or team member

  description_template:
    sections:
      - "## Objective"
      - "## Acceptance Criteria"
      - "## Success Metrics"
      - "## Dependencies"
      - "## Resources"
      - "## Agent Coordination Notes"
```

### Labeling System
```yaml
label_taxonomy:
  agent_labels:
    - "agent:mary" (Business Analyst tasks)
    - "agent:john" (Product Manager coordination)
    - "agent:james" (Developer implementation)
    - "agent:quinn" (QA validation)
    - "agent:sally" (UX design)
    - "agent:alex" (Infrastructure)

  workflow_phase_labels:
    - "phase:research" (Market research and analysis)
    - "phase:ideation" (Concept development)
    - "phase:specification" (PRD and architecture)
    - "phase:development" (Implementation)
    - "phase:validation" (Testing and QA)

  priority_labels:
    - "priority:urgent" (Blocking or critical)
    - "priority:high" (Important for current sprint)
    - "priority:medium" (Next sprint consideration)
    - "priority:low" (Future backlog)

  type_labels:
    - "type:feature" (New functionality)
    - "type:bug" (Issue or defect)
    - "type:improvement" (Enhancement)
    - "type:research" (Investigation or analysis)
    - "type:coordination" (Agent coordination task)

  coordination_labels:
    - "coordination:pm-review" (Requires PM approval)
    - "coordination:cross-agent" (Multiple agents involved)
    - "coordination:human-approval" (Human decision needed)
    - "coordination:quality-gate" (Quality validation required)
```

## Agent-Specific Linear Practices

### Mary (Business Analyst)
```yaml
mary_linear_practices:
  research_issues:
    creation:
      - Use "[Research]" prefix in titles
      - Include research methodology in description
      - Set appropriate timeline estimates
      - Link to relevant data sources

    management:
      - Update progress with research findings
      - Create sub-issues for different research areas
      - Use comments for interim insights
      - Link to related market analysis issues

    coordination:
      - Tag John for strategic input
      - Create handoff issues for other agents
      - Document key insights for team visibility
      - Update stakeholder communication issues

  market_analysis:
    competitive_analysis:
      - Create dedicated issues for each competitor
      - Use structured templates for consistency
      - Track competitor feature updates
      - Link to product strategy discussions

    user_research:
      - Create issues for each research method
      - Document user persona development
      - Track user feedback collection
      - Link to UX design implications
```

### John (Product Manager & PM Coordinator)
```yaml
john_linear_practices:
  strategic_coordination:
    project_management:
      - Create master coordination issues
      - Break down complex initiatives
      - Set up project timelines and milestones
      - Coordinate cross-agent dependencies

    roadmap_planning:
      - Create quarterly roadmap issues
      - Link features to business objectives
      - Track progress against roadmap goals
      - Coordinate stakeholder communication

  agent_coordination:
    assignment_management:
      - Assign issues based on agent expertise
      - Set clear deadlines and expectations
      - Monitor agent workload and capacity
      - Escalate blocking issues promptly

    quality_orchestration:
      - Create quality gate validation issues
      - Coordinate cross-agent reviews
      - Track quality metrics and improvements
      - Manage human approval workflows

  stakeholder_communication:
    reporting:
      - Create weekly status update issues
      - Track stakeholder feedback and decisions
      - Document strategic decisions and rationale
      - Coordinate executive review sessions
```

### James (Developer)
```yaml
james_linear_practices:
  development_coordination:
    feature_development:
      - Create technical specification issues
      - Break down development tasks by component
      - Link issues to GitHub pull requests
      - Track technical debt and improvements

    architecture_decisions:
      - Document architectural choices
      - Create issues for technical research
      - Coordinate with Alex on infrastructure
      - Track performance optimization tasks

  code_quality:
    implementation:
      - Link Linear issues to Git commits
      - Update issue status based on development progress
      - Create issues for code review findings
      - Track bug fixes and resolutions

    integration:
      - Coordinate with Quinn on testing requirements
      - Create issues for integration testing
      - Track deployment and release activities
      - Document technical dependencies
```

### Quinn (QA Engineer)
```yaml
quinn_linear_practices:
  quality_validation:
    test_planning:
      - Create comprehensive test plan issues
      - Break down testing by feature and component
      - Set up automated testing issues
      - Coordinate manual testing schedules

    quality_gates:
      - Create quality validation checkpoints
      - Track testing progress and results
      - Document quality metrics and trends
      - Escalate quality issues promptly

  cross_agent_validation:
    coordination:
      - Review development issues for testability
      - Coordinate with Sally on UX testing
      - Validate business requirements with Mary
      - Support James with technical testing

    reporting:
      - Create quality dashboard issues
      - Track defect trends and resolution
      - Document testing best practices
      - Report on system reliability metrics
```

### Sally (UX Designer)
```yaml
sally_linear_practices:
  design_coordination:
    ux_design:
      - Create design specification issues
      - Document user experience requirements
      - Coordinate with Mary on user research
      - Track design system consistency

    accessibility:
      - Create accessibility compliance issues
      - Document WCAG requirements and testing
      - Coordinate accessibility validation
      - Track accessibility improvements

  human_collaboration:
    ag_ui_integration:
      - Create design review issues for human feedback
      - Document design decisions and rationale
      - Track user testing sessions and results
      - Coordinate design iteration cycles
```

## Project Management Best Practices

### Project Structure
```yaml
project_organization:
  hierarchy:
    initiatives:
      - Quarterly business objectives
      - Major product features
      - Infrastructure improvements
      - Quality improvements

    projects:
      - Feature development projects
      - Research and analysis projects
      - Technical debt reduction
      - Process improvement initiatives

    epics:
      - Major feature sets
      - Cross-functional initiatives
      - Integration projects
      - Platform improvements

    issues:
      - Individual tasks and stories
      - Bug reports and fixes
      - Research activities
      - Coordination tasks

  milestone_management:
    sprint_planning:
      - Weekly sprint cycles
      - Clear sprint goals and objectives
      - Capacity planning by agent
      - Risk assessment and mitigation

    release_planning:
      - Monthly release cycles
      - Feature freeze dates
      - Quality gate checkpoints
      - Stakeholder communication plans
```

### Automation Rules
```yaml
automation_setup:
  status_updates:
    automatic_transitions:
      - Move to "In Progress" when assigned
      - Move to "Review" when PR created
      - Move to "Testing" when development complete
      - Move to "Done" when all validation passes

  notification_rules:
    agent_notifications:
      - Notify John on all agent issue updates
      - Notify relevant agents on cross-agent issues
      - Escalate blocked issues to PM coordination
      - Alert on missed deadlines or targets

  integration_automation:
    github_sync:
      - Automatically link issues to pull requests
      - Update issue status based on PR status
      - Create issues from commit references
      - Track code review completion

    quality_automation:
      - Create testing issues when development complete
      - Trigger quality gate validation automatically
      - Update quality metrics dashboards
      - Escalate quality failures to relevant agents
```

## Monitoring and Reporting

### Performance Metrics
```yaml
linear_metrics:
  agent_performance:
    productivity_metrics:
      - Issues completed per sprint
      - Average time to completion
      - Quality of issue descriptions
      - Coordination effectiveness

    quality_metrics:
      - Issue accuracy and completeness
      - Cross-agent collaboration quality
      - Stakeholder satisfaction scores
      - Process improvement contributions

  system_health:
    integration_metrics:
      - API response times and reliability
      - Webhook delivery success rates
      - Data synchronization accuracy
      - Error rates and resolution times

    workflow_metrics:
      - Issue cycle time by type
      - Bottleneck identification
      - Process efficiency improvements
      - Automation success rates
```

### Reporting Dashboards
```yaml
dashboard_configuration:
  agent_dashboards:
    individual_performance:
      - Personal issue queues and progress
      - Workload distribution and capacity
      - Quality metrics and improvements
      - Coordination effectiveness scores

    team_coordination:
      - Cross-agent collaboration metrics
      - Project progress and milestones
      - Quality gate success rates
      - Stakeholder communication status

  executive_reporting:
    strategic_overview:
      - Quarterly objective progress
      - Resource utilization and efficiency
      - Quality trends and improvements
      - Customer satisfaction metrics

    operational_metrics:
      - System reliability and performance
      - Process automation effectiveness
      - Cost optimization achievements
      - Innovation and improvement initiatives
```

## Integration Patterns

### MCP Protocol Integration
```yaml
mcp_integration:
  primary_operations:
    issue_management:
      - Create issues through MCP when available
      - Update issue status via MCP protocols
      - Retrieve issue data with MCP queries
      - Synchronize with external systems

    data_synchronization:
      - Real-time status updates via MCP
      - Bidirectional data flow with GitHub
      - Context sharing with other tools
      - Performance monitoring integration

  fallback_strategies:
    direct_api_usage:
      - Automatic fallback to REST API
      - Maintain functionality during MCP downtime
      - Monitor MCP availability and performance
      - Seamless transition between protocols
```

### GitHub Integration
```yaml
github_linear_sync:
  bidirectional_sync:
    issue_to_pr_linking:
      - Automatically link Linear issues to pull requests
      - Update Linear status based on PR progress
      - Create Linear issues from GitHub issues
      - Sync labels and milestones

    workflow_coordination:
      - Trigger Linear updates on CI/CD events
      - Create deployment tracking issues
      - Monitor code quality metrics in Linear
      - Coordinate release planning across tools
```

---

*These Linear integration best practices ensure optimal project management coordination across the BMAD Auto autonomous system, enabling efficient tracking, reporting, and collaboration between AI agents and human stakeholders.*