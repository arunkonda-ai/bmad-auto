# Data Model: Foundation & PM Orchestration Hub

**Date**: 2025-09-28
**Feature**: Foundation & PM Orchestration Hub
**Phase**: 1 - Data Model Design

## Core Entities

### PMDecisionContext

**Purpose**: Captures complete PM decision-making context and reasoning for cognitive framework enhancement

**Attributes**:
- `decision_id: string (UUID)` - Unique decision identifier
- `decision_type: enum` - Type of decision made
  - Values: 'task_assignment', 'quality_gate', 'resource_allocation', 'escalation', 'model_assignment'
- `context_data: JSON` - Complete decision context and inputs
- `reasoning_process: text` - Step-by-step PM logical reasoning
- `outcome: text` - Final decision made with rationale
- `confidence_score: integer (1-10)` - PM confidence in decision
- `agent_assignments: JSON` - Mapping of agents to tasks if applicable
- `resource_optimization: JSON` - Resource allocation decisions
- `learning_notes: text` - Notes for future cognitive improvement
- `created_at: timestamp` - Decision timestamp
- `updated_at: timestamp` - Last modification timestamp

**Relationships**:
- Links to TaskBreakdown (one-to-many)
- Links to QualityGateExecution (one-to-many)
- Links to ModelAssignment (one-to-many)

**Validation Rules**:
- decision_id must be unique UUID
- confidence_score must be between 1-10
- reasoning_process required for all decisions
- context_data must be valid JSON

### AgentState

**Purpose**: Represents current agent status including active tasks, capabilities, and performance metrics

**Attributes**:
- `agent_id: string` - Unique agent identifier (e.g., 'john-pm', 'james-dev')
- `agent_name: string` - Human-readable agent name
- `agent_role: enum` - Agent specialization
  - Values: 'pm', 'architect', 'developer', 'qa', 'ux', 'analyst', 'coordinator', 'specialist'
- `status: enum` - Current operational status
  - Values: 'active', 'busy', 'idle', 'error', 'offline'
- `capabilities: JSON array` - List of agent capabilities and skills
- `active_tasks: JSON array` - Currently assigned task identifiers
- `resource_utilization: JSON` - Current resource usage metrics
- `performance_metrics: JSON` - Performance tracking data
- `communication_history: JSON array` - Recent inter-agent messages
- `extension_config: JSON` - Agent extension configuration
- `last_activity: timestamp` - Last agent activity timestamp
- `created_at: timestamp` - Agent registration timestamp
- `updated_at: timestamp` - Last state update

**Relationships**:
- Links to WorkflowExecution (many-to-many through task assignments)
- Links to ModelAssignment (one-to-many)
- Links to QualityGate (many-to-many as reviewers)

**Validation Rules**:
- agent_id must be unique and follow naming convention
- status transitions must follow defined state machine
- active_tasks must reference valid task identifiers
- performance_metrics updated at least every 30 seconds

### WorkflowExecution

**Purpose**: Tracks workflow progress including phases, tasks, approvals, and performance metrics

**Attributes**:
- `execution_id: string (UUID)` - Unique workflow execution identifier
- `workflow_name: string` - Name of workflow template being executed
- `execution_status: enum` - Current workflow status
  - Values: 'pending', 'running', 'paused', 'completed', 'failed', 'cancelled'
- `trigger_type: enum` - How workflow was initiated
  - Values: 'manual', 'scheduled', 'agent_request', 'quality_gate', 'escalation'
- `triggered_by: string` - Agent or user who initiated workflow
- `input_context: JSON` - Initial workflow parameters and context
- `current_phase: string` - Current workflow phase or node
- `execution_path: JSON array` - Sequence of nodes executed
- `task_assignments: JSON` - Current agent task assignments
- `pending_approvals: JSON array` - Quality gates awaiting approval
- `performance_metrics: JSON` - Workflow execution metrics
- `error_log: JSON array` - Errors encountered during execution
- `started_at: timestamp` - Workflow start time
- `completed_at: timestamp` - Workflow completion time (if finished)
- `last_activity: timestamp` - Last workflow activity

**Relationships**:
- Links to PMDecisionContext (many-to-one)
- Links to AgentState (many-to-many through task assignments)
- Links to QualityGateExecution (one-to-many)

**Validation Rules**:
- execution_id must be unique UUID
- workflow_name must reference valid workflow template
- execution_path must be chronologically ordered
- performance_metrics updated in real-time

### ModelAssignment

**Purpose**: Manages AI model provider assignments with cost optimization and performance tracking

**Attributes**:
- `assignment_id: string (UUID)` - Unique assignment identifier
- `agent_id: string` - Agent receiving model assignment
- `task_id: string` - Task requiring AI model processing
- `provider_name: enum` - AI model provider assigned
  - Values: 'claude_code', 'anthropic_claude', 'zai_glm'
- `model_name: string` - Specific model assigned (e.g., 'claude-sonnet-4', 'glm-4.5')
- `assignment_reason: enum` - Reason for model selection
  - Values: 'complexity_high', 'cost_optimization', 'provider_preference', 'fallback'
- `task_complexity: integer (1-10)` - Assessed task complexity
- `estimated_cost: decimal` - Estimated processing cost
- `actual_cost: decimal` - Actual processing cost (if completed)
- `performance_score: decimal` - Model performance rating for this task
- `processing_time: integer` - Task processing time in milliseconds
- `tokens_used: integer` - Token consumption for this assignment
- `assignment_status: enum` - Current assignment status
  - Values: 'pending', 'active', 'completed', 'failed', 'cancelled'
- `created_at: timestamp` - Assignment creation time
- `completed_at: timestamp` - Assignment completion time

