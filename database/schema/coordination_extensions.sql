-- T014: SQLite coordination.db Extensions for BMAD Auto
-- Purpose: Extend existing coordination.db with BMAD Auto specific tables
-- Preserves: All existing .bmad-core coordination data
-- Author: James (Developer)
-- Date: 2025-10-01

-- =====================================================
-- Multi-Provider Plan Management
-- =====================================================
CREATE TABLE IF NOT EXISTS provider_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_name TEXT NOT NULL,      -- 'anthropic_claude', 'zai_glm', 'claude_code'
    plan_tier TEXT NOT NULL,          -- 'pro', 'max', 'lite', 'free'
    monthly_limit INTEGER,
    usage_count INTEGER DEFAULT 0,
    reset_date DATETIME,
    cost_per_request REAL,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider_name, plan_tier)
);

CREATE INDEX IF NOT EXISTS idx_provider_plans_active ON provider_plans(is_active);
CREATE INDEX IF NOT EXISTS idx_provider_plans_provider ON provider_plans(provider_name);

-- =====================================================
-- PM Decision Reasoning Capture
-- =====================================================
CREATE TABLE IF NOT EXISTS pm_decision_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_context TEXT NOT NULL,  -- JSON context that led to decision
    decision_type TEXT NOT NULL,     -- 'task_assignment', 'quality_gate', 'resource_allocation'
    reasoning_process TEXT,          -- Step-by-step PM logic
    outcome TEXT,                   -- Final decision made
    confidence_score INTEGER CHECK (confidence_score >= 1 AND confidence_score <= 10),
    learning_notes TEXT,            -- Notes for future cognitive enhancement
    model_assignments TEXT,         -- JSON of model provider assignments
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pm_decision_log_type ON pm_decision_log(decision_type);
CREATE INDEX IF NOT EXISTS idx_pm_decision_log_created ON pm_decision_log(created_at);
CREATE INDEX IF NOT EXISTS idx_pm_decision_log_confidence ON pm_decision_log(confidence_score);

-- =====================================================
-- Agent Extension Management
-- =====================================================
CREATE TABLE IF NOT EXISTS agent_extensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL,        -- 'pm', 'dev', 'architect', 'qa', 'ux', 'analyst'
    extension_type TEXT NOT NULL,    -- 'capability', 'workflow', 'integration', 'spec_kit'
    extension_config TEXT,          -- JSON configuration
    base_agent_hash TEXT,           -- .bmad-core file integrity
    spec_kit_enabled BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(agent_name, extension_type)
);

CREATE INDEX IF NOT EXISTS idx_agent_extensions_agent ON agent_extensions(agent_name);
CREATE INDEX IF NOT EXISTS idx_agent_extensions_active ON agent_extensions(is_active);
CREATE INDEX IF NOT EXISTS idx_agent_extensions_spec_kit ON agent_extensions(spec_kit_enabled);

-- =====================================================
-- LangGraph Workflow State Persistence
-- =====================================================
CREATE TABLE IF NOT EXISTS langgraph_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_id TEXT UNIQUE NOT NULL,
    workflow_name TEXT NOT NULL,
    execution_status TEXT DEFAULT 'running',
    trigger_type TEXT NOT NULL,      -- 'manual', 'scheduled', 'agent_request'
    triggered_by TEXT NOT NULL,      -- Agent/human who triggered
    input_context TEXT,              -- JSON input parameters
    current_node TEXT,               -- Current workflow node
    execution_path TEXT,             -- JSON array of nodes executed
    performance_metrics TEXT,        -- JSON performance data
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_langgraph_executions_id ON langgraph_executions(execution_id);
CREATE INDEX IF NOT EXISTS idx_langgraph_executions_status ON langgraph_executions(execution_status);
CREATE INDEX IF NOT EXISTS idx_langgraph_executions_workflow ON langgraph_executions(workflow_name);
CREATE INDEX IF NOT EXISTS idx_langgraph_executions_triggered ON langgraph_executions(triggered_by);

-- =====================================================
-- External Service Integration Tracking
-- =====================================================
CREATE TABLE IF NOT EXISTS external_service_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,      -- 'github', 'linear', 'mcp'
    operation_type TEXT NOT NULL,    -- 'cli_command', 'api_call', 'fallback'
    agent_id TEXT NOT NULL,
    command_or_endpoint TEXT,        -- CLI command or API endpoint
    operation_status TEXT NOT NULL,  -- 'success', 'failed', 'fallback_used'
    response_data TEXT,              -- Operation result
    error_message TEXT,              -- Error details if failed
    execution_time_ms INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_external_service_ops_service ON external_service_operations(service_name);
