# BMAD Auto API Reference

## Overview

This reference provides comprehensive documentation for the BMAD Auto REST API, including endpoints for workflow management, agent coordination, quality gates, and system administration. All endpoints return JSON responses and support standard HTTP status codes.

## Base Configuration

### API Base URL
```
Production: https://api.bmad-auto.com/v1
Development: http://localhost:8000/v1
```

### Authentication
```http
Authorization: Bearer <jwt_token>
X-API-Key: <api_key>
```

### Common Headers
```http
Content-Type: application/json
Accept: application/json
X-Request-ID: <unique_request_id>
```

## Workflow Management API

### Create Workflow

Create a new workflow for autonomous product development.

```http
POST /workflows
```

**Request Body:**
```json
{
  "workflow_type": "feature_development",
  "phase": "research",
  "priority": "high",
  "context": {
    "objective": "Implement user authentication system",
    "description": "Add secure login and registration functionality",
    "deliverables": [
      "Authentication API endpoints",
      "JWT token management",
      "User registration flow",
      "Password security implementation"
    ],
    "requirements": [
      "OAuth2 integration",
      "Multi-factor authentication",
      "Session management",
      "Security audit compliance"
    ],
    "constraints": {
      "timeline": "2 weeks",
      "budget": "$50000",
      "team_size": "3 developers"
    },
    "stakeholders": ["product_manager", "security_team", "development_team"],
    "success_criteria": [
      "99.9% authentication success rate",
      "Sub-200ms response time",
      "SOC2 compliance",
      "Zero security vulnerabilities"
    ]
  },
  "requested_by": "user_id_123",
  "deadline": "2024-02-15T23:59:59Z"
}
```

**Response:**
```json
{
  "workflow_id": "wf_abc123def456",
  "status": "pending",
  "phase": "research",
  "priority": "high",
  "created_at": "2024-01-15T10:30:00Z",
  "estimated_completion": "2024-02-15T18:00:00Z",
  "assigned_agents": [],
  "next_steps": [
    "Market research analysis",
    "Technical feasibility assessment",
    "Resource allocation planning"
  ]
}
```

### Get Workflow Status

Retrieve current status and progress of a workflow.

```http
GET /workflows/{workflow_id}
```

**Response:**
```json
{
  "workflow_id": "wf_abc123def456",
  "phase": "development",
  "status": "in_progress",
  "priority": "high",
  "progress_percentage": 65.5,
  "current_agent": "james",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:22:00Z",
  "estimated_completion": "2024-02-10T16:00:00Z",
  "context": {
    "objective": "Implement user authentication system",
    "deliverables": ["Authentication API endpoints", "JWT token management"],
    "current_milestone": "API endpoint implementation"
  },
  "checkpoints": [
    {
      "timestamp": "2024-01-15T11:00:00Z",
      "phase": "research",
      "agent": "mary",
      "action": "Market analysis completed",
      "result": {
        "competitive_analysis": "completed",
        "user_research": "completed",
        "market_assessment": "favorable"
      },
      "confidence_score": 0.92
    },
    {
      "timestamp": "2024-01-17T09:15:00Z",
      "phase": "specification",
      "agent": "john",
      "action": "PRD generation completed",
      "result": {
        "prd_document": "generated",
        "technical_specs": "approved",
        "implementation_plan": "finalized"
      },
      "confidence_score": 0.88
    }
  ],
  "human_approvals_required": [
    {
      "approval_type": "security_review",
      "required_role": "security_engineer",
      "description": "Review authentication implementation for security compliance",
      "blocking": true
    }
  ],
  "error_count": 0,
  "retry_attempts": 0
}
```

### List Workflows

Get paginated list of workflows with filtering options.

```http
GET /workflows?phase=development&status=in_progress&limit=20&offset=0
```

**Query Parameters:**
- `phase` (optional): Filter by workflow phase
- `status` (optional): Filter by workflow status
- `agent` (optional): Filter by assigned agent
- `priority` (optional): Filter by priority level
- `limit` (optional): Number of results per page (default: 50, max: 100)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "workflows": [
    {
      "workflow_id": "wf_abc123def456",
      "phase": "development",
      "status": "in_progress",
      "priority": "high",
      "progress_percentage": 65.5,
      "current_agent": "james",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-20T14:22:00Z"
    }
  ],
  "total_count": 157,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

### Update Workflow

Update workflow context, priority, or other modifiable fields.

```http
PATCH /workflows/{workflow_id}
```

