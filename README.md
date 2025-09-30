# BMAD Auto - Autonomous Product Orchestration System

**Enterprise-grade autonomous product development using a coordinated 10-agent ecosystem.**

## Overview

BMAD Auto is a PM-centric autonomous orchestration system that manages complete product lifecycles from Research → Ideation → PRD → Architecture → MVP → Scale. Built on the proven `.bmad-core` methodology, it adds sophisticated multi-agent coordination, database-driven state management, and intelligent workflow orchestration.

### Key Features

- 🤖 **10-Agent Ecosystem**: PM coordination hub managing specialized agents (Architect, Developer, QA, UX, Analyst, and more)
- 🔄 **LangGraph Orchestration**: Intelligent workflow coordination with state persistence and recovery
- 🗄️ **Hybrid Database**: PostgreSQL for state management + coordination.db for BMAD integration
- 🤝 **Multi-Provider AI**: Anthropic Claude + Z.ai GLM with intelligent model assignment
- 🔗 **External Integration**: GitHub CLI + Linear API + MCP protocol for seamless tool access
- ✅ **Quality Gates**: Automated validation with human oversight and PM decision reasoning
- 🛡️ **100% .bmad-core Preservation**: Extension overlay architecture with zero modifications

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ (optional, for advanced features)
- Git
- 8GB RAM, 4 CPU cores minimum

### Installation

1. **Clone into your project:**
```bash
cd your-project-folder/
git clone https://github.com/your-org/bmad-auto.git .bmad-auto/
```

2. **Run installation:**
```bash
cd .bmad-auto/
./scripts/install.sh
```

3. **Configure environment:**
```bash
# Edit .env with your settings
cp .env.example .env
nano .env
```

4. **Activate and verify:**
```bash
source bmad-auto-env/bin/activate
python3 -c "from intercept.pm_coordinator import PMCoordinator; print('✓ BMAD Auto ready!')"
```

## Project Structure

When installed in your project, BMAD Auto creates this structure:

```
your-project/
├── .bmad-auto/              # BMAD Auto installation
│   ├── agents/             # Agent extensions
│   ├── workflows/          # LangGraph workflows
│   ├── intercept/          # PM coordination hub
│   ├── orchestration/      # Core orchestration
│   ├── database/           # Database schemas
│   ├── .bmad-core/         # Core BMAD methodology
│   └── bmad-auto-env/      # Python virtual environment
├── src/                    # Your product code
├── docs/                   # Your documentation
└── README.md               # Your project readme
```

## Architecture

BMAD Auto implements a **database-driven, PM-centric orchestration architecture**:

- **PM Coordination Hub**: John (PM) as central orchestrator
- **LangGraph Workflows**: State-managed agent coordination
- **Extension Overlay**: Zero-modification enhancement of .bmad-core
- **Multi-Provider AI**: Intelligent model selection for cost optimization
- **Quality Gates**: Automated validation with human oversight

See `docs/01-foundation/system-architecture.md` for complete details.

## Usage

### Basic PM Coordination

```python
from intercept.pm_coordinator import PMCoordinator

# Initialize PM coordinator
pm = PMCoordinator(
    bmad_core_path='.bmad-core',
    db_path='intercept/coordination.db'
)

# Autonomous task breakdown
pm.break_down_task("Build user authentication system")

# Agent assignment with reasoning
pm.assign_to_agent(task_id="T001", agent="james")

# Quality gate validation
pm.validate_quality_gate(deliverable_id="D001")
```

### Agent Development Workflow

```python
# James (Developer) working on implementation
from intercept.agent_loader import load_agent

agent = load_agent("james", extensions=["dev-extension.yaml"])
result = agent.implement_feature("user-authentication")
```

### Multi-Provider AI Integration

BMAD Auto automatically selects optimal AI models:

- **Complex tasks**: Anthropic Claude Sonnet/Opus 4
- **Routine operations**: Z.ai GLM 4.5
- **File search**: Z.ai GLM 4.5-Air (cost optimization)

Configure via Claude Code terminal or environment variables.

## Development

### Running Tests

```bash
pytest tests/ -v --cov=intercept --cov=orchestration
```

### Contributing

See `docs/development/contributing.md` for development guidelines.

## Documentation

- **Architecture**: `docs/01-foundation/system-architecture.md`
- **PRD**: `planning/requirements/prd.md`
- **Technical Specs**: `planning/architecture/bmad-auto-comprehensive-technical-architecture.md`
- **Best Practices**: `docs/05-best-practices/`
- **Tasks**: `specs/001-foundation-pm-orchestration/tasks.md`

## Status

- **Current Phase**: Foundation & PM Orchestration (Tasks T001-T029 complete, 57%)
- **MVP Target**: 12 weeks (Weeks 1-12)
- **Production Ready**: External integration + performance optimization

## License

[Specify your license]

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/bmad-auto/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/bmad-auto/discussions)
- **Documentation**: `docs/` directory

---

**Built with ❤️ using BMAD methodology**
