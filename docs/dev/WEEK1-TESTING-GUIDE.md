# Week 1 Safety Features - Testing Guide

**Status**: ✅ Implementation Complete
**Date**: 2025-09-30

---

## 🚀 Quick Start Testing

### 1. Deploy Database Schema

```bash
# Ensure PostgreSQL is running
brew services start postgresql

# Create database if needed
createdb bmad_auto

# Apply schema
psql bmad_auto < .bmad-auto/database/schema/state_persistence.sql
```

### 2. Run Automated Tests

```bash
# Run all Week 1 tests
.bmad-auto/tests/run_week1_tests.sh

# Or run individually
python3 -m pytest .bmad-auto/tests/integration/test_git_coordinator.py -v
python3 -m pytest .bmad-auto/tests/integration/test_workflow_state.py -v
```

---

## 🧪 Manual Testing - Git Coordinator

### Test 1: Auto-Commit Functionality

```python
from integration.git_coordinator import GitCoordinator

git = GitCoordinator()

# Test auto-commit
result = git.auto_commit(
    agent_name="James",
    task_id="T037",
    description="Manual test of git coordinator"
)

print(f"Success: {result['success']}")
print(f"Commit: {result['commit_hash'][:8]}")
print(f"Message: {result['message']}")
```

**Expected Output**:
```
Success: True
Commit: abc12345
Message: [James] T037: Manual test of git coordinator
...
```

### Test 2: Checkpoint Creation

```python
from integration.git_coordinator import GitCoordinator

git = GitCoordinator()

# Create checkpoint
checkpoint = git.create_checkpoint(
    name="before-refactor",
    description="Safe point before major refactoring"
)

print(f"Success: {checkpoint['success']}")
print(f"Checkpoint: {checkpoint['checkpoint_name']}")
print(f"Tag: {checkpoint['tag']}")
print(f"Commit: {checkpoint['commit_hash'][:8]}")
```

**Expected Output**:
```
Success: True
Checkpoint: before-refactor
Tag: checkpoint-before-refactor
Commit: def45678
```

### Test 3: Git Status

```python
from integration.git_coordinator import GitCoordinator

git = GitCoordinator()

# Get status
status = git.get_status()

print(f"Branch: {status['branch']}")
print(f"Has changes: {status['has_changes']}")
print(f"Recent commits:\n{status['recent_commits']}")
print(f"Checkpoints: {status['checkpoints']}")
```

### Test 4: Rollback

```python
from integration.git_coordinator import GitCoordinator

git = GitCoordinator()

# Create a test commit
git.auto_commit("James", "TEST-ROLLBACK", "Commit to rollback")

# Rollback
result = git.rollback(commits=1)

print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
```

### Test 5: Restore Checkpoint

```python
from integration.git_coordinator import GitCoordinator

git = GitCoordinator()

# Restore to checkpoint
result = git.restore_checkpoint("before-refactor")

print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
```

---

## 🧪 Manual Testing - Workflow State Persistence

### Test 1: Save Session State

```python
import asyncio
from orchestration.workflow_state import WorkflowStatePersistence

async def test_save():
    state = WorkflowStatePersistence("postgresql://localhost/bmad_auto")
    await state.initialize()

    success = await state.save_conversation_state(
        session_id="manual-test-001",
        messages=[
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ],
        agent_contexts={"james": {"task": "T037"}},
        task_progress={"T037": "in_progress"},
        current_task="T037"
    )

    print(f"Save success: {success}")
    await state.close()

asyncio.run(test_save())
```

### Test 2: Restore Session State

```python
import asyncio
from orchestration.workflow_state import WorkflowStatePersistence

async def test_restore():
    state = WorkflowStatePersistence("postgresql://localhost/bmad_auto")
    await state.initialize()

    restored = await state.restore_session("manual-test-001")

    if restored:
        print(f"Session ID: {restored['session_id']}")
        print(f"Messages: {len(restored['messages'])}")
        print(f"Current task: {restored['current_task']}")
        print(f"Agent contexts: {restored['agent_contexts']}")
    else:
        print("Session not found")

    await state.close()

asyncio.run(test_restore())
```

