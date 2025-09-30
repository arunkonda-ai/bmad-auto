# 📁 BMAD Auto Project Structure & File Management

## Overview
This document defines the comprehensive folder structure for BMAD Auto project lifecycle management, from initial research through production deployment and archival.

## Core Principles

1. **Separation of Concerns**: Active work vs. archived materials
2. **Agent Ownership**: Clear responsibility for document types
3. **Lifecycle Management**: Research → Planning → Development → Deployment → Archive
4. **Version Control**: Track evolution of documents and decisions
5. **Easy Access**: Quick location of current vs. historical information

## Root Structure

```
.bmad-auto/
├── 🏗️ src/                          # Core application code
├── 📋 docs/                         # Living documentation
├── 🔬 research/                     # Active research & analysis
├── 📝 planning/                     # Product strategy & requirements
├── 🚀 deployment/                   # Deployment & operational files
├── 📦 archive/                      # Completed/superseded materials
├── 🧪 testing/                      # Test files & validation
└── 📊 reports/                      # Generated reports & metrics
```

## Detailed Structure

### 📋 `docs/` - Living Documentation
Current, active documentation that drives development:

```
docs/
├── architecture/                    # System architecture docs
│   ├── system-overview.md
│   ├── agent-specifications.md
│   └── integration-patterns.md
├── api/                            # API documentation
│   ├── workflow-endpoints.md
│   ├── agent-endpoints.md
│   └── api-changelog.md
├── operations/                     # Operational guides
│   ├── deployment-guide.md
│   ├── monitoring-setup.md
│   └── troubleshooting.md
└── PROJECT_STRUCTURE.md            # This file
```

### 🔬 `research/` - Active Research & Analysis
Mary's domain for market research, competitive analysis, and ongoing investigations:

```
research/
├── active/                         # Current research projects
│   ├── market-analysis/
│   ├── competitive-intelligence/
│   └── user-research/
├── findings/                       # Research conclusions
│   ├── YYYY-MM-DD-research-title.md
│   └── research-summary.md
└── sources/                        # External materials & references
    ├── competitor-docs/
    ├── market-reports/
    └── reference-materials/
```

### 📝 `planning/` - Product Strategy & Requirements
John's domain for product strategy, PRDs, and planning documents:

```
planning/
├── strategy/                       # Product strategy documents
│   ├── product-vision.md

│   ├── roadmap-YYYY-QX.md
│   └── competitive-positioning.md
├── requirements/                   # Product requirements
│   ├── prd-phase-1.md
│   ├── prd-phase-2.md
│   └── user-stories/
├── planning-sessions/              # Meeting notes & decisions
│   ├── YYYY-MM-DD-planning-session.md
│   └── decision-log.md
└── workflows/                      # Process definitions
    ├── development-workflow.md
    └── approval-processes.md
```

### 🚀 `deployment/` - Deployment & Operations
James & Alex's domain for infrastructure, deployment, and operational concerns:

```
deployment/
├── infrastructure/                 # Infrastructure as code
│   ├── docker/
│   ├── kubernetes/
│   └── terraform/
├── configs/                       # Configuration files
│   ├── production.env.template
│   ├── staging.env.template
│   └── monitoring-config.yml
├── scripts/                       # Deployment scripts
│   ├── deploy.sh
│   ├── backup.sh
│   └── health-check.sh
└── runbooks/                      # Operational procedures
    ├── incident-response.md
    ├── scaling-procedures.md
    └── backup-recovery.md
```

### 🧪 `testing/` - Test Files & Validation
Quinn's domain for testing artifacts and validation materials:

```
testing/
├── phase-testing/                 # Phase-specific tests
│   ├── phase1/
│   │   ├── test_phase1.py
│   │   ├── setup_phase1.py
│   │   └── PHASE1_TESTING_GUIDE.md
│   └── phase2/
├── automated/                     # Automated test suites
│   ├── unit-tests/
│   ├── integration-tests/
│   └── e2e-tests/
├── manual/                        # Manual testing procedures
│   ├── test-plans/
│   ├── test-cases/
│   └── validation-checklists/
└── results/                       # Test execution results
    ├── YYYY-MM-DD-test-results.json
    └── performance-benchmarks/
```

### 📊 `reports/` - Generated Reports & Metrics
System-generated reports and performance metrics:

```
reports/
├── daily/                         # Daily automated reports
├── weekly/                        # Weekly summaries
├── metrics/                       # Performance metrics
│   ├── agent-performance/
│   ├── workflow-analytics/
│   └── system-health/
└── executive/                     # Executive summaries
    ├── sprint-reports/
    └── milestone-reports/
```

### 📦 `archive/` - Completed/Superseded Materials
Organized archive of completed work and superseded documents:

```
archive/
├── YYYY/                          # Yearly organization
│   ├── QX/                        # Quarterly breakdown
│   │   ├── research/              # Archived research
│   │   ├── planning/              # Archived planning docs
│   │   ├── implementations/       # Completed features
│   │   └── decisions/             # Historical decisions
├── superseded/                    # Replaced documents
│   ├── old-prds/
│   ├── deprecated-specs/
│   └── obsolete-workflows/
└── completed-phases/              # Finished development phases
    ├── phase-1-complete/
    └── phase-2-complete/
```

## File Naming Conventions

### Research Documents (Mary)
- `YYYY-MM-DD-research-topic.md`
- `competitive-analysis-COMPANY.md`
- `market-segment-SEGMENT.md`

### Planning Documents (John)
- `prd-FEATURE-vX.X.md`
- `roadmap-YYYY-QX.md`
- `user-story-FEATURE.md`

### Technical Documents (James/Alex)
- `architecture-COMPONENT.md`
- `deployment-ENV.md`
- `runbook-PROCEDURE.md`

### Testing Documents (Quinn)
- `test-plan-FEATURE.md`
- `validation-PHASE.md`
- `results-YYYY-MM-DD.json`

### UX Documents (Sally)
- `ux-research-FEATURE.md`
- `design-system-COMPONENT.md`
- `accessibility-audit-YYYY-MM-DD.md`

## Workflow Integration

### Document Creation Flow
1. **Research Phase**: Mary creates documents in `research/active/`
2. **Planning Phase**: John creates PRDs in `planning/requirements/`
3. **Development Phase**: James/Alex create technical docs in `docs/architecture/`
4. **Testing Phase**: Quinn creates test plans in `testing/phase-testing/`
5. **Completion**: Documents move to appropriate `archive/` subdirectories

### Version Control Strategy
- **Active documents**: Keep in main directories with version suffixes
- **Superseded versions**: Move to `archive/superseded/`
- **Git tracking**: All documents under version control
- **Change logs**: Maintain in each directory's README.md

## Maintenance Procedures

### Monthly Archive Process
1. **Review active documents** for completion status
2. **Move completed work** to appropriate archive directories
3. **Update indexes** in README.md files
4. **Clean up** temporary and working files

### Quarterly Reviews
1. **Archive entire quarters** of completed work
2. **Review folder structure** for optimization
3. **Update conventions** based on team feedback
4. **Generate summary reports** of archived work

## Agent Responsibilities

### Mary (Business Analyst)
- **Owns**: `research/` directory
- **Maintains**: Market intelligence, competitive analysis
- **Archives**: Completed research to `archive/YYYY/QX/research/`

### John (Product Manager)
- **Owns**: `planning/` directory and overall structure coordination
- **Maintains**: PRDs, roadmaps, strategic documents
- **Archives**: Completed planning phases to `archive/YYYY/QX/planning/`

### James (Developer)
- **Owns**: Technical implementation in `src/` and `deployment/`
- **Maintains**: Architecture docs, deployment procedures
- **Archives**: Completed implementations to `archive/YYYY/QX/implementations/`

### Quinn (QA Engineer)
- **Owns**: `testing/` directory
- **Maintains**: Test suites, validation procedures
- **Archives**: Test results and completed validation phases

### Sally (UX Designer)
- **Owns**: UX-related documents across directories
- **Maintains**: Design systems, accessibility standards
- **Archives**: Design iterations and completed UX phases

### Alex (Architect)
- **Owns**: System architecture and infrastructure design
- **Maintains**: Technical specifications, integration patterns
- **Archives**: Architectural decisions and completed system designs

## Benefits of This Structure

1. **Clear Ownership**: Each agent knows their domain
2. **Lifecycle Management**: Documents flow naturally from active to archive
3. **Easy Navigation**: Logical grouping by function and time
4. **Historical Context**: Easy access to decisions and evolution
5. **Scalability**: Structure grows with project complexity
6. **Compliance**: Audit trail for regulatory requirements