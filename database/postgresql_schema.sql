-- T013: PostgreSQL Schema for Core BMAD Auto Entities
-- Database: bmad_auto
-- Purpose: Core entities for PM decisions, agent state, workflow execution, and model assignments
-- Author: James (Developer)
-- Date: 2025-09-28

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- PM Decision Context Table
-- =====================================================
CREATE TABLE IF NOT EXISTS pm_decision_context (
    decision_id VARCHAR(255) PRIMARY KEY,
    decision_type VARCHAR(50) NOT NULL CHECK (decision_type IN (
        'task_assignment', 'quality_gate', 'resource_allocation',
        'escalation', 'agent_coordination', 'workflow_optimization'
    )),
    context_data JSONB NOT NULL,
    reasoning_process TEXT NOT NULL,
    outcome TEXT NOT NULL,
    confidence_score INTEGER NOT NULL CHECK (confidence_score >= 1 AND confidence_score <= 10),
    agent_assignments JSONB,
    resource_optimization JSONB,
    learning_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for PM Decision Context
CREATE INDEX IF NOT EXISTS idx_pm_decision_context_type ON pm_decision_context(decision_type);
CREATE INDEX IF NOT EXISTS idx_pm_decision_context_created ON pm_decision_context(created_at);
CREATE INDEX IF NOT EXISTS idx_pm_decision_context_confidence ON pm_decision_context(confidence_score);
CREATE INDEX IF NOT EXISTS idx_pm_decision_context_context_data ON pm_decision_context USING GIN(context_data);
CREATE INDEX IF NOT EXISTS idx_pm_decision_context_agent_assignments ON pm_decision_context USING GIN(agent_assignments);

-- =====================================================
-- Agent State Table
-- =====================================================
CREATE TABLE IF NOT EXISTS agent_state (
    agent_id VARCHAR(255) PRIMARY KEY,
    agent_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'active', 'busy', 'idle', 'offline', 'error', 'maintenance'
    )),
    current_task JSONB,
    capabilities JSONB,
    load_factor DECIMAL(3,2) NOT NULL DEFAULT 0.0 CHECK (load_factor >= 0.0 AND load_factor <= 1.0),
    coordination_status JSONB,
    performance_metrics JSONB,
    resource_usage JSONB,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Agent State
CREATE INDEX IF NOT EXISTS idx_agent_state_status ON agent_state(status);
CREATE INDEX IF NOT EXISTS idx_agent_state_type ON agent_state(agent_type);
CREATE INDEX IF NOT EXISTS idx_agent_state_load_factor ON agent_state(load_factor);
CREATE INDEX IF NOT EXISTS idx_agent_state_last_updated ON agent_state(last_updated);
CREATE INDEX IF NOT EXISTS idx_agent_state_capabilities ON agent_state USING GIN(capabilities);
CREATE INDEX IF NOT EXISTS idx_agent_state_current_task ON agent_state USING GIN(current_task);

-- =====================================================
-- Workflow Execution Table
-- =====================================================
CREATE TABLE IF NOT EXISTS workflow_execution (
    execution_id VARCHAR(255) PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN (
        'pending', 'in_progress', 'completed', 'failed', 'paused', 'cancelled'
    )),
    current_node VARCHAR(255),
    execution_path JSONB,
    performance_metrics JSONB,
    langgraph_state JSONB,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Workflow Execution
