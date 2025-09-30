# BMAD Auto State Management Implementation

## Overview

The BMAD Auto state management system implements PM-centric database context coordination with command simulation state persistence. John (PM) manages all state distribution across 10 agents using JSON protocol, vector embeddings for learning, and AG UI integration for human collaboration state tracking.

## Architecture Overview

### PM-Centric State Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                 ARUN STRATEGIC STATE LAYER                     │
│            (Strategic Context, Quality Gate Approvals)         │
├─────────────────────────────────────────────────────────────────┤
│                  PM ORCHESTRATION STATE LAYER                  │
│         (PM Context Distribution, Agent Coordination)          │
├─────────────────────────────────────────────────────────────────┤
│                  AGENT EXECUTION STATE LAYER                   │
│        (Agent Decisions, Learning Storage, Task Progress)      │
├─────────────────────────────────────────────────────────────────┤
│                 COMMAND SIMULATION STATE LAYER                 │
│          (Simulated Commands, API Logs, Integration State)     │
├─────────────────────────────────────────────────────────────────┤
│                  AG UI COLLABORATION STATE                     │
│        (Human Interactions, Approval Workflows, Monitoring)    │
└─────────────────────────────────────────────────────────────────┘
```

### Core State Management Components
- **PMContextManager**: PM-centric context distribution and coordination state
- **AgentLearningStorage**: Vector embeddings and agent decision storage
- **CommandSimulationLogger**: Command simulation state and audit trails
- **AGUIStateCoordinator**: Human-AI collaboration state management
- **DatabaseContextPersistence**: JSON protocol database state persistence

## PM Database Context Management

### PM Context Database Implementation
```python
# bmad-auto/src/services/database_context.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Any
from ..models.pm_context import PMTaskContext, AgentDecision
from .vector_storage import VectorEmbeddingManager

class PMContextDatabaseManager:
    """PM-centric database context management with vector storage integration"""

    def __init__(self, database_url: str):
        self.engine = create_async_engine(
            database_url,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            echo=False
        )
        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session with automatic cleanup"""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    async def store_pm_task_context(self, pm_context: PMTaskContext) -> str:
        """Store PM task context with vector embeddings for semantic retrieval"""
        async with self.get_session() as session:
            try:
                # Generate vector embedding for context
                context_embedding = await self.vector_manager.generate_embedding(
                    pm_context.context_data
                )

                # Create database entry
                db_context = PMTaskContextDB(
                    task_id=pm_context.task_id,
                    pm_id="john",
                    agent_id=pm_context.assigned_agent,
                    context_data=pm_context.to_json(),
                    vector_embedding=context_embedding,
                    created_at=datetime.utcnow(),
                    status="assigned"
                )

                session.add(db_context)
                await session.flush()

                return db_context.task_id

            except Exception as e:
                logger.error(f"Failed to store PM context: {e}")
                raise

    async def load_workflow_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Load workflow state with consistency validation"""
        async with self.get_session() as session:
            try:
                db_state = await session.get(WorkflowStateDB, workflow_id)
                if db_state:
                    return WorkflowState(**db_state.to_dict())
                return None

            except Exception as e:
                logger.error(f"Failed to load workflow state: {e}")
                return None
```

### PM Context Database Schema
```python
# bmad-auto/src/models/pm_context_schema.py
from sqlalchemy import Column, String, DateTime, Text, Integer, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid

Base = declarative_base()

class PMTaskContextDB(Base):
    """Database model for PM task context and coordination"""
    __tablename__ = "pm_task_contexts"

    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pm_id = Column(String(20), nullable=False, default="john", index=True)
    agent_id = Column(String(20), nullable=False, index=True)
    context_data = Column(JSON, nullable=False)
    vector_embedding = Column(ARRAY(Float), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(20), nullable=False, default="assigned")
    boundaries = Column(JSON, nullable=False, default=dict)
    priority = Column(String(20), nullable=False, default="medium")