**Relationships**:
- Links to AgentState (many-to-one)
- Links to PMDecisionContext (many-to-one for assignment decisions)
- Links to WorkflowExecution (many-to-one)

**Validation Rules**:
- assignment_id must be unique UUID
- task_complexity must be between 1-10
- cost values must be positive decimals
- performance_score between 0.0-10.0

### QualityGateExecution

**Purpose**: Defines validation checkpoints with criteria, approval workflows, and outcome tracking

**Attributes**:
- `gate_id: string (UUID)` - Unique quality gate identifier
- `gate_name: string` - Human-readable gate name
- `workflow_execution_id: string` - Associated workflow execution
- `gate_type: enum` - Type of quality validation
  - Values: 'content_validation', 'technical_review', 'security_check', 'performance_test', 'final_approval'
- `validation_criteria: JSON` - Defined success criteria
- `automated_checks: JSON array` - Automated validation results
- `reviewer_assignments: JSON array` - Assigned reviewers (agents and humans)
- `approval_status: enum` - Current approval status
  - Values: 'pending', 'in_review', 'approved', 'rejected', 'requires_revision'
- `pm_decision: string` - PM approval/rejection reasoning
- `quality_score: decimal (0.0-10.0)` - Assessed quality rating
- `improvement_suggestions: text` - Recommendations for improvement
- `reviewer_feedback: JSON array` - Individual reviewer feedback
- `escalation_required: boolean` - Whether human escalation needed
- `escalation_reason: text` - Reason for escalation if applicable
- `created_at: timestamp` - Gate creation time
- `reviewed_at: timestamp` - Review completion time
- `approved_at: timestamp` - Final approval time

**Relationships**:
- Links to WorkflowExecution (many-to-one)
- Links to PMDecisionContext (one-to-one for PM decisions)
- Links to AgentState (many-to-many through reviewer assignments)

**Validation Rules**:
- gate_id must be unique UUID
- quality_score must be between 0.0-10.0
- approval_status transitions must follow defined workflow
- pm_decision required for final approval/rejection

### ResourceMetrics

**Purpose**: Monitors system resource utilization with optimization recommendations

**Attributes**:
- `metric_id: string (UUID)` - Unique metric identifier
- `measurement_time: timestamp` - When measurement was taken
- `agent_id: string` - Agent being measured (null for system-wide)
- `cpu_usage: decimal (0.0-100.0)` - CPU utilization percentage
- `memory_usage: decimal` - Memory usage in MB
- `disk_usage: decimal` - Disk usage in MB
- `network_io: decimal` - Network I/O in MB/s
- `active_sessions: integer` - Number of active Claude Code sessions
- `database_connections: integer` - Active database connections
- `response_time: integer` - Average response time in milliseconds
- `error_rate: decimal (0.0-100.0)` - Error rate percentage
- `optimization_score: decimal (0.0-10.0)` - Resource optimization rating
- `optimization_suggestions: JSON array` - Recommended optimizations
- `alert_level: enum` - Resource usage alert level
  - Values: 'normal', 'warning', 'critical', 'emergency'
- `created_at: timestamp` - Metric collection time

**Relationships**:
- Links to AgentState (many-to-one, nullable for system metrics)
- Links to WorkflowExecution (many-to-one, nullable for system metrics)

**Validation Rules**:
- metric_id must be unique UUID
- percentage values must be between 0.0-100.0
- optimization_score must be between 0.0-10.0
- measurement_time must be current or recent

## Entity Relationships

### Primary Relationships

1. **PMDecisionContext** ↔ **WorkflowExecution**
   - One decision may impact multiple workflow executions
   - Each workflow execution may trigger multiple PM decisions

2. **WorkflowExecution** ↔ **AgentState**
   - Workflows assign tasks to multiple agents
   - Agents can participate in multiple concurrent workflows

3. **QualityGateExecution** ↔ **PMDecisionContext**
   - Quality gates require PM approval decisions
   - PM decisions may create new quality gates

4. **ModelAssignment** ↔ **AgentState**
   - Agents receive multiple model assignments over time
   - Model assignments track agent performance

### Data Flow Patterns

1. **Task Assignment Flow**:
   PMDecisionContext → WorkflowExecution → AgentState → ModelAssignment

2. **Quality Validation Flow**:
   WorkflowExecution → QualityGateExecution → PMDecisionContext

3. **Resource Monitoring Flow**:
   AgentState → ResourceMetrics → PMDecisionContext (for optimization)

## State Management

### Workflow State Persistence

- All entity states persisted in PostgreSQL for durability
- LangGraph workflow states linked to WorkflowExecution entities
- State transitions logged for audit and debugging
- Recovery mechanisms for interrupted workflows

### Agent State Synchronization

- Real-time state updates every 30 seconds maximum
- Event-driven state changes for critical status updates
- Conflict resolution for concurrent state modifications
- State validation before persistence

### Decision Reasoning Persistence

- Complete PM decision context captured for learning
- Decision patterns stored for future optimization
- Historical decision analysis for system improvement
- Privacy protection for sensitive decision data

## Performance Considerations

### Database Optimization

- Indexed fields: decision_id, agent_id, execution_id, gate_id
- Partitioned tables for high-volume metrics data
- Connection pooling for concurrent agent access
- Query optimization for real-time dashboard updates

### Data Retention

- Active workflow data: Unlimited retention
- Historical metrics: 90-day rolling window
- Decision reasoning: 1-year retention for learning
- Error logs: 30-day retention with critical error archival

### Scalability Patterns

- Horizontal scaling through database partitioning
- Caching layer for frequently accessed agent states
- Asynchronous processing for non-critical updates
- Bulk operations for metrics collection and reporting