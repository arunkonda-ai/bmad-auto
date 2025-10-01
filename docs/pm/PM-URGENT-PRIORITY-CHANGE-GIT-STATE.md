# 🚨 PM URGENT: Priority Change - Git & State Persistence

**Date**: 2025-09-30
**PM Coordinator**: John (PM)
**Decision Type**: Critical Priority Override
**Reason**: Data loss prevention for human user

---

## 🎯 Critical User Problem Identified

### Issue Description

**User Report**: "Facing huge problem in data loss and document info loss because of not having git commits to be able to go back if required"

**Impact**:
- Cannot recover from mistakes or bugs
- Lost work between sessions (documentation gaps)
- No safety net for experimental development
- User anxiety about making changes

**Business Criticality**: 🚨 **BLOCKING USER PRODUCTIVITY**

---

## 📊 Current Task Sequence (Problems)

According to official tasks.md:

**State Persistence**: T029 (6 tasks away)
- Current sequence: T025 → T026 → T027 → T028 → **T029**
- Estimated: 3+ weeks away

**Git Integration**: T037 (13 tasks away)
- Current sequence: T031-T036 → **T037**
- Estimated: 4-5 weeks away

**Problem**: User needs these NOW, not in 4-5 weeks!

---

## 💡 PM Decision: Immediate Priority Override

### APPROVED: Pull Forward Critical Safety Features

**New Priority Order**:

1. **T029 (State Persistence)** - IMMEDIATE
2. **T037 (Git Integration)** - IMMEDIATE
3. **T031-T036 (API Layer)** - After safety features

**Rationale**:
- User safety > System features
- Data loss is unacceptable
- Git commits enable rollback and experimentation
- State persistence prevents session loss
- API layer can wait if user can't work safely

---

## 🎯 Revised Sprint Plan: Safety First

### Week 1: Critical Safety Infrastructure (REVISED)

#### Priority 1: Basic Git Integration (T037 - Simplified)
**Duration**: 8 hours
**Goal**: Enable automatic git commits for all agent work

**Deliverables**:
1. Automatic commit after each task completion
2. Descriptive commit messages with agent attribution
3. Branch management for development work
4. Easy rollback capability

**File**: `.bmad-auto/integration/github_coordinator.py` (target: 250 lines)

**Essential Features Only**:
- ✅ `git add` all changed files automatically
- ✅ `git commit` with agent-generated messages
- ✅ Branch creation for agent work
- ✅ Rollback commands if needed
- ⏸️ DEFER: GitHub API integration (not needed for local safety)
- ⏸️ DEFER: Pull request automation (MVP not needed)

---

#### Priority 2: Session State Persistence (T029 - Core Only)
**Duration**: 12 hours
**Goal**: Never lose conversation or work context

**Deliverables**:
1. Save conversation state to database after each message
2. Restore state on system restart
3. Agent context preservation
4. Task progress tracking

**File**: `.bmad-auto/orchestration/workflow_state.py` (target: 280 lines)

**Essential Features Only**:
- ✅ PostgreSQL state persistence
- ✅ Conversation history storage
- ✅ Agent working memory preservation
- ✅ Quick restore (<30 seconds)
- ⏸️ DEFER: Complex workflow recovery (MVP not needed)
- ⏸️ DEFER: LangSmith integration (can add later)

---

#### Priority 3: User Safety Commands (NEW - Not in tasks.md)
**Duration**: 4 hours
**Goal**: Give user easy rollback and safety controls

**Deliverables**:
1. `/rollback` command - Undo last N commits
2. `/checkpoint` command - Create safe restore point
3. `/status` command - Show current state and recent changes
4. `/restore` command - Restore from checkpoint

**File**: `.bmad-auto/commands/safety_commands.py` (target: 200 lines)

**User-Facing Commands**:
```bash
# Create checkpoint before risky work
/checkpoint "Before API implementation"

# Check what changed recently
/status

# Rollback if something broke
/rollback 3  # Undo last 3 commits

# Restore to named checkpoint
/restore "Before API implementation"
```

---

### Week 2: API Implementation (Original Plan)
**Resume T031-T036 after safety features complete**

---

## 📋 Implementation Specifications

### T037: Git Integration (Simplified for MVP)

**Requirements**:
```python
class GitCoordinator:
    """Automatic git operations for agent safety"""

    def auto_commit(self, agent_name: str, task_id: str, changes: List[str]):
        """
        Automatically commit agent work

        Commit message format:
        [Agent: {agent}] {task_id}: {description}

        - Files: {changed_files}
        - Duration: {time_taken}
        - Status: {success/failure}
        """

    def create_checkpoint(self, name: str, description: str):
        """Create named checkpoint for rollback"""

    def rollback(self, commits: int):
        """Undo last N commits safely"""

    def get_status(self) -> Dict:
        """Show current branch, recent commits, uncommitted changes"""
```

**Git Operations**:
- Auto-commit after each agent task (success or failure)
- Create feature branches for multi-task work
- Tag important milestones
- Preserve full history for debugging

