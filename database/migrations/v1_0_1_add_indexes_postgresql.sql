-- Sample Migration: Add additional performance indexes
-- Version: v1_0_1
-- Description: Add additional performance indexes

-- UP
CREATE INDEX IF NOT EXISTS idx_pm_decision_context_outcome ON pm_decision_context(outcome);
CREATE INDEX IF NOT EXISTS idx_agent_state_created_at ON agent_state(created_at);
CREATE INDEX IF NOT EXISTS idx_workflow_execution_completed_at ON workflow_execution(completed_at);

-- DOWN
DROP INDEX IF EXISTS idx_pm_decision_context_outcome;
DROP INDEX IF EXISTS idx_agent_state_created_at;
DROP INDEX IF EXISTS idx_workflow_execution_completed_at;