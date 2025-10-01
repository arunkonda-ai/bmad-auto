# 🚨 James: URGENT - Safety Features Implementation

**Date**: 2025-09-30
**Priority**: 🚨 CRITICAL - User Data Loss Prevention
**Duration**: Week 1 (24 hours total)
**Status**: IMMEDIATE START REQUIRED

---

## 🎯 Mission Critical

**User Problem**: Data loss and no rollback capability causing productivity blocker

**Your Task**: Implement safety infrastructure BEFORE continuing API work

**Why This Matters**: User cannot work effectively without safety net. This blocks everything else.

---

## 📋 Week 1 Implementation Plan

### Day 1-2: Git Integration (T037 Simplified) - 8 hours

#### Task 1: Basic Git Coordinator (4 hours)

**File**: `.bmad-auto/integration/git_coordinator.py` (target: 250 lines)

**Core Functionality**:

```python
"""
Git Coordinator - Automatic Version Control for Agent Safety
Simplified MVP: Local git operations only, no GitHub API
"""

import subprocess
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class GitCoordinator:
    """
    Automatic git operations for agent work safety

    Features:
    - Auto-commit after each agent task
    - Named checkpoints for safe experimentation
    - Easy rollback for mistakes
    - Clear status visibility
    """

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self._verify_git_repo()

    def _verify_git_repo(self):
        """Verify this is a git repository"""
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise ValueError(f"Not a git repository: {self.repo_path}")

    def auto_commit(
        self,
        agent_name: str,
        task_id: str,
        description: str,
        files: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Automatically commit agent work

        Args:
            agent_name: Agent who made changes (e.g., "James")
            task_id: Task identifier (e.g., "T037")
            description: What was done
            files: Specific files to commit (None = all changes)

        Returns:
            Dict with commit_hash, message, timestamp
        """
        try:
            # Stage files
            if files:
                for file in files:
                    subprocess.run(
                        ["git", "add", file],
                        cwd=self.repo_path,
                        check=True
                    )
            else:
                # Stage all changes
                subprocess.run(
                    ["git", "add", "."],
                    cwd=self.repo_path,
                    check=True
                )

            # Create commit message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            commit_message = f"""[{agent_name}] {task_id}: {description}

Agent: {agent_name}
Task: {task_id}
Timestamp: {timestamp}
Auto-committed by BMAD Auto safety system
"""

            # Commit changes
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            # Get commit hash
            commit_hash = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            return {
                "success": True,
                "commit_hash": commit_hash,
                "message": commit_message,
                "timestamp": timestamp
            }

        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": str(e),
                "stderr": e.stderr if hasattr(e, 'stderr') else ""
            }

    def create_checkpoint(self, name: str, description: str) -> Dict:
        """
        Create named checkpoint for easy restoration

        Args:
            name: Checkpoint name (e.g., "before-api-work")
            description: What this checkpoint represents

        Returns:
            Dict with checkpoint info
        """
        try:
            # First commit any outstanding changes
            self.auto_commit(
                agent_name="System",
                task_id="CHECKPOINT",
                description=f"Checkpoint: {name}"
            )

            # Get current commit
            commit_hash = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            # Create git tag for checkpoint
            tag_name = f"checkpoint-{name}"
            subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", description],
                cwd=self.repo_path,
                check=True
            )

            return {
                "success": True,
                "checkpoint_name": name,
                "tag": tag_name,
                "commit_hash": commit_hash,
                "description": description
            }

        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": str(e)
            }

    def rollback(self, commits: int = 1) -> Dict:
        """
        Rollback last N commits (soft reset - keeps changes)

        Args:
            commits: Number of commits to undo

        Returns:
            Dict with rollback status
        """
        try:
            # Soft reset (keeps working directory changes)
            subprocess.run(
                ["git", "reset", "--soft", f"HEAD~{commits}"],
                cwd=self.repo_path,
                check=True
            )

            return {
                "success": True,
                "commits_rolled_back": commits,
                "message": f"Rolled back {commits} commit(s). Changes preserved in working directory."
            }

        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": str(e)
            }

    def restore_checkpoint(self, checkpoint_name: str) -> Dict:
        """
        Restore to named checkpoint

        Args:
            checkpoint_name: Name of checkpoint to restore

        Returns:
            Dict with restore status
        """
        try:
            tag_name = f"checkpoint-{checkpoint_name}"

            # Reset to checkpoint tag
            subprocess.run(
                ["git", "reset", "--hard", tag_name],
                cwd=self.repo_path,
                check=True
            )

            return {
                "success": True,
                "checkpoint": checkpoint_name,
                "message": f"Restored to checkpoint: {checkpoint_name}"
            }

        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Checkpoint '{checkpoint_name}' not found"
            }

    def get_status(self) -> Dict:
        """
        Get current git status and recent commits

        Returns:
            Dict with status info
        """
        try:
            # Current branch
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            # Uncommitted changes
            status = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout

            # Recent commits (last 5)
            log = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout

            # Available checkpoints
            tags = subprocess.run(
                ["git", "tag", "-l", "checkpoint-*"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip().split("\n")

            checkpoints = [t.replace("checkpoint-", "") for t in tags if t]

            return {
                "success": True,
                "branch": branch,
                "uncommitted_changes": status,
                "has_changes": bool(status.strip()),
                "recent_commits": log,
                "checkpoints": checkpoints
            }

        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": str(e)
            }
```

