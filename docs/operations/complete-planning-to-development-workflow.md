# Complete Planning to Development Workflow - BMAD Auto

**PM Orchestration**: John (Product Manager)
**Framework**: GitHub Spec Kit + BMAD Auto + Alex's File Organization
**Date**: 2025-09-22

## **Overview: Document-Driven Development Flow**

BMAD Auto follows a systematic document-driven development approach where every feature flows through organized phases from research to implementation.

## **1. Document Sources for Planning**

### **Primary Planning Inputs**

#### **A. Research Findings** (`/research/findings/`)
- **Market Research**: `2024-12-01-youtube-creator-market-research.md`
- **Technical Analysis**: `openbnb-repoagent-analysis.md`, `github-spec-kit-integration-analysis.md`
- **Competitive Analysis**: `competitive-analysis-youtube-creator-tools.md`
- **Scaling Analysis**: `2024-12-01-rapid-scaling-analysis.md`

#### **B. Foundation Documentation** (`/docs/01-foundation/`)
- **System Architecture**: `system-architecture.md`
- **Agent Framework**: `agent-framework.md`
- **Cognitive Framework**: `cognitive-framework.md`
- **Quality Framework**: `quality-framework.md`
- **Integration Principles**: `integration-principles.md`

#### **C. Implementation Guides** (`/docs/02-implementation/`)
- **Agent Development**: `agent-development.md`
- **State Management**: `state-management.md`
- **Workflow Orchestration**: `workflow-orchestration.md`
- **Integration Implementation**: `integration-implementation.md`
- **Phase 1 Foundation**: `phase-1-pm-hub-foundation.md`

#### **D. Best Practices** (`/docs/05-best-practices/`)
- **Claude Code**: `claude-code-best-practices.md`
- **GitHub Integration**: `github-integration-best-practices.md`
- **Linear Integration**: `linear-integration-best-practices.md`
- **Context Engineering**: `context-engineering-best-practices.md`

### **Secondary Planning Inputs**

#### **E. Architecture Documentation** (`/docs/architecture/`)
- **Tech Stack**: `tech-stack.md`
- **Coding Standards**: `coding-standards.md`
- **Source Tree**: `source-tree.md`
- **Automated Systems**: `automated-systems/recommendation-routing-design.md`

#### **F. Operational Guides** (`/docs/03-operations/`)
- **Deployment**: `deployment-guide.md`
- **Monitoring**: `monitoring-observability.md`
- **Tool Integration**: `unified-tool-integration-workflow.md`

## **2. Planning Workflow Process**

### **Step 1: Research Analysis & Consolidation**

#### **PM John's Research Review Process**
```bash
# 1. Review all research findings
cd /Users/apple/ai-projects/Omcaro/.bmad-auto/research/findings/

# 2. Identify key insights and patterns
research_insights = analyze_research_documents([
    "openbnb-repoagent-analysis.md",
    "github-spec-kit-integration-analysis.md",
    "youtube-creator-market-research.md"
])

# 3. Create consolidated planning brief
create_planning_brief(research_insights)
```

#### **Research Consolidation Output**
- **File**: `/planning/requirements/consolidated-research-brief.md`
- **Content**: Key insights, technical feasibility, market opportunities
- **Next Step**: Strategic planning document creation

### **Step 2: Strategic Planning Document Creation**

#### **Planning Document Generation**
```yaml
# Planning template structure
planning_document:
  source_research:
    - research/findings/openbnb-repoagent-analysis.md
    - research/findings/github-spec-kit-integration-analysis.md
  foundation_reference:
    - docs/01-foundation/system-architecture.md
    - docs/01-foundation/agent-framework.md
  implementation_guide:
    - docs/02-implementation/agent-development.md
  best_practices:
    - docs/05-best-practices/claude-code-best-practices.md
```

