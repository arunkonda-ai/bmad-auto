"""
Integration tests for Git Coordinator
Tests auto-commit, checkpoints, and rollback functionality
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from integration.git_coordinator import GitCoordinator


class TestGitCoordinator:
    """Test suite for GitCoordinator"""

    @pytest.fixture
    def git_coordinator(self):
        """Create GitCoordinator instance"""
        return GitCoordinator()

    def test_verify_git_repo(self, git_coordinator):
        """Test that we're in a valid git repository"""
        assert git_coordinator.repo_path.exists()

    def test_auto_commit(self, git_coordinator):
        """Test auto-commit functionality"""
        result = git_coordinator.auto_commit(
            agent_name="James",
            task_id="T037-TEST",
            description="Test auto-commit functionality"
        )

        assert result["success"] is True
        assert "commit_hash" in result
        assert len(result["commit_hash"]) > 0
        assert "timestamp" in result

    def test_create_checkpoint(self, git_coordinator):
        """Test checkpoint creation"""
        result = git_coordinator.create_checkpoint(
            name="test-checkpoint",
            description="Testing checkpoint functionality"
        )

        assert result["success"] is True
        assert result["checkpoint_name"] == "test-checkpoint"
        assert "commit_hash" in result
        assert result["tag"] == "checkpoint-test-checkpoint"

    def test_get_status(self, git_coordinator):
        """Test git status retrieval"""
        result = git_coordinator.get_status()

        assert result["success"] is True
        assert "branch" in result
        assert "uncommitted_changes" in result
        assert "recent_commits" in result
        assert "checkpoints" in result

    def test_rollback(self, git_coordinator):
        """Test rollback functionality"""
        # First create a commit to rollback
        git_coordinator.auto_commit(
            agent_name="James",
            task_id="T037-ROLLBACK-TEST",
            description="Commit to be rolled back"
        )

        # Now rollback
        result = git_coordinator.rollback(commits=1)

        assert result["success"] is True
        assert result["commits_rolled_back"] == 1

    def test_checkpoint_in_status(self, git_coordinator):
        """Test that created checkpoints appear in status"""
        # Create checkpoint
        checkpoint_name = "test-status-checkpoint"
        git_coordinator.create_checkpoint(
            name=checkpoint_name,
            description="Testing status visibility"
        )

        # Check status
        status = git_coordinator.get_status()
        assert checkpoint_name in status["checkpoints"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])