**Request Body:**
```json
{
  "priority": "critical",
  "context": {
    "constraints": {
      "timeline": "1 week",
      "additional_requirement": "Emergency security patch"
    }
  },
  "deadline": "2024-01-25T23:59:59Z"
}
```

### Cancel Workflow

Cancel an active workflow.

```http
DELETE /workflows/{workflow_id}
```

**Request Body:**
```json
{
  "reason": "Business requirements changed",
  "force": false
}
```

## Agent Management API

### Get Agent Status

Retrieve current status and capabilities of a specific agent.

```http
GET /agents/{agent_type}
```

**Response:**
```json
{
  "agent_type": "james",
  "status": "busy",
  "current_workflows": [
    "wf_abc123def456",
    "wf_def456ghi789"
  ],
  "capabilities": {
    "technical_architecture": 0.95,
    "code_implementation": 0.92,
    "performance_optimization": 0.88,
    "security_implementation": 0.85
  },
  "performance_metrics": {
    "avg_response_time": 1.23,
    "success_rate": 0.96,
    "quality_score": 0.91,
    "tasks_completed_today": 12
  },
  "last_activity": "2024-01-20T14:20:00Z",
  "available_capacity": 0.15
}
```

### List All Agents

Get status overview of all agents.

```http
GET /agents
```

**Response:**
```json
{
  "agents": [
    {
      "agent_type": "mary",
      "status": "idle",
      "current_workflows": [],
      "performance_score": 0.94,
      "available_capacity": 1.0
    },
    {
      "agent_type": "john",
      "status": "busy",
      "current_workflows": ["wf_xyz789abc123"],
      "performance_score": 0.89,
      "available_capacity": 0.25
    },
    {
      "agent_type": "james",
      "status": "busy",
      "current_workflows": ["wf_abc123def456", "wf_def456ghi789"],
      "performance_score": 0.92,
      "available_capacity": 0.15
    }
  ],
  "system_performance": {
    "overall_efficiency": 0.91,
    "average_response_time": 1.45,
    "active_workflows": 8,
    "pending_workflows": 3
  }
}
```

### Assign Agent to Workflow

Manually assign a specific agent to a workflow.

```http
POST /workflows/{workflow_id}/assign
```

**Request Body:**
```json
{
  "agent_type": "james",
  "force_assignment": false,
  "reason": "Specific technical expertise required"
}
```

## Quality Gates API

### Trigger Quality Gate

Manually trigger a quality gate validation.

```http
POST /workflows/{workflow_id}/quality-gates/{gate_type}/validate
```

**Request Body:**
```json
{
  "validation_data": {
    "code_coverage": 85.5,
    "security_scan_results": "passed",
    "performance_benchmarks": {
      "response_time": 180,
      "throughput": 1250
    }
  },
  "override_thresholds": false
}
```

**Response:**
```json
{
  "validation_id": "qg_validation_123",
  "gate_type": "development_complete",
  "workflow_id": "wf_abc123def456",
  "status": "passed",
  "score": 0.92,
  "validation_results": {
    "code_coverage": {
      "actual": 85.5,
      "required": 80.0,
      "status": "passed"
    },
    "security_scan": {
      "vulnerabilities_found": 0,
      "status": "passed"
    },
    "performance": {
      "response_time": {
        "actual": 180,
        "threshold": 200,
        "status": "passed"
      }
    }
  },
  "validated_at": "2024-01-20T15:30:00Z",
  "validator": "quinn",
  "next_gate": "ux_validation"
}
```

### Get Quality Gate Results

Retrieve quality gate validation history for a workflow.

```http
GET /workflows/{workflow_id}/quality-gates
```

**Response:**
```json
{
  "workflow_id": "wf_abc123def456",
  "quality_gates": [
    {
      "gate_type": "development_complete",
      "status": "passed",
      "score": 0.92,
      "validated_at": "2024-01-20T15:30:00Z",
      "validator": "quinn",
      "duration_seconds": 45.2
    },
    {
      "gate_type": "security_review",
      "status": "pending",
      "initiated_at": "2024-01-20T15:35:00Z"
    }
  ],
  "overall_status": "in_progress",
  "completion_percentage": 60.0
}
```

## Integration Management API

### External Service Status

Check status of external service integrations.

```http
GET /integrations/status
```