class AgentDecisionDB(Base):
    """Database model for agent decision storage and PM review"""
    __tablename__ = "agent_decisions"

    decision_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    agent_id = Column(String(20), nullable=False, index=True)
    decision_data = Column(JSON, nullable=False)
    decision_rationale = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=False, default=0.0)
    requires_pm_review = Column(Boolean, nullable=False, default=False)
    pm_reviewed = Column(Boolean, nullable=False, default=False)
    pm_criticism = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    vector_embedding = Column(ARRAY(Float), nullable=True)

class CommandSimulationLogDB(Base):
    """Database model for command simulation audit and learning"""
    __tablename__ = "command_simulation_logs"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pm_id = Column(String(20), nullable=False, default="john")
    agent_id = Column(String(20), nullable=True, index=True)
    command_type = Column(String(50), nullable=False, index=True)
    original_command = Column(Text, nullable=False)
    simulated_action = Column(JSON, nullable=False)
    external_service = Column(String(30), nullable=True, index=True)
    success = Column(Boolean, nullable=False, default=True)
    error_details = Column(Text, nullable=True)
    execution_time = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

class AGUICollaborationDB(Base):
    """Database model for AG UI human-AI collaboration state"""
    __tablename__ = "agui_collaboration_state"

    collaboration_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    collaboration_type = Column(String(30), nullable=False, index=True)  # approval, discussion, monitoring
    human_participants = Column(ARRAY(String), nullable=False)
    ai_participants = Column(ARRAY(String), nullable=False)
    discussion_context = Column(JSON, nullable=False)
    approval_required = Column(Boolean, nullable=False, default=False)
    approval_timeout = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False, default="active")
    resolution = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Agent assignment
    current_agent = Column(String(20), index=True)
    agent_workload = Column(JSON, default=dict)

    # Timing
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    estimated_completion = Column(DateTime)

    # Context and progress
    context = Column(JSON, nullable=False)
    checkpoints = Column(JSON, default=list)
    progress_percentage = Column(Float, default=0.0)

    # Human oversight
    human_approvals_required = Column(JSON, default=list)
    approval_history = Column(JSON, default=list)

    # Error handling and versioning
    error_count = Column(Integer, default=0)
    last_error = Column(Text)
    retry_attempts = Column(Integer, default=0)
    version = Column(Integer, default=1)

    def to_dict(self) -> dict:
        """Convert database model to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

class AgentStateDB(Base):
    """Database model for agent state persistence"""
    __tablename__ = "agent_states"

    agent_id = Column(String(50), primary_key=True)
    agent_type = Column(String(20), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="idle")
    current_workflows = Column(JSON, default=list)
    capabilities = Column(JSON, default=dict)
    performance_metrics = Column(JSON, default=dict)
    last_activity = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
```

## PM Context Coordination

### PM Context Distribution Manager
```python
# bmad-auto/src/orchestration/pm_context_manager.py
from ..services.database_context import PMContextDatabaseManager
from ..services.vector_storage import VectorEmbeddingManager
from ..services.command_logger import CommandLogger
from ..services.agui_coordinator import AGUICoordinator

class PMContextCoordinator:
    """PM-centric context distribution and coordination management"""

    def __init__(self):
        self.db_manager = PMContextDatabaseManager()
        self.vector_manager = VectorEmbeddingManager()
        self.command_logger = CommandLogger()
        self.agui_coordinator = AGUICoordinator()
        self.agent_contexts: Dict[str, Dict[str, Any]] = {}

    async def distribute_context_to_agent(self, agent_id: str,
                                         context: Dict[str, Any],
                                         task_boundaries: Dict[str, Any]) -> str:
        """PM distributes context to specific agent with defined boundaries"""
        try:
            # Create PM task context
            pm_task_context = PMTaskContext(
                pm_id="john",
                assigned_agent=agent_id,
                context_data=context,
                boundaries=task_boundaries,
                priority=context.get("priority", "medium")
            )

            # Store in database with vector embedding
            task_id = await self.db_manager.store_pm_task_context(pm_task_context)

            # Log PM coordination action
            await self.command_logger.log_pm_coordination_action({
                "action": "context_distribution",
                "task_id": task_id,
                "agent_id": agent_id,
                "context_summary": context.get("summary", "context_distributed"),
                "boundaries": task_boundaries
            })

            # Update agent's working context
            if agent_id not in self.agent_contexts:
                self.agent_contexts[agent_id] = {}

            self.agent_contexts[agent_id][task_id] = {
                "context": context,
                "boundaries": task_boundaries,
                "assigned_at": datetime.utcnow(),
                "status": "assigned"
            }

            return task_id

        except Exception as e:
            logger.error(f"Failed to distribute context to agent {agent_id}: {e}")
            raise

    async def create_checkpoint(self, workflow_id: str,
                              checkpoint: WorkflowCheckpoint) -> bool:
        """Create workflow checkpoint with atomic persistence"""
        try:
            current_state = await self.load_workflow_state(workflow_id)
            if not current_state:
                return False

            # Add checkpoint
            current_state.checkpoints.append(checkpoint)
            current_state.updated_at = datetime.now()

            # Calculate progress update
            progress_update = self._calculate_progress_from_checkpoints(
                current_state.checkpoints
            )
            current_state.progress_percentage = progress_update

            # Persist updated state
            return await self.db.persist_workflow_state(current_state)

        except Exception as e:
            logger.error(f"Failed to create checkpoint: {e}")
            return False

    def _validate_state_transition(self, current: WorkflowState,
                                 updated: WorkflowState) -> bool:
        """Validate state transition rules"""
        # Define valid transitions
        valid_transitions = {
            WorkflowStatus.PENDING: [WorkflowStatus.IN_PROGRESS, WorkflowStatus.FAILED],
            WorkflowStatus.IN_PROGRESS: [WorkflowStatus.AWAITING_APPROVAL, WorkflowStatus.COMPLETED, WorkflowStatus.FAILED],
            WorkflowStatus.AWAITING_APPROVAL: [WorkflowStatus.IN_PROGRESS, WorkflowStatus.COMPLETED, WorkflowStatus.ESCALATED],
            WorkflowStatus.COMPLETED: [],  # Terminal state
            WorkflowStatus.FAILED: [WorkflowStatus.PENDING, WorkflowStatus.IN_PROGRESS],
            WorkflowStatus.ESCALATED: [WorkflowStatus.IN_PROGRESS, WorkflowStatus.FAILED]
        }

        if updated.status not in valid_transitions.get(current.status, []):
            logger.warning(f"Invalid transition: {current.status} -> {updated.status}")
            return False

        return True
```

## Agent Decision State Management

### Agent Decision Storage and PM Review
```python
# bmad-auto/src/orchestration/agent_decision_manager.py
from ..models.pm_context_schema import AgentDecisionDB
from ..services.vector_storage import VectorEmbeddingManager

class AgentDecisionStateManager:
    """Manages agent decision storage and PM review cycles"""

    def __init__(self, pm_context_coordinator: PMContextCoordinator):
        self.pm_coordinator = pm_context_coordinator
        self.db_manager = pm_context_coordinator.db_manager
        self.vector_manager = VectorEmbeddingManager()
        self.pending_pm_reviews: Dict[str, List[str]] = {}  # agent_id -> [decision_ids]

    async def store_agent_decision(self, task_id: str, agent_id: str,
                                 decision_data: Dict[str, Any]) -> str:
        """Store agent decision for PM review and learning"""
        try:
            # Generate decision embedding for learning
            decision_embedding = await self.vector_manager.generate_embedding(
                decision_data
            )

            # Create decision record
            decision_record = AgentDecisionDB(
                task_id=task_id,
                agent_id=agent_id,
                decision_data=decision_data,
                decision_rationale=decision_data.get("rationale", ""),
                confidence_score=decision_data.get("confidence", 0.0),
                requires_pm_review=decision_data.get("complexity", 0.0) > 0.7,
                vector_embedding=decision_embedding
            )

            # Store in database
            async with self.db_manager.get_session() as session:
                session.add(decision_record)
                await session.flush()
                decision_id = decision_record.decision_id

            # Add to PM review queue if needed
            if decision_record.requires_pm_review:
                if agent_id not in self.pending_pm_reviews:
                    self.pending_pm_reviews[agent_id] = []
                self.pending_pm_reviews[agent_id].append(decision_id)

            # Store learning pattern
            await self._store_decision_learning_pattern(decision_record)

            return decision_id

        except Exception as e:
            logger.error(f"Failed to store agent decision: {e}")
            raise

    async def process_pm_criticism(self, decision_id: str,
                                 pm_criticism: Dict[str, Any]) -> bool:
        """Process PM criticism and update agent decision record"""
        try:
            async with self.db_manager.get_session() as session:
                decision_record = await session.get(AgentDecisionDB, decision_id)
                if not decision_record:
                    return False

                # Update with PM criticism
                decision_record.pm_reviewed = True
                decision_record.pm_criticism = pm_criticism

                # Remove from pending reviews
                agent_id = decision_record.agent_id
                if agent_id in self.pending_pm_reviews:
                    if decision_id in self.pending_pm_reviews[agent_id]:
                        self.pending_pm_reviews[agent_id].remove(decision_id)

                await session.commit()

            # Store criticism learning for agent improvement
            await self._store_criticism_learning_pattern(decision_record, pm_criticism)

            return True

        except Exception as e:
            logger.error(f"Failed to process PM criticism: {e}")
            return False

    async def release_agent_from_workflow(self, agent_type: AgentType,
                                        workflow_id: str) -> bool:
        """Release agent from workflow with state cleanup"""
        async with self._get_coordination_lock(agent_type.value):
            try:
                agent_state = await self.get_agent_state(agent_type)

                # Remove workflow from agent
                if workflow_id in agent_state.current_workflows:
                    agent_state.current_workflows.remove(workflow_id)

                # Update agent status
                if not agent_state.current_workflows:
                    agent_state.status = AgentStatus.IDLE

                agent_state.last_activity = datetime.now()

                # Persist updated state
                await self._persist_agent_state(agent_state)

                return True

            except Exception as e:
                logger.error(f"Failed to release agent: {e}")
                return False

    def _get_coordination_lock(self, key: str) -> asyncio.Lock:
        """Get or create coordination lock for thread-safe operations"""
        if key not in self.coordination_locks:
            self.coordination_locks[key] = asyncio.Lock()
        return self.coordination_locks[key]
```

## Command Simulation State Management

### Command Simulation Logger
```python
# bmad-auto/src/services/command_simulation_state.py
from ..models.pm_context_schema import CommandSimulationLogDB
from ..integration.linear_mcp import LinearMCP
from ..integration.github_api import GitHubAPI

class CommandSimulationStateManager:
    """Manage state for command simulation and external coordination"""

    def __init__(self, pm_context_coordinator: PMContextCoordinator):
        self.pm_coordinator = pm_context_coordinator
        self.db_manager = pm_context_coordinator.db_manager
        self.linear_mcp = LinearMCP()
        self.github_api = GitHubAPI()
        self.command_queue = asyncio.Queue()

    async def log_simulated_command(self, pm_id: str, agent_id: str,
                                  command_type: str, command_data: Dict[str, Any]) -> str:
        """Log simulated command execution for audit and learning"""
        try:
            start_time = time.time()
            success = True
            error_details = None
            simulated_action = {}

            # Simulate command based on type
            if command_type == "linear_update":
                simulated_action = await self._simulate_linear_command(command_data)
            elif command_type == "github_operation":
                simulated_action = await self._simulate_github_command(command_data)
            elif command_type == "agui_notification":
                simulated_action = await self._simulate_agui_command(command_data)
            else:
                simulated_action = await self._simulate_generic_command(command_data)

            execution_time = time.time() - start_time

            # Create log record
            log_record = CommandSimulationLogDB(
                pm_id=pm_id,
                agent_id=agent_id,
                command_type=command_type,
                original_command=str(command_data),
                simulated_action=simulated_action,
                external_service=command_data.get("service", None),
                success=success,
                error_details=error_details,
                execution_time=execution_time
            )

            # Store in database
            async with self.db_manager.get_session() as session:
                session.add(log_record)
                await session.flush()
                log_id = log_record.log_id

            return log_id

        except Exception as e:
            logger.error(f"Failed to log simulated command: {e}")
            raise

    async def _simulate_linear_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate Linear command through MCP or API"""
        if self.linear_mcp.mcp_available:
            return await self.linear_mcp.simulate_via_mcp(command_data)
        else:
            return await self.linear_mcp.simulate_via_api(command_data)

    async def sync_linear_to_workflow(self, linear_issue_id: str) -> bool:
        """Sync Linear issue updates back to workflow state"""
        try:
            # Get Linear issue details
            linear_issue = await self.linear.get_issue(linear_issue_id)
            if not linear_issue:
                return False

            # Find corresponding workflow
            workflow_id = linear_issue.identifier  # Assuming Linear identifier matches workflow_id
            workflow_state = await self.state_manager.load_workflow_state(workflow_id)

            if not workflow_state:
                logger.warning(f"No workflow found for Linear issue {linear_issue_id}")
                return False

            # Generate updates from Linear changes
            updates = self._linear_to_workflow_updates(linear_issue, workflow_state)

            if updates:
                await self.state_manager.update_workflow_state(workflow_id, updates)

            return True

        except Exception as e:
            logger.error(f"Failed to sync from Linear: {e}")
            return False
