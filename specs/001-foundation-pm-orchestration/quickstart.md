# Quickstart: Foundation & PM Orchestration Hub

**Date**: 2025-09-28
**Feature**: Foundation & PM Orchestration Hub
**Phase**: 1 - Quickstart Guide

## Overview

This quickstart guide validates the Foundation & PM Orchestration Hub implementation through core user scenarios. It provides step-by-step validation of PM-centric agent coordination, multi-provider AI integration, and quality gate management.

## Prerequisites

### System Requirements
- Python 3.11+ with virtual environment
- PostgreSQL 15+ with createdb privileges
- SQLite 3.x for coordination.db extension
- Claude Code terminal access
- 8GB RAM minimum, 4 CPU cores
- 50GB available storage

### Environment Setup
```bash
# Clone and enter project directory
cd /path/to/bmad-auto

# Create Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install core dependencies
pip install langgraph langsmith psycopg2-binary pyyaml fastapi uvicorn

# Set environment variables
export POSTGRESQL_URL="postgresql://user:pass@localhost:5432/bmad_auto"
export LANGGRAPH_API_KEY="your-langgraph-key"
export CLAUDE_CODE_PATH="/path/to/claude-code"
```

### Database Setup
```bash
# Create PostgreSQL database
createdb bmad_auto

# Initialize database schema
python -m bmad_auto.database.init_schema

# Verify coordination.db extension
sqlite3 intercept/coordination.db ".tables"
```

## Core Scenario Validation

### Scenario 1: PM Task Assignment and Agent Coordination

**Objective**: Validate PM orchestration hub can break down tasks and coordinate agents

**Test Steps**:

1. **Start PM Orchestration Hub**
   ```bash
   python -m bmad_auto.orchestration.pm_coordinator
   ```
   **Expected**: PM hub starts, logs "PM Coordinator operational", database connections established

2. **Submit New Product Development Task**
   ```bash
   curl -X POST http://localhost:8000/api/v1/pm/decisions \
     -H "Content-Type: application/json" \
     -d '{
       "decision_type": "task_assignment",
       "context_data": {
         "task": "Implement user authentication system",
         "priority": "high",
         "timeline": "2 weeks"
       },
       "reasoning_process": "Breaking down authentication into: API design, security review, implementation, testing",
       "outcome": "Assigned to James (dev) and Quinn (qa) with Alex (architect) for review",
       "confidence_score": 8,
       "agent_assignments": {
         "james-dev": "API implementation",
         "quinn-qa": "Security testing",
         "alex-architect": "Architecture review"
       }
     }'
   ```
   **Expected**: 201 response with decision_id, PM decision logged with reasoning

3. **Verify Agent Assignment**
   ```bash
   curl http://localhost:8000/api/v1/agents
   ```
   **Expected**: Agents show assigned tasks, status updates, resource allocation

4. **Check Workflow Creation**
   ```bash
   curl http://localhost:8000/api/v1/workflows
   ```
   **Expected**: New workflow execution created, agents assigned to phases

**Success Criteria**:
- PM decision captured with complete reasoning trail
- Agents automatically assigned based on capabilities
- Workflow execution initiated with proper task breakdown
- All agent states updated within 30 seconds

### Scenario 2: Multi-Provider AI Model Assignment

**Objective**: Validate intelligent AI model assignment based on task complexity

**Test Steps**:

1. **Submit Complex Architecture Task**
   ```bash
   curl -X POST http://localhost:8000/api/v1/models/assign \
     -H "Content-Type: application/json" \
     -d '{
       "agent_id": "alex-architect",
       "task_id": "arch-001",
       "task_complexity": 9
     }'
   ```
   **Expected**: Claude Sonnet 4 assigned for complex reasoning

2. **Submit Routine Development Task**
   ```bash
   curl -X POST http://localhost:8000/api/v1/models/assign \
     -H "Content-Type: application/json" \
     -d '{
       "agent_id": "james-dev",
       "task_id": "dev-001",
       "task_complexity": 3
     }'
   ```
   **Expected**: Z.ai GLM 4.5 assigned for cost optimization

3. **Verify Model Assignment Logic**
   ```bash
   curl http://localhost:8000/api/v1/models/assignments
   ```
   **Expected**: Different models assigned based on complexity, cost tracking