**Testing** (30 minutes):
```python
# Test file: tests/integration/test_git_coordinator.py
def test_auto_commit():
    git = GitCoordinator()
    result = git.auto_commit(
        agent_name="James",
        task_id="T037",
        description="Git coordinator implementation"
    )
    assert result["success"] == True
    assert "commit_hash" in result
```

---

#### Task 2: Integration with Agent System (4 hours)

**File**: `.bmad-auto/orchestration/agent_git_integration.py` (target: 150 lines)

```python
"""
Agent Git Integration
Automatically commits agent work after task completion
"""

from integration.git_coordinator import GitCoordinator
from orchestration.agent_manager import AgentStateManager

class AgentGitIntegration:
    """
    Hooks git coordinator into agent lifecycle
    Auto-commits after each agent task
    """

    def __init__(self, git_coordinator: GitCoordinator, agent_manager: AgentStateManager):
        self.git = git_coordinator
        self.agents = agent_manager

    async def on_task_complete(self, agent_id: str, task_id: str, task_result: Dict):
        """
        Called when agent completes task
        Automatically commits the work
        """
        # Get agent info
        agent_state = await self.agents.get_agent_status(agent_id)
        agent_name = agent_state.get("agent_name", agent_id)

        # Get changed files
        files = task_result.get("modified_files", None)

        # Auto-commit
        commit_result = self.git.auto_commit(
            agent_name=agent_name,
            task_id=task_id,
            description=task_result.get("description", "Task completed"),
            files=files
        )

        # Log result
        if commit_result["success"]:
            print(f"✅ Auto-committed: {commit_result['commit_hash'][:8]}")
        else:
            print(f"⚠️  Commit failed: {commit_result.get('error')}")

        return commit_result
```

---

### Day 3-4: State Persistence (T029 Core) - 12 hours

#### Task 3: Database Schema for State (2 hours)

**File**: `.bmad-auto/database/schema/state_persistence.sql`

```sql
-- Session state persistence
CREATE TABLE IF NOT EXISTS session_state (
    session_id TEXT PRIMARY KEY,
    conversation_history JSONB NOT NULL,
    agent_contexts JSONB,
    task_progress JSONB,
    current_task TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Checkpoints for user safety
CREATE TABLE IF NOT EXISTS checkpoints (
    checkpoint_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    git_commit_hash TEXT,
    session_state JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_session_updated ON session_state(updated_at);
CREATE INDEX idx_checkpoint_name ON checkpoints(name);
```

---

#### Task 4: State Persistence Implementation (8 hours)

**File**: `.bmad-auto/orchestration/workflow_state.py` (target: 280 lines)

```python
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
        self.pool = await asyncpg.create_pool(self.conn_string)

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
```

---

### Day 5: User Safety Commands (4 hours)

**File**: `.bmad-auto/commands/safety_commands.py` (target: 200 lines)

