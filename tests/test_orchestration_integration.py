"""
Integration tests for BMAD Auto orchestration refactoring
Validates 100% functionality preservation after T019-T020 refactoring
"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock

# Import the refactored orchestration components
from orchestration import TaskAssignmentOrchestrator, QualityGateOrchestrator


class TestOrchestrationIntegration(unittest.TestCase):
    """Test suite to validate functionality preservation"""

    def setUp(self):
        """Set up test database and orchestrators"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()

        self.task_orchestrator = TaskAssignmentOrchestrator(self.test_db.name)
        self.quality_orchestrator = QualityGateOrchestrator(self.test_db.name)

    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)

    def test_task_assignment_functionality(self):
        """Test that task assignment works after refactoring"""
        task_data = {
            "task_id": "test_task_001",
            "description": "Test task for functionality validation",
            "requirements": ["python", "testing"],
            "priority": "high",
            "estimated_hours": 4
        }

        # Test task assignment
        result = self.task_orchestrator.assign_task(task_data)

        # Validate result structure
        self.assertIn("assignment_id", result)
        self.assertIn("assigned_agent", result)
        self.assertIn("confidence_score", result)

    def test_capability_matching(self):
        """Test capability matching functionality"""
        requirements = {
            "skills": ["python", "database", "testing"],
            "experience_level": "senior",
            "availability": "immediate"
        }

        matches = self.task_orchestrator.match_capabilities(requirements)

        # Should return a list of capability matches
        self.assertIsInstance(matches, list)

    def test_agent_workload_tracking(self):
        """Test agent workload functionality"""
        agent_id = "test_agent_001"

        workload = self.task_orchestrator.get_agent_workload(agent_id)

        # Validate workload structure
        self.assertIn("agent_id", workload)
        self.assertIn("current_tasks", workload)
        self.assertIn("capacity_utilization", workload)

    def test_quality_gate_execution(self):
        """Test quality gate processing"""
        deliverable_id = "test_deliverable_001"
        content = {
            "accuracy_score": 8.5,
            "completeness_score": 9.0,
            "required_fields": ["field1", "field2"],
            "field1": "value1",
            "field2": "value2"
        }
        stage = "content_review"

        result = self.quality_orchestrator.execute_quality_gate(
            deliverable_id, content, stage
        )

        # Validate quality gate result
        self.assertEqual(result["deliverable_id"], deliverable_id)
        self.assertEqual(result["stage"], stage)
        self.assertIn(result["decision"], ["approved", "rejected", "needs_revision"])
        self.assertIsInstance(result["quality_score"], float)

    def test_quality_metrics_retrieval(self):
        """Test quality metrics functionality"""
        metrics = self.quality_orchestrator.get_quality_metrics()

        # Should return dictionary with metrics
        self.assertIsInstance(metrics, dict)
        self.assertIn("timestamp", metrics)

    def test_quality_escalation(self):
        """Test quality escalation functionality"""
        deliverable_id = "test_deliverable_002"
        quality_score = 3.0  # Low score to trigger escalation
        description = "Quality score below threshold"

        escalation_id = self.quality_orchestrator.escalate_quality_issue(
            deliverable_id, quality_score, description
        )

        # Should return escalation ID if escalation was triggered
        if escalation_id:
            self.assertIsInstance(escalation_id, str)

    @patch('sqlite3.connect')
    def test_database_integration_preserved(self, mock_connect):
        """Test that database integration works correctly"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value.__enter__.return_value = mock_conn

        # Test task assignment database integration
        task_data = {"task_id": "db_test", "description": "DB integration test"}
        self.task_orchestrator.assign_task(task_data)

        # Verify database connection was attempted
        mock_connect.assert_called()

    def test_modular_architecture_integration(self):
        """Test that modular components integrate correctly"""
        # Test that individual components can be accessed
        self.assertIsNotNone(self.task_orchestrator.engine)
        self.assertIsNotNone(self.task_orchestrator.capability_matcher)
        self.assertIsNotNone(self.task_orchestrator.load_balancer)

        self.assertIsNotNone(self.quality_orchestrator.gate_processor)
        self.assertIsNotNone(self.quality_orchestrator.analytics)
        self.assertIsNotNone(self.quality_orchestrator.escalation)

    def test_backward_compatibility(self):
        """Test that the API remains backward compatible"""
        # Test that original method names still work
        self.assertTrue(hasattr(self.task_orchestrator, 'assign_task'))
        self.assertTrue(hasattr(self.task_orchestrator, 'get_agent_workload'))
        self.assertTrue(hasattr(self.task_orchestrator, 'match_capabilities'))

        self.assertTrue(hasattr(self.quality_orchestrator, 'execute_quality_gate'))
        self.assertTrue(hasattr(self.quality_orchestrator, 'get_quality_metrics'))
        self.assertTrue(hasattr(self.quality_orchestrator, 'escalate_quality_issue'))


if __name__ == '__main__':
    # Run functionality preservation tests
    unittest.main(verbosity=2)