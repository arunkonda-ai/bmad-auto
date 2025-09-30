# James (Developer) - API Implementation Assignment T031-T036

**Date**: 2025-09-29
**Assigned By**: John (PM)
**Prerequisites**: T021-T024 Agent Extension System (Awaiting Quinn's approval)
**Priority**: HIGH - Critical API layer for PM orchestration
**Update Progress In**: `.bmad-auto/docs/dev/Dev-sessions-specs-progress.md`

---

## 🎯 IMPLEMENTATION OBJECTIVE

Implement the **complete API layer (T031-T036)** as thin wrappers around existing orchestration components, exposing PM coordination capabilities through RESTful endpoints.

**Why This Makes Sense**:
- ✅ T021-T024 provides all underlying functionality
- ✅ APIs are thin presentation layer over orchestration logic
- ✅ Contract tests (T006-T012) already define expected behavior
- ✅ OpenAPI spec provides complete API contract

---

## 📋 COMPLETED FOUNDATION OVERVIEW

### **What You've Already Built** (T001-T024):
- ✅ **T017-T020**: PM Orchestration Hub with decision capture, task assignment, quality gates
- ✅ **T021-T024**: Agent Extension System with state synchronization and capability management
- ✅ **T015**: Database connection management (PostgreSQL + SQLite)
- ✅ **T006-T012**: Complete contract tests defining API behavior

### **What You're Building Now** (T031-T036):
**FastAPI application** exposing orchestration capabilities through REST endpoints:
- **T031**: PM Decisions API (`/pm/decisions`)
- **T032**: Agent State API (`/agents/{agent_id}`)
- **T033**: Workflow API (`/workflows`)
- **T034**: Model Assignment API (`/models/assign`)
- **T035**: Quality Gate API (`/quality-gates`)
- **T036**: FastAPI main application with routing and middleware

---

## 📚 CRITICAL REFERENCES

### **API Contract Specification**:
```
.bmad-auto/specs/001-foundation-pm-orchestration/contracts/pm-orchestration-api.yaml
```
**This is your source of truth** - All endpoints, schemas, and responses are defined here.

### **Contract Tests** (Expected Behavior):
```
.bmad-auto/tests/contract/
├── test_pm_decisions_api.py     # T031 test cases
├── test_agent_state_api.py      # T032 test cases
├── test_workflow_api.py         # T033 test cases
├── test_model_assignment_api.py # T034 test cases
└── test_quality_gate_api.py     # T035 test cases
```

### **Underlying Implementation** (You'll Import These):
```python
from intercept.pm_coordinator import PMCoordinator
from intercept.decision_capture import PMDecisionCapture
from orchestration.agent_manager import AgentStateManager
from agents.capability_manager import CapabilityManager
from orchestration.quality_gate_simple import QualityGateManager
```

---

## 🏗️ IMPLEMENTATION TASKS

## **T031: PM Decisions API** ⭐ START HERE

### **File**: `.bmad-auto/api/pm_decisions.py`
### **Purpose**: Expose PM decision-making context and reasoning capture
### **Lines Target**: 150-250 lines

### **Endpoints to Implement**:

```python
# POST /pm/decisions - Create PM decision
# GET  /pm/decisions - List PM decisions with filtering
# GET  /pm/decisions/{decision_id} - Get specific PM decision
```

### **Implementation Template**:

```python
"""
PM Decisions API - Expose PM decision-making context and reasoning.

Provides RESTful interface for capturing and retrieving PM decisions
with complete reasoning trails and agent assignment context.
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID, uuid4

from intercept.decision_capture import PMDecisionCapture

router = APIRouter(prefix="/pm", tags=["PM Decisions"])

# Pydantic Models (from OpenAPI schema)

class DecisionType(str):
    TASK_ASSIGNMENT = "task_assignment"
    QUALITY_GATE = "quality_gate"
    RESOURCE_ALLOCATION = "resource_allocation"
    ESCALATION = "escalation"
    MODEL_ASSIGNMENT = "model_assignment"


class PMDecisionRequest(BaseModel):
    """Request schema for creating PM decision."""
    decision_type: str = Field(..., description="Type of PM decision")
    context_data: Dict[str, Any] = Field(..., description="Decision context")
    reasoning_process: str = Field(..., min_length=10, description="PM reasoning steps")
    outcome: str = Field(..., min_length=5, description="Decision outcome")
    confidence_score: int = Field(..., ge=1, le=10, description="PM confidence 1-10")
    agent_assignments: Optional[Dict[str, str]] = Field(None, description="Agent assignments")
    resource_optimization: Optional[Dict[str, Any]] = Field(None, description="Resource optimization data")
    learning_notes: Optional[str] = Field(None, description="Learning notes for improvement")

    @validator('decision_type')
    def validate_decision_type(cls, v):
        valid_types = ['task_assignment', 'quality_gate', 'resource_allocation', 'escalation', 'model_assignment']
        if v not in valid_types:
            raise ValueError(f"Decision type must be one of: {valid_types}")
        return v


class PMDecisionResponse(BaseModel):
    """Response schema for PM decision."""
    decision_id: str
    decision_type: str
    context_data: Dict[str, Any]
    reasoning_process: str
    outcome: str
    confidence_score: int
    agent_assignments: Optional[Dict[str, str]]
    resource_optimization: Optional[Dict[str, Any]]
    learning_notes: Optional[str]
    created_at: datetime
    updated_at: datetime


# Initialize PM Decision Capture
decision_capture = PMDecisionCapture(db_path='intercept/coordination.db')


@router.post("/decisions", response_model=PMDecisionResponse, status_code=201)
async def create_pm_decision(decision: PMDecisionRequest):
    """
    Create new PM decision context.

    Captures complete PM decision-making process including:
    - Decision context and input data
    - Step-by-step reasoning process
    - Final outcome and confidence level
    - Agent assignments and resource optimization
    """
    try:
        # Capture decision using existing PMDecisionCapture
        decision_id = decision_capture.capture_decision(
            decision_type=decision.decision_type,
            context_data=decision.context_data,
            reasoning_process=decision.reasoning_process,
            outcome=decision.outcome,
            confidence_score=decision.confidence_score,
            agent_assignments=decision.agent_assignments,
            resource_optimization=decision.resource_optimization,
            learning_notes=decision.learning_notes
        )

        # Retrieve the created decision
        created_decision = decision_capture.get_decision(decision_id)

        if not created_decision:
            raise HTTPException(status_code=500, detail="Failed to create decision")

        return PMDecisionResponse(
            decision_id=str(decision_id),
            decision_type=created_decision['decision_type'],
            context_data=created_decision['context_data'],
            reasoning_process=created_decision['reasoning_process'],
            outcome=created_decision['outcome'],
            confidence_score=created_decision['confidence_score'],
            agent_assignments=created_decision.get('agent_assignments'),
            resource_optimization=created_decision.get('resource_optimization'),
            learning_notes=created_decision.get('learning_notes'),
            created_at=created_decision['created_at'],
            updated_at=created_decision['updated_at']
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid decision data: {str(e)}")


@router.get("/decisions", response_model=Dict[str, Any])
async def list_pm_decisions(
    decision_type: Optional[str] = Query(None, description="Filter by decision type"),
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Results offset")
):
    """
    List PM decisions with filtering and pagination.

    Returns paginated list of PM decisions with optional filtering
    by decision type and agent involvement.
    """
    try:
        # Retrieve decisions from PMDecisionCapture
        decisions = decision_capture.list_decisions(
            decision_type=decision_type,
            agent_id=agent_id,
            limit=limit,
            offset=offset
        )

        total = decision_capture.count_decisions(
            decision_type=decision_type,
            agent_id=agent_id
        )

        return {
            "decisions": [
                PMDecisionResponse(
                    decision_id=str(d['decision_id']),
                    decision_type=d['decision_type'],
                    context_data=d['context_data'],
                    reasoning_process=d['reasoning_process'],
                    outcome=d['outcome'],
                    confidence_score=d['confidence_score'],
                    agent_assignments=d.get('agent_assignments'),
                    resource_optimization=d.get('resource_optimization'),
                    learning_notes=d.get('learning_notes'),
                    created_at=d['created_at'],
                    updated_at=d['updated_at']
                )
                for d in decisions
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list decisions: {str(e)}")


@router.get("/decisions/{decision_id}", response_model=PMDecisionResponse)
async def get_pm_decision(decision_id: str = Path(..., description="PM decision ID")):
    """
    Get specific PM decision by ID.

    Retrieves complete PM decision context including all reasoning
    and outcome data.
    """
    try:
        decision = decision_capture.get_decision(decision_id)

        if not decision:
            raise HTTPException(status_code=404, detail=f"PM decision {decision_id} not found")

        return PMDecisionResponse(
            decision_id=str(decision['decision_id']),
            decision_type=decision['decision_type'],
            context_data=decision['context_data'],
            reasoning_process=decision['reasoning_process'],
            outcome=decision['outcome'],
            confidence_score=decision['confidence_score'],
            agent_assignments=decision.get('agent_assignments'),
            resource_optimization=decision.get('resource_optimization'),
            learning_notes=decision.get('learning_notes'),
            created_at=decision['created_at'],
            updated_at=decision['updated_at']
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve decision: {str(e)}")
```

### **T031 Implementation Checklist**:
- [ ] Create `.bmad-auto/api/pm_decisions.py`
- [ ] Import `PMDecisionCapture` from `intercept.decision_capture`
- [ ] Implement 3 endpoints: POST, GET (list), GET (by ID)
- [ ] Use Pydantic models from OpenAPI schema
- [ ] Add proper error handling and HTTP status codes
- [ ] Validate file size: 150-250 lines
- [ ] Test against `test_pm_decisions_api.py` contract tests

---

## **T032: Agent State API**

### **File**: `.bmad-auto/api/agent_state.py`
### **Purpose**: Expose agent status tracking and coordination
### **Lines Target**: 200-250 lines

### **Endpoints to Implement**:

```python
# GET   /agents - List all agents
# GET   /agents/{agent_id} - Get agent state
# PATCH /agents/{agent_id} - Update agent state
```

### **Implementation Guidance**:

```python
"""
Agent State API - Real-time agent status and coordination interface.

Provides RESTful access to agent state management, status tracking,
and capability information for 10-agent ecosystem.
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from orchestration.agent_manager import AgentStateManager, AgentStatus

router = APIRouter(prefix="/agents", tags=["Agent State"])

# Initialize AgentStateManager
agent_manager = AgentStateManager()


class AgentRole(str):
    PM = "pm"
    ARCHITECT = "architect"
    DEVELOPER = "developer"
    QA = "qa"
    UX = "ux"
    ANALYST = "analyst"


class AgentStateResponse(BaseModel):
    """Response schema for agent state."""
    agent_id: str
    agent_name: str
    agent_role: str
    status: str  # AgentStatus enum
    capabilities: List[str]
    active_tasks: List[str]
    resource_utilization: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    last_activity: datetime
    created_at: datetime
    updated_at: datetime


class AgentStateUpdate(BaseModel):
    """Request schema for updating agent state."""
    status: Optional[str] = Field(None, description="New agent status")
    capabilities: Optional[List[str]] = Field(None, description="Updated capabilities")
    extension_config: Optional[Dict[str, Any]] = Field(None, description="Extension configuration")


@router.get("", response_model=List[AgentStateResponse])
async def list_agents(
    status: Optional[str] = Query(None, description="Filter by status"),
    role: Optional[str] = Query(None, description="Filter by role")
):
    """
    List all agents with optional filtering.

    Returns current status and capabilities of all agents
    in the 10-agent ecosystem.
    """
    # Implementation:
    # 1. Query agent_manager for all registered agents
    # 2. Apply status and role filters
    # 3. Return list of AgentStateResponse
    pass


@router.get("/{agent_id}", response_model=AgentStateResponse)
async def get_agent_state(agent_id: str = Path(..., description="Agent ID")):
    """
    Get specific agent state.

    Retrieves complete state information for a single agent
    including status, capabilities, and performance metrics.
    """
    # Implementation:
    # 1. Query agent_manager.get_agent_status(agent_id)
    # 2. If not found, raise 404
    # 3. Return AgentStateResponse with full state
    pass


@router.patch("/{agent_id}", response_model=AgentStateResponse)
async def update_agent_state(
    agent_id: str = Path(..., description="Agent ID"),
    update: AgentStateUpdate = ...
):
    """
    Update agent state.

    Updates agent status, capabilities, or configuration.
    Used for agent lifecycle management and coordination.
    """
    # Implementation:
    # 1. Validate agent exists
    # 2. Apply updates using agent_manager.update_agent_status()
    # 3. Return updated AgentStateResponse
    pass
```

### **T032 Implementation Checklist**:
- [ ] Create `.bmad-auto/api/agent_state.py`
- [ ] Import `AgentStateManager` from `orchestration.agent_manager`
- [ ] Implement 3 endpoints: GET (list), GET (by ID), PATCH (update)
- [ ] Handle async operations properly
- [ ] Add filtering logic for status and role
- [ ] Validate file size: 200-250 lines
- [ ] Test against `test_agent_state_api.py` contract tests

---

## **T033: Workflow API**

### **File**: `.bmad-auto/api/workflows.py`
### **Purpose**: Expose LangGraph workflow management
### **Lines Target**: 200-250 lines

### **Endpoints to Implement**:

```python
# POST /workflows - Start new workflow
# GET  /workflows - List workflows with filtering
# GET  /workflows/{execution_id} - Get specific workflow execution
```

### **Key Implementation Points**:
- Integrate with PM Coordinator's workflow registration system
- Handle workflow state persistence
- Provide real-time workflow status updates
- Support workflow filtering by status and agent

### **T033 Implementation Checklist**:
- [ ] Create `.bmad-auto/api/workflows.py`
- [ ] Import workflow management from PM Coordinator
- [ ] Implement workflow creation and tracking
- [ ] Add workflow status enumeration (pending, running, completed, failed)
- [ ] Validate file size: 200-250 lines
- [ ] Test against `test_workflow_api.py` contract tests

---

## **T034: Model Assignment API**

### **File**: `.bmad-auto/api/model_assignment.py`
### **Purpose**: Expose multi-provider AI model assignment
### **Lines Target**: 150-200 lines

### **Endpoints to Implement**:

```python
# POST /models/assign - Assign AI model to agent task
```

### **Key Implementation Points**:
- Integrate with multi-provider model assignment logic
- Support Claude Code, Anthropic Claude, Z.ai GLM providers
- Implement intelligent model selection based on task complexity
- Track model assignments and costs

### **T034 Implementation Checklist**:
- [ ] Create `.bmad-auto/api/model_assignment.py`
- [ ] Implement intelligent model assignment algorithm
- [ ] Support provider preferences (claude_code, anthropic_claude, zai_glm)
- [ ] Add cost estimation and tracking
- [ ] Validate file size: 150-200 lines
- [ ] Test against `test_model_assignment_api.py` contract tests

---

## **T035: Quality Gate API**

### **File**: `.bmad-auto/api/quality_gates.py`
### **Purpose**: Expose quality gate management and approval workflows
### **Lines Target**: 200-250 lines

### **Endpoints to Implement**:

```python
# GET  /quality-gates - List quality gates requiring approval
# POST /quality-gates/{gate_id}/approve - Approve quality gate with PM decision
```

### **Key Implementation Points**:
- Integrate with QualityGateManager from orchestration
- Support approval workflow with PM decision capture
- Handle escalation to human oversight
- Track quality metrics and scores

### **T035 Implementation Checklist**:
- [ ] Create `.bmad-auto/api/quality_gates.py`
- [ ] Import quality gate orchestration components
- [ ] Implement approval workflow with PM reasoning
- [ ] Add quality score validation (0.0-10.0)
- [ ] Validate file size: 200-250 lines
- [ ] Test against `test_quality_gate_api.py` contract tests

---

## **T036: FastAPI Main Application** ⭐ COMPLETE LAST

### **File**: `.bmad-auto/api/main.py`
### **Purpose**: FastAPI application with routing, middleware, and configuration
### **Lines Target**: 150-200 lines

### **Implementation Template**:

```python
"""
BMAD Auto PM Orchestration Hub API - Main Application.

FastAPI application providing RESTful interface to PM-centric
10-agent coordination and orchestration capabilities.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
import time
from typing import Dict, Any

# Import all API routers
from .pm_decisions import router as pm_decisions_router
from .agent_state import router as agent_state_router
from .workflows import router as workflows_router
from .model_assignment import router as model_assignment_router
from .quality_gates import router as quality_gates_router

# Initialize FastAPI application
app = FastAPI(
    title="PM Orchestration Hub API",
    description="Core API for PM-centric agent coordination and workflow management",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all API requests with timing."""
    start_time = time.time()

    logger.info(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    duration = time.time() - start_time
    logger.info(f"Response: {response.status_code} ({duration:.3f}s)")

    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.

    Returns system health status and basic metrics.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": time.time()
    }


# System status endpoint
@app.get("/api/v1/status", tags=["System"])
async def system_status() -> Dict[str, Any]:
    """
    Get comprehensive system status.

    Returns status of all agents, active workflows, and system health.
    """
    from intercept.pm_coordinator import PMCoordinator

    coordinator = PMCoordinator()
    status = coordinator.get_system_status()

    return status


# Include all API routers with /api/v1 prefix
app.include_router(pm_decisions_router, prefix="/api/v1")
app.include_router(agent_state_router, prefix="/api/v1")
app.include_router(workflows_router, prefix="/api/v1")
app.include_router(model_assignment_router, prefix="/api/v1")
app.include_router(quality_gates_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### **T036 Implementation Checklist**:
- [ ] Create `.bmad-auto/api/main.py`
- [ ] Import all 5 API routers (T031-T035)
- [ ] Configure FastAPI with CORS middleware
- [ ] Add request logging middleware
- [ ] Implement health check and system status endpoints
- [ ] Add exception handlers for validation and general errors
- [ ] Configure OpenAPI documentation URLs
- [ ] Validate file size: 150-200 lines
- [ ] Test complete API integration

---

## 🧪 TESTING STRATEGY

### **Contract Test Integration**:

Your APIs must pass **all existing contract tests** (T006-T012):

```bash
# Run contract tests after implementation
cd .bmad-auto
pytest tests/contract/test_pm_decisions_api.py -v
pytest tests/contract/test_agent_state_api.py -v
pytest tests/contract/test_workflow_api.py -v
pytest tests/contract/test_model_assignment_api.py -v
pytest tests/contract/test_quality_gate_api.py -v
```

### **Manual Testing**:

```bash
# Start FastAPI server
cd .bmad-auto/api
python main.py

# Test endpoints with curl
curl -X POST http://localhost:8000/api/v1/pm/decisions \
  -H "Content-Type: application/json" \
  -d '{
    "decision_type": "task_assignment",
    "context_data": {"task": "Test task"},
    "reasoning_process": "Testing API endpoint",
    "outcome": "API test successful",
    "confidence_score": 8
  }'