```python
"""
User Safety Commands
Easy-to-use commands for git and state management
"""

from integration.git_coordinator import GitCoordinator
from orchestration.workflow_state import WorkflowStatePersistence

class SafetyCommands:
    """User-facing safety command handlers"""

    def __init__(self, git: GitCoordinator, state: WorkflowStatePersistence):
        self.git = git
        self.state = state

    def handle_checkpoint(self, name: str, description: str) -> str:
        """
        /checkpoint [name] [description]
        Create safe restore point
        """
        # Create git checkpoint
        git_result = self.git.create_checkpoint(name, description)

        if not git_result["success"]:
            return f"❌ Failed to create checkpoint: {git_result.get('error')}"

        # Save session state
        # TODO: Get current session state from coordinator

        return f"""✅ Checkpoint created: {name}

Git tag: {git_result['tag']}
Commit: {git_result['commit_hash'][:8]}

You can restore with: /restore {name}
"""

    def handle_rollback(self, commits: int = 1) -> str:
        """
        /rollback [N]
        Undo last N commits
        """
        result = self.git.rollback(commits)

        if result["success"]:
            return f"""✅ {result['message']}

Run 'git status' to see preserved changes.
To discard changes: git reset --hard HEAD
"""
        else:
            return f"❌ Rollback failed: {result.get('error')}"

    def handle_status(self) -> str:
        """
        /status
        Show current state and recent changes
        """
        result = self.git.get_status()

        if not result["success"]:
            return f"❌ Failed to get status: {result.get('error')}"

        output = f"""📊 System Status

Branch: {result['branch']}

Recent commits:
{result['recent_commits']}

Uncommitted changes:
{result['uncommitted_changes'] if result['has_changes'] else '(none)'}

Available checkpoints:
{chr(10).join(f"  - {cp}" for cp in result['checkpoints']) if result['checkpoints'] else '(none)'}
"""
        return output

    def handle_restore(self, checkpoint_name: str) -> str:
        """
        /restore [checkpoint]
        Restore to named checkpoint
        """
        result = self.git.restore_checkpoint(checkpoint_name)

        if result["success"]:
            return f"""✅ {result['message']}

System restored to checkpoint: {checkpoint_name}
All changes after this point have been discarded.
"""
        else:
            return f"❌ {result.get('message', 'Restore failed')}"
```

---

## ✅ Week 1 Deliverables Checklist

### Git Integration
- [ ] `git_coordinator.py` - Auto-commit functionality
- [ ] Integration with agent system
- [ ] Checkpoint creation working
- [ ] Rollback capability tested
- [ ] Status reporting functional

### State Persistence
- [ ] Database schema deployed
- [ ] `workflow_state.py` - Save/restore working
- [ ] Session state persists across restarts
- [ ] Restore time <30 seconds
- [ ] Checkpoint database integration

### User Commands
- [ ] `/checkpoint` - Create named restore points
- [ ] `/rollback` - Undo commits
- [ ] `/status` - View current state
- [ ] `/restore` - Restore checkpoints
- [ ] Commands integrated with PM agent

### Testing
- [ ] Git operations tested with real commits
- [ ] State persistence tested with system restart
- [ ] User commands tested end-to-end
- [ ] Documentation updated

---

## 🚀 Quick Start

```bash
# Deploy database schema
psql bmad_auto < .bmad-auto/database/schema/state_persistence.sql

# Test git coordinator
python3 -m pytest tests/integration/test_git_coordinator.py

# Test state persistence
python3 -m pytest tests/integration/test_workflow_state.py

# Manual testing
python3 << EOF
from integration.git_coordinator import GitCoordinator

git = GitCoordinator()

# Test auto-commit
result = git.auto_commit("James", "T037", "Initial git integration")
print(result)

# Test checkpoint
checkpoint = git.create_checkpoint("test", "Testing checkpoint")
print(checkpoint)

# Test status
status = git.get_status()
print(status)
EOF
```

---

**Priority**: 🚨 CRITICAL
**Start**: IMMEDIATELY
**User Impact**: ELIMINATES DATA LOSS RISK
**Status**: Ready for implementation

---

**PM Coordinator**: John (PM)
**Assignment**: James (Developer)
**Support**: Quinn (QA) for testing validation