### Test 3: Database Checkpoint

```python
import asyncio
from orchestration.workflow_state import WorkflowStatePersistence

async def test_checkpoint():
    state = WorkflowStatePersistence("postgresql://localhost/bmad_auto")
    await state.initialize()

    success = await state.create_checkpoint(
        name="manual-checkpoint-001",
        description="Testing checkpoint functionality",
        git_commit_hash="abc123",
        session_state={
            "messages": [{"role": "user", "content": "Test"}],
            "agent_contexts": {}
        }
    )

    print(f"Checkpoint success: {success}")
    await state.close()

asyncio.run(test_checkpoint())
```

### Test 4: List Sessions

```python
import asyncio
from orchestration.workflow_state import WorkflowStatePersistence

async def test_list():
    state = WorkflowStatePersistence("postgresql://localhost/bmad_auto")
    await state.initialize()

    sessions = await state.list_sessions(limit=10)

    print(f"Found {len(sessions)} sessions:")
    for session in sessions:
        print(f"  - {session['session_id']} (updated: {session['updated_at']})")

    await state.close()

asyncio.run(test_list())
```

---

## 🧪 Manual Testing - Safety Commands

### Test 1: Checkpoint Command

```python
from integration.git_coordinator import GitCoordinator
from orchestration.workflow_state import WorkflowStatePersistence
from commands.safety_commands import SafetyCommands

git = GitCoordinator()
# Note: For full testing, initialize state with database
state = None  # Would be WorkflowStatePersistence instance

commands = SafetyCommands(git, state)

# Create checkpoint
result = commands.handle_checkpoint(
    name="feature-complete",
    description="Feature implementation complete"
)

print(result)
```

### Test 2: Status Command

```python
from integration.git_coordinator import GitCoordinator
from commands.safety_commands import SafetyCommands

git = GitCoordinator()
commands = SafetyCommands(git, None)

# Get status
result = commands.handle_status()

print(result)
```

### Test 3: List Checkpoints

```python
from integration.git_coordinator import GitCoordinator
from commands.safety_commands import SafetyCommands

git = GitCoordinator()
commands = SafetyCommands(git, None)

# List checkpoints
result = commands.handle_list_checkpoints()

print(result)
```

### Test 4: Rollback Command

```python
from integration.git_coordinator import GitCoordinator
from commands.safety_commands import SafetyCommands

git = GitCoordinator()
commands = SafetyCommands(git, None)

# Rollback 1 commit
result = commands.handle_rollback(commits=1)

print(result)
```

---

## ✅ Week 1 Deliverables Checklist

### Git Integration
- [x] `git_coordinator.py` - Auto-commit functionality
- [x] Integration with agent system
- [x] Checkpoint creation working
- [x] Rollback capability tested
- [x] Status reporting functional

### State Persistence
- [x] Database schema deployed
- [x] `workflow_state.py` - Save/restore working
- [x] Session state persists across restarts
- [x] Restore time <30 seconds (target)
- [x] Checkpoint database integration

### User Commands
- [x] `/checkpoint` - Create named restore points
- [x] `/rollback` - Undo commits
- [x] `/status` - View current state
- [x] `/restore` - Restore checkpoints
- [x] Commands ready for PM agent integration

### Testing
- [x] Git operations tested with real commits
- [x] State persistence test suite created
- [x] Integration tests implemented
- [x] Manual testing guide documented

---

## 🎯 Next Steps

1. **Integration with PM Agent**: Hook safety commands into PM orchestration hub
2. **Auto-commit Hooks**: Integrate auto-commit into agent task lifecycle
3. **User Interface**: Add safety commands to PM dashboard
4. **Monitoring**: Add LangFuse monitoring for safety operations
5. **Documentation**: Update user documentation with safety features

---

**Status**: ✅ Week 1 Complete - All Deliverables Implemented
**Testing**: Manual and automated tests ready
**Ready for**: PM Integration (Week 2)