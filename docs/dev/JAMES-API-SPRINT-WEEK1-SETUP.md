# 🚀 James: API Implementation Sprint - Week 1 Setup

**Date**: 2025-09-30
**Sprint Goal**: FastAPI foundation + Core endpoints (PM Decisions, Agent State)
**Duration**: Week 1 of 4-week sprint
**Estimated Effort**: 30 hours

---

## 🎯 Week 1 Objectives

### Primary Deliverables
1. ✅ FastAPI application setup with proper structure
2. ✅ PM Decisions API (`/pm/decisions`) operational
3. ✅ Agent State API (`/agents/{agent_id}`) operational
4. ✅ Integration with existing backend logic
5. ✅ Basic integration tests

---

## 📋 Task Breakdown

### T036: FastAPI Application Setup (8 hours)

#### Step 1: Project Structure (2 hours)
Create FastAPI application with clean architecture:

```
.bmad-auto/api/
├── __init__.py
├── main.py                    # FastAPI app entry point
├── config.py                  # Configuration management
├── dependencies.py            # Dependency injection
├── models/                    # Pydantic models
│   ├── __init__.py
│   ├── pm_decision.py
│   ├── agent_state.py
│   └── common.py
├── routes/                    # API endpoints
│   ├── __init__.py
│   ├── pm_decisions.py
│   ├── agent_state.py
│   └── health.py
└── middleware/                # API middleware
    ├── __init__.py
    ├── error_handler.py
    └── logging.py
```

#### Step 2: FastAPI Main Application (2 hours)

**File**: `.bmad-auto/api/main.py` (target: ~150 lines)

```python
"""
BMAD Auto API - FastAPI Application
Provides REST API access to PM orchestration, agent coordination, and workflows
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from api.routes import pm_decisions, agent_state, health
from api.middleware import error_handler, logging

# Create FastAPI application
app = FastAPI(
    title="BMAD Auto API",
    description="PM-Centric Autonomous Orchestration System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Custom middleware
app.middleware("http")(logging.log_requests)
app.add_exception_handler(Exception, error_handler.handle_exception)

# Include routers
app.include_router(
    pm_decisions.router,
    prefix="/pm/decisions",
    tags=["PM Decisions"]
)
app.include_router(
    agent_state.router,
    prefix="/agents",
    tags=["Agent State"]
)
app.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "BMAD Auto API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

#### Step 3: Configuration Management (2 hours)

**File**: `.bmad-auto/api/config.py` (target: ~100 lines)

```python
"""
BMAD Auto API Configuration
Environment-based configuration with validation
"""

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    app_name: str = "BMAD Auto API"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "bmad_auto"
    postgres_user: str = "postgres"
    postgres_password: str = ""

    # SQLite coordination.db
    coordination_db_path: str = ".bmad-auto/intercept/coordination.db"

    # BMAD Core
    bmad_core_path: str = ".bmad-core"

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Logging
    log_level: str = "INFO"
    log_file: str = ".bmad-auto/logs/api.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
```

#### Step 4: Dependency Injection (2 hours)

**File**: `.bmad-auto/api/dependencies.py` (target: ~150 lines)

```python
"""
FastAPI Dependency Injection
Provides reusable dependencies for route handlers
"""

from fastapi import Depends, HTTPException, status
from typing import AsyncGenerator
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.config import get_settings, Settings
from intercept.pm_coordinator import PMCoordinator
from orchestration.agent_manager import AgentStateManager
from database.connection_manager import DatabaseConnectionManager

async def get_db_connection():
    """Get database connection from pool"""
    settings = get_settings()
    db_manager = DatabaseConnectionManager(
        host=settings.postgres_host,
        port=settings.postgres_port,
        database=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password
    )

    async with db_manager.get_connection() as conn:
        yield conn

async def get_pm_coordinator(
    settings: Settings = Depends(get_settings)
) -> PMCoordinator:
    """Get PM Coordinator instance"""
    coordinator = PMCoordinator(
        bmad_core_path=settings.bmad_core_path,
        db_path=settings.coordination_db_path
    )
    return coordinator

async def get_agent_manager(
    settings: Settings = Depends(get_settings)
) -> AgentStateManager:
    """Get Agent State Manager instance"""
    manager = AgentStateManager(
        coordination_db_path=settings.coordination_db_path
    )
    return manager