#### **PM Planning Process**
1. **Load Research**: Review Mary's analysis reports
2. **Reference Foundation**: Use system architecture and frameworks
3. **Apply Best Practices**: Follow Claude and GitHub integration standards
4. **Create Spec**: Generate GitHub Spec Kit specification
5. **Define Phases**: Break into development phases

### **Step 3: Spec Kit Integration Planning**

#### **GitHub Spec Kit Specification Creation**
```bash
# Using GitHub Spec Kit methodology
specify init bmad-auto-feature \
  --template=agent-development \
  --pm-coordination=john \
  --agents="james,alex,quinn"

# Generate specification document
specify plan \
  --input-docs="research/findings/*.md" \
  --foundation-docs="docs/01-foundation/*.md" \
  --output="planning/specifications/feature-spec.md"
```

#### **Specification Document Structure**
```markdown
# Feature Specification: [Feature Name]

## Source Documents
- Research: [List research findings used]
- Foundation: [List foundation docs referenced]
- Implementation: [List implementation guides]
- Best Practices: [List practices applied]

## Requirements
- Functional requirements from research
- Technical requirements from architecture
- Quality requirements from best practices

## Implementation Plan
- Agent assignments based on capabilities
- Development phases with dependencies
- Quality gates and validation criteria
```

## **3. File Organization Flow Through Phases**

### **Document Flow Process**

#### **Research Phase Flow**
```
External Research → Mary (Analyst) →
/research/findings/[analysis].md →
File Organizer (Alex's System) →
PM Review (John) →
/planning/requirements/[consolidated-brief].md
```

#### **Planning Phase Flow**
```
/research/findings/ + /docs/01-foundation/ →
PM Analysis (John) →
GitHub Spec Kit Integration →
/planning/specifications/[feature-spec].md →
Agent Assignment Planning →
/planning/strategy/[implementation-roadmap].md
```

#### **Development Phase Flow**
```
/planning/specifications/ →
PM Coordination (John) →
Agent Assignment (James, Alex, Quinn) →
/src/[implementation]/ + /docs/stories/[story].md →
Quality Gates (Quinn) →
/docs/qa/gates/[validation].yml
```

### **Alex's File Organization Integration**

#### **Automatic Document Routing**
```python
# File organization rules for planning workflow
PLANNING_ROUTING_RULES = {
    "research_analysis": "/research/findings/",
    "planning_briefs": "/planning/requirements/",
    "specifications": "/planning/specifications/",
    "implementation_roadmaps": "/planning/strategy/",
    "development_stories": "/docs/stories/",
    "quality_validations": "/docs/qa/gates/",
    "agent_assignments": "/config/agents/assignments/"
}
```

#### **Document Lifecycle Tracking**
```json
{
  "document_flow": {
    "research_input": "research/findings/openbnb-repoagent-analysis.md",
    "planning_output": "planning/requirements/repoagent-integration-brief.md",
    "specification": "planning/specifications/repoagent-integration-spec.md",
    "implementation": "docs/stories/repoagent-integration-story.md",
    "validation": "docs/qa/gates/repoagent-integration-validation.yml"
  }
}
```

## **4. Complete Development Workflow**

### **Phase 1: Research to Planning**

#### **Step 1: Research Collection**
```bash
# Mary completes research
research_output = mary.analyze([
    "OpenBMB/RepoAgent capabilities",
    "GitHub Spec Kit integration",
    "Technical feasibility assessment"
])

# File organization system processes
alex.organize_file(research_output, destination="/research/findings/")
```

#### **Step 2: Planning Brief Creation**
```bash
# John (PM) creates planning brief
planning_brief = john.create_planning_brief(
    research_inputs=[
        "/research/findings/openbnb-repoagent-analysis.md",
        "/research/findings/github-spec-kit-integration-analysis.md"
    ],
    foundation_docs=[
        "/docs/01-foundation/system-architecture.md",
        "/docs/01-foundation/agent-framework.md"
    ]
)

# Auto-organize planning brief
alex.organize_file(planning_brief, destination="/planning/requirements/")
```