```

## AG UI Collaboration State Management

### Human-AI Collaboration State
```python
# bmad-auto/src/services/agui_state_manager.py
from ..models.pm_context_schema import AGUICollaborationDB
from .agui_coordinator import AGUICoordinator

class AGUICollaborationStateManager:
    """Manage state for AG UI human-AI collaboration workflows"""

    def __init__(self, pm_context_coordinator: PMContextCoordinator):
        self.pm_coordinator = pm_context_coordinator
        self.db_manager = pm_context_coordinator.db_manager
        self.agui_coordinator = AGUICoordinator()
        self.active_collaborations: Dict[str, Dict[str, Any]] = {}

    async def create_human_collaboration_session(self, task_id: str,
                                               collaboration_type: str,
                                               context: Dict[str, Any]) -> str:
        """Create AG UI collaboration session for human-AI interaction"""
        try:
            collaboration_record = AGUICollaborationDB(
                task_id=task_id,
                collaboration_type=collaboration_type,
                human_participants=["arun"],  # Can be extended
                ai_participants=["john"],  # PM coordinates
                discussion_context=context,
                approval_required=context.get("requires_approval", False),
                approval_timeout=context.get("timeout", None)
            )

            # Store in database
            async with self.db_manager.get_session() as session:
                session.add(collaboration_record)
                await session.flush()
                collaboration_id = collaboration_record.collaboration_id

            # Initialize AG UI interface
            await self.agui_coordinator.initialize_collaboration_session(
                collaboration_id=collaboration_id,
                session_type=collaboration_type,
                participants=context.get("participants", []),
                initial_context=context
            )

            # Track active collaboration
            self.active_collaborations[collaboration_id] = {
                "type": collaboration_type,
                "task_id": task_id,
                "status": "active",
                "created_at": datetime.utcnow()
            }

            return collaboration_id

        except Exception as e:
            logger.error(f"Failed to create collaboration session: {e}")
            raise

    async def process_human_response(self, collaboration_id: str,
                                   human_response: Dict[str, Any]) -> bool:
        """Process human response in AG UI collaboration"""
        try:
            async with self.db_manager.get_session() as session:
                collaboration = await session.get(AGUICollaborationDB, collaboration_id)
                if not collaboration:
                    return False

                # Update collaboration with human response
                collaboration.resolution = human_response
                collaboration.status = "resolved"
                collaboration.resolved_at = datetime.utcnow()

                # Remove from active tracking
                if collaboration_id in self.active_collaborations:
                    del self.active_collaborations[collaboration_id]

                await session.commit()

            # Notify PM of resolution
            await self.pm_coordinator.process_human_collaboration_result(
                collaboration_id, human_response
            )

            return True

        except Exception as e:
            logger.error(f"Failed to process human response: {e}")
            return False

    async def validate_all_states(self) -> Dict[str, bool]:
        """Validate consistency of all active workflow states"""
        results = {}

        try:
            # Get all active workflows
            active_workflows = await self.state_manager.db.get_active_workflows()

            for workflow_id in active_workflows:
                try:
                    workflow_state = await self.state_manager.load_workflow_state(workflow_id)
                    results[workflow_id] = self._validate_state_consistency(workflow_state)

                except Exception as e:
                    logger.error(f"Validation failed for {workflow_id}: {e}")
                    results[workflow_id] = False

        except Exception as e:
            logger.error(f"State validation batch failed: {e}")

        return results

    def _validate_state_consistency(self, state: WorkflowState) -> bool:
        """Validate internal state consistency"""
        validations = [
            self._validate_checkpoint_consistency(state),
            self._validate_agent_assignment_consistency(state),
            self._validate_progress_consistency(state),
            self._validate_approval_consistency(state)
        ]

        return all(validations)