---

### T029: State Persistence (Core MVP)

**Requirements**:
```python
class WorkflowStatePersistence:
    """PostgreSQL-backed state management"""

    def save_conversation_state(self, session_id: str, messages: List[Dict]):
        """Save all conversation messages to database"""

    def save_agent_context(self, agent_id: str, context: Dict):
        """Preserve agent working memory and task state"""

    def restore_session(self, session_id: str) -> SessionState:
        """Restore complete session within 30 seconds"""

    def save_task_progress(self, task_id: str, status: str, data: Dict):
        """Track task completion for resumption"""
```

**Database Schema**:
```sql
-- Session state table
CREATE TABLE session_state (
    session_id TEXT PRIMARY KEY,
    conversation_history JSONB,
    agent_contexts JSONB,
    task_progress JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Checkpoint table
CREATE TABLE checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    git_commit_hash TEXT,
    session_state JSONB,
    created_at TIMESTAMP
);
```

---

## ✅ Success Criteria for Week 1

### User Safety Validation
- [ ] User can commit work automatically after each task
- [ ] User can see what changed with `/status`
- [ ] User can rollback mistakes with `/rollback`
- [ ] User can create and restore checkpoints
- [ ] Conversation state persists across restarts
- [ ] No data loss between sessions

### Technical Validation
- [ ] Git integration: Auto-commits working
- [ ] State persistence: <30 second restore time
- [ ] Database: Session state saved after each message
- [ ] Commands: `/checkpoint`, `/rollback`, `/restore`, `/status` operational

---

## 🎯 PM Reasoning for Priority Override

### Why Override Official Task Order?

**User Need > Task Sequence**:
- Official tasks.md designed for feature completeness
- User experiencing real productivity blocker
- Data loss is unacceptable risk
- Safety features enable confident development

**Cost/Benefit Analysis**:
- **Cost**: 1 week delay on API implementation
- **Benefit**: User can work confidently without data loss fear
- **Risk Mitigation**: Prevents catastrophic work loss
- **User Experience**: Dramatically improved

**Alternative Considered**: Continue with API first
**Rejected Because**: User cannot work effectively with data loss risk

---

## 📞 Implementation Assignment

### James: Immediate Focus Change

**STOP**: API implementation planning
**START**: Safety features (T029 + T037 simplified)

**Week 1 Tasks**:
1. **Day 1-2**: T037 Git integration (8 hours)
   - Auto-commit functionality
   - Branch management
   - Basic rollback capability

2. **Day 3-4**: T029 State persistence (12 hours)
   - PostgreSQL session storage
   - Conversation history preservation
   - Quick restore functionality

3. **Day 5**: Safety commands (4 hours)
   - `/checkpoint`, `/rollback`, `/restore`, `/status`
   - User-facing safety controls

**Deliverable**: Working safety infrastructure enabling confident development

---

## 📊 Updated Timeline

### Before Priority Change
- Week 1-3: API Implementation (T031-T036)
- Week 4: Claude Code (T025)
- Week 5: State Persistence (T029)
- Week 6: Git Integration (T037)
- **User Risk**: 6 weeks of data loss exposure

### After Priority Change
- Week 1: Safety Features (T029 + T037 simplified)
- Week 2-4: API Implementation (T031-T036)
- Week 5: Claude Code (T025)
- **User Risk**: ELIMINATED after Week 1

**Net Timeline Impact**: Same MVP date, but user protected immediately

---

## 🚨 Risk Mitigation

### Implementation Risks

**Git Integration Challenges**:
- Mitigation: Start with local git only (no GitHub API needed)
- Fallback: Manual commit commands if auto-commit fails

**State Persistence Complexity**:
- Mitigation: Simple JSON storage first, optimize later
- Fallback: File-based backup if database issues

**User Learning Curve**:
- Mitigation: Simple commands (`/checkpoint`, `/rollback`)
- Documentation: Quick reference guide

---

## ✅ PM Approval Statement

**I, John (PM), approve immediate priority override to implement safety features before API layer.**

**Approved Changes**:
1. ✅ T037 (Git Integration) - Pull forward from Week 6 to Week 1
2. ✅ T029 (State Persistence) - Pull forward from Week 5 to Week 1
3. ✅ T031-T036 (API Layer) - Defer to Week 2-4
4. ✅ New safety commands - Add to Week 1

**Reasoning**: User productivity and data safety is paramount. Cannot have user lose work for 6 weeks while waiting for safety features.

**Success Definition**: After Week 1, user can work with confidence knowing:
- All work is automatically committed to git
- Conversation state persists across restarts
- Easy rollback if anything breaks
- Checkpoints for experimental work

---

**Next Action**: James begins T037 (Git Integration - simplified) immediately.

---

**PM Coordinator**: John (PM)
**Decision Date**: 2025-09-30
**Priority**: 🚨 CRITICAL USER SAFETY
**Status**: ✅ APPROVED - BEGIN IMMEDIATELY