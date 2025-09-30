# BMAD Auto: Visual Workflow Summary

## **Complete Document Flow: Research → Planning → Development**

```
📊 RESEARCH PHASE
┌─────────────────────────────────────────────────────────────┐
│ INPUT SOURCES                                               │
│ • External research (OpenBMB, Spec Kit, Market data)       │
│ • Mary (Analyst) research assignments                      │
│ • Competitive analysis and technical feasibility           │
│                                                            │
│ DOCUMENT LOCATIONS:                                        │
│ ├── /research/findings/openbnb-repoagent-analysis.md      │
│ ├── /research/findings/github-spec-kit-integration.md     │
│ └── /research/findings/market-research.md                 │
│                                                            │
│ ALEX'S FILE ORGANIZER: Auto-routes to research/findings/  │
└─────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
📋 PLANNING PHASE
┌─────────────────────────────────────────────────────────────┐
│ PM JOHN'S CONSOLIDATION PROCESS                            │
│                                                            │
│ INPUTS:                                                    │
│ ├── Research findings (Mary's analysis)                   │
│ ├── Foundation docs (/docs/01-foundation/)                │
│ ├── Architecture guides (/docs/architecture/)             │
│ └── Best practices (/docs/05-best-practices/)             │
│                                                            │
│ PLANNING OUTPUTS:                                          │
│ ├── /planning/requirements/consolidated-brief.md          │
│ ├── /planning/specifications/feature-spec.md              │
│ └── /planning/strategy/implementation-roadmap.md          │
│                                                            │
│ SPEC KIT INTEGRATION:                                      │
│ • specify plan --research-input --foundation-docs         │
│ • Template-driven specification creation                  │
│ • Agent assignment planning                               │
└─────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
🛠️ DEVELOPMENT PHASE
┌─────────────────────────────────────────────────────────────┐
│ AGENT COORDINATION (John → James, Alex, Quinn, Sally)             │
│                                                            │
│ DEVELOPMENT INPUTS:                                        │
│ ├── /planning/specifications/feature-spec.md              │
│ ├── /docs/01-foundation/system-architecture.md            │
│ ├── /docs/architecture/coding-standards.md                │
│ └── /docs/05-best-practices/claude-code-best-practices.md │
│                                                            │
│ DEVELOPMENT PROCESS:                                       │
│ ├── John: Create story from specification                 │
│ ├── James: Implement following BMAD standards             │
│ ├── Alex: Design integration architecture                 │
│ └── Quinn: Validate quality gates                         │
│                                                            │
│ DEVELOPMENT OUTPUTS:                                       │
│ ├── /docs/stories/feature-story-v1.md                     │
│ ├── /src/services/feature_service.py                      │
│ └── /docs/qa/gates/feature-validation.yml                 │
└─────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
📚 DOCUMENTATION & INTEGRATION
┌─────────────────────────────────────────────────────────────┐
│ AUTOMATED DOCUMENTATION & ORGANIZATION                     │
│                                                            │
│ AUTO-DOCUMENTATION:                                        │
│ ├── RepoAgent: Analyze code and generate docs             │
│ ├── GitHub Actions: Trigger documentation pipeline        │
│ └── Alex's Organizer: Route docs to correct folders       │
│                                                            │
│ FINAL ORGANIZATION:                                        │
│ ├── /docs/02-implementation/feature-guide.md              │
│ ├── /src/services/ (properly organized code)              │
│ └── /docs/qa/gates/ (validation records)                  │
│                                                            │
│ INTEGRATION COMPLETION:                                    │
│ • Unified workflow execution                              │
│ • Linear task tracking updates                            │
│ • PM approval and release coordination                    │
└─────────────────────────────────────────────────────────────┘
```

## **Key Workflow Stages**

### **Stage 1: Research Collection**
```
External Input → Mary Analysis → /research/findings/ → PM Review
```

### **Stage 2: Strategic Planning**
```
Research + Foundation + Best Practices → PM Consolidation →
/planning/requirements/ → Specification Creation → /planning/specifications/
```

### **Stage 3: Spec Kit Development**
```
Specification → GitHub Spec Kit Templates → Agent Assignment →
Development Stories → /docs/stories/
```

### **Stage 4: Agent Implementation**
```
Stories + Standards → James (Dev) + Alex (Arch) + Quinn (QA) →
Implementation + Validation → /src/ + /docs/qa/
```

### **Stage 5: Auto-Documentation**
```
Implementation → RepoAgent Analysis → Documentation Generation →
Alex's Organization → /docs/02-implementation/
```

## **File Movement Flow**

### **Research Phase Movement**
```
External Sources
    ↓ (Mary Analysis)
/research/findings/[topic]-analysis.md
    ↓ (Alex Auto-Organization)
Properly categorized research files
    ↓ (PM Review)
/planning/requirements/[topic]-brief.md
```

### **Planning Phase Movement**
```
/planning/requirements/ + /docs/01-foundation/
    ↓ (PM Strategic Analysis)
/planning/specifications/[feature]-spec.md
    ↓ (Spec Kit Integration)
/planning/strategy/[feature]-roadmap.md
```

### **Development Phase Movement**
```
/planning/specifications/
    ↓ (PM Coordination)
/docs/stories/[feature]-story-v1.md
    ↓ (Agent Implementation)
/src/services/[feature]_service.py
    ↓ (Quality Validation)
/docs/qa/gates/[feature]-validation.yml
```

### **Documentation Phase Movement**
```
/src/services/
    ↓ (RepoAgent Auto-Documentation)
/docs/auto-generated/
    ↓ (Alex's Organization)
/docs/02-implementation/[feature]-guide.md
```

## **PM John's Command Workflow**

### **Daily PM Commands**
```bash
# 1. Review and consolidate research
*research "review Mary's analysis findings"

# 2. Create planning documents
*create-prd  # Uses research as foundation

# 3. Generate specifications
specify plan --research="/research/findings/" --output="/planning/specifications/"

# 4. Coordinate development
*create-story  # Convert specs to development stories
*coordinate-agents "james,alex,quinn"

# 5. Monitor and validate
*validate-progress
*approve-quality-gates

# 6. Document and release
*doc-out
specify release --complete=true
```

## **Developer (James) Workflow Integration**

### **Spec Kit Development Process**
```bash
# 1. Load development context
*develop-story  # Loads story + standards + best practices

# 2. Follow Spec Kit implementation
specify implement --story="/docs/stories/feature-story-v1.md" --agent=james

# 3. Execute systematic development
implement_requirements()
design_technical_approach()
code_following_bmad_standards()
create_tests_and_validation()
update_documentation()

# 4. Coordinate with PM
specify validate --implementation="/src/" --pm-review=john
```

## **Complete Integration Benefits**

### **Systematic Document Flow**
- **No Lost Information**: Every research finding feeds into planning
- **Traceability**: Clear path from research to implementation
- **Quality Assurance**: Multiple validation points throughout
- **Automated Organization**: Files automatically go to correct locations

### **PM Coordination Excellence**
- **Strategic Oversight**: John coordinates all phases
- **Agent Coordination**: Systematic assignment and tracking
- **Quality Gates**: Built-in validation at every step
- **Tool Integration**: Seamless Claude/GitHub/Linear coordination

### **Development Efficiency**
- **Spec-Driven**: Clear specifications before implementation
- **Standard Compliance**: BMAD standards enforced throughout
- **Auto-Documentation**: Documentation generated automatically
- **File Organization**: Everything properly organized by Alex's system

**Result**: Complete visibility and control from research idea to production implementation with full documentation and quality validation.