### **Phase 2: Specification Creation**

#### **Step 3: GitHub Spec Kit Integration**
```bash
# Generate specification using Spec Kit
specify create \
  --name="repoagent-integration" \
  --input-research="/planning/requirements/repoagent-integration-brief.md" \
  --template="bmad-auto-feature" \
  --pm-coordination="john"

# Output: /planning/specifications/repoagent-integration-spec.md
```

#### **Step 4: Implementation Roadmap**
```yaml
# Implementation roadmap creation
implementation_roadmap:
  phases:
    - phase_1: "Core RepoAgent integration"
      agents: ["james", "alex"]
      deliverables: ["integration_service", "configuration"]

    - phase_2: "Workflow automation"
      agents: ["james", "quinn"]
      deliverables: ["automated_pipeline", "quality_gates"]

    - phase_3: "File organization integration"
      agents: ["alex", "john"]
      deliverables: ["unified_workflow", "documentation"]

# Output: /planning/strategy/repoagent-implementation-roadmap.md
```

### **Phase 3: Development Execution**

#### **Step 5: PM Coordination & Agent Assignment**
```bash
# John coordinates development
john.coordinate_development(
    specification="/planning/specifications/repoagent-integration-spec.md",
    roadmap="/planning/strategy/repoagent-implementation-roadmap.md",
    agents=["james", "alex", "quinn"]
)

# Create development story
story = john.create_story(
    specification=repoagent_spec,
    assigned_agents=["james", "alex"],
    quality_criteria=quinn.quality_requirements
)

# Output: /docs/stories/repoagent-integration-story-v1.md
```

#### **Step 6: Agent Development Process**
```bash
# James (Developer) implements
james.develop_story(
    story="/docs/stories/repoagent-integration-story-v1.md",
    architecture_reference="/docs/01-foundation/system-architecture.md",
    coding_standards="/docs/architecture/coding-standards.md"
)

# Alex (Architect) designs integration
alex.design_integration(
    specification="/planning/specifications/repoagent-integration-spec.md",
    existing_architecture="/src/services/unified_integration_service.py"
)

# Implementation output: /src/services/repoagent_integration_service.py
```

#### **Step 7: Quality Validation**
```bash
# Quinn (QA) validates implementation
quinn.validate_implementation(
    story="/docs/stories/repoagent-integration-story-v1.md",
    implementation="/src/services/repoagent_integration_service.py",
    quality_criteria="/planning/specifications/repoagent-integration-spec.md"
)

# Validation output: /docs/qa/gates/repoagent-integration-validation.yml
```

### **Phase 4: Integration & Documentation**

#### **Step 8: Automated Documentation**
```bash
# RepoAgent generates documentation
repoagent analyze --target="/src/services/repoagent_integration_service.py"
repoagent generate --output="/docs/auto-generated/"

# Alex's system organizes documentation
alex.organize_documentation("/docs/auto-generated/", "/docs/02-implementation/")
```

#### **Step 9: Final Integration**
```bash
# Unified integration service coordinates
unified_service.execute_workflow(
    workflow="spec_driven_development",
    context={
        "specification": "/planning/specifications/repoagent-integration-spec.md",
        "implementation": "/src/services/repoagent_integration_service.py",
        "validation": "/docs/qa/gates/repoagent-integration-validation.yml"
    }
)
```

## **5. Spec Kit Development Workflow Integration**

### **Spec Kit Commands in BMAD Auto**

#### **Project Initialization**
```bash
# Initialize new feature development
cd /Users/apple/ai-projects/Omcaro/.bmad-auto
specify init feature-name \
  --template=bmad-auto-feature \
  --pm=john \
  --agents="james,alex,quinn"
```

#### **Specification Creation**
```bash
# Create feature specification
specify plan \
  --feature=feature-name \
  --research-input="/research/findings/" \
  --foundation-docs="/docs/01-foundation/" \
  --output="/planning/specifications/"
```

