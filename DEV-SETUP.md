# BMAD Auto Development Setup Guide

**Last Updated**: 2025-10-01
**Status**: Standalone Repository - Ready for Spec-Based Development
**Repository**: bmad-auto (independent from old repo structure)

---

## 🎯 Quick Start (2 Minutes)

### 1. Environment Activation
```bash
cd /Users/apple/ai-projects/bmad-auto/
source bmad-auto-env/bin/activate
export PYTHONPATH=.
```

### 2. Verify Installation
```bash
# Test imports
python3 -c "from intercept.pm_coordinator import PMCoordinator; print('✓ Ready')"

# Run tests (91/125 passing - expected for initial setup)
pytest tests/ -q
```

### 3. Start Development
```bash
# Check current spec tasks
cat specs/001-foundation-pm-orchestration/tasks.md

# Begin implementation following spec-based workflow
```

---

## 📁 Repository Structure

### Public vs Private Files

**✅ PUBLIC (committed to GitHub)**:
- All source code (`*.py`)
- Tests (`tests/**`)
- Specifications (`specs/**`)
- Documentation (`docs/**` - excluding private files)
- Configuration templates (`.env.example`)
- Infrastructure (`orchestration/`, `database/`, `intercept/`)
- `.bmad-core/` (preserved agent definitions)

**🔒 PRIVATE (local only - in .gitignore)**:
- Environment files (`.env`, `.env.local`)
- Session handoffs (`docs/pm/SESSION-*.md`)
- PM decision logs (`docs/pm/PM-DECISION-*.md`)
- Working drafts (`docs/**/*-DRAFT.md`, `docs/**/*-LOCAL.md`)
- Database files (`*.db`, `coordination.db`)
- Virtual environment (`bmad-auto-env/`)
- API keys, secrets (`*.key`, `credentials.json`)
- Debug/scratch directories

### Key Directories

```
bmad-auto/
├── specs/                          # Spec-based development (GitHub Spec Kit)
│   └── 001-foundation-pm-orchestration/
│       ├── spec.md                 # Feature specification
│       ├── plan.md                 # Technical planning
│       ├── tasks.md                # Implementation tasks (T001-T050+)
│       ├── research.md             # Technical research
│       ├── data-model.md           # Entity definitions
│       ├── quickstart.md           # User scenarios
│       └── contracts/              # API contracts
├── intercept/                      # PM Coordination Hub
│   ├── pm_coordinator.py          # ✅ Core PM orchestration
│   ├── agent_loader.py            # ✅ Agent extension system
│   └── coordination.db            # 🔒 Local database (gitignored)
├── orchestration/                  # Multi-agent coordination
│   ├── task_assignment_core.py    # ✅ Task assignment engine
│   ├── quality_gate_simple.py     # ✅ Quality validation
│   └── workflow_state.py          # Workflow persistence
├── database/                       # Database layer
│   ├── connection_manager.py      # ✅ DB connections
│   ├── postgresql_schema.sql      # PostgreSQL schema
│   └── schema/                    # Schema definitions
├── agents/                         # Agent extensions
│   └── pm_extension.yaml          # PM enhancements
├── tests/                          # Test suites
│   ├── contract/                  # API contract tests
│   ├── entities/                  # Entity validation tests
│   └── integration/               # Integration scenarios
├── docs/                           # Documentation
│   ├── pm/                        # 🔒 Private PM docs
│   ├── dev/                       # Development guides
│   └── operations/                # Operations docs
└── .bmad-core/                    # ✅ Preserved BMAD foundation
    ├── agents/                    # Core agent definitions
    ├── tasks/                     # Agent tasks
    ├── templates/                 # Document templates
    └── workflows/                 # Agent workflows
```

---

## 🚀 Spec-Based Development Workflow

### GitHub Spec Kit Methodology

