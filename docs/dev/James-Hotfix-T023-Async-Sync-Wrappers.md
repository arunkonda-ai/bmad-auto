# James (Developer) - HOTFIX: T023 Async/Sync Wrapper Implementation

**Date**: 2025-09-29
**Assigned By**: John (PM)
**Priority**: 🚨 **CRITICAL BLOCKER** - Unblocks 15 tests
**Estimated Time**: 2 hours
**Architectural Guidance**: Winston (Architect) - Option 1 implementation
**Update Progress In**: `.bmad-auto/docs/dev/Dev-sessions-specs-progress.md`

---

## 🎯 HOTFIX OBJECTIVE

Add synchronous wrapper methods to `AgentStateManager` class to enable testing and CLI usage while preserving async architecture for future scaling.

**Why This Approach**:
- ✅ Unblocks 15 tests immediately
- ✅ Preserves async foundation for 10-agent concurrent operations (NFR3A)
- ✅ Minimal code changes (2 hours vs 6 hours for rewrite)
- ✅ Architect-approved solution
- ✅ Maintains BMAD compliance (file stays under 300 lines)

---

## 📋 IMPLEMENTATION SPECIFICATION

### **File to Modify**: `.bmad-auto/orchestration/agent_manager.py`

**Current Line Count**: 254 lines
**Target Line Count**: 280-295 lines (adding ~40 lines of sync wrappers)
**BMAD Compliance**: ✅ Still within 300-line limit

---

## 🔧 SYNC WRAPPER IMPLEMENTATION

### **Pattern**: Add synchronous wrapper methods for all public async methods

**Implementation Template**:

```python
# Add these methods to AgentStateManager class (starting around line 250)

    # ==========================================
    # SYNCHRONOUS WRAPPER METHODS
    # For CLI and test usage - call async methods via asyncio.run()
    # ==========================================

    def register_agent_sync(
        self,
        agent_id: str,
        agent_name: str,
        capabilities: List[str]
    ) -> bool:
        """
        Synchronous wrapper for register_agent.

        Use this method for CLI operations and testing.
        For async contexts, use register_agent() directly.
        """
        import asyncio
        return asyncio.run(self.register_agent(agent_id, agent_name, capabilities))

    def update_agent_status_sync(
        self,
        agent_id: str,
        status: AgentStatus,
        current_task: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Synchronous wrapper for update_agent_status.

        Use this method for CLI operations and testing.
        For async contexts, use update_agent_status() directly.
        """
        import asyncio
        return asyncio.run(
            self.update_agent_status(agent_id, status, current_task, error_message)
        )

    def get_agent_status_sync(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Synchronous wrapper for get_agent_status.

        Use this method for CLI operations and testing.
        For async contexts, use get_agent_status() directly.
        """
        import asyncio
        return asyncio.run(self.get_agent_status(agent_id))

    def get_all_agents_sync(
        self,
        status_filter: Optional[AgentStatus] = None
    ) -> List[Dict[str, Any]]:
        """
        Synchronous wrapper for get_all_agents.

        Use this method for CLI operations and testing.
        For async contexts, use get_all_agents() directly.
        """
        import asyncio
        return asyncio.run(self.get_all_agents(status_filter))

    def send_message_sync(
        self,
        from_agent: str,
        to_agent: str,
        message: Dict[str, Any]
    ) -> bool:
        """
        Synchronous wrapper for send_message.

        Use this method for CLI operations and testing.
        For async contexts, use send_message() directly.
        """
        import asyncio
        return asyncio.run(self.send_message(from_agent, to_agent, message))

    def get_agent_messages_sync(
        self,
        agent_id: str,
        mark_as_read: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Synchronous wrapper for get_agent_messages.

        Use this method for CLI operations and testing.
        For async contexts, use get_agent_messages() directly.
        """
        import asyncio
        return asyncio.run(self.get_agent_messages(agent_id, mark_as_read))

    def check_agent_health_sync(self, agent_id: str) -> Dict[str, Any]:
        """
        Synchronous wrapper for check_agent_health.

        Use this method for CLI operations and testing.
        For async contexts, use check_agent_health() directly.
        """
        import asyncio
        return asyncio.run(self.check_agent_health(agent_id))
```

---

## 📚 IMPLEMENTATION CHECKLIST

### **Phase 1: Add Sync Wrappers** (30 minutes)

- [ ] Open `.bmad-auto/orchestration/agent_manager.py`
- [ ] Locate end of `AgentStateManager` class (around line 250)
- [ ] Add comment section: "SYNCHRONOUS WRAPPER METHODS"
- [ ] Implement 7 sync wrapper methods:
  - [ ] `register_agent_sync()`
  - [ ] `update_agent_status_sync()`
  - [ ] `get_agent_status_sync()`
  - [ ] `get_all_agents_sync()`
  - [ ] `send_message_sync()`
  - [ ] `get_agent_messages_sync()`
  - [ ] `check_agent_health_sync()`