4. **Test Claude Code Terminal Integration**
   ```bash
   python -m bmad_auto.orchestration.model_provider test_claude_code_session
   ```
   **Expected**: Session created, model switching functional, context preserved

**Success Criteria**:
- Complex tasks (7-10) assigned to Claude models
- Routine tasks (1-5) assigned to Z.ai GLM models
- Claude Code terminal integration functional
- Cost optimization and usage tracking working

### Scenario 3: Quality Gate Management and Human Approval

**Objective**: Validate quality gate workflows with PM approval

**Test Steps**:

1. **Trigger Quality Gate**
   ```bash
   # Simulate agent completing task requiring approval
   curl -X POST http://localhost:8000/api/v1/quality-gates \
     -H "Content-Type: application/json" \
     -d '{
       "gate_name": "Security Review Gate",
       "workflow_execution_id": "workflow-001",
       "gate_type": "security_check",
       "validation_criteria": {
         "security_scan": "passed",
         "code_review": "completed",
         "vulnerability_check": "clean"
       }
     }'
   ```
   **Expected**: Quality gate created, pending PM approval

2. **Review Quality Gate Details**
   ```bash
   curl http://localhost:8000/api/v1/quality-gates?status=pending
   ```
   **Expected**: Gate details with validation criteria, reviewer feedback

3. **PM Approval Workflow**
   ```bash
   curl -X POST http://localhost:8000/api/v1/quality-gates/{gate_id}/approve \
     -H "Content-Type: application/json" \
     -d '{
       "approval_status": "approved",
       "pm_decision": "Security review passed all criteria, code quality meets standards",
       "quality_score": 8.5,
       "improvement_suggestions": "Consider adding integration tests for edge cases"
     }'
   ```
   **Expected**: Gate approved, workflow continues, decision reasoning captured

4. **Verify Approval Workflow**
   ```bash
   curl http://localhost:8000/api/v1/workflows/{execution_id}
   ```
   **Expected**: Workflow advanced to next phase, no pending approvals

**Success Criteria**:
- Quality gates automatically created at workflow transitions
- Human approval workflow functional with complete context
- PM decisions captured with reasoning and improvement suggestions
- Workflow execution resumes after approval

### Scenario 4: System Recovery and State Persistence

**Objective**: Validate system recovery after restart maintains state

**Test Steps**:

1. **Create Active Workflow with Multiple Agents**
   ```bash
   # Start complex workflow with multiple phases
   curl -X POST http://localhost:8000/api/v1/workflows \
     -H "Content-Type: application/json" \
     -d '{
       "workflow_name": "full_product_development",
       "trigger_type": "manual",
       "triggered_by": "john-pm",
       "input_context": {
         "product": "API Gateway",
         "phases": ["research", "architecture", "development", "testing", "deployment"]
       }
     }'
   ```

2. **Verify Active State**
   ```bash
   curl http://localhost:8000/api/v1/workflows
   curl http://localhost:8000/api/v1/agents
   ```
   **Expected**: Multiple agents active, workflow in progress

3. **Simulate System Restart**
   ```bash
   # Stop PM coordinator
   pkill -f pm_coordinator

   # Wait 5 seconds, restart
   sleep 5
   python -m bmad_auto.orchestration.pm_coordinator
   ```

4. **Verify State Recovery**
   ```bash
   # Check within 30 seconds of restart
   curl http://localhost:8000/api/v1/workflows
   curl http://localhost:8000/api/v1/agents
   ```
   **Expected**: All workflow states restored, agents resume from last checkpoint

**Success Criteria**:
- System restarts within 30 seconds
- All workflow states recovered from PostgreSQL
- Agent states restored with active tasks
- No data loss or corruption during restart

### Scenario 5: Resource Monitoring and Optimization

**Objective**: Validate resource monitoring and optimization recommendations

**Test Steps**:

1. **Start Resource Monitoring**
   ```bash
   python -m bmad_auto.orchestration.resource_monitor
   ```
   **Expected**: Resource monitoring active, metrics collection started