```

---

### T031: PM Decisions API Implementation (10 hours)

#### Pydantic Models (2 hours)

**File**: `.bmad-auto/api/models/pm_decision.py` (target: ~150 lines)

```python
"""
PM Decision Pydantic Models
Request/response schemas for PM decisions API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class DecisionType(str, Enum):
    TASK_ASSIGNMENT = "task_assignment"
    QUALITY_GATE = "quality_gate"
    RESOURCE_ALLOCATION = "resource_allocation"
    ESCALATION = "escalation"

class PMDecisionCreate(BaseModel):
    """Request model for creating PM decision"""
    decision_type: DecisionType
    context_data: Dict[str, Any]
    reasoning_process: str
    outcome: str
    confidence_score: int = Field(ge=1, le=10)
    agent_assignments: Optional[Dict[str, str]] = None
    learning_notes: Optional[str] = None

class PMDecisionResponse(BaseModel):
    """Response model for PM decision"""
    decision_id: str
    decision_type: DecisionType
    context_data: Dict[str, Any]
    reasoning_process: str
    outcome: str
    confidence_score: int
    agent_assignments: Optional[Dict[str, str]]
    learning_notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class PMDecisionList(BaseModel):
    """Response model for PM decision list"""
    decisions: List[PMDecisionResponse]
    total: int
    page: int
    page_size: int
```

#### API Endpoints (8 hours)

**File**: `.bmad-auto/api/routes/pm_decisions.py` (target: ~250 lines)

```python
"""
PM Decisions API Routes
Endpoints for PM decision creation and retrieval
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from uuid import uuid4
from datetime import datetime

from api.models.pm_decision import (
    PMDecisionCreate,
    PMDecisionResponse,
    PMDecisionList,
    DecisionType
)
from api.dependencies import get_pm_coordinator, get_db_connection
from intercept.pm_coordinator import PMCoordinator

router = APIRouter()

@router.post("/", response_model=PMDecisionResponse, status_code=201)
async def create_pm_decision(
    decision: PMDecisionCreate,
    coordinator: PMCoordinator = Depends(get_pm_coordinator),
    db = Depends(get_db_connection)
):
    """
    Create new PM decision with reasoning capture

    Captures complete decision context, reasoning process, and outcome
    for cognitive framework enhancement and audit trail.
    """
    try:
        # Generate decision ID
        decision_id = str(uuid4())

        # Store decision in database via coordinator
        result = await coordinator.capture_decision(
            decision_id=decision_id,
            decision_type=decision.decision_type,
            context_data=decision.context_data,
            reasoning_process=decision.reasoning_process,
            outcome=decision.outcome,
            confidence_score=decision.confidence_score,
            agent_assignments=decision.agent_assignments,
            learning_notes=decision.learning_notes
        )

        # Return created decision
        return PMDecisionResponse(
            decision_id=decision_id,
            decision_type=decision.decision_type,
            context_data=decision.context_data,
            reasoning_process=decision.reasoning_process,
            outcome=decision.outcome,
            confidence_score=decision.confidence_score,
            agent_assignments=decision.agent_assignments,
            learning_notes=decision.learning_notes,
            created_at=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create PM decision: {str(e)}"
        )

@router.get("/", response_model=PMDecisionList)
async def list_pm_decisions(
    decision_type: Optional[DecisionType] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    coordinator: PMCoordinator = Depends(get_pm_coordinator),
    db = Depends(get_db_connection)
):
    """
    List PM decisions with filtering and pagination

    Supports filtering by decision type and paginated results
    for efficient decision history retrieval.
    """
    try:
        # Calculate offset
        offset = (page - 1) * page_size

        # Retrieve decisions from database
        decisions = await coordinator.get_decisions(
            decision_type=decision_type,
            limit=page_size,
            offset=offset
        )

        # Get total count
        total = await coordinator.count_decisions(
            decision_type=decision_type
        )

        return PMDecisionList(
            decisions=decisions,
            total=total,
            page=page,
            page_size=page_size
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve PM decisions: {str(e)}"
        )