BMAD Auto uses [GitHub Spec Kit](https://github.com/anthropics/spec-kit) for structured development:

1. **Specification** (`spec.md`) - WHAT and WHY
2. **Research** (`research.md`) - Technical decisions
3. **Planning** (`plan.md`) - HOW to implement
4. **Tasks** (`tasks.md`) - Step-by-step implementation
5. **Contracts** (`contracts/`) - API interfaces
6. **Quickstart** (`quickstart.md`) - User scenarios
7. **Implementation** - Code following tasks
8. **Validation** - Tests verify contracts

### Current Development Status

**Spec 001: Foundation & PM Orchestration Hub**
- ✅ Specification complete
- ✅ Research complete
- ✅ Planning complete
- ✅ Tasks defined (T001-T050+)
- ✅ Contracts defined
- 🔄 Implementation in progress

**Completed Tasks** (from old repo migration):
- ✅ T001-T005: Foundation setup
- ✅ T011: Entity tests created
- ✅ T012: Integration scenarios created
- ✅ T017: PM Coordinator implemented
- ✅ T019-T020: Orchestration modules refactored
- ✅ T021: Agent loader implemented

**Next Tasks** (prioritized):
- 🎯 T013-T016: Complete database layer
- 🎯 T018: PM decision reasoning capture
- 🎯 T023-T030: Multi-provider AI integration
- 🎯 T031-T036: External service integration

### Task Execution Workflow

```bash
# 1. Review task from tasks.md
cat specs/001-foundation-pm-orchestration/tasks.md | grep "T013"

# 2. Check if tests exist (TDD approach)
ls tests/contract/test_database_layer.py

# 3. Write test if needed (Red phase)
# Edit: tests/contract/test_database_layer.py

# 4. Implement feature (Green phase)
# Edit: database/postgresql_schema.sql

# 5. Verify test passes
pytest tests/contract/test_database_layer.py -v

# 6. Refactor if needed (Refactor phase)

# 7. Update task as complete
# Edit: specs/001-foundation-pm-orchestration/tasks.md
# Mark: [x] T013 Implement PostgreSQL schema
```

---

## 🗄️ Database Setup

### Current State
- ✅ SQLite `coordination.db` (empty, needs schema)
- ⏳ PostgreSQL (optional for MVP, recommended for production)

### SQLite Setup (Minimal - MVP)

```bash
# coordination.db is automatically created but needs schema
source bmad-auto-env/bin/activate
export PYTHONPATH=.

# Initialize schema (when SQL files are ready)
sqlite3 coordination.db < database/schema/coordination_extensions.sql
```

### PostgreSQL Setup (Recommended)

```bash
# 1. Install PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# 2. Create database
psql postgres
CREATE DATABASE bmad_auto;
CREATE USER bmad_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE bmad_auto TO bmad_user;
\q

# 3. Apply schema (when ready)
psql -U bmad_user -d bmad_auto -f database/postgresql_schema.sql

# 4. Update .env
DATABASE_URL=postgresql://bmad_user:your_password@localhost:5432/bmad_auto
```

---

## ⚙️ Configuration

### Environment Variables (.env)

**Minimal Configuration (MVP)**:
```bash
# Database
COORDINATION_DB_PATH=coordination.db
DATABASE_URL=sqlite:///coordination.db  # Or PostgreSQL URL

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

**Full Configuration (Production)**:
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/bmad_auto
COORDINATION_DB_PATH=intercept/coordination.db

# LangGraph/LangSmith
LANGSMITH_API_KEY=your_key_here
LANGSMITH_PROJECT=bmad-auto-dev

# AI Models (Claude Code Integration)
CLAUDE_MODEL=claude-sonnet-4-20250514
GLM_MODEL=glm-4.5

# External Services
GITHUB_TOKEN=your_github_token
LINEAR_API_KEY=your_linear_key

# Development
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

---

## 🧪 Testing Strategy

### Test Organization

```
tests/
├── contract/           # API contract tests (Phase 3.2)
│   ├── test_pm_decisions_api.py      # T006
│   ├── test_agent_state_api.py       # T007
│   └── test_workflow_api.py          # T008
├── entities/           # Entity validation (Phase 3.2)
│   └── test_core_entities.py         # T011 ✅
├── integration/        # Integration scenarios (Phase 3.2)
│   └── test_quickstart_scenarios.py  # T012 ✅
└── unit/              # Unit tests (per implementation)
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/entities/test_core_entities.py -v

# Test with coverage
pytest tests/ --cov=intercept --cov=orchestration --cov=database

# Quick smoke test
pytest tests/ -q --tb=no

# Current status: 91 passing, 34 failing (expected for initial setup)
```

### TDD Workflow

**Rule**: Tests MUST be written before implementation (Phase 3.2 before 3.3)

1. Write failing test (Red)
2. Implement minimal code to pass (Green)
3. Refactor for quality (Refactor)
4. Repeat

---

## 🔧 Development Commands

### Common Operations

```bash
# Activate environment (always first!)
source bmad-auto-env/bin/activate
export PYTHONPATH=.

# Run specific task implementation
# Example: Working on T013 (PostgreSQL schema)
vim database/postgresql_schema.sql

# Test the implementation
pytest tests/contract/test_database_layer.py -v

# Check code quality
flake8 database/
black database/
isort database/

# Interactive Python REPL
python3
>>> from intercept.pm_coordinator import PMCoordinator
>>> pm = PMCoordinator()
```

### Git Workflow (Public Repository)

```bash
# Check what will be committed (verify no private files)
git status
git diff

# Verify .gitignore is working
git status --ignored

# Commit implementation
git add database/postgresql_schema.sql tests/contract/test_database_layer.py
git commit -m "feat(T013): implement PostgreSQL schema for core entities"

# Push to public repository
git push origin main
```

---

## 📊 Current Implementation Status

### Completed Infrastructure
- ✅ Python virtual environment with all dependencies
- ✅ .bmad-core preservation and agent loader
- ✅ PM Coordinator core framework
- ✅ Orchestration modules (task assignment, quality gates)
- ✅ Test infrastructure (91 passing tests)
- ✅ Spec-based development structure

### In Progress (Next Sprint)
- 🔄 Database schema implementation (T013-T016)
- 🔄 PM decision reasoning capture (T018)
- 🔄 Multi-provider AI integration (T023-T030)
- 🔄 External service coordination (T031-T036)

### Not Started
- ⏳ Advanced quality analytics (T037-T040)
- ⏳ Performance optimization (T041-T045)
- ⏳ Monitoring and observability (T046-T050)

---

## 🎯 Next Steps

### Immediate Actions (This Session)

1. **Complete Database Layer** (T013-T016)
   - Implement PostgreSQL schema
   - Extend coordination.db
   - Database connection management
   - Migration system

2. **PM Decision Reasoning** (T018)
   - Implement decision capture system
   - Test reasoning trails
   - Validate cognitive framework integration

3. **Multi-Provider AI** (T023-T030)
   - Claude Code terminal integration
   - Model assignment algorithms
   - Usage tracking and optimization

### Weekly Goals

**Week 1**: Database layer complete, tests passing
**Week 2**: PM decision reasoning operational
**Week 3**: Multi-provider AI integration functional
**Week 4**: External service coordination (GitHub, Linear)

---

## 📚 References

### Key Documentation
- **Spec Kit Methodology**: `specs/001-foundation-pm-orchestration/`
- **Architecture**: `planning/architecture/bmad-auto-comprehensive-technical-architecture.md`
- **Requirements**: `planning/requirements/prd.md`
- **Installation**: `docs/INSTALLATION-GUIDE.md`
- **Best Practices**: `docs/05-best-practices/`

### External Resources
- [GitHub Spec Kit](https://github.com/anthropics/spec-kit)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [BMAD Core User Guide](`.bmad-core/user-guide.md`)

---

## 🚨 Important Reminders

### Before Every Commit
1. ✅ Check `git status` for private files
2. ✅ Verify .env and session docs are gitignored
3. ✅ Run tests: `pytest tests/ -q`
4. ✅ Code quality: `flake8 . && black . --check`
5. ✅ No secrets or API keys in code

### Daily Development Checklist
1. ✅ Activate virtual environment
2. ✅ Set PYTHONPATH=.
3. ✅ Check task list in tasks.md
4. ✅ Write tests before implementation (TDD)
5. ✅ Update task status after completion
6. ✅ Document decisions in private PM docs

---

**Ready for standalone spec-based development!**

For questions or issues, refer to:
- Session handoffs: `docs/pm/SESSION-HANDOFF-NEW-WORKSPACE-2025-10-01.md` (private)
- Development guide: This file
- Spec tasks: `specs/001-foundation-pm-orchestration/tasks.md`