```

## Performance Optimization

### Caching Strategy
```python
# state/caching.py
class StateCacheManager:
    """Redis-based state caching for performance optimization"""

    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.cache_ttl = 3600  # 1 hour default TTL

    async def cache_workflow_state(self, workflow_state: WorkflowState) -> bool:
        """Cache workflow state with intelligent TTL"""
        try:
            cache_key = f"workflow:{workflow_state.workflow_id}"

            # Determine TTL based on workflow activity
            ttl = self._calculate_dynamic_ttl(workflow_state)

            # Serialize and cache
            serialized_state = json.dumps(workflow_state.dict(), default=str)
            await self.redis.setex(cache_key, ttl, serialized_state)

            return True

        except Exception as e:
            logger.error(f"Failed to cache workflow state: {e}")
            return False

    async def get_cached_workflow_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Retrieve workflow state from cache"""
        try:
            cache_key = f"workflow:{workflow_id}"
            cached_data = await self.redis.get(cache_key)

            if cached_data:
                state_dict = json.loads(cached_data)
                return WorkflowState(**state_dict)

            return None

        except Exception as e:
            logger.error(f"Failed to retrieve cached state: {e}")
            return None

    def _calculate_dynamic_ttl(self, workflow_state: WorkflowState) -> int:
        """Calculate TTL based on workflow activity and status"""
        base_ttl = 3600

        # Active workflows get shorter TTL for fresher data
        if workflow_state.status == WorkflowStatus.IN_PROGRESS:
            return base_ttl // 2

        # Completed workflows can be cached longer
        elif workflow_state.status == WorkflowStatus.COMPLETED:
            return base_ttl * 24  # 24 hours

        return base_ttl
```

---

*This PM-centric state management implementation provides database context coordination, command simulation state persistence, agent learning storage, and AG UI collaboration state management for the complete BMAD Auto ecosystem while preserving `.bmad-core` infrastructure integrity.*