@router.get("/{decision_id}", response_model=PMDecisionResponse)
async def get_pm_decision(
    decision_id: str,
    coordinator: PMCoordinator = Depends(get_pm_coordinator),
    db = Depends(get_db_connection)
):
    """
    Get specific PM decision by ID

    Retrieves complete decision context and reasoning for analysis.
    """
    try:
        decision = await coordinator.get_decision(decision_id)

        if not decision:
            raise HTTPException(
                status_code=404,
                detail=f"PM decision {decision_id} not found"
            )

        return decision

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve PM decision: {str(e)}"
        )
```

---

### T032: Agent State API Implementation (10 hours)

#### Pydantic Models (2 hours)

**File**: `.bmad-auto/api/models/agent_state.py` (target: ~150 lines)

```python
"""
Agent State Pydantic Models
Request/response schemas for agent state API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class AgentStatus(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

class AgentStateUpdate(BaseModel):
    """Request model for updating agent state"""
    status: AgentStatus
    current_task: Optional[str] = None
    performance_metrics: Optional[Dict[str, float]] = None
    error_message: Optional[str] = None

class AgentStateResponse(BaseModel):
    """Response model for agent state"""
    agent_id: str
    agent_name: str
    status: AgentStatus
    current_task: Optional[str]
    capabilities: List[str]
    performance_metrics: Optional[Dict[str, float]]
    error_message: Optional[str]
    last_updated: datetime

    class Config:
        from_attributes = True

class AgentStateList(BaseModel):
    """Response model for agent state list"""
    agents: List[AgentStateResponse]
    total: int
```

#### API Endpoints (8 hours)

**File**: `.bmad-auto/api/routes/agent_state.py` (target: ~250 lines)

Similar structure to pm_decisions.py with GET/PUT operations for agent state management.

---

### Integration Testing (2 hours)

**File**: `.bmad-auto/tests/api/test_pm_decisions_api.py` (target: ~200 lines)

```python
"""
PM Decisions API Integration Tests
Tests for PM decisions endpoint functionality
"""

import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_create_pm_decision(test_client: AsyncClient):
    """Test creating PM decision via API"""
    decision_data = {
        "decision_type": "task_assignment",
        "context_data": {"task": "T031 API Implementation"},
        "reasoning_process": "Analyzed task complexity and agent capabilities",
        "outcome": "Assigned to James (Developer)",
        "confidence_score": 9
    }

    response = await test_client.post("/pm/decisions/", json=decision_data)

    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert result["decision_type"] == "task_assignment"
    assert result["confidence_score"] == 9
    assert "decision_id" in result
```

---

## ✅ Week 1 Success Criteria

### Functional Requirements
- [ ] FastAPI application runs without errors
- [ ] PM Decisions API: POST and GET endpoints operational
- [ ] Agent State API: GET and PUT endpoints operational
- [ ] Endpoints integrate with existing backend (pm_coordinator, agent_manager)
- [ ] Basic error handling implemented
- [ ] Health check endpoint operational

### Quality Requirements
- [ ] All files BMAD compliant (100-300 lines)
- [ ] Pydantic models for request/response validation
- [ ] Dependency injection properly configured
- [ ] Integration tests for core endpoints
- [ ] API documentation (OpenAPI) auto-generated

### Documentation Requirements
- [ ] Update `Dev-sessions-specs-progress.md` with Week 1 completion
- [ ] Document API endpoints in project docs
- [ ] Create API usage examples

---

## 🔧 Development Setup

### Install Dependencies
```bash
cd .bmad-auto
pip install fastapi uvicorn httpx pytest-asyncio pydantic-settings
```

### Run FastAPI Application
```bash
cd .bmad-auto
python -m api.main
# Or: uvicorn api.main:app --reload
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

---

## 📊 Progress Tracking

### Daily Updates Required
Update `Dev-sessions-specs-progress.md` with:
- Files created with line counts
- Endpoints completed
- Integration status
- Blockers encountered

### End of Week 1 Deliverable
Create summary document: `API-Sprint-Week1-Summary.md`
- Completion status
- Challenges overcome
- Week 2 preparation notes

---

**Ready to Begin**: Start with FastAPI setup (Step 1) and progress through tasks sequentially.

**Support Available**: PM (John) for questions, Quinn (QA) for testing coordination.

**Timeline**: Complete Week 1 objectives by end of session batch (~30 hours work).

---

**PM Coordinator**: John (PM)
**Sprint**: API Implementation (Week 1 of 4)
**Status**: ✅ APPROVED TO BEGIN