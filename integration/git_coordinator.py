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