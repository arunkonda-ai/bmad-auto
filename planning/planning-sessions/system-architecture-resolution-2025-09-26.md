---
type: system-architecture-resolution
version: 1.0
created: 2025-09-26
status: ready-for-execution
priority: critical
session-context: pre-github-spec-kit-integration
---

# 🏗️ BMAD Auto System Architecture Resolution & GitHub Spec Kit Preparation

## **CRITICAL ISSUE IDENTIFIED**

### **Duplicate Storage Systems Conflict**
The current BMAD Auto system has **conflicting storage approaches** running in parallel:

**❌ Current Problem:**
- **Python Database Approach**: `pm_coordinator.py` + `state_manager.py` using SQLite for runtime state
- **YAML File Approach**: `workflow-states.yaml` defining same state management in files
- **Result**: Same data stored twice, sync issues, maintenance complexity

**✅ Industry Standard Solution:**
- **Python + SQLite**: Runtime coordination, agent status, workflow execution state
- **MD/YAML Files**: Configuration schemas, workflow templates, static definitions
- **File System**: Agent work products, generated artifacts, collaboration documents

## **SYSTEM VALIDATION & RESOLUTION TASKS**

### **Phase 1: Storage Architecture Resolution (Priority 1)**

#### **Task 1.1: Analyze Current Duplicate Storage**
```bash
# Files to examine for conflicts:
.bmad-auto/intercept/pm_coordinator.py        # SQLite coordination database
.bmad-auto/intercept/state_manager.py         # SQLite state management
.bmad-auto/state/workflow-states.yaml         # Duplicate YAML state system
```

**Expected Finding**: Both systems manage coordination_log, agent_status, workflow_state

#### **Task 1.2: Resolve Storage Conflicts**
**Action**: Keep Python SQLite for runtime state, convert YAML to configuration only

**Specific Changes:**
1. **Keep in Database (Python)**:
   - Agent coordination status (who's busy, available, error state)
   - Active workflow execution state (current stage, progress, context)
   - PM decision log (approvals, rejections, escalations)
   - Real-time performance metrics

2. **Keep in YAML Files (Configuration)**:
   - Agent workflow templates and schemas
   - Coordination rules and policies
   - System configuration parameters
   - Static workflow definitions

3. **Remove from YAML**:
   - Runtime agent status tracking
   - Active coordination logs
   - Session state management
   - Dynamic workflow state

#### **Task 1.3: Update workflow-states.yaml**
Convert from runtime state management to configuration schema:
```yaml
# BEFORE: Runtime state tracking (REMOVE)
operations:
  update_agent_status: # DELETE - this belongs in database
  log_coordination: # DELETE - this belongs in database

# AFTER: Configuration schema only (KEEP)
schemas:
  coordination_log: # Schema definition only
  agent_status: # Schema definition only
config:
  state_directory: # Configuration parameters
  backup_directory: # Configuration parameters
```

### **Phase 2: System Validation (Priority 2)**

#### **Task 2.1: Verify Python Coordination System**
**Test Commands:**
```bash
cd .bmad-auto/intercept
python3 pm_coordinator.py status
python3 pm_coordinator.py coordinate james create-architecture '{"complexity": "medium"}'
python3 state_manager.py agent-status
python3 state_manager.py workflows
```

**Expected Results:**
- SQLite database created and functional
- Agent coordination working
- State tracking operational
- No errors or conflicts

#### **Task 2.2: Test Agent Workflow Patterns**
**Current Status**: Only Mary (Analyst) has complete workflow pattern
**Required**: All 10 agents need defined workflows

**Test Mary's Pattern (Working Example)**:
```bash
# Check Mary's research workflow
ls -la .bmad-auto/research/active/     # Input folder
ls -la .bmad-auto/research/findings/   # Output folder
cat .bmad-auto/research/README.md      # Workflow documentation
```

**Action**: Document this pattern for replication to other 9 agents

#### **Task 2.3: Validate CLAUDE.md Navigation**
**Check**: `.bmad-auto/CLAUDE.md` accuracy for all agent navigation
**Action**: Update any broken references or missing sections

### **Phase 3: GitHub Spec Kit Readiness (Priority 3)**

#### **Task 3.1: System Integration Points**
**Verify these integration points work:**
1. **PM Coordination**: `pm_coordinator.py` can handle Spec Kit workflows
2. **Agent Workflows**: File-based workflows can integrate with Spec Kit
3. **State Management**: Database state won't conflict with Spec Kit
4. **Documentation**: CLAUDE.md supports Spec Kit navigation

#### **Task 3.2: PRD Alignment Check**
**Reference**: `.bmad-auto/planning/requirements/prd.md` (76KB comprehensive PRD)
**Action**: Validate current system capabilities match PRD Phase 1 requirements

**Key PRD Requirements to Verify**:
- FR1: PM Hub Foundation (pm_coordinator.py implementation)
- FR2: Agent Coordination Framework (10-agent ecosystem)
- FR3: Workflow Orchestration (LangGraph integration)
- FR4: Quality Gates (validation pipeline)

## **EXPECTED OUTCOMES**

### **After Resolution:**
1. **Single Source of Truth**: Database for runtime state, files for configuration
2. **No Storage Conflicts**: Clear boundaries between Python and YAML usage
3. **All Agents Defined**: Complete workflow patterns for 10-agent ecosystem
4. **Spec Kit Ready**: Clean architecture for GitHub Spec Kit integration
5. **PRD Aligned**: System capabilities match comprehensive PRD requirements

### **GitHub Spec Kit Integration Path:**
Once this resolution is complete:
1. **Spec Kit Setup**: In separate directory (`.bmad-auto/spec-kit/`)
2. **Constitution Creation**: From existing PRD principles
3. **Specification Generation**: Using `/specify` command on PRD sections
4. **Implementation Planning**: Using `/plan` command for development phases

## **SUCCESS CRITERIA**

### **Technical Validation:**
- [ ] No duplicate storage systems
- [ ] Python coordination database fully functional
- [ ] YAML files contain configuration only (no runtime state)
- [ ] All 10 agents have workflow patterns defined
- [ ] System passes integration tests

### **Documentation Validation:**
- [ ] CLAUDE.md navigation updated and accurate
- [ ] PRD requirements align with system capabilities
- [ ] Clear storage boundaries documented
- [ ] Agent workflow patterns documented

### **Integration Readiness:**
- [ ] GitHub Spec Kit can integrate without conflicts
- [ ] Existing BMAD Auto system preserved
- [ ] Development can proceed from current system state
- [ ] No architectural restart required

## **CRITICAL SUCCESS FACTORS**

1. **Preserve Existing Work**: Don't restart, resolve conflicts and build forward
2. **Industry Standards**: Follow Python+Database+YAML hybrid approach
3. **Clear Boundaries**: Document what goes where (database vs files vs config)
4. **Complete Agent System**: All 10 agents with defined workflows
5. **PRD Continuity**: Build from existing comprehensive PRD, not restart

---

**Next Steps After Completion**: GitHub Spec Kit integration with clean, conflict-free BMAD Auto architecture ready for PRD-to-product development.