**Response:**
```json
{
  "integrations": {
    "linear": {
      "status": "healthy",
      "last_sync": "2024-01-20T15:25:00Z",
      "response_time": 0.145,
      "sync_success_rate": 0.98
    },
    "github": {
      "status": "healthy",
      "last_sync": "2024-01-20T15:28:00Z",
      "response_time": 0.089,
      "api_rate_limit_remaining": 4850
    },
    "openai": {
      "status": "healthy",
      "response_time": 1.234,
      "requests_today": 1247,
      "cost_today": 23.45
    }
  },
  "overall_health": "healthy"
}
```

### Sync with External Service

Trigger manual synchronization with external services.

```http
POST /integrations/{service_name}/sync
```

**Request Body:**
```json
{
  "sync_type": "full",
  "workflow_ids": ["wf_abc123def456"],
  "force_sync": false
}
```

## System Administration API

### System Health

Get comprehensive system health status.

```http
GET /health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T15:30:00Z",
  "version": "1.2.0",
  "environment": "production",
  "components": {
    "database": {
      "status": "healthy",
      "response_time": 0.012,
      "active_connections": 15,
      "max_connections": 100
    },
    "redis": {
      "status": "healthy",
      "response_time": 0.003,
      "memory_usage": "245MB",
      "connected_clients": 8
    },
    "agents": {
      "status": "healthy",
      "active_agents": 5,
      "average_response_time": 1.45
    },
    "external_services": {
      "status": "healthy",
      "services_up": 3,
      "services_total": 3
    }
  },
  "metrics": {
    "active_workflows": 8,
    "pending_workflows": 3,
    "completed_today": 15,
    "system_uptime": "7d 14h 23m"
  }
}
```

### System Metrics

Get detailed system performance metrics.

```http
GET /metrics
```

**Response Format:** Prometheus metrics format

```
# HELP bmad_workflow_requests_total Total number of workflow requests
# TYPE bmad_workflow_requests_total counter
bmad_workflow_requests_total{phase="research",agent="mary",status="success"} 47
bmad_workflow_requests_total{phase="development",agent="james",status="success"} 23

# HELP bmad_workflow_duration_seconds Time spent processing workflows
# TYPE bmad_workflow_duration_seconds histogram
bmad_workflow_duration_seconds_bucket{phase="research",agent="mary",le="60"} 15
bmad_workflow_duration_seconds_bucket{phase="research",agent="mary",le="120"} 28
```

## Error Handling

### Standard Error Response Format

```json
{
  "error": {
    "code": "WORKFLOW_NOT_FOUND",
    "message": "Workflow with ID 'wf_invalid123' not found",
    "details": {
      "workflow_id": "wf_invalid123",
      "timestamp": "2024-01-20T15:30:00Z",
      "request_id": "req_xyz789abc123"
    },
    "suggestions": [
      "Verify the workflow ID is correct",
      "Check if the workflow was deleted",
      "Ensure you have access permissions"
    ]
  }
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., workflow already exists)
- `422 Unprocessable Entity` - Validation errors
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

### Common Error Codes

- `WORKFLOW_NOT_FOUND` - Specified workflow does not exist
- `AGENT_UNAVAILABLE` - Requested agent is not available
- `VALIDATION_FAILED` - Input validation failed
- `QUALITY_GATE_FAILED` - Quality gate validation failed
- `INTEGRATION_ERROR` - External service integration error
- `RATE_LIMIT_EXCEEDED` - API rate limit exceeded
- `INSUFFICIENT_PERMISSIONS` - User lacks required permissions
- `SYSTEM_OVERLOADED` - System at capacity

## Rate Limiting

API requests are rate limited per API key:

- **Standard users**: 1000 requests/hour
- **Premium users**: 5000 requests/hour
- **Enterprise users**: 20000 requests/hour

Rate limit headers are included in all responses:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1642694400
```

## Webhooks

### Workflow Status Updates

Register webhook endpoints to receive real-time workflow updates:

```http
POST /webhooks/register
```

**Request Body:**
```json
{
  "url": "https://your-domain.com/bmad-webhooks",
  "events": ["workflow.created", "workflow.completed", "quality_gate.failed"],
  "secret": "your_webhook_secret"
}
```

**Webhook Payload Example:**
```json
{
  "event": "workflow.completed",
  "timestamp": "2024-01-20T15:30:00Z",
  "data": {
    "workflow_id": "wf_abc123def456",
    "status": "completed",
    "phase": "validation",
    "success": true,
    "duration_seconds": 3600,
    "final_deliverables": ["authentication_system", "security_audit_report"]
  },
  "signature": "sha256=a1b2c3d4e5f6..."
}
```

---

*This API reference provides comprehensive documentation for integrating with BMAD Auto's autonomous product orchestration capabilities.*