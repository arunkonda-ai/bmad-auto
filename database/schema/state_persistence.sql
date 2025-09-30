-- Session state persistence for BMAD Auto
-- Prevents data loss and enables quick recovery

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

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_session_updated ON session_state(updated_at);
CREATE INDEX IF NOT EXISTS idx_checkpoint_name ON checkpoints(name);
CREATE INDEX IF NOT EXISTS idx_checkpoint_created ON checkpoints(created_at);

-- Comments for documentation
COMMENT ON TABLE session_state IS 'Stores conversation history and agent state for session recovery';
COMMENT ON TABLE checkpoints IS 'Named restore points for safe experimentation';
COMMENT ON COLUMN session_state.conversation_history IS 'Complete message history in JSON format';
COMMENT ON COLUMN session_state.agent_contexts IS 'Current working memory for all agents';
COMMENT ON COLUMN session_state.task_progress IS 'Status of in-progress tasks';
COMMENT ON COLUMN checkpoints.git_commit_hash IS 'Git commit associated with this checkpoint';
COMMENT ON COLUMN checkpoints.session_state IS 'Complete session state at checkpoint time';