### **Phase 2: Add Documentation** (15 minutes)

- [ ] Add module-level docstring explaining sync vs async usage:

```python
"""
Agent State Synchronization - Real-time agent status tracking and coordination.

Provides concurrent 10-agent state management with inter-agent communication
and session recovery capabilities.

USAGE PATTERNS:
--------------
For async contexts (FastAPI, LangGraph workflows):
    manager = AgentStateManager()
    await manager.register_agent('pm', 'John', ['orchestration'])

For synchronous contexts (CLI, testing):
    manager = AgentStateManager()
    manager.register_agent_sync('pm', 'John', ['orchestration'])

All async methods have corresponding *_sync() wrappers using asyncio.run().
"""
```

### **Phase 3: Validate BMAD Compliance** (15 minutes)

- [ ] Check file line count:
```bash
wc -l .bmad-auto/orchestration/agent_manager.py
# Expected: 280-295 lines (within 300-line limit) ✓
```

- [ ] Run basic import test:
```python
from orchestration.agent_manager import AgentStateManager
manager = AgentStateManager()
# Should import without errors
print("AgentStateManager imported successfully")
```

### **Phase 4: Smoke Test Sync Wrappers** (30 minutes)

- [ ] Test `register_agent_sync()`:
```python
from orchestration.agent_manager import AgentStateManager, AgentStatus

manager = AgentStateManager()
result = manager.register_agent_sync('pm', 'John', ['orchestration'])
print(f"Register result: {result}")  # Should be True

status = manager.get_agent_status_sync('pm')
print(f"Agent status: {status}")  # Should return dict with agent info
```

- [ ] Test `update_agent_status_sync()`:
```python
result = manager.update_agent_status_sync(
    'pm',
    AgentStatus.BUSY,
    current_task='Testing sync wrappers'
)
print(f"Update result: {result}")  # Should be True
```

- [ ] Test error handling:
```python
# Test with non-existent agent
status = manager.get_agent_status_sync('nonexistent')
print(f"Nonexistent agent status: {status}")  # Should be None
```

### **Phase 5: Update Progress** (15 minutes)

- [ ] Update Dev-sessions-specs-progress.md:

```markdown
## 🔥 HOTFIX: T023 Async/Sync Wrapper Implementation - James

**Hotfix Date**: 2025-09-29
**Developer**: James
**Duration**: [Actual time spent]
**Issue**: Async/sync architecture mismatch blocking 15 tests

### Implementation Details:
- **File Modified**: `.bmad-auto/orchestration/agent_manager.py`
- **Lines Added**: ~40 lines (sync wrappers)
- **Final Line Count**: [Actual count] lines
- **BMAD Compliance**: ✅ Within 300-line limit

### Sync Wrappers Added:
- ✅ `register_agent_sync()`
- ✅ `update_agent_status_sync()`
- ✅ `get_agent_status_sync()`
- ✅ `get_all_agents_sync()`
- ✅ `send_message_sync()`
- ✅ `get_agent_messages_sync()`
- ✅ `check_agent_health_sync()`

### Testing Results:
- ✅ Import test passed
- ✅ Register agent sync test passed
- ✅ Update status sync test passed
- ✅ Error handling validated

### Recommendations:
- ✅ Hotfix complete, ready for Quinn's testing
- ✅ Notify Quinn to resume T023-T024 testing
- ✅ Document sync vs async usage patterns for team
```

---

## 🧪 TESTING VALIDATION

### **Success Criteria**:

1. ✅ **All sync wrappers functional**: Can call without `await`
2. ✅ **Async core preserved**: Original async methods unchanged
3. ✅ **BMAD compliance**: File stays under 300 lines
4. ✅ **Smoke tests pass**: Basic registration and status update work
5. ✅ **Quinn unblocked**: QA can resume testing with sync methods

### **Test Script for Quick Validation**:

```python
#!/usr/bin/env python3
"""Quick validation script for sync wrapper implementation."""

from orchestration.agent_manager import AgentStateManager, AgentStatus

def test_sync_wrappers():
    """Test all sync wrapper methods."""
    print("🧪 Testing AgentStateManager sync wrappers...\n")

    manager = AgentStateManager()

    # Test 1: Register agent
    print("Test 1: Register agent sync")
    result = manager.register_agent_sync('pm', 'John', ['orchestration'])
    assert result == True, "Register agent failed"
    print("✅ PASSED\n")

    # Test 2: Get agent status
    print("Test 2: Get agent status sync")
    status = manager.get_agent_status_sync('pm')
    assert status is not None, "Get status failed"
    assert status['agent_id'] == 'pm', "Agent ID mismatch"
    print(f"✅ PASSED - Status: {status}\n")

    # Test 3: Update agent status
    print("Test 3: Update agent status sync")
    result = manager.update_agent_status_sync(
        'pm',
        AgentStatus.BUSY,
        current_task='Testing'
    )
    assert result == True, "Update status failed"
    print("✅ PASSED\n")

    # Test 4: Get all agents
    print("Test 4: Get all agents sync")
    agents = manager.get_all_agents_sync()
    assert len(agents) > 0, "No agents found"
    print(f"✅ PASSED - Found {len(agents)} agents\n")

    # Test 5: Error handling
    print("Test 5: Error handling (non-existent agent)")
    status = manager.get_agent_status_sync('nonexistent')
    assert status is None, "Should return None for non-existent agent"
    print("✅ PASSED\n")

    print("🎉 All sync wrapper tests passed!")
    return True

if __name__ == "__main__":
    try:
        test_sync_wrappers()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
```

**Run the test**:
```bash
cd .bmad-auto
python3 -c "from orchestration.agent_manager import AgentStateManager; m = AgentStateManager(); print('✅ Import successful')"
```

---

## 🚨 COMMON ISSUES & SOLUTIONS

### **Issue 1: Import Error on asyncio.run()**
❌ **Error**: `RuntimeError: asyncio.run() cannot be called from a running event loop`

✅ **Solution**: This is expected if testing within Jupyter or async context. Use regular async methods in those contexts. Sync wrappers are for CLI and pytest only.

### **Issue 2: Event Loop Warnings**
⚠️ **Warning**: "Task was destroyed but it is pending"

✅ **Solution**: This is harmless for sync wrappers. The asyncio.run() creates a new event loop per call, which is intentional.

### **Issue 3: Performance Concerns**
⚠️ **Concern**: Creating new event loop per call may be slow

✅ **Response**: This is acceptable for CLI and testing. For production high-performance scenarios, use async methods directly. Sync wrappers are convenience methods.

---

## 📞 ESCALATION & QUESTIONS

### **If You Encounter Issues**:

1. **Import errors**: Verify Python 3.11+ and all dependencies installed
2. **Async errors**: Ensure you're not testing within an existing event loop
3. **File size concerns**: Extract documentation to separate file if needed
4. **Functional issues**: Verify async core methods work with manual `await` testing

### **Escalate to John (PM) If**:
- Cannot add wrappers within 300-line BMAD limit
- Async core methods have bugs preventing wrapper implementation
- Significant architectural issues discovered during implementation
- Cannot complete within 2-hour estimate

---

## 🎯 COMPLETION CRITERIA

### **Hotfix Complete When**:

1. ✅ All 7 sync wrapper methods implemented
2. ✅ Documentation added (module docstring + method docstrings)
3. ✅ BMAD compliance verified (file < 300 lines)
4. ✅ Smoke tests pass (registration + status update)
5. ✅ Progress updated in Dev-sessions-specs-progress.md
6. ✅ Quinn notified to resume testing

### **Expected Outcome**:
- Quinn can immediately resume T023-T024 testing
- 15 blocked tests can now execute
- Async architecture preserved for future scaling
- MVP timeline stays on track

---

## 🚀 READY TO IMPLEMENT?

### **Pre-Implementation Checklist**:
- [ ] Read Quinn's testing results (T021-T024-Testing-Results-Quinn.md)
- [ ] Review Winston's architectural analysis (Option 1 guidance)
- [ ] Understand sync wrapper pattern (`asyncio.run()` for each async method)
- [ ] Development environment ready (Python 3.11+, all dependencies)

### **Implementation Time**: 2 hours
- 30 min: Add sync wrappers
- 15 min: Add documentation
- 15 min: Validate BMAD compliance
- 30 min: Smoke test sync wrappers
- 15 min: Update progress
- 15 min: Buffer for issues

---

**Start Implementation Now** - Quinn is standing by to resume testing immediately after this hotfix!

**Good luck, James! This hotfix unblocks 15 tests and keeps the MVP on track.**

---

**Document Created**: 2025-09-29
**Priority**: 🚨 CRITICAL BLOCKER
**Estimated Duration**: 2 hours
**Dependencies**: None (can start immediately)
**Update Progress In**: `.bmad-auto/docs/dev/Dev-sessions-specs-progress.md`
**Notify When Complete**: Quinn (QA) - Ready to resume testing