curl http://localhost:8000/api/v1/agents
curl http://localhost:8000/api/v1/workflows
```

### **Interactive API Testing**:

```bash
# Open Swagger UI
open http://localhost:8000/api/v1/docs

# Or ReDoc
open http://localhost:8000/api/v1/redoc
```

---

## 📊 BMAD COMPLIANCE VALIDATION

### **File Size Compliance**:

All API files must remain within **100-300 lines**:

```python
# Check file sizes
wc -l .bmad-auto/api/*.py

# Expected:
# pm_decisions.py:      150-250 lines ✓
# agent_state.py:       200-250 lines ✓
# workflows.py:         200-250 lines ✓
# model_assignment.py:  150-200 lines ✓
# quality_gates.py:     200-250 lines ✓
# main.py:              150-200 lines ✓
```

### **If Any File Exceeds 300 Lines**:
1. Extract Pydantic models to separate file: `api/models.py`
2. Extract shared utilities to: `api/utils.py`
3. Keep router logic modular and focused

---

## 🚀 IMPLEMENTATION SEQUENCE

### **Recommended Order**:

1. **T036 First**: Create `main.py` with empty routers
   - Set up FastAPI application structure
   - Configure middleware and exception handlers
   - Test basic health check endpoint

2. **T031**: Implement PM Decisions API
   - Simplest integration with existing PMDecisionCapture
   - Test thoroughly before moving forward

3. **T032**: Implement Agent State API
   - Integrate with AgentStateManager
   - Async operations require careful handling

4. **T033**: Implement Workflow API
   - More complex workflow state management
   - Integrate with PM Coordinator

5. **T034**: Implement Model Assignment API
   - Relatively straightforward model assignment logic

6. **T035**: Implement Quality Gate API
   - Complex approval workflows
   - Integrate with quality orchestration

7. **Return to T036**: Complete integration testing
   - Verify all routers work together
   - Test complete API surface

---

## 📝 PROGRESS TRACKING

### **Update Dev-sessions-specs-progress.md After Each Task**:

```markdown
## 🛠️ T031-T036 API IMPLEMENTATION - James (Developer)

**Implementation Date**: 2025-09-29
**Session Duration**: [Track as you work]

### T031: PM Decisions API
- **Status**: ✅ COMPLETE / 🔄 IN PROGRESS / ⏳ NOT STARTED
- **File**: `.bmad-auto/api/pm_decisions.py`
- **Lines**: [Actual line count]
- **Notes**: [Any implementation notes or issues]

### T032: Agent State API
- **Status**: ✅ COMPLETE / 🔄 IN PROGRESS / ⏳ NOT STARTED
- **File**: `.bmad-auto/api/agent_state.py`
- **Lines**: [Actual line count]
- **Notes**: [Any implementation notes]

[Continue for T033-T036...]

### Overall T031-T036 Assessment:
- **BMAD Compliance**: All files 100-300 lines ✅ / ⚠️ / ❌
- **Contract Tests**: All passing ✅ / ⚠️ / ❌
- **Integration**: FastAPI app operational ✅ / ⚠️ / ❌
- **Recommendation**: READY FOR PRODUCTION / NEEDS FIXES
```

---

## 🎯 SUCCESS CRITERIA

### **T031-T036 Complete When**:

1. **All 6 Files Implemented**:
   - ✅ pm_decisions.py (150-250 lines)
   - ✅ agent_state.py (200-250 lines)
   - ✅ workflows.py (200-250 lines)
   - ✅ model_assignment.py (150-200 lines)
   - ✅ quality_gates.py (200-250 lines)
   - ✅ main.py (150-200 lines)

2. **All Contract Tests Pass**:
   - ✅ test_pm_decisions_api.py (100% pass)
   - ✅ test_agent_state_api.py (100% pass)
   - ✅ test_workflow_api.py (100% pass)
   - ✅ test_model_assignment_api.py (100% pass)
   - ✅ test_quality_gate_api.py (100% pass)

3. **FastAPI Application Operational**:
   - ✅ Server starts without errors
   - ✅ Swagger UI accessible at `/api/v1/docs`
   - ✅ Health check returns 200 OK
   - ✅ System status endpoint returns agent data

4. **BMAD Compliance**:
   - ✅ All files within 100-300 line limits
   - ✅ Modular architecture maintained
   - ✅ No modifications to existing orchestration files

---

## 🚨 COMMON PITFALLS TO AVOID

### **1. File Size Violations**:
❌ **Don't**: Put all Pydantic models in endpoint files
✅ **Do**: Extract shared models to `api/models.py` if needed

### **2. Tight Coupling**:
❌ **Don't**: Duplicate orchestration logic in API layer
✅ **Do**: Use thin wrappers calling existing components

### **3. Async/Sync Confusion**:
❌ **Don't**: Mix sync and async calls incorrectly
✅ **Do**: Use `async def` for all FastAPI endpoints, call sync functions with proper handling

### **4. Missing Error Handling**:
❌ **Don't**: Let exceptions bubble up without context
✅ **Do**: Catch specific exceptions, return proper HTTP status codes

### **5. Schema Mismatches**:
❌ **Don't**: Deviate from OpenAPI contract specifications
✅ **Do**: Match Pydantic models exactly to OpenAPI schemas

---

## 📞 QUESTIONS & ESCALATION

### **If You Encounter Issues**:

1. **Contract Test Failures**: Review OpenAPI spec, ensure exact schema match
2. **Import Errors**: Verify all orchestration components exist from T021-T024
3. **File Size Issues**: Extract shared code to separate modules
4. **Performance Concerns**: Use async operations, avoid blocking calls

### **Escalate to John (PM) If**:
- Contract specifications are ambiguous or incomplete
- Orchestration components don't provide needed functionality
- BMAD compliance cannot be achieved with current architecture
- Critical blocker preventing implementation

---

## 🎬 READY TO START?

### **Pre-Implementation Checklist**:
- [ ] Quinn has approved T021-T024 (Agent Extension System)
- [ ] Read OpenAPI contract specification completely
- [ ] Review existing orchestration components (PM Coordinator, Agent Manager)
- [ ] Understand contract test expectations
- [ ] Development environment ready (FastAPI, uvicorn installed)

### **Let's Build the API Layer!**

Start with **T036 (main.py)** to set up FastAPI structure, then implement endpoints in order: T031 → T032 → T033 → T034 → T035.

**Good luck, James! The orchestration layer is waiting for its API interface.**

---

**Document Created**: 2025-09-29
**Priority**: HIGH
**Estimated Duration**: 8-10 hours for all 6 tasks
**Dependencies**: T021-T024 approval by Quinn
**Update Progress In**: `.bmad-auto/docs/dev/Dev-sessions-specs-progress.md`