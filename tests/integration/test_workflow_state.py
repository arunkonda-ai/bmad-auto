"""
Integration tests for Workflow State Persistence
Tests session save/restore and checkpoint functionality
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from orchestration.workflow_state import WorkflowStatePersistence


class TestWorkflowStatePersistence:
    """Test suite for WorkflowStatePersistence"""

    @pytest.fixture
    async def state_manager(self):
        """Create WorkflowStatePersistence instance"""
        # Use test database connection
        conn_string = "postgresql://localhost/bmad_auto"
        state = WorkflowStatePersistence(conn_string)
        await state.initialize()
        yield state
        await state.close()

    @pytest.mark.asyncio
    async def test_save_and_restore_session(self, state_manager):
        """Test saving and restoring session state"""
        session_id = "test-session-001"
        messages = [
            {"role": "user", "content": "Test message 1"},
            {"role": "assistant", "content": "Test response 1"}
        ]
        agent_contexts = {"james": {"current_task": "T037"}}
        task_progress = {"T037": "in_progress"}

        # Save session
        success = await state_manager.save_conversation_state(
            session_id=session_id,
            messages=messages,
            agent_contexts=agent_contexts,
            task_progress=task_progress,
            current_task="T037"
        )

        assert success is True

        # Restore session
        restored = await state_manager.restore_session(session_id)

        assert restored is not None
        assert restored["session_id"] == session_id
        assert len(restored["messages"]) == 2
        assert restored["agent_contexts"]["james"]["current_task"] == "T037"
        assert restored["current_task"] == "T037"

    @pytest.mark.asyncio
    async def test_create_checkpoint(self, state_manager):
        """Test checkpoint creation"""
        checkpoint_name = "test-checkpoint"
        session_state = {
            "messages": [{"role": "user", "content": "Test"}],
            "agent_contexts": {},
            "task_progress": {}
        }

        success = await state_manager.create_checkpoint(
            name=checkpoint_name,
            description="Test checkpoint",
            git_commit_hash="abc123",
            session_state=session_state
        )

        assert success is True

    @pytest.mark.asyncio
    async def test_restore_checkpoint(self, state_manager):
        """Test checkpoint restoration"""
        checkpoint_name = "test-restore-checkpoint"
        session_state = {
            "messages": [{"role": "user", "content": "Checkpoint test"}],
            "agent_contexts": {"test": "data"},
            "task_progress": {"T001": "completed"}
        }

        # Create checkpoint
        await state_manager.create_checkpoint(
            name=checkpoint_name,
            description="Test restoration",
            git_commit_hash="def456",
            session_state=session_state
        )

        # Restore checkpoint
        restored = await state_manager.restore_checkpoint(checkpoint_name)

        assert restored is not None
        assert restored["name"] == checkpoint_name
        assert restored["git_commit"] == "def456"
        assert restored["session_state"]["agent_contexts"]["test"] == "data"

    @pytest.mark.asyncio
    async def test_list_sessions(self, state_manager):
        """Test listing recent sessions"""
        # Create test sessions
        for i in range(3):
            await state_manager.save_conversation_state(
                session_id=f"test-session-{i}",
                messages=[{"role": "user", "content": f"Message {i}"}]
            )

        # List sessions
        sessions = await state_manager.list_sessions(limit=5)

        assert len(sessions) >= 3
        assert all("session_id" in s for s in sessions)

    @pytest.mark.asyncio
    async def test_list_checkpoints(self, state_manager):
        """Test listing all checkpoints"""
        # Create test checkpoints
        for i in range(2):
            await state_manager.create_checkpoint(
                name=f"test-list-checkpoint-{i}",
                description=f"Checkpoint {i}",
                git_commit_hash=f"hash{i}",
                session_state={}
            )

        # List checkpoints
        checkpoints = await state_manager.list_checkpoints()

        assert len(checkpoints) >= 2
        assert all("name" in cp for cp in checkpoints)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])