CREATE INDEX IF NOT EXISTS idx_workflow_execution_status ON workflow_execution(status);
CREATE INDEX IF NOT EXISTS idx_workflow_execution_workflow_id ON workflow_execution(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_execution_started_at ON workflow_execution(started_at);
CREATE INDEX IF NOT EXISTS idx_workflow_execution_current_node ON workflow_execution(current_node);
CREATE INDEX IF NOT EXISTS idx_workflow_execution_langgraph_state ON workflow_execution USING GIN(langgraph_state);

-- =====================================================
-- Model Assignment Table
-- =====================================================
CREATE TABLE IF NOT EXISTS model_assignment (
    assignment_id VARCHAR(255) PRIMARY KEY,
    task_context JSONB NOT NULL,
    assigned_provider VARCHAR(100) NOT NULL CHECK (assigned_provider IN (
        'anthropic_claude', 'zai_glm', 'claude_code_terminal'
    )),
    assigned_model VARCHAR(100) NOT NULL,
    assignment_reason TEXT NOT NULL,
    confidence_score DECIMAL(3,2) NOT NULL CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    cost_estimate DECIMAL(10,4) NOT NULL DEFAULT 0.0,
    performance_prediction JSONB NOT NULL,
    alternative_assignments JSONB,
    assignment_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Model Assignment
CREATE INDEX IF NOT EXISTS idx_model_assignment_provider ON model_assignment(assigned_provider);
CREATE INDEX IF NOT EXISTS idx_model_assignment_model ON model_assignment(assigned_model);
CREATE INDEX IF NOT EXISTS idx_model_assignment_confidence ON model_assignment(confidence_score);
CREATE INDEX IF NOT EXISTS idx_model_assignment_cost ON model_assignment(cost_estimate);
CREATE INDEX IF NOT EXISTS idx_model_assignment_timestamp ON model_assignment(assignment_timestamp);
CREATE INDEX IF NOT EXISTS idx_model_assignment_task_context ON model_assignment USING GIN(task_context);

-- =====================================================
-- Quality Gate Execution Table
-- =====================================================
CREATE TABLE IF NOT EXISTS quality_gate_execution (
    gate_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    deliverable_id VARCHAR(255) NOT NULL,
    quality_stage VARCHAR(100) NOT NULL CHECK (quality_stage IN (
        'validation', 'review', 'integration', 'approval'
    )),
    pm_decision VARCHAR(50) CHECK (pm_decision IN (
        'approved', 'rejected', 'needs_revision'
    )),
    pm_reasoning TEXT,
    agent_reviews JSONB,
    quality_score INTEGER CHECK (quality_score >= 1 AND quality_score <= 10),
    improvement_suggestions TEXT,
    human_escalation BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Quality Gate Execution
CREATE INDEX IF NOT EXISTS idx_quality_gate_deliverable ON quality_gate_execution(deliverable_id);
CREATE INDEX IF NOT EXISTS idx_quality_gate_stage ON quality_gate_execution(quality_stage);
CREATE INDEX IF NOT EXISTS idx_quality_gate_pm_decision ON quality_gate_execution(pm_decision);
CREATE INDEX IF NOT EXISTS idx_quality_gate_quality_score ON quality_gate_execution(quality_score);
CREATE INDEX IF NOT EXISTS idx_quality_gate_escalation ON quality_gate_execution(human_escalation);
CREATE INDEX IF NOT EXISTS idx_quality_gate_created_at ON quality_gate_execution(created_at);

-- =====================================================
-- Update Triggers for Timestamp Management
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers
CREATE TRIGGER update_pm_decision_context_updated_at
    BEFORE UPDATE ON pm_decision_context
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quality_gate_execution_updated_at
    BEFORE UPDATE ON quality_gate_execution
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Performance Optimization Views
-- =====================================================

-- Active agents view for quick status checking
CREATE OR REPLACE VIEW active_agents AS
SELECT
    agent_id,
    agent_type,
    status,
    load_factor,
    last_updated
FROM agent_state
WHERE status IN ('active', 'busy', 'idle')
ORDER BY load_factor ASC;

-- Recent PM decisions view
CREATE OR REPLACE VIEW recent_pm_decisions AS
SELECT
    decision_id,
    decision_type,
    outcome,
    confidence_score,
    created_at
FROM pm_decision_context
WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER BY created_at DESC;

-- Active workflows view
CREATE OR REPLACE VIEW active_workflows AS
SELECT
    execution_id,
    workflow_id,
    status,
    current_node,
    started_at,
    last_updated
FROM workflow_execution
WHERE status IN ('pending', 'in_progress', 'paused')
ORDER BY started_at ASC;

-- =====================================================
-- Schema Validation and Comments
-- =====================================================

-- Add table comments for documentation
COMMENT ON TABLE pm_decision_context IS 'PM decision reasoning capture for cognitive framework enhancement';
COMMENT ON TABLE agent_state IS 'Real-time agent status and coordination tracking';
COMMENT ON TABLE workflow_execution IS 'LangGraph workflow orchestration state management';
COMMENT ON TABLE model_assignment IS 'Multi-provider AI model assignment optimization';
COMMENT ON TABLE quality_gate_execution IS 'Quality validation and approval workflow tracking';

-- Add key column comments
COMMENT ON COLUMN pm_decision_context.context_data IS 'Complete decision context in JSONB format';
COMMENT ON COLUMN pm_decision_context.reasoning_process IS 'Step-by-step PM logical reasoning';
COMMENT ON COLUMN agent_state.load_factor IS 'Agent workload factor (0.0-1.0)';
COMMENT ON COLUMN workflow_execution.langgraph_state IS 'LangGraph checkpoint and state data';
COMMENT ON COLUMN model_assignment.confidence_score IS 'Assignment confidence (0.0-1.0)';

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version VARCHAR(50) PRIMARY KEY,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_version (version, description)
VALUES ('1.0.0', 'Initial BMAD Auto core entities schema')
ON CONFLICT (version) DO NOTHING;