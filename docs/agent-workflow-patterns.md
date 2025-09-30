# Agent Workflow Patterns - BMAD Auto
# Documentation of working agent patterns for 10-agent ecosystem replication

## Mary (Analyst) - Working Pattern ✅

### Directory Structure
```
.bmad-auto/research/
├── active/              # 📥 Input: New research tasks
├── findings/            # 📤 Output: Completed research reports
├── source-materials/    # 📚 Reference materials
├── README.md            # 📖 Workflow documentation
└── RESEARCH_TEMPLATE.md # 📝 Standard template
```

### Workflow Process
1. **Task Assignment**: New research tasks placed in `active/` directory
2. **Template Usage**: Uses `RESEARCH_TEMPLATE.md` for consistency
3. **File Naming**: `YYYY-MM-DD-[research-topic]-analysis.md`
4. **Output**: Completed research moved to `findings/`
5. **Integration**: Results feed into BMAD Auto planning

### Current Status
- **Active Tasks**: 0 (empty active/ directory)
- **Completed Research**: 5 reports in findings/
- **Integration Status**: Research integrated into comprehensive PRD

### Success Metrics
- ✅ Clear input/output separation
- ✅ Consistent file naming and templates
- ✅ Integration with PM coordination
- ✅ Quality research outputs produced

## Required Agent Patterns (To Be Implemented)

### John (PM) - Coordination Hub
**Status**: Partially implemented (Python coordination working)
**Required**:
- Workflow directory structure like Mary's pattern
- PM decision templates
- Integration with other 9 agents

### James (Developer) - Implementation
**Status**: Not implemented
**Required Pattern**:
```
.bmad-auto/development/
├── active/              # Current development tasks
├── completed/           # Finished implementations
├── code-review/         # Code review queue
└── DEV_TEMPLATE.md      # Development template
```

### Quinn (QA) - Quality Assurance
**Status**: Not implemented
**Required Pattern**:
```
.bmad-auto/quality/
├── validation-queue/    # Items awaiting QA
├── test-reports/        # QA test results
├── quality-gates/       # Quality gate definitions
└── QA_TEMPLATE.md       # QA process template
```

### Sally (UX) - User Experience
**Status**: Not implemented
**Required Pattern**:
```
.bmad-auto/design/
├── design-requests/     # UX design tasks
├── design-artifacts/    # Completed designs
├── user-research/       # UX research
└── UX_TEMPLATE.md       # UX process template
```

### Alex (Architect) - System Architecture
**Status**: Not implemented
**Required Pattern**:
```
.bmad-auto/architecture/
├── architecture-requests/  # Architecture tasks
├── technical-designs/      # Completed architectures
├── system-analysis/        # System assessments
└── ARCH_TEMPLATE.md        # Architecture template
```

### Remaining 5 Agents (PO, SM, BMAD Orchestrator, BMAD Master, Additional Agent)
**Status**: Not defined
**Required**: Patterns following Mary's successful model

## Pattern Replication Template

### Standard Agent Directory Structure
```
.bmad-auto/{agent-domain}/
├── active/              # 📥 Current tasks for this agent
├── {output-directory}/  # 📤 Completed work products
├── templates/           # 📝 Agent-specific templates
├── README.md            # 📖 Agent workflow documentation
└── {AGENT}_TEMPLATE.md  # 📋 Standard work template
```

### Standard Agent Workflow
1. **Task Reception**: Receive tasks in `active/` directory
2. **Template Application**: Use standardized templates
3. **Work Execution**: Follow agent-specific processes
4. **Output Generation**: Produce consistent work products
5. **PM Coordination**: Integrate with Python coordination system
6. **Quality Gates**: Pass validation before completion

### Integration Requirements
- **Python Coordination**: Must integrate with `pm_coordinator.py`
- **State Tracking**: Status tracked in `state_manager.py` database
- **GitHub Integration**: Issues/notifications via GitHub
- **LangFuse Monitoring**: Performance tracking enabled

### Template Standards
- Consistent metadata headers
- Clear acceptance criteria
- Integration checkpoints
- Quality validation steps
- PM approval workflows

## Implementation Priority

### Phase 1 (Current): Core Validation
1. ✅ Mary (Analyst) - Working pattern validated
2. 🔄 John (PM) - Python coordination validated, directory pattern needed
3. ⏳ System integration validated

### Phase 2: Primary Agents
1. James (Developer) - Implementation workflows
2. Quinn (QA) - Quality validation processes
3. Alex (Architect) - Technical design workflows

### Phase 3: Secondary Agents
1. Sally (UX) - Design and research workflows
2. PO (Product Owner) - Product management workflows
3. SM (Scrum Master) - Process management workflows

### Phase 4: Advanced Agents
1. BMAD Orchestrator - Meta-coordination workflows
2. BMAD Master - System optimization workflows
3. Additional specialized agents as needed

## Success Criteria for Each Agent

### Technical Validation
- [ ] Directory structure matches Mary's pattern
- [ ] Templates created and functional
- [ ] Python coordination integration working
- [ ] State management tracking operational
- [ ] GitHub integration functional

### Process Validation
- [ ] Clear task input/output flow
- [ ] Consistent file naming and organization
- [ ] Quality templates and standards
- [ ] PM coordination workflow
- [ ] Integration with other agents

### Integration Validation
- [ ] Works with existing Python system
- [ ] Integrates with GitHub Spec Kit (planned)
- [ ] Supports PRD requirements
- [ ] Maintains .bmad-core compatibility principles
- [ ] Enables autonomous orchestration goals