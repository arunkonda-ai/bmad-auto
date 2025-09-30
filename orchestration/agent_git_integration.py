"""
Agent Git Integration
Automatically commits agent work after task completion
"""

from typing import Dict, Optional
from integration.git_coordinator import GitCoordinator


class AgentGitIntegration:
    """
    Hooks git coordinator into agent lifecycle
    Auto-commits after each agent task
    """

    def __init__(self, git_coordinator: GitCoordinator, agent_manager=None):
        self.git = git_coordinator
        self.agents = agent_manager

    async def on_task_complete(
        self,
        agent_id: str,
        task_id: str,
        task_result: Dict
    ) -> Dict:
        """
        Called when agent completes task
        Automatically commits the work

        Args:
            agent_id: Agent identifier
            task_id: Task identifier
            task_result: Task execution results

        Returns:
            Dict with commit result
        """
        # Get agent info
        agent_name = task_result.get("agent_name", agent_id)

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

    def sync_commit(
        self,
        agent_name: str,
        task_id: str,
        description: str,
        files: Optional[list] = None
    ) -> Dict:
        """
        Synchronous version of auto-commit for non-async contexts

        Args:
            agent_name: Agent who made changes
            task_id: Task identifier
            description: What was done
            files: Specific files to commit

        Returns:
            Dict with commit result
        """
        commit_result = self.git.auto_commit(
            agent_name=agent_name,
            task_id=task_id,
            description=description,
            files=files
        )

        if commit_result["success"]:
            print(f"✅ Auto-committed: {commit_result['commit_hash'][:8]}")
        else:
            print(f"⚠️  Commit failed: {commit_result.get('error')}")

        return commit_result

    def create_task_checkpoint(
        self,
        task_id: str,
        description: str
    ) -> Dict:
        """
        Create checkpoint before starting risky task

        Args:
            task_id: Task identifier
            description: Task description

        Returns:
            Dict with checkpoint result
        """
        checkpoint_name = f"task-{task_id}"
        result = self.git.create_checkpoint(
            name=checkpoint_name,
            description=f"Before {task_id}: {description}"
        )

        if result["success"]:
            print(f"🔖 Checkpoint created: {checkpoint_name}")
        else:
            print(f"⚠️  Checkpoint failed: {result.get('error')}")

        return result

    def get_git_status(self) -> Dict:
        """
        Get current git status for monitoring

        Returns:
            Dict with git status info
        """
        return self.git.get_status()