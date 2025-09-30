
# Implementation Plan: Foundation & PM Orchestration Hub

**Branch**: `001-foundation-pm-orchestration` | **Date**: 2025-09-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-foundation-pm-orchestration/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
PM-centric orchestration hub that coordinates 10 autonomous AI agents through multi-provider AI integration (Claude Code terminal, Anthropic Claude, Z.ai GLM) with intelligent model assignment, hybrid database architecture (PostgreSQL + coordination.db), and comprehensive quality gate management while preserving 100% BMAD-core compatibility through extension overlay pattern.

## Technical Context
**Language/Version**: Python 3.11+ (LangGraph orchestration), TypeScript/JavaScript (Agent extensions), YAML/Markdown (Configuration)
**Primary Dependencies**: LangGraph, LangSmith, PostgreSQL, SQLite, Claude Code terminal integration, Anthropic Claude API, Z.ai GLM API
**Storage**: PostgreSQL (primary state management), SQLite coordination.db (BMAD integration), LangGraph state persistence
**Testing**: pytest (Python), Jest (JavaScript), integration testing for multi-agent coordination
**Target Platform**: Local development environment (macOS/Linux), Claude Code terminal integration
**Project Type**: Hybrid orchestration system (agent coordination + dashboard interface)
**Performance Goals**: <2s routine operations, <10s complex multi-agent coordination, 10-agent concurrent operations
**Constraints**: 100-300 line file limits, .bmad-core preservation (zero modifications), local resource optimization
**Scale/Scope**: 10 autonomous agents, PM-centric coordination, multi-provider AI optimization, quality gate management

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Status**: Constitution template found but not project-specific yet. Applying BMAD-core principles:
- ✅ **File Size Compliance**: All agent files must remain 100-300 lines through modular architecture
- ✅ **BMAD-core Preservation**: Zero modifications to existing .bmad-core files - extension overlay pattern only
- ✅ **Test-First Development**: TDD mandatory for all orchestration components
- ✅ **Local-First Architecture**: Claude Code terminal integration, local resource optimization
- ✅ **PM-Centric Coordination**: All agent coordination flows through John (PM) hub

**Violations**: None identified - architecture aligns with BMAD principles

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# BMAD Auto Extension Overlay Structure
.bmad-core/                           # PRESERVED - Zero modifications
├── agents/                           # Original BMAD agents
├── tasks/                            # Original BMAD tasks
├── workflows/                        # Original BMAD workflows
└── templates/                        # Original BMAD templates

.bmad-auto/                          # Extension overlay
├── orchestration/                   # PM coordination hub
│   ├── pm_coordinator.py           # John (PM) orchestration logic
│   ├── agent_manager.py            # Agent lifecycle management
│   ├── quality_gates.py            # Quality gate orchestration
│   └── model_provider.py           # Multi-AI provider management
├── agents/                          # Agent extensions
│   ├── pm_extension.yaml           # PM orchestration capabilities
│   ├── dev_extension.yaml          # Developer agent extensions
│   ├── qa_extension.yaml           # QA agent extensions
│   └── analyst_extension.yaml      # Analyst agent extensions
├── workflows/                       # LangGraph workflows
│   ├── task_breakdown.yaml         # Task decomposition workflows
│   ├── agent_coordination.yaml     # Inter-agent coordination
│   └── quality_validation.yaml     # Quality gate workflows
└── database/                        # Database schemas and migrations
    ├── postgresql_schema.sql        # Primary state management
    ├── coordination_extensions.sql  # Extended coordination.db
    └── migrations/                  # Database evolution

.bmad-auto/intercept/                # PM coordination system
├── pm_coordinator.py               # Central PM hub implementation
├── decision_capture.py             # PM decision reasoning
├── agent_loader.py                 # Dynamic agent extension loading
└── coordination.db                 # Extended SQLite database

tests/
├── orchestration/                  # PM coordination tests
├── agents/                         # Agent extension tests
├── workflows/                      # LangGraph workflow tests
├── integration/                    # Cross-agent integration tests
└── contract/                       # API contract tests
```

**Structure Decision**: Hybrid extension overlay preserving .bmad-core integrity while adding orchestration capabilities through .bmad-auto directory and .bmad-auto/intercept/ coordination system. No modifications to existing .bmad-core structure.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (data-model.md, contracts/, quickstart.md)
- PM Orchestration Hub → core coordination tasks [P]
- Agent Extension Loader → modular agent enhancement tasks [P]
- Multi-Provider AI Integration → intelligent model assignment tasks
- Quality Gate Management → automated validation tasks [P]
- Database Architecture → hybrid PostgreSQL + coordination.db tasks
- Claude Code Integration → terminal session management tasks

**Entity-Based Task Generation**:
- PMDecisionContext → decision reasoning capture implementation
- AgentState → agent lifecycle management system
- WorkflowExecution → LangGraph workflow coordination
- ModelAssignment → multi-provider AI optimization
- QualityGateExecution → approval workflow system
- ResourceMetrics → monitoring and optimization framework

**Ordering Strategy**:
- TDD order: Contract tests → Entity tests → Integration tests → Implementation
- Dependency order: Database → Core entities → Orchestration → Integration
- Foundation first: PM Hub → Agent Extensions → Workflows → Quality Gates
- Mark [P] for parallel execution of independent components

**Estimated Output**: 35-40 numbered, ordered tasks covering:
- Database setup and schema migration (5 tasks)
- Core entity implementation with tests (12 tasks)
- PM orchestration hub development (8 tasks)
- Agent extension overlay system (6 tasks)
- Multi-provider AI integration (7 tasks)
- Quality gate and approval workflows (5 tasks)
- Integration testing and validation (7 tasks)

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (None - architecture aligns with BMAD principles)

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