2. **Generate Load with Multiple Agents**
   ```bash
   # Start 5 concurrent workflows
   for i in {1..5}; do
     curl -X POST http://localhost:8000/api/v1/workflows \
       -H "Content-Type: application/json" \
       -d '{
         "workflow_name": "concurrent_test_'$i'",
         "trigger_type": "manual",
         "triggered_by": "john-pm"
       }' &
   done
   ```

3. **Monitor Resource Metrics**
   ```bash
   curl http://localhost:8000/api/v1/metrics/resources?time_range=1h
   ```
   **Expected**: Resource usage metrics, optimization suggestions

4. **Verify Alert Thresholds**
   ```bash
   # Check if alerts triggered at 80% resource usage
   curl http://localhost:8000/api/v1/metrics/resources | jq '.[] | select(.alert_level != "normal")'
   ```
   **Expected**: Alerts at appropriate thresholds, optimization recommendations

**Success Criteria**:
- Resource metrics collected every 30 seconds
- Alerts triggered at 80% and 95% thresholds
- Optimization recommendations generated
- System maintains performance under load

## Performance Validation

### Response Time Targets

**Routine Operations** (Target: <2 seconds):
```bash
# Test PM decision creation
time curl -X POST http://localhost:8000/api/v1/pm/decisions -d @test_decision.json

# Test agent status retrieval
time curl http://localhost:8000/api/v1/agents

# Test quality gate approval
time curl -X POST http://localhost:8000/api/v1/quality-gates/{gate_id}/approve -d @approval.json
```

**Complex Multi-Agent Coordination** (Target: <10 seconds):
```bash
# Test workflow initiation with full task breakdown
time curl -X POST http://localhost:8000/api/v1/workflows -d @complex_workflow.json

# Test resource optimization with 10 agents
time curl http://localhost:8000/api/v1/metrics/resources?optimization=true
```

### Concurrent Operations

**10-Agent Load Test**:
```bash
# Start 10 concurrent agent operations
python -m bmad_auto.testing.concurrent_load_test --agents=10 --duration=300
```
**Expected**: All operations complete successfully, no resource conflicts

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check PostgreSQL status
   pg_isready -h localhost -p 5432

   # Verify database exists
   psql -l | grep bmad_auto
   ```

2. **Claude Code Integration Failures**
   ```bash
   # Test Claude Code access
   claude --version

   # Verify session creation
   python -c "from bmad_auto.orchestration.model_provider import test_claude_session; test_claude_session()"
   ```

3. **Agent Communication Issues**
   ```bash
   # Check agent status
   curl http://localhost:8000/api/v1/agents | jq '.[] | select(.status != "active")'

   # Restart failed agents
   python -m bmad_auto.orchestration.agent_manager restart_failed
   ```

4. **Performance Issues**
   ```bash
   # Check resource usage
   curl http://localhost:8000/api/v1/metrics/resources | jq '.[] | select(.alert_level != "normal")'

   # Optimize database connections
   python -m bmad_auto.database.optimize_connections
   ```

## Success Validation Checklist

### Core Functionality
- [ ] PM orchestration hub operational
- [ ] Agent coordination and task assignment working
- [ ] Multi-provider AI model assignment functional
- [ ] Quality gate management with human approval
- [ ] System recovery and state persistence validated

### Performance Targets
- [ ] Routine operations complete in <2 seconds
- [ ] Complex coordination completes in <10 seconds
- [ ] 10-agent concurrent operations successful
- [ ] Resource usage within acceptable limits

### Integration Validation
- [ ] Claude Code terminal integration working
- [ ] PostgreSQL and coordination.db connectivity
- [ ] LangGraph workflow execution functional
- [ ] API contracts validated with test scenarios

### Quality Assurance
- [ ] PM decision reasoning captured completely
- [ ] Agent extension overlay preserves .bmad-core
- [ ] Error handling and recovery mechanisms working
- [ ] Resource monitoring and optimization active

## Next Steps

After successful quickstart validation:

1. **Proceed to `/tasks` command** for detailed implementation planning
2. **Run comprehensive test suite** for integration validation
3. **Deploy to staging environment** for full system testing
4. **Initialize agent learning framework** for continuous improvement

**Quickstart Status**: ✅ All scenarios validated, ready for implementation phase