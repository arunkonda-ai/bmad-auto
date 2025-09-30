# <!-- Powered by BMAD™ Core -->
template:
  id: bmad-auto-enhancement-proposal-v2
  name: BMAD Auto Enhancement Proposal Template
  version: 2.0
  output:
    format: markdown
    filename: planning/proposals/[enhancement-name]-proposal.md
    title: "{{enhancement_name}} Enhancement Proposal"
  template_source: .bmad-core/templates/brownfield-prd-tmpl.yaml (adapted)

workflow:
  mode: interactive
  elicitation: structured

metadata:
  type: enhancement-proposal
  version: 1.0
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  status: [draft|review|approved|rejected|implemented]
  owners: [agent-name, john]
  reviewers: [john, human, alex]
  template_source: .bmad-core/templates/brownfield-prd-tmpl.yaml (adapted)

sections:
  - id: proposal-overview
    title: Enhancement Proposal Overview
    instruction: |
      High-level summary of the proposed enhancement following BMAD Core standards
    sections:
      - id: proposal-summary
        title: Proposal Summary
        type: definition-list
        items:
          - term: "Enhancement Type"
            definition: "[Agent Addition|PM Hub Enhancement|Context Framework|Integration|Process|Technical|Quality]"
          - term: "Priority"
            definition: "[High|Medium|Low]"
          - term: "Effort Estimate"
            definition: "[Small (1-2 weeks)|Medium (3-4 weeks)|Large (1-2 months)|XL (2+ months)]"
          - term: "Proposed Timeline"
            definition: "[Specific timeframe]"
          - term: "BMAD Auto Component"
            definition: "[Specify which part of BMAD Auto system this affects]"

  - id: research-foundation
    title: Research Foundation and Trigger
    instruction: |
      All enhancement proposals must be grounded in research findings from Mary or documented user needs
    sections:
      - id: source-research
        title: Source Research
        instruction: |
          **Primary Research Document**: [Research Title](../research/findings/research-doc.md)
          - **Key Findings**: Specific insights that triggered this proposal
          - **Research Date**: When the research was completed
          - **Research Author**: Who conducted the research (typically Mary)
          - **Research Type**: [Market Analysis|Technical Research|User Study|Competitive Analysis]
      - id: discovered-opportunity
        title: Discovered Opportunity
        type: structured-list
        items:
          - "User Need Identified: Specific user problem or opportunity within BMAD Auto"
          - "BMAD Auto Gap: Specific capability gap in current system"
          - "Technical Possibility: New technical capability or improvement opportunity"
          - "Process Improvement: Workflow or automation enhancement opportunity"
          - "Agent Ecosystem Enhancement: Improvement to 10-agent coordination"

  - id: current-state-analysis
    title: Current BMAD Auto State Analysis
    instruction: |
      Comprehensive analysis of existing BMAD Auto system state and limitations
    sections:
      - id: existing-implementation
        title: Existing BMAD Auto Implementation
        instruction: |
          **Current Documentation**: [Current State](../docs/01-foundation/system-architecture.md)
          - **What exists today**: Current BMAD Auto functionality and capabilities
          - **Agent Ecosystem State**: Current 10-agent system status
          - **PM Hub Capabilities**: Current PM coordination functionality
          - **Context Engineering State**: Current cognitive framework status
          - **Limitations**: What doesn't work well or is missing
          - **User Pain Points**: Specific problems users experience with current system
      - id: gap-analysis
        title: Gap Analysis
        type: structured-list
        items:
          - "Functional Gaps: Missing capabilities compared to user needs"
          - "Agent Coordination Gaps: Limitations in current 10-agent ecosystem"
          - "PM Hub Gaps: Missing PM coordination capabilities"
          - "Context Engineering Gaps: Cognitive framework limitations"
          - "Integration Gaps: External service integration limitations"
          - "Quality Gaps: Performance, security, or usability issues"
          - ".bmad-core Integration Gaps: Command simulation limitations"

  - id: bmad-auto-integration-analysis
    title: BMAD Auto Integration Analysis
    instruction: |
      Specific analysis of how this enhancement integrates with existing BMAD Auto components
    sections:
      - id: affected-components
        title: Affected BMAD Auto Components
        type: component-analysis
        components:
          - component: "PM Hub Foundation"
            document: "../docs/02-implementation/phase-1-pm-hub-foundation.md"
            impact_level: "[None|Minor|Moderate|Major]"
            integration_complexity: "[Simple|Moderate|Complex]"
          - component: "10-Agent Ecosystem"
            document: "../docs/01-foundation/agent-framework.md"
            impact_level: "[None|Minor|Moderate|Major]"
            integration_complexity: "[Simple|Moderate|Complex]"
          - component: "Context Engineering Framework"
            document: "../docs/01-foundation/cognitive-framework.md"
            impact_level: "[None|Minor|Moderate|Major]"
            integration_complexity: "[Simple|Moderate|Complex]"
          - component: "Quality Framework"
            document: "../docs/01-foundation/quality-framework.md"
            impact_level: "[None|Minor|Moderate|Major]"
            integration_complexity: "[Simple|Moderate|Complex]"
          - component: ".bmad-core Preservation"
            document: "../docs/01-foundation/integration-principles.md"
            impact_level: "[None|Minor|Moderate|Major]"
            integration_complexity: "[Simple|Moderate|Complex]"
      - id: documentation-updates
        title: Documentation Updates Required
        type: document-list
        documents:
          - document: "System Architecture"
            path: "../docs/01-foundation/system-architecture.md"
            sections_affected: "{{sections}}"
          - document: "Agent Framework"
            path: "../docs/01-foundation/agent-framework.md"
            sections_affected: "{{sections}}"
          - document: "Implementation Guides"
            path: "../docs/02-implementation/"
            sections_affected: "{{sections}}"

  - id: conflicts-dependencies
    title: Conflicts and Dependencies
    instruction: |
      Critical analysis of potential conflicts with existing BMAD Auto system and dependencies
    sections:
      - id: bmad-auto-conflicts
        title: BMAD Auto System Conflicts
        type: conflict-analysis
        template: |
          #### Conflict {{conflict_number}}: {{conflict_description}}
          **Existing BMAD Auto Component**: [Document](link) - Current functionality description
          **Proposed Change**: How this enhancement conflicts or changes the existing functionality
          **Impact on .bmad-core**: Any risk to .bmad-core preservation requirements
          **Resolution Strategy**: Proposed approach to resolve the conflict while maintaining system integrity
      - id: dependencies
        title: Dependencies
        type: dependency-analysis
        categories:
          - category: "BMAD Auto Technical Dependencies"
            items:
              - "PM Hub Foundation dependencies"
              - "Agent ecosystem coordination dependencies"
              - "Context Engineering framework dependencies"
              - ".bmad-core integration dependencies"
          - category: "External Service Dependencies"
            items:
              - "Linear integration dependencies"
              - "GitHub integration dependencies"
              - "MCP protocol dependencies"
          - category: "Implementation Dependencies"
            items:
              - "Agent training or knowledge transfer needed"
              - "Tool changes or new tool requirements"
              - "Workflow updates required for implementation"

  - id: proposed-solution
    title: Proposed BMAD Auto Enhancement Solution
    instruction: |
      Detailed solution description that maintains BMAD Auto system integrity and follows established patterns
    sections:
      - id: enhancement-description
        title: Enhancement Description
        instruction: |
          **Detailed Solution**: Comprehensive description of the proposed BMAD Auto enhancement
          - **User Value**: Specific benefits BMAD Auto users will experience
          - **System Value**: Benefits to BMAD Auto autonomous orchestration capabilities
          - **Agent Ecosystem Value**: Improvements to 10-agent coordination and effectiveness
          - **Technical Approach**: High-level technical implementation strategy that preserves .bmad-core
      - id: implementation-strategy
        title: Implementation Strategy
        type: phased-approach
        phases:
          - phase: "Phase 1: Foundation and Analysis"
            scope: "{{foundation_scope}}"
            timeline: "{{foundation_timeline}}"
            agent_assignments: "{{foundation_agents}}"
            success_criteria: "{{foundation_success}}"
            bmad_core_preservation: "{{foundation_preservation}}"
          - phase: "Phase 2: Core Enhancement Implementation"
            scope: "{{core_scope}}"
            timeline: "{{core_timeline}}"
            agent_assignments: "{{core_agents}}"
            success_criteria: "{{core_success}}"
            bmad_core_preservation: "{{core_preservation}}"
          - phase: "Phase 3: Integration and Optimization"
            scope: "{{optimization_scope}}"
            timeline: "{{optimization_timeline}}"
            agent_assignments: "{{optimization_agents}}"
            success_criteria: "{{optimization_success}}"
            bmad_core_preservation: "{{optimization_preservation}}"

  - id: impact-assessment
    title: BMAD Auto Impact Assessment
    instruction: |
      Comprehensive assessment of impacts on existing BMAD Auto system and capabilities
    sections:
      - id: positive-impacts
        title: Positive Impacts on BMAD Auto
        type: impact-list
        categories:
          - category: "PM Hub Coordination"
            impacts: "{{pm_hub_improvements}}"
          - category: "Agent Ecosystem Effectiveness"
            impacts: "{{agent_ecosystem_improvements}}"
          - category: "Context Engineering Capabilities"
            impacts: "{{context_engineering_improvements}}"
          - category: "Quality and Reliability"
            impacts: "{{quality_improvements}}"
          - category: "External Integration Capabilities"
            impacts: "{{integration_improvements}}"
      - id: risk-assessment
        title: Risk Assessment
        type: risk-matrix
        risk_categories:
          - category: "BMAD Auto System Risks"
            risks:
              - risk: "PM Hub disruption or coordination failures"
                probability: "[High|Medium|Low]"
                impact: "[High|Medium|Low]"
                mitigation: "{{mitigation_strategy}}"
              - risk: "Agent ecosystem instability or conflicts"
                probability: "[High|Medium|Low]"
                impact: "[High|Medium|Low]"
                mitigation: "{{mitigation_strategy}}"
              - risk: ".bmad-core preservation violation"
                probability: "[High|Medium|Low]"
                impact: "[High|Medium|Low]"
                mitigation: "{{mitigation_strategy}}"

  - id: resource-requirements
    title: Resource Requirements and Agent Coordination
    instruction: |
      Detailed resource planning following BMAD Auto 10-agent ecosystem coordination principles
    sections:
      - id: agent-assignments
        title: BMAD Auto Agent Assignments
        type: agent-coordination
        primary_agents:
          - agent: "John (PM)"
            role: "Project coordination and stakeholder management"
            responsibilities: "{{john_responsibilities}}"
          - agent: "{{primary_agent}}"
            role: "{{primary_role}}"
            responsibilities: "{{primary_responsibilities}}"
        supporting_agents:
          - agent: "Mary (Analyst)"
            role: "Additional research, validation, and market intelligence"
            responsibilities: "{{mary_responsibilities}}"
          - agent: "Alex (Architect)"
            role: "Technical architecture review and system integration guidance"
            responsibilities: "{{alex_responsibilities}}"
          - agent: "James (Developer)"
            role: "Technical implementation and development support"
            responsibilities: "{{james_responsibilities}}"
          - agent: "Sally (UX)"
            role: "User experience design and AG UI integration"
            responsibilities: "{{sally_responsibilities}}"
          - agent: "Quinn (QA)"
            role: "Quality validation, testing strategy, and quality gate compliance"
            responsibilities: "{{quinn_responsibilities}}"
      - id: timeline-effort
        title: Timeline and Effort Estimation
        type: effort-breakdown
        estimation:
          total_effort: "{{total_story_points}}"
          timeline: "{{start_to_completion}}"
          critical_path: "{{critical_dependencies}}"
          milestone_schedule: "{{key_delivery_dates}}"

  - id: approval-workflow
    title: BMAD Auto Approval Workflow
    instruction: |
      Approval process following BMAD Auto quality gates and stakeholder review requirements
    sections:
      - id: pm-review
        title: John (PM) Review Requirements
        type: checklist
        items:
          - "Business value clearly articulated and aligned with BMAD Auto strategy"
          - "Resource requirements reasonable within 10-agent ecosystem capacity"
          - "Timeline realistic given current BMAD Auto development phase"
          - "Integration impact assessed and .bmad-core preservation confirmed"
          - "Risk mitigation planned and acceptable"
          - "Agent coordination plan feasible and clear"
      - id: human-approval
        title: Human Approval Requirements
        type: checklist
        items:
          - "Strategic alignment with BMAD Auto product vision confirmed"
          - "Resource allocation approved within current capacity"
          - "Risk assessment acceptable for current development phase"
          - "ROI justification validated for enhancement investment"
          - "Implementation plan approved and integration strategy sound"
      - id: brainstorming-session
        title: Enhancement Brainstorming Session
        type: session-plan
        details:
          scheduled_date: "[To be determined by John (PM)]"
          participants: "John (PM), Human, relevant BMAD Auto agents"
          agenda:
            - "Review enhancement proposal and research foundation"
            - "Discuss BMAD Auto system integration strategy"
            - "Validate resource requirements and agent assignments"
            - "Confirm timeline and milestone alignment with current phases"
            - "Address risks and concerns, especially .bmad-core preservation"
            - "Make go/no-go decision and next steps"

  - id: next-steps
    title: Next Steps and Implementation Path
    instruction: |
      Clear action plan for approved or rejected enhancement proposals
    sections:
      - id: if-approved
        title: If Enhancement Approved
        type: action-plan
        steps:
          - step: "Documentation Updates"
            description: "Update specific BMAD Auto documents with enhancement details"
            documents: "{{documents_to_update}}"
          - step: "Planning Integration"
            description: "Integrate enhancement into current BMAD Auto development roadmap"
            integration_method: "{{integration_approach}}"
          - step: "Agent Coordination"
            description: "Finalize agent assignments and coordination protocols"
            coordination_plan: "{{coordination_details}}"
          - step: "Implementation Kickoff"
            description: "Begin enhancement implementation following BMAD Auto quality gates"
            kickoff_actions: "{{kickoff_steps}}"
      - id: if-rejected
        title: If Enhancement Rejected
        type: rejection-process
        steps:
          - step: "Documentation Archive"
            description: "Archive proposal with clear rejection reasons and lessons learned"
          - step: "Alternative Analysis"
            description: "Consider alternative approaches or modified scope if applicable"
          - step: "Future Consideration"
            description: "Document conditions under which proposal might be reconsidered"

  - id: related-documents
    title: Related BMAD Auto Documents
    instruction: |
      Comprehensive linking to relevant BMAD Auto documentation following established citation standards
    sections:
      - id: source-materials
        title: Source Materials
        type: document-list
        documents:
          - "[Triggering Research](../research/findings/trigger-research.md)"
          - "[BMAD Auto System Architecture](../docs/01-foundation/system-architecture.md)"
          - "[Current Implementation Status](../docs/02-implementation/)"
      - id: integration-targets
        title: Integration Target Documents
        type: document-list
        documents:
          - "[Comprehensive PRD](../planning/requirements/bmad-auto-comprehensive-prd.md)"
          - "[Technical Architecture](../planning/architecture/bmad-auto-technical-architecture.md)"
          - "[Agent Framework](../docs/01-foundation/agent-framework.md)"
          - "[Quality Framework](../docs/01-foundation/quality-framework.md)"

changelog:
  - date: "2025-01-18"
    version: "2.0"
    description: "Updated to follow BMAD Core template standards with BMAD Auto specific sections"
    author: "Winston (Architect)"
  - date: "2024-12-01"
    version: "1.0"
    description: "Initial enhancement proposal template"
    author: "John (PM)"