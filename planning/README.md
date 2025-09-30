# <!-- Powered by BMAD™ Core -->
template:
  id: bmad-auto-planning-directory-v2
  name: BMAD Auto Planning Directory Structure
  version: 2.0
  output:
    format: markdown
    filename: planning/README.md
    title: "BMAD Auto Planning Directory"

workflow:
  mode: documentation
  elicitation: structured

sections:
  - id: directory-overview
    title: 📝 Planning Directory Overview
    instruction: |
      **Owner**: John (Product Manager)

      This directory contains all product strategy, requirements, and planning documentation for the BMAD Auto project following BMAD Core template standards.
    sections:
      - id: purpose
        title: Purpose
        instruction: |
          Centralized repository for product strategy, requirements, and planning documentation supporting the BMAD Auto autonomous product orchestration system implementation.

  - id: structure-definition
    title: Directory Structure
    instruction: |
      Organized following BMAD Core standards with clear separation of concerns and standardized documentation formats.
    sections:
      - id: strategy-section
        title: 📁 strategy/ - Product Strategy Documents
        type: structured-list
        items:
          - "product-vision.md: Long-term product vision and strategic goals"
          - "roadmap-YYYY-QX.md: Quarterly roadmaps and milestone tracking"
          - "competitive-positioning.md: Market positioning and differentiation strategy"
          - "repoagent-implementation-roadmap.md: Strategic implementation planning"

      - id: requirements-section
        title: 📁 requirements/ - Product Requirements
        type: structured-list
        items:
          - "bmad-auto-comprehensive-prd.md: Complete PRD following BMAD Core template"
          - "prd-brownfield-research-based.md: Brownfield enhancement specifications"
          - "repoagent-integration-spec.md: Integration requirements and specifications"
          - "mary-openbnb-research-assignment.md: Research-driven requirements"
          - "REQUIREMENTS_TEMPLATE.md: Standard template for new requirements"

      - id: architecture-section
        title: 📁 architecture/ - Technical Architecture
        type: structured-list
        items:
          - "bmad-auto-technical-architecture.md: Complete system architecture following BMAD Core standards"
          - "integration-architecture.md: External service integration design"
          - "data-architecture.md: Data flow and persistence architecture"

      - id: design-section
        title: 📁 design/ - UX/UI Specifications
        type: structured-list
        items:
          - "bmad-orchestration-ux-specification.md: Complete UX design following BMAD Core standards"
          - "interface-design.md: UI component and interaction design"
          - "user-journey-maps.md: User experience flows and touchpoints"

      - id: planning-sessions-section
        title: 📁 planning-sessions/ - Meeting Notes & Decisions
        type: structured-list
        items:
          - "YYYY-MM-DD-planning-session.md: Planning meeting notes and decisions"
          - "2025-01-18-comprehensive-agent-workflow-automation.md: Agent workflow planning"
          - "decision-log.md: Key architectural and strategic decisions"
          - "sprint-planning/: Sprint planning and retrospective documentation"

  - id: template-standards
    title: BMAD Core Template Standards
    instruction: |
      All documents in this directory MUST follow BMAD Core template standards as defined in .bmad-core/templates/
    sections:
      - id: prd-standards
        title: PRD Template Standards
        instruction: |
          **Primary Template**: .bmad-core/templates/brownfield-prd-tmpl.yaml
          **Use Case**: BMAD Auto is a brownfield enhancement to existing BMAD Core system
          **Required Sections**:
          - Intro Project Analysis and Context
          - Requirements (Functional, Non-Functional, Compatibility)
          - UI Enhancement Goals (if applicable)
          - Technical Constraints and Integration Requirements
          - Epic Structure with detailed stories

      - id: architecture-standards
        title: Architecture Template Standards
        instruction: |
          **Primary Template**: .bmad-core/templates/brownfield-architecture-tmpl.yaml
          **Required Sections**:
          - Existing System Analysis
          - Enhancement Architecture Design
          - Integration Strategy
          - Implementation Approach
          - Risk Assessment and Mitigation

      - id: document-headers
        title: Required Document Headers
        type: code-block
        language: yaml
        instruction: |
          All documents must include standardized metadata headers:
        content: |
          ---
          type: [prd|architecture|design|strategy]
          version: X.Y
          created: YYYY-MM-DD
          updated: YYYY-MM-DD
          status: [draft|review|approved|active|archived]
          owners: [john, james, alex, sally, quinn]
          template_source: .bmad-core/templates/[template-name].yaml
          ---

  - id: planning-status
    title: Current Planning Status
    instruction: |
      Track implementation progress through phases with clear status indicators
    sections:
      - id: completed-status
        title: ✅ Completed
        type: checklist
        items:
          - "Phase 1 PM Hub foundation architecture and implementation"
          - "10-agent ecosystem role definitions and responsibilities"
          - "Context Engineering cognitive framework design"
          - "Quality gate pipeline and validation procedures"
          - "Integration principles and .bmad-core preservation rules"

      - id: in-progress-status
        title: 🔄 In Progress
        type: checklist
        items:
          - "Phase 2 expanded agent ecosystem implementation"
          - "Command simulation layer development"
          - "State management system enhancement"
          - "Linear integration workflow refinement"

      - id: upcoming-status
        title: 📋 Upcoming
        type: checklist
        items:
          - "Phase 3 context intelligence with vector embeddings"
          - "Phase 4 human-AI collaboration (AG UI integration)"
          - "Enterprise scalability and optimization features"
          - "Production deployment and monitoring setup"

  - id: workflow-procedures
    title: Document Creation and Review Procedures
    instruction: |
      Standardized workflow for creating, reviewing, and maintaining planning documentation
    sections:
      - id: creation-procedure
        title: Document Creation Procedure
        type: numbered-list
        items:
          - "Select appropriate BMAD Core template from .bmad-core/templates/"
          - "Create document with required metadata header"
          - "Follow template structure and elicitation requirements"
          - "Include proper cross-references and citations"
          - "Submit for stakeholder review workflow"

      - id: review-workflow
        title: Stakeholder Review Workflow
        instruction: |
          All planning documents require multi-stage review:
        type: workflow
        stages:
          - stage: "Technical Review"
            owner: "James (Developer)"
            criteria: "Implementation feasibility and technical accuracy"
          - stage: "Architecture Review"
            owner: "Alex (Architect)"
            criteria: "System integration and design consistency"
          - stage: "Quality Review"
            owner: "Quinn (QA)"
            criteria: "Testability, validation, and quality gates"
          - stage: "UX Review"
            owner: "Sally (UX Designer)"
            criteria: "User experience and interface considerations"
          - stage: "Final Approval"
            owner: "John (PM)"
            criteria: "Strategic alignment and business requirements"

      - id: maintenance-procedure
        title: Document Maintenance
        type: numbered-list
        items:
          - "Update version numbers for material changes"
          - "Maintain cross-reference accuracy across documents"
          - "Archive superseded versions to ../archive/superseded/"
          - "Update this README when adding new document types"

  - id: file-naming-standards
    title: File Naming Standards
    instruction: |
      Consistent naming conventions following BMAD Core standards
    sections:
      - id: naming-patterns
        title: Naming Patterns
        type: definition-list
        items:
          - term: "PRD Documents"
            definition: "prd-[feature-name]-v[X.Y].md"
          - term: "Architecture Documents"
            definition: "architecture-[component-name]-v[X.Y].md"
          - term: "Strategy Documents"
            definition: "[strategy-type]-[timeframe].md"
          - term: "Planning Sessions"
            definition: "YYYY-MM-DD-[session-topic].md"
          - term: "Templates"
            definition: "[DOCUMENT-TYPE]_TEMPLATE.md"

      - id: version-control
        title: Version Control
        instruction: |
          - Semantic versioning: MAJOR.MINOR (e.g., v2.1)
          - MAJOR: Breaking changes or complete rewrites
          - MINOR: Significant additions or modifications
          - Update version in both filename and document header

  - id: integration-references
    title: Integration with BMAD Core
    instruction: |
      Maintain consistency with .bmad-core infrastructure and preserve all existing functionality
    sections:
      - id: core-preservation
        title: .bmad-core Preservation Rules
        type: critical-notice
        content: |
          🚨 CRITICAL: NEVER modify any files in .bmad-core/
          - All enhancements must work with existing .bmad-core infrastructure
          - Use command simulation layer for .bmad-core integration
          - Follow integration principles from docs/01-foundation/integration-principles.md

      - id: template-mapping
        title: Template Source Mapping
        type: mapping-table
        columns: [Document Type, BMAD Core Template, Local Template]
        rows:
          - ["PRD", ".bmad-core/templates/brownfield-prd-tmpl.yaml", "REQUIREMENTS_TEMPLATE.md"]
          - ["Architecture", ".bmad-core/templates/brownfield-architecture-tmpl.yaml", "architecture/ARCHITECTURE_TEMPLATE.md"]
          - ["Enhancement Proposal", ".bmad-core/templates/enhancement-tmpl.yaml", "ENHANCEMENT_PROPOSAL_TEMPLATE.md"]

  - id: archive-procedures
    title: Archive and Lifecycle Management
    instruction: |
      Systematic approach to document lifecycle and historical preservation
    sections:
      - id: archive-triggers
        title: Archive Triggers
        type: checklist
        items:
          - "Document superseded by newer version"
          - "Planning phase completed and moved to implementation"
          - "Strategic direction changed requiring document retirement"
          - "Annual cleanup of outdated planning documents"

      - id: archive-locations
        title: Archive Locations
        type: definition-list
        items:
          - term: "Completed Phases"
            definition: "../archive/YYYY/QX/planning/"
          - term: "Superseded Documents"
            definition: "../archive/superseded/"
          - term: "Historical Versions"
            definition: "../archive/versions/[document-name]/vX.Y/"

changelog:
  - date: "2025-01-18"
    version: "2.0"
    description: "Updated to follow BMAD Core template standards"
    author: "Winston (Architect)"
  - date: "2024-12-01"
    version: "1.0"
    description: "Initial planning directory structure"
    author: "John (PM)"