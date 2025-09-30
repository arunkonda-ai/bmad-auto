# <!-- Powered by BMAD™ Core -->
template:
  id: bmad-auto-brownfield-prd-template-v2
  name: BMAD Auto Brownfield Enhancement PRD Template
  version: 2.0
  output:
    format: markdown
    filename: planning/requirements/[enhancement-name]-prd.md
    title: "{{project_name}} Brownfield Enhancement PRD"
  template_source: .bmad-core/templates/brownfield-prd-tmpl.yaml

workflow:
  mode: interactive
  elicitation: advanced-elicitation

metadata:
  type: prd
  version: 1.0
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  status: [draft|review|approved|active|archived]
  owners: [john, james, alex, sally, quinn]
  template_source: .bmad-core/templates/brownfield-prd-tmpl.yaml

sections:
  - id: intro-analysis
    title: Intro Project Analysis and Context
    instruction: |
      IMPORTANT - SCOPE ASSESSMENT REQUIRED:

      This PRD is for SIGNIFICANT enhancements to existing BMAD Auto project that require comprehensive planning and multiple stories. Before proceeding:

      1. **Assess Enhancement Complexity**: If this is a simple feature addition or bug fix that could be completed in 1-2 focused development sessions, STOP and recommend: "For simpler changes, consider using the brownfield-create-epic or brownfield-create-story task with the Product Owner instead. This full PRD process is designed for substantial enhancements that require architectural planning and multiple coordinated stories."

      2. **Project Context**: Determine if we're working in an IDE with the project already loaded or if the user needs to provide project information. If project files are available, analyze existing documentation in the docs folder. If insufficient documentation exists, recommend running the document-project task first.

      3. **Deep Assessment Requirement**: You MUST thoroughly analyze the existing BMAD Auto project structure, patterns, and constraints before making ANY suggestions. Every recommendation must be grounded in actual project analysis, not assumptions.

      Gather comprehensive information about the existing BMAD Auto project. This section must be completed before proceeding with requirements.

      CRITICAL: Throughout this analysis, explicitly confirm your understanding with the user. For every assumption you make about the existing project, ask: "Based on my analysis, I understand that [assumption]. Is this correct?"

      Do not proceed with any recommendations until the user has validated your understanding of the existing system.
    sections:
      - id: existing-project-overview
        title: Existing BMAD Auto Project Overview
        instruction: Check if document-project analysis was already performed. If yes, reference that output instead of re-analyzing.
        sections:
          - id: analysis-source
            title: Analysis Source
            instruction: |
              Indicate one of the following:
              - Document-project output available at: {{path}}
              - IDE-based fresh analysis
              - User-provided information
          - id: current-state
            title: Current BMAD Auto State
            instruction: |
              - If document-project output exists: Extract summary from "High Level Architecture" and "Technical Summary" sections
              - Otherwise: Brief description of what the BMAD Auto project currently does and its primary purpose
              - Reference: ../docs/01-foundation/system-architecture.md
      - id: documentation-analysis
        title: Available Documentation Analysis
        instruction: |
          If document-project was run:
          - Note: "Document-project analysis available - using existing technical documentation"
          - List key documents created by document-project
          - Skip the missing documentation check below

          Otherwise, check for existing documentation:
        sections:
          - id: available-docs
            title: Available Documentation
            type: checklist
            items:
              - BMAD Auto System Architecture [[LLM: Check ../docs/01-foundation/system-architecture.md]]
              - Agent Framework Documentation [[LLM: Check ../docs/01-foundation/agent-framework.md]]
              - 10-Agent Ecosystem Design [[LLM: Check ../docs/01-foundation/agent-framework.md]]
              - Context Engineering Framework [[LLM: Check ../docs/01-foundation/cognitive-framework.md]]
              - Quality Framework [[LLM: Check ../docs/01-foundation/quality-framework.md]]
              - Integration Principles [[LLM: Check ../docs/01-foundation/integration-principles.md]]
              - Technical Implementation Guides [[LLM: Check ../docs/02-implementation/]]
              - .bmad-core Preservation Rules [[LLM: Critical - check ../docs/01-foundation/integration-principles.md]]
              - Phase Implementation Status [[LLM: Check ../docs/02-implementation/phase-1-pm-hub-foundation.md]]
            instruction: |
              - If document-project was already run: "Using existing project analysis from document-project output."
              - If critical documentation is missing and no document-project: "I recommend running the document-project task first..."
      - id: enhancement-scope
        title: Enhancement Scope Definition
        instruction: Work with user to clearly define what type of enhancement this is. This is critical for scoping and approach.
        sections:
          - id: enhancement-type
            title: Enhancement Type
            type: checklist
            instruction: Determine with user which applies
            items:
              - New Agent Addition to 10-Agent Ecosystem
              - PM Hub Foundation Enhancement
              - Context Engineering Framework Extension
              - Command Simulation Layer Development
              - State Management System Enhancement
              - Integration with External Services (Linear, GitHub, etc.)
              - Quality Gate Pipeline Enhancement
              - Human-AI Collaboration Features (AG UI)
              - Performance/Scalability Improvements
              - "Other: {{other_type}}"
          - id: enhancement-description
            title: Enhancement Description
            instruction: 2-3 sentences describing what the user wants to add or change to BMAD Auto
          - id: impact-assessment
            title: Impact Assessment
            type: checklist
            instruction: Assess the scope of impact on existing BMAD Auto codebase
            items:
              - Minimal Impact (isolated additions within agent ecosystem)
              - Moderate Impact (some existing orchestration changes)
              - Significant Impact (substantial PM Hub or framework changes)
              - Major Impact (architectural changes to core system)
      - id: goals-context
        title: Goals and Background Context
        sections:
          - id: goals
            title: Goals
            type: bullet-list
            instruction: Bullet list of 1-line desired outcomes this BMAD Auto enhancement will deliver if successful
          - id: background
            title: Background Context
            type: paragraphs
            instruction: 1-2 short paragraphs explaining why this enhancement is needed for BMAD Auto, what problem it solves, and how it fits with the existing autonomous product orchestration system
      - id: changelog
        title: Change Log
        type: table
        columns: [Date, Version, Description, Author]

  - id: requirements
    title: Requirements
    instruction: |
      Draft functional and non-functional requirements based on your validated understanding of the existing BMAD Auto project. Before presenting requirements, confirm: "These requirements are based on my understanding of your existing BMAD Auto system. Please review carefully and confirm they align with your project's reality."
    elicit: true
    sections:
      - id: functional
        title: Functional Requirements
        type: numbered-list
        prefix: FR
        instruction: Each Requirement will be a bullet markdown with identifier starting with FR
        examples:
          - "FR1: The enhanced PM Hub will integrate with the new agent coordination service without breaking current workflow orchestration."
      - id: non-functional
        title: Non Functional Requirements
        type: numbered-list
        prefix: NFR
        instruction: Each Requirement will be a bullet markdown with identifier starting with NFR. Include constraints from existing BMAD Auto system
        examples:
          - "NFR1: Enhancement must maintain existing performance characteristics and not exceed current memory usage by more than 20%."
          - "NFR2: All new agents must comply with the 300-line size limit constraint."
      - id: compatibility
        title: Compatibility Requirements
        instruction: Critical for BMAD Auto brownfield - what must remain compatible with existing system
        type: numbered-list
        prefix: CR
        template: "{{requirement}}: {{description}}"
        items:
          - id: cr1
            template: "CR1: {{bmad_core_compatibility}} - NEVER modify .bmad-core/ files"
          - id: cr2
            template: "CR2: {{agent_ecosystem_compatibility}} - Maintain existing 10-agent framework"
          - id: cr3
            template: "CR3: {{pm_hub_compatibility}} - Preserve existing PM coordination functionality"
          - id: cr4
            template: "CR4: {{integration_compatibility}} - Maintain existing Linear/GitHub integrations"
          - id: cr5
            template: "CR5: {{quality_gate_compatibility}} - Preserve existing validation pipeline"

  - id: ui-enhancement-goals
    title: User Interface Enhancement Goals
    condition: Enhancement includes UI changes or AG UI integration
    instruction: For UI changes, capture how they will integrate with existing BMAD Auto interface patterns and AG UI framework
    sections:
      - id: existing-ui-integration
        title: Integration with Existing BMAD Auto UI
        instruction: Describe how new UI elements will fit with existing AG UI patterns, PM Hub interface, and agent coordination views
      - id: modified-screens
        title: Modified/New Screens and Views
        instruction: List only the screens/views that will be modified or added to BMAD Auto system
      - id: ui-consistency
        title: UI Consistency Requirements
        instruction: Specific requirements for maintaining visual and interaction consistency with existing BMAD Auto application and AG UI framework

  - id: technical-constraints
    title: Technical Constraints and Integration Requirements
    instruction: This section replaces separate architecture documentation. Gather detailed technical constraints from existing BMAD Auto project analysis.
    sections:
      - id: existing-tech-stack
        title: Existing BMAD Auto Technology Stack
        instruction: |
          If document-project output available:
          - Extract from "Actual Tech Stack" table in High Level Architecture section
          - Include version numbers and any noted constraints

          Otherwise, document the current BMAD Auto technology stack:
        template: |
          **Backend Framework**: FastAPI + SQLAlchemy + PostgreSQL
          **Orchestration**: LangGraph + YAML workflows
          **AI Framework**: Context Engineering cognitive primitives
          **State Management**: Enhanced persistence with recovery
          **Integration**: MCP protocol + direct API fallbacks
          **Monitoring**: LangSmith + custom observability
          **Agent Architecture**: 10-agent ecosystem with PM Hub coordination
          **External Dependencies**: {{external_dependencies}}
      - id: integration-approach
        title: Integration Approach
        instruction: Define how the enhancement will integrate with existing BMAD Auto architecture
        template: |
          **PM Hub Integration Strategy**: {{pm_hub_integration}}
          **Agent Ecosystem Integration Strategy**: {{agent_integration}}
          **Context Engineering Integration Strategy**: {{context_integration}}
          **State Management Integration Strategy**: {{state_integration}}
          **.bmad-core Preservation Strategy**: {{bmad_core_preservation}}
      - id: code-organization
        title: Code Organization and Standards
        instruction: Based on existing BMAD Auto project analysis, define how new code will fit existing patterns
        template: |
          **File Structure Approach**: {{file_structure}}
          **Agent Size Compliance**: Maximum 300 lines per agent file
          **Naming Conventions**: {{naming_conventions}}
          **Coding Standards**: {{coding_standards}}
          **Documentation Standards**: {{documentation_standards}}
      - id: deployment-operations
        title: Deployment and Operations
        instruction: How the enhancement fits existing BMAD Auto deployment pipeline
        template: |
          **Build Process Integration**: {{build_integration}}
          **Deployment Strategy**: {{deployment_strategy}}
          **Monitoring and Logging**: {{monitoring_logging}}
          **Configuration Management**: {{config_management}}
      - id: risk-assessment
        title: Risk Assessment and Mitigation
        instruction: |
          If document-project output available:
          - Reference "Technical Debt and Known Issues" section
          - Include "Workarounds and Gotchas" that might impact enhancement
          - Note any identified constraints from "Critical Technical Debt"

          Build risk assessment incorporating existing known issues:
        template: |
          **Technical Risks**: {{technical_risks}}
          **Integration Risks**: {{integration_risks}}
          **.bmad-core Preservation Risks**: {{bmad_core_risks}}
          **Agent Ecosystem Risks**: {{agent_ecosystem_risks}}
          **Deployment Risks**: {{deployment_risks}}
          **Mitigation Strategies**: {{mitigation_strategies}}

  - id: epic-structure
    title: Epic and Story Structure
    instruction: |
      For BMAD Auto brownfield projects, favor a single comprehensive epic unless the user is clearly requesting multiple unrelated enhancements. Before presenting the epic structure, confirm: "Based on my analysis of your existing BMAD Auto project, I believe this enhancement should be structured as [single epic/multiple epics] because [rationale based on actual project analysis]. Does this align with your understanding of the work required?"
    elicit: true
    sections:
      - id: epic-approach
        title: Epic Approach
        instruction: Explain the rationale for epic structure - typically single epic for brownfield unless multiple unrelated features
        template: "**Epic Structure Decision**: {{epic_decision}} with rationale"

  - id: epic-details
    title: "Epic 1: {{enhancement_title}}"
    instruction: |
      Comprehensive epic that delivers the BMAD Auto enhancement while maintaining existing functionality

      CRITICAL STORY SEQUENCING FOR BMAD AUTO BROWNFIELD:
      - Stories must ensure existing PM Hub and agent ecosystem functionality remains intact
      - Each story should include verification that existing workflows still work
      - Stories should be sequenced to minimize risk to existing system
      - Include rollback considerations for each story
      - Focus on incremental integration rather than big-bang changes
      - Size stories for AI agent execution in existing BMAD Auto codebase context
      - MANDATORY: Present the complete story sequence and ask: "This story sequence is designed to minimize risk to your existing BMAD Auto system. Does this order make sense given your project's architecture and constraints?"
      - Stories must be logically sequential with clear dependencies identified
      - Each story must deliver value while maintaining system integrity
      - Stories must respect .bmad-core preservation requirements
    template: |
      **Epic Goal**: {{epic_goal}}

      **Integration Requirements**: {{integration_requirements}}
      **.bmad-core Preservation**: {{bmad_core_preservation}}
    sections:
      - id: story
        title: "Story 1.{{story_number}} {{story_title}}"
        repeatable: true
        template: |
          As a {{user_type}},
          I want {{action}},
          so that {{benefit}}.
        sections:
          - id: acceptance-criteria
            title: Acceptance Criteria
            type: numbered-list
            instruction: Define criteria that include both new functionality and existing BMAD Auto system integrity
            item_template: "{{criterion_number}}: {{criteria}}"
          - id: integration-verification
            title: Integration Verification
            instruction: Specific verification steps to ensure existing BMAD Auto functionality remains intact
            type: numbered-list
            prefix: IV
            items:
              - template: "IV1: {{existing_pm_hub_verification}}"
              - template: "IV2: {{agent_ecosystem_verification}}"
              - template: "IV3: {{bmad_core_preservation_verification}}"
              - template: "IV4: {{performance_impact_verification}}"

changelog:
  - date: "2025-01-18"
    version: "2.0"
    description: "Updated to follow BMAD Core brownfield-prd-tmpl.yaml template standards"
    author: "Winston (Architect)"
  - date: "2024-12-01"
    version: "1.0"
    description: "Initial requirements template for BMAD Auto"
    author: "John (PM)"