CREATE INDEX IF NOT EXISTS idx_external_service_ops_agent ON external_service_operations(agent_id);
CREATE INDEX IF NOT EXISTS idx_external_service_ops_status ON external_service_operations(operation_status);
CREATE INDEX IF NOT EXISTS idx_external_service_ops_created ON external_service_operations(created_at);

-- =====================================================
-- Quality Gate Tracking
-- =====================================================
CREATE TABLE IF NOT EXISTS quality_gate_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deliverable_id TEXT NOT NULL,
    quality_stage TEXT NOT NULL,     -- 'validation', 'review', 'integration', 'approval'
    pm_decision TEXT,               -- 'approved', 'rejected', 'needs_revision'
    pm_reasoning TEXT,              -- Detailed PM decision logic
    agent_reviews TEXT,             -- JSON of agent-specific reviews
    quality_score INTEGER CHECK (quality_score >= 1 AND quality_score <= 10),
    improvement_suggestions TEXT,    -- PM guidance for improvements
    human_escalation BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_quality_gate_deliverable ON quality_gate_executions(deliverable_id);
CREATE INDEX IF NOT EXISTS idx_quality_gate_stage ON quality_gate_executions(quality_stage);
CREATE INDEX IF NOT EXISTS idx_quality_gate_decision ON quality_gate_executions(pm_decision);
CREATE INDEX IF NOT EXISTS idx_quality_gate_score ON quality_gate_executions(quality_score);
CREATE INDEX IF NOT EXISTS idx_quality_gate_escalation ON quality_gate_executions(human_escalation);

-- =====================================================
-- Insert Default Data
-- =====================================================

-- Initialize provider plans with default values
INSERT OR IGNORE INTO provider_plans (provider_name, plan_tier, monthly_limit, cost_per_request, is_active)
VALUES
    ('claude_code', 'free', NULL, 0.0, 1),
    ('anthropic_claude', 'pro', 5000, 0.003, 0),
    ('zai_glm', 'lite', 15000, 0.001, 0);

-- Initialize PM agent extension
INSERT OR IGNORE INTO agent_extensions (agent_name, extension_type, extension_config, spec_kit_enabled, is_active)
VALUES (
    'pm',
    'orchestration',
    '{"capabilities": ["task_assignment", "quality_gates", "decision_reasoning"], "spec_kit_commands": ["/specify", "/plan"]}',
    1,
    1
);

-- =====================================================
-- Utility Views
-- =====================================================

-- View for active provider plans
CREATE VIEW IF NOT EXISTS active_provider_plans AS
SELECT
    provider_name,
    plan_tier,
    monthly_limit,
    usage_count,
    CAST(usage_count AS REAL) / NULLIF(monthly_limit, 0) * 100 AS usage_percentage,
    reset_date,
    cost_per_request
FROM provider_plans
WHERE is_active = 1;

-- View for recent PM decisions
CREATE VIEW IF NOT EXISTS recent_pm_decisions AS
SELECT
    decision_type,
    reasoning_process,
    outcome,
    confidence_score,
    created_at
FROM pm_decision_log
ORDER BY created_at DESC
LIMIT 100;

-- View for active LangGraph executions
CREATE VIEW IF NOT EXISTS active_workflows AS
SELECT
    execution_id,
    workflow_name,
    execution_status,
    current_node,
    triggered_by,
    started_at,
    (julianday('now') - julianday(last_activity)) * 24 * 60 AS minutes_since_activity
FROM langgraph_executions
WHERE execution_status IN ('running', 'paused')
ORDER BY last_activity DESC;

-- View for quality gate statistics
CREATE VIEW IF NOT EXISTS quality_gate_stats AS
SELECT
    quality_stage,
    pm_decision,
    COUNT(*) AS execution_count,
    AVG(quality_score) AS avg_quality_score,
    SUM(CASE WHEN human_escalation = 1 THEN 1 ELSE 0 END) AS escalation_count
FROM quality_gate_executions
GROUP BY quality_stage, pm_decision;

-- =====================================================
-- Database Version Tracking
-- =====================================================
CREATE TABLE IF NOT EXISTS schema_version (
    version TEXT PRIMARY KEY,
    description TEXT,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO schema_version (version, description)
VALUES ('1.0.0', 'Initial BMAD Auto coordination.db extensions');

-- =====================================================
-- Success Message
-- =====================================================
SELECT 'BMAD Auto coordination.db extensions applied successfully!' AS status;
