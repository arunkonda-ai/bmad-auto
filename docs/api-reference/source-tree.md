# Source Tree Structure - BMAD Auto

## Project Root Structure
```
Omcaro/
├── .bmad-auto/                    # BMAD Auto implementation
│   ├── src/                       # Source code
│   │   ├── services/              # Business logic services
│   │   ├── controllers/           # FastAPI endpoints
│   │   ├── cognitive/             # Neural Field & Context Engineering
│   │   ├── models/                # Pydantic data models
│   │   ├── utils/                 # Utilities and helpers
│   │   └── main.py                # FastAPI application entry
│   ├── docs/                      # Documentation
│   ├── config/                    # Configuration files
│   └── testing/                   # Test suites
├── .bmad-core/                    # BMAD Core (preserved, never modify)
├── docs/                          # Project documentation
├── youtube-creator-platform/      # Production validation SaaS
└── bmad-ai-system/               # Framework structure
```

## Key Directories

### `/src/services/`
- `pm_coordination_service.py` - John's PM orchestration hub
- `state_management_service.py` - Enhanced state persistence
- `agent_service.py` - Agent coordination logic
- `workflow_service.py` - Workflow management

### `/src/controllers/`
- `pm_coordination_controller.py` - PM API endpoints
- `state_management_controller.py` - State management API
- `agent_controller.py` - Agent coordination API
- `workflow_controller.py` - Workflow API

### `/src/cognitive/`
- `neural_field.py` - Neural Field intelligence system
- `database.py` - Context database integration
- `primitives.py` - Context Engineering primitives (Atom, Molecule, Cell)

### `/src/models/`
- `workflow.py` - Workflow and task models
- `agent_personas.py` - Agent configuration models

## File Naming Conventions
- Services: `{domain}_service.py`
- Controllers: `{domain}_controller.py`
- Models: `{domain}.py`
- Tests: `test_{module}.py`
- Config: `{env}_config.yaml`

## Import Structure
- Relative imports within packages: `from .module import Class`
- Cross-package imports: `from services.module import Class`
- External dependencies: Standard imports at top of file