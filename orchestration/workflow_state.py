"""
Workflow State Persistence - Core MVP
Saves conversation and agent state to prevent data loss
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
import asyncpg


class WorkflowStatePersistence:
    """
    PostgreSQL-backed state management for session persistence

    Features:
    - Save conversation history after each message
    - Preserve agent working contexts
    - Track task progress
    - Quick restore on system restart
    """

    def __init__(self, db_connection_string: str):
        self.conn_string = db_connection_string
        self.pool: Optional[asyncpg.Pool] = None

    async def initialize(self):
        """Initialize database connection pool"""
        self.pool = await asyncpg.create_pool(
            self.conn_string,
            min_size=2,
            max_size=10
        )

    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()

    async def save_conversation_state(
        self,
        session_id: str,
        messages: List[Dict],
        agent_contexts: Optional[Dict] = None,
        task_progress: Optional[Dict] = None,
        current_task: Optional[str] = None
    ) -> bool:
        """
        Save complete conversation state

        Args:
            session_id: Unique session identifier
            messages: List of conversation messages
            agent_contexts: Current agent working memory
            task_progress: Status of in-progress tasks
            current_task: Active task identifier

        Returns:
            True if save successful
        """
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO session_state (
                        session_id,
                        conversation_history,
                        agent_contexts,
                        task_progress,
                        current_task,
                        updated_at
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (session_id) DO UPDATE SET
                        conversation_history = $2,
                        agent_contexts = $3,
                        task_progress = $4,
                        current_task = $5,
                        updated_at = $6
                    """,
                    session_id,
                    json.dumps(messages),
                    json.dumps(agent_contexts) if agent_contexts else None,
                    json.dumps(task_progress) if task_progress else None,
                    current_task,
                    datetime.now()
                )

            return True

        except Exception as e:
            print(f"❌ Failed to save state: {e}")
            return False

    async def restore_session(self, session_id: str) -> Optional[Dict]:
        """
        Restore complete session state

        Args:
            session_id: Session to restore

        Returns:
            Dict with session state or None if not found
        """
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT
                        conversation_history,
                        agent_contexts,
                        task_progress,
                        current_task,
                        created_at,
                        updated_at
                    FROM session_state
                    WHERE session_id = $1
                    """,
                    session_id
                )

                if not row:
                    return None

                return {
                    "session_id": session_id,
                    "messages": json.loads(row["conversation_history"]),
                    "agent_contexts": json.loads(row["agent_contexts"]) if row["agent_contexts"] else {},
                    "task_progress": json.loads(row["task_progress"]) if row["task_progress"] else {},
                    "current_task": row["current_task"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                }

        except Exception as e:
            print(f"❌ Failed to restore session: {e}")
            return None

    async def list_sessions(self, limit: int = 10) -> List[Dict]:
        """
        List recent sessions

        Args:
            limit: Maximum number of sessions to return

        Returns:
            List of session summaries
        """
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT
                        session_id,
                        current_task,
                        created_at,
                        updated_at
                    FROM session_state
                    ORDER BY updated_at DESC
                    LIMIT $1
                    """,
                    limit
                )

                return [
                    {
                        "session_id": row["session_id"],
                        "current_task": row["current_task"],
                        "created_at": row["created_at"],
                        "updated_at": row["updated_at"]
                    }
                    for row in rows
                ]

        except Exception as e:
            print(f"❌ Failed to list sessions: {e}")
            return []

    async def create_checkpoint(
        self,
        name: str,
        description: str,
        git_commit_hash: str,
        session_state: Dict
    ) -> bool:
        """
        Create named checkpoint for restoration

        Args:
            name: Checkpoint identifier
            description: What this checkpoint represents
            git_commit_hash: Associated git commit
            session_state: Complete session state

        Returns:
            True if successful
        """
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO checkpoints (name, description, git_commit_hash, session_state)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (name) DO UPDATE SET
                        description = $2,
                        git_commit_hash = $3,
                        session_state = $4,
                        created_at = CURRENT_TIMESTAMP
                    """,
                    name,
                    description,
                    git_commit_hash,
                    json.dumps(session_state)
                )

            return True

        except Exception as e:
            print(f"❌ Failed to create checkpoint: {e}")
            return False

    async def restore_checkpoint(self, name: str) -> Optional[Dict]:
        """
        Restore session from named checkpoint

        Args:
            name: Checkpoint to restore

        Returns:
            Dict with checkpoint data or None
        """
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(
                    """
                    SELECT git_commit_hash, session_state, created_at
                    FROM checkpoints
                    WHERE name = $1
                    """,
                    name
                )

                if not row:
                    return None

                return {
                    "name": name,
                    "git_commit": row["git_commit_hash"],
                    "session_state": json.loads(row["session_state"]),
                    "created_at": row["created_at"]
                }

        except Exception as e:
            print(f"❌ Failed to restore checkpoint: {e}")
            return None

    async def list_checkpoints(self) -> List[Dict]:
        """
        List all available checkpoints

        Returns:
            List of checkpoint summaries
        """
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT
                        name,
                        description,
                        git_commit_hash,
                        created_at
                    FROM checkpoints
                    ORDER BY created_at DESC
                    """
                )

                return [
                    {
                        "name": row["name"],
                        "description": row["description"],
                        "git_commit": row["git_commit_hash"],
                        "created_at": row["created_at"]
                    }
                    for row in rows
                ]

        except Exception as e:
            print(f"❌ Failed to list checkpoints: {e}")
            return []