#### **Development Coordination**
```bash
# Coordinate development with agents
specify coordinate \
  --specification="/planning/specifications/feature-spec.md" \
  --agents="james,alex,quinn" \
  --pm-oversight=john \
  --quality-gates=enabled
```

#### **Implementation Tracking**
```bash
# Track implementation progress
specify track \
  --feature=feature-name \
  --agents-status=check \
  --quality-gates=validate \
  --pm-review=required
```

### **Developer (James) Workflow with Spec Kit**

#### **Story Implementation Process**
```bash
# 1. Load development context
james.load_context([
    "/docs/stories/feature-story-v1.md",
    "/docs/architecture/coding-standards.md",
    "/docs/05-best-practices/claude-code-best-practices.md"
])

# 2. Follow Spec Kit development process
specify implement \
  --story="/docs/stories/feature-story-v1.md" \
  --agent=james \
  --compliance=bmad-auto

# 3. Generate implementation
james.implement([
    "analyze requirements",
    "design technical approach",
    "implement code following standards",
    "create tests and validation",
    "update documentation"
])

# 4. Validate with PM coordination
specify validate \
  --implementation="/src/services/new_service.py" \
  --pm-review=john \
  --quality-check=quinn
```

## **6. Complete Workflow Example: RepoAgent Integration**

### **End-to-End Document Flow**

#### **Phase 1: Research to Planning**
```
Input: External research on RepoAgent
↓
Mary: /research/findings/openbnb-repoagent-analysis.md
↓
Alex: Auto-organized to research findings
↓
John: /planning/requirements/repoagent-integration-brief.md
↓
Alex: Auto-organized to planning requirements
```

#### **Phase 2: Specification Creation**
```
Input: /planning/requirements/repoagent-integration-brief.md
       /docs/01-foundation/system-architecture.md
↓
Spec Kit: specify plan --input=brief --foundation=architecture
↓
Output: /planning/specifications/repoagent-integration-spec.md
↓
Alex: Auto-organized to planning specifications
```

#### **Phase 3: Development**
```
Input: /planning/specifications/repoagent-integration-spec.md
↓
John: PM coordination and agent assignment
↓
James: Implementation following spec and standards
↓
Output: /src/services/repoagent_integration_service.py
       /docs/stories/repoagent-integration-story-v1.md
↓
Alex: Auto-organized to appropriate folders
```

#### **Phase 4: Quality & Integration**
```
Input: Implementation + Story + Specification
↓
Quinn: Quality validation and testing
↓
Output: /docs/qa/gates/repoagent-integration-validation.yml
↓
RepoAgent: Auto-documentation generation
↓
Final: /docs/02-implementation/repoagent-integration-guide.md
```

## **7. PM Workflow Commands**

### **John's Daily Workflow**
```bash
# 1. Review research and plan features
*research "repoagent integration opportunities"
*create-prd  # Uses research findings as input

# 2. Create specifications using Spec Kit
specify plan --research-input="/research/findings/" --output="/planning/specifications/"

# 3. Coordinate agent development
*create-story  # Converts specifications to agent stories
*coordinate-agents "james,alex,quinn"

# 4. Monitor and validate progress
*validate-progress
*approve-quality-gates

# 5. Document and organize results
*doc-out  # Finalize documentation
specify release --feature-complete=true
```

### **Integration Points Summary**

**Document Sources → Planning → Spec Kit → Development → Organization**

This workflow ensures every feature is:
1. **Research-backed** (Mary's analysis)
2. **Foundation-aligned** (Architecture docs)
3. **Best-practice compliant** (Claude standards)
4. **Systematically developed** (Spec Kit methodology)
5. **Quality-validated** (Quinn's gates)
6. **Properly organized** (Alex's system)
7. **PM-coordinated** (John's oversight)

The complete system creates a seamless flow from research documents through organized development to validated implementation.