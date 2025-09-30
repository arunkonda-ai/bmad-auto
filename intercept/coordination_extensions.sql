-- BMAD Auto Extensions to coordination.db
-- This file extends existing coordination.db with new tables
-- PRESERVES existing coordination data and structure

-- Multi-Provider Plan Management
CREATE TABLE IF NOT EXISTS provider_plans (
    id INTEGER PRIMARY KEY,
    provider_name TEXT NOT NULL,      -- 'anthropic_claude', 'zai_glm', 'claude_code'
    plan_tier TEXT NOT NULL,          -- 'pro', 'max', 'lite'
    monthly_limit INTEGER,
    usage_count INTEGER DEFAULT 0,
    reset_date DATETIME,
    cost_per_request REAL,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- PM Decision Reasoning Capture
CREATE TABLE IF NOT EXISTS pm_decision_log (
    id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,  -- JSON context that led to decision
    decision_type TEXT NOT NULL,     -- 'task_assignment', 'quality_gate', 'resource_allocation'
    reasoning_process TEXT,          -- Step-by-step PM logic
    outcome TEXT,                   -- Final decision made
    confidence_score INTEGER,       -- PM confidence 1-10
    learning_notes TEXT,            -- Notes for future cognitive enhancement
    model_assignments TEXT,         -- JSON of model provider assignments
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Agent Extension Management
CREATE TABLE IF NOT EXISTS agent_extensions (
    id INTEGER PRIMARY KEY,
    agent_name TEXT NOT NULL,        -- 'pm', 'dev', 'architect', etc.
    extension_type TEXT NOT NULL,    -- 'capability', 'workflow', 'integration', 'spec_kit'
    extension_config TEXT,          -- JSON configuration
    base_agent_hash TEXT,           -- .bmad-core file integrity
    spec_kit_enabled BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- LangGraph Workflow State Persistence
CREATE TABLE IF NOT EXISTS langgraph_executions (
    id INTEGER PRIMARY KEY,
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

-- External Service Integration Tracking
CREATE TABLE IF NOT EXISTS external_service_operations (
    id INTEGER PRIMARY KEY,
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

-- Quality Gate Tracking
CREATE TABLE IF NOT EXISTS quality_gate_executions (
    id INTEGER PRIMARY KEY,
    deliverable_id TEXT NOT NULL,
    quality_stage TEXT NOT NULL,     -- 'validation', 'review', 'integration', 'approval'
    pm_decision TEXT,               -- 'approved', 'rejected', 'needs_revision'
    pm_reasoning TEXT,              -- Detailed PM decision logic
    agent_reviews TEXT,             -- JSON of agent-specific reviews
    quality_score INTEGER,          -- 1-10 quality rating
    improvement_suggestions TEXT,    -- PM guidance for improvements
    human_escalation BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_provider_plans_provider ON provider_plans(provider_name);
CREATE INDEX IF NOT EXISTS idx_pm_decision_log_type ON pm_decision_log(decision_type);
CREATE INDEX IF NOT EXISTS idx_agent_extensions_agent ON agent_extensions(agent_name);
CREATE INDEX IF NOT EXISTS idx_langgraph_executions_status ON langgraph_executions(execution_status);
CREATE INDEX IF NOT EXISTS idx_external_service_operations_service ON external_service_operations(service_name);
CREATE INDEX IF NOT EXISTS idx_quality_gate_executions_stage ON quality_gate_executions(quality_stage);

-- Insert initial provider plans for multi-model AI strategy
INSERT OR IGNORE INTO provider_plans (provider_name, plan_tier, monthly_limit, cost_per_request) VALUES
('anthropic_claude', 'sonnet', 1000000, 0.000003),
('anthropic_claude', 'opus', 500000, 0.000015),
('zai_glm', 'lite', 3000000, 0.000001),
('zai_glm', 'pro', 2000000, 0.000002),
('claude_code', 'terminal', -1, 0.0);  -- Unlimited local terminal sessions

-- Insert initial agent extensions for core agents
INSERT OR IGNORE INTO agent_extensions (agent_name, extension_type, extension_config, spec_kit_enabled) VALUES
('pm', 'orchestration', '{"coordination_hub": true, "decision_capture": true}', 1),
('architect', 'design', '{"modular_patterns": true, "bmad_core_preservation": true}', 1),
('dev', 'implementation', '{"size_compliance": 300, "real_integration": true}', 1),
('qa', 'quality_gates', '{"automation_target": 0.85, "playwright_mcp": true}', 1),
('ux', 'collaboration', '{"agui_integration": true, "accessibility": true}', 1),
('analyst', 'research', '{"web_search": true, "context7": true}', 1);