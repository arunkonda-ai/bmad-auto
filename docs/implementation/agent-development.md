# BMAD Auto Agent Development Guide

## Overview

This guide provides implementation patterns for developing 10 AI agents within the PM-centric BMAD Auto ecosystem. All agents coordinate through John (PM) using database context, maintain independence within defined boundaries, and report decisions for PM review and criticism.

## Agent Architecture Standards

### Size Compliance Framework
**File Size Requirements**:
- **Core Agent Logic**: 100-200 lines maximum
- **Capabilities Extension**: 50-100 lines maximum
- **Integration Layer**: 50-100 lines maximum
- **Validation Logic**: 50-100 lines maximum
- **Total Agent Package**: 300 lines maximum across all files

### BMAD Auto Directory Structure
```
project-root/
├── .bmad-core/                    # PRESERVED - Never Modified
│   ├── agents/                    # 10 original agents (bmad-orchestrator, bmad-master, etc.)
│   ├── tasks/                     # Core task templates
│   └── workflows/                 # Standard BMAD workflows
├── bmad-auto/                     # AUTONOMOUS LAYER
│   ├── src/
│   │   ├── agents/                # PM-coordinated agent implementations
│   │   │   ├── john/              # PM orchestration hub
│   │   │   │   ├── core.py        # PM orchestration logic (100-200 lines)
│   │   │   │   ├── agent_coordinator.py # Agent coordination (50-100 lines)
│   │   │   │   ├── quality_orchestrator.py # Quality coordination (50-100 lines)
│   │   │   │   └── arun_interface.py # Strategic interface (50-100 lines)
│   │   │   ├── mary/              # Business analyst
│   │   │   │   ├── core.py        # Market intelligence (100-200 lines)
│   │   │   │   ├── pm_integration.py # PM coordination (50-100 lines)
│   │   │   │   ├── capabilities.py # Research capabilities (50-100 lines)
│   │   │   │   └── context_handler.py # Context processing (50-100 lines)
│   │   │   ├── james/             # Developer
│   │   │   ├── quinn/             # QA Engineer
│   │   │   ├── sally/             # UX Designer
│   │   │   ├── alex/              # System Architect
│   │   │   ├── po/                # Product Owner
│   │   │   ├── sm/                # Scrum Master
│   │   │   ├── bmad_orchestrator/ # Meta-orchestration
│   │   │   └── bmad_master/       # AI system enhancement
│   │   ├── services/              # Shared services
│   │   │   ├── database_context.py # Context management
│   │   │   ├── command_simulation.py # API interception
│   │   │   ├── vector_storage.py   # Learning embeddings
│   │   │   ├── agui_coordinator.py # Human-AI interface
│   │   │   └── command_logger.py   # Action logging
│   │   ├── orchestration/         # PM orchestration logic
│   │   │   ├── pm_hub.py          # Central coordination
│   │   │   ├── workflow_manager.py # Workflow coordination
│   │   │   └── quality_gates.py   # Quality validation
│   │   └── integration/           # External service coordination
│   │       ├── linear_mcp.py      # Linear integration
│   │       ├── github_api.py      # GitHub coordination
│   │       └── external_apis.py   # Other external services
│   └── config/                    # Configuration files
└── docs-new/                      # Consolidated documentation
```

### PM-Coordinated Agent Template
```python
# bmad-auto/src/agents/{agent_name}/core.py - Agent Domain Logic (100-200 lines)
from typing import Dict, List, Optional, Any
from ...services.database_context import DatabaseContextManager
from ...services.command_logger import CommandLogger
from ...models.pm_context import PMTaskContext, PMBoundaries
from ...utils.logging_config import get_logger

class PMCoordinatedAgent:
    """Agent implementation with PM-centric coordination"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.pm_coordinator = "john"
        self.logger = get_logger(f"agent.{agent_id}")
        self.context_manager = DatabaseContextManager()
        self.pm_interface = self._initialize_pm_interface()

    async def process_pm_task(self, pm_context: PMTaskContext) -> Dict[str, Any]:
        """Process task assigned by PM with defined boundaries"""
        try:
            # Report approach to PM
            await self._report_approach_to_pm(pm_context)

            # Execute within PM-defined boundaries
            result = await self._execute_within_boundaries(pm_context)

            # Report decisions and outcome to PM
            await self._report_completion_to_pm(result, pm_context)

            return result

        except Exception as e:
            await self._report_error_to_pm(e, pm_context)
            return {"error": str(e), "status": "failed", "pm_escalation": True}

    async def _report_approach_to_pm(self, pm_context: PMTaskContext):
        """Report planned approach to PM for validation"""
        approach_report = {
            "agent_id": self.agent_id,
            "task_analysis": self._analyze_task_complexity(pm_context),
            "planned_approach": self._define_approach(pm_context),
            "resource_requirements": self._estimate_resources(pm_context),
            "risk_assessment": self._assess_risks(pm_context)
        }

        await self.context_manager.store_agent_approach(
            pm_context.task_id, approach_report
        )

    async def _execute_within_boundaries(self, pm_context: PMTaskContext) -> Dict[str, Any]:
        """Execute domain logic within PM-defined boundaries"""
        # Validate boundaries
        if not self._validate_boundaries(pm_context.boundaries):
            raise ValueError(f"Task exceeds agent boundaries: {pm_context.boundaries}")

        # Execute domain-specific logic
        return await self._execute_domain_logic(pm_context)

    async def _execute_domain_logic(self, pm_context: PMTaskContext) -> Dict[str, Any]:
        """Agent-specific domain logic - implement in subclasses"""
        raise NotImplementedError("Agents must implement domain-specific logic")

    async def _report_completion_to_pm(self, result: Dict[str, Any], pm_context: PMTaskContext):
        """Report completion and decisions to PM for review"""
        completion_report = {
            "agent_id": self.agent_id,
            "task_id": pm_context.task_id,
            "result_summary": result,
            "decisions_made": self._extract_decisions(result),
            "confidence_score": result.get("confidence_score", 0.0),
            "next_steps_recommendation": self._recommend_next_steps(result)
        }

        await self.context_manager.store_agent_completion(
            pm_context.task_id, completion_report
        )
```

## 10-Agent PM-Coordinated Implementations

### Mary (Business Analyst) - PM Coordination
```python
# mary/core.py
class MaryAgent(PMCoordinatedAgent):
    """Business Analyst - Market Intelligence Specialist under PM coordination"""

    def __init__(self):
        super().__init__("mary")
        self.domain = "market_intelligence"
        self.research_tools = self._initialize_research_tools()
        self.analysis_frameworks = self._load_analysis_frameworks()

    async def _execute_domain_logic(self, pm_context: PMTaskContext) -> Dict[str, Any]:
        """Execute market analysis within PM-defined scope"""
        task_type = pm_context.task_type

        if task_type == "market_research":
            return await self._conduct_scoped_market_research(pm_context)
        elif task_type == "competitive_analysis":
            return await self._analyze_competitive_landscape(pm_context)
        elif task_type == "user_research":
            return await self._conduct_user_research(pm_context)
        elif task_type == "market_validation":
            return await self._validate_market_assumptions(pm_context)

        raise ValueError(f"Unsupported task type for Mary: {task_type}")

    async def _conduct_scoped_market_research(self, pm_context: PMTaskContext) -> Dict[str, Any]:
        """Market research within PM-defined boundaries"""
        # PM boundary validation
        scope = pm_context.boundaries.research_scope
        timeline = pm_context.boundaries.timeline

        # Independent decision within boundaries
        research_approach = self._decide_research_methodology(scope, timeline)

        # Execute research with decision logging
        results = await self._execute_research_with_logging(research_approach)

        # Report decisions to PM
        decision_log = {
            "methodology_chosen": research_approach.methodology,
            "reasoning": research_approach.rationale,
            "scope_coverage": results.scope_coverage,
            "confidence_level": results.confidence
        }

        return {
            "market_analysis": results.data,
            "decision_log": decision_log,
            "pm_review_required": results.complexity > pm_context.boundaries.complexity_threshold,
            "confidence_score": results.confidence
        }
```

### John (Product Manager) - Central Orchestration Hub
```python
# bmad-auto/src/agents/john/core.py
from ...services.agui_coordinator import AGUICoordinator
from ...services.command_logger import CommandLogger
from ...orchestration.pm_hub import PMOrchestrationHub
from .agent_coordinator import AgentCoordinator
from .quality_orchestrator import QualityOrchestrator
from .arun_interface import ArunInterface

class JohnPMAgent(PMOrchestrationHub):
    """John - PM Central Orchestration Hub managing 10-agent ecosystem"""

    def __init__(self):
        super().__init__("john")
        self.role = "pm_orchestrator"
        self.agent_coordinator = AgentCoordinator()  # From john/agent_coordinator.py
        self.quality_orchestrator = QualityOrchestrator()  # From john/quality_orchestrator.py
        self.arun_interface = ArunInterface()  # From john/arun_interface.py
        self.agui_coordinator = AGUICoordinator()  # From services/
        self.command_logger = CommandLogger()  # From services/

    async def process_arun_task(self, arun_task: ArunTaskContext) -> Dict[str, Any]:
        """Process task from Arun with impact assessment"""
        # Evaluate task impact and feasibility
        impact_assessment = await self._evaluate_task_impact(arun_task)

        # Determine agent assignment strategy
        agent_strategy = await self._plan_agent_coordination(arun_task, impact_assessment)

        # Execute orchestration
        orchestration_result = await self._orchestrate_agent_execution(agent_strategy)

        # Coordinate quality validation
        quality_assessment = await self._coordinate_quality_validation(orchestration_result)

        # Present to Arun for strategic approval
        return await self._present_to_arun_for_approval(quality_assessment)

    async def _plan_agent_coordination(self, arun_task: ArunTaskContext,
                                     impact_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Plan which agents to involve and how to coordinate them"""
        coordination_strategy = {
            "primary_agents": self._select_primary_agents(arun_task.type),
            "supporting_agents": self._select_supporting_agents(impact_assessment),
            "context_distribution": self._plan_context_distribution(arun_task),
            "validation_sequence": self._plan_validation_sequence(arun_task.complexity),
            "human_gates": self._identify_human_collaboration_points(arun_task)
        }

        # Log PM orchestration decision
        self.command_logger.log_pm_orchestration_decision(
            task_id=arun_task.task_id,
            strategy=coordination_strategy,
            reasoning=self._document_orchestration_reasoning(coordination_strategy)
        )

        return coordination_strategy

    async def criticize_and_redirect_agent(self, agent_id: str,
                                         completion_report: Dict[str, Any]) -> Dict[str, Any]:
        """PM criticism and redirection of agent work"""
        # Analyze agent completion
        quality_analysis = self._analyze_agent_work_quality(completion_report)

        if quality_analysis.requires_improvement:
            criticism = {
                "agent_id": agent_id,
                "quality_issues": quality_analysis.issues,
                "improvement_requirements": quality_analysis.improvements,
                "redirection_instructions": self._generate_redirection_instructions(quality_analysis),
                "new_boundaries": self._adjust_agent_boundaries(agent_id, quality_analysis)
            }

            # Store criticism for agent
            await self.context_manager.store_pm_criticism(
                agent_id=agent_id,
                criticism=criticism
            )

            return criticism

        # Approve agent work
        return {"status": "approved", "next_phase": self._determine_next_phase(completion_report)}
```

### James (Developer) - Technical Implementation Specialist
```python
# bmad-auto/src/agents/james/core.py
from ...services.database_context import DatabaseContextManager
from ...integration.github_api import GitHubAPI
from .pm_integration import PMCoordinationInterface
from .capabilities import TechnicalCapabilities
from .context_handler import DatabaseContextHandler

class JamesAgent(PMCoordinatedAgent):
    """James - Technical Implementation under PM and Architect coordination"""

    def __init__(self):
        super().__init__("james")
        self.domain = "technical_implementation"
        self.architect_coordinator = "alex"
        self.pm_interface = PMCoordinationInterface("james")  # From james/pm_integration.py
        self.capabilities = TechnicalCapabilities()  # From james/capabilities.py
        self.context_handler = DatabaseContextHandler("james")  # From james/context_handler.py
        self.github_api = GitHubAPI()  # From integration/

    async def _execute_domain_logic(self, pm_context: PMTaskContext) -> Dict[str, Any]:
        """Execute technical implementation within PM+Architect guidance"""
        task_type = pm_context.task_type

        if task_type == "technical_feasibility":
            return await self._assess_technical_feasibility(pm_context)
        elif task_type == "implementation":
            return await self._implement_technical_solution(pm_context)
        elif task_type == "code_review":
            return await self._conduct_code_review(pm_context)
        elif task_type == "performance_optimization":
            return await self._optimize_performance(pm_context)

        raise ValueError(f"Unsupported task type for James: {task_type}")

    async def _implement_technical_solution(self, pm_context: PMTaskContext) -> Dict[str, Any]:
        """Technical implementation with autonomous decisions within boundaries"""
        # Coordinate with Alex (Architect) for technical constraints
        architecture_constraints = await self._get_architecture_constraints(pm_context)

        # Make independent technical decisions within constraints
        implementation_approach = self._decide_implementation_strategy(
            pm_context.requirements,
            architecture_constraints,
            pm_context.boundaries
        )

        # Execute implementation with decision logging
        implementation_result = await self._execute_implementation(
            implementation_approach,
            pm_context
        )

        # Report technical decisions to PM
        technical_decisions = {
            "architecture_choices": implementation_approach.architecture_decisions,
            "technology_selections": implementation_approach.tech_stack,
            "performance_considerations": implementation_result.performance_metrics,
            "security_measures": implementation_result.security_implementation,
            "code_quality_metrics": implementation_result.quality_scores
        }

        # Command logging for external operations
        if implementation_result.github_operations:
            self.command_logger.log_github_operations(
                agent_id="james",
                operations=implementation_result.github_operations,
                pm_coordination=True
            )

        return {
            "implementation_result": implementation_result.deliverables,
            "technical_decisions": technical_decisions,
            "quality_validation": implementation_result.quality_report,
            "pm_review_points": self._identify_pm_review_points(implementation_result),
            "confidence_score": implementation_result.confidence
        }

### Additional 7 Agents (Abbreviated Examples)

### Additional 7 Agents with BMAD Auto Structure

# bmad-auto/src/agents/quinn/core.py
class QuinnAgent(PMCoordinatedAgent):
    """Quinn - Quality Validation Specialist under PM coordination"""

    def __init__(self):
        super().__init__("quinn")
        self.domain = "quality_validation"
        self.pm_interface = PMCoordinationInterface("quinn")
        self.capabilities = QualityCapabilities()
        self.context_handler = DatabaseContextHandler("quinn")

# bmad-auto/src/agents/sally/core.py
class SallyAgent(PMCoordinatedAgent):
    """Sally - User Experience Specialist with PM validation"""

    def __init__(self):
        super().__init__("sally")
        self.domain = "user_experience"
        self.pm_interface = PMCoordinationInterface("sally")
        self.capabilities = UXCapabilities()
        self.context_handler = DatabaseContextHandler("sally")

# bmad-auto/src/agents/alex/core.py
class AlexAgent(PMCoordinatedAgent):
    """Alex - Infrastructure Authority with PM oversight"""

    def __init__(self):
        super().__init__("alex")
        self.role = "infrastructure_authority"
        self.pm_coordination_level = "high"
        self.pm_interface = PMCoordinationInterface("alex")
        self.capabilities = InfrastructureCapabilities()

# bmad-auto/src/agents/po/core.py
class ProductOwnerAgent(PMCoordinatedAgent):
    """Product Owner - Backlog Management under PM coordination"""

    def __init__(self):
        super().__init__("po")
        self.domain = "backlog_management"
        self.pm_interface = PMCoordinationInterface("po")
        self.linear_mcp = LinearMCP()  # From integration/

# bmad-auto/src/agents/sm/core.py
class ScrumMasterAgent(PMCoordinatedAgent):
    """Scrum Master - Process Facilitation with PM oversight"""

    def __init__(self):
        super().__init__("sm")
        self.domain = "process_facilitation"
        self.pm_interface = PMCoordinationInterface("sm")

# bmad-auto/src/agents/bmad_orchestrator/core.py
class BMADOrchestratorAgent(PMCoordinatedAgent):
    """BMAD Orchestrator - Meta-orchestration integrated with PM"""

    def __init__(self):
        super().__init__("bmad_orchestrator")
        self.bmad_core_interface = BMADCoreInterface()  # Links to .bmad-core/
        self.pm_interface = PMCoordinationInterface("bmad_orchestrator")

# bmad-auto/src/agents/bmad_master/core.py
class BMADMasterAgent(PMCoordinatedAgent):
    """BMAD Master - AI System Enhancement under PM oversight"""

    def __init__(self):
        super().__init__("bmad_master")
        self.ai_optimization_tools = AIOptimizationTools()
        self.pm_interface = PMCoordinationInterface("bmad_master")
```

## PM Coordination Interface Implementation

### PM Integration Layer
```python
# bmad-auto/src/agents/{agent_name}/pm_integration.py - PM Coordination Interface (50-100 lines)
from ...services.database_context import DatabaseContextManager
from ...services.vector_storage import AgentLearningStorage
from ...services.command_logger import CommandLogger
from ...models.pm_context import PMTaskContext

class PMCoordinationInterface:
    """Interface for agent coordination with PM hub"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.pm_coordinator = "john"
        self.context_manager = DatabaseContextManager()  # From services/
        self.learning_storage = AgentLearningStorage()  # From services/
        self.command_logger = CommandLogger()  # From services/

    async def receive_pm_task_assignment(self, pm_task: PMTaskContext) -> Dict[str, Any]:
        """Receive task assignment from PM with boundaries"""
        # Validate task against agent capabilities
        capability_check = self._validate_task_capability(pm_task)

        if not capability_check.can_execute:
            return {
                "status": "capability_mismatch",
                "reason": capability_check.reason,
                "suggested_agents": capability_check.better_suited_agents
            }

        # Accept task and store context
        await self.context_manager.store_task_assignment(
            agent_id=self.agent_id,
            task=pm_task,
            acceptance_timestamp=datetime.utcnow()
        )

        return {"status": "accepted", "estimated_completion": capability_check.time_estimate}

    async def report_decision_to_pm(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Report agent decision to PM for review"""
        decision_report = {
            "agent_id": self.agent_id,
            "decision_type": decision_context.type,
            "decision_rationale": decision_context.reasoning,
            "alternatives_considered": decision_context.alternatives,
            "confidence_level": decision_context.confidence,
            "requires_pm_approval": decision_context.impact > self.approval_threshold
        }

        await self.context_manager.store_agent_decision(
            decision_report
        )

        # Store in learning system
        await self.learning_storage.store_decision_pattern(
            agent_id=self.agent_id,
            decision_context=decision_context,
            vector_embedding=self._generate_decision_embedding(decision_context)
        )

        return decision_report

    async def receive_pm_criticism(self, criticism: Dict[str, Any]) -> Dict[str, Any]:
        """Receive and process PM criticism for improvement"""
        # Process PM feedback
        improvement_plan = self._process_pm_feedback(criticism)

        # Update agent approach based on criticism
        updated_approach = await self._adjust_approach_based_on_criticism(
            criticism,
            improvement_plan
        )

        # Learn from criticism
        await self.learning_storage.store_criticism_learning(
            agent_id=self.agent_id,
            criticism=criticism,
            improvement_actions=improvement_plan,
            learning_vector=self._generate_criticism_embedding(criticism)
        )

        return {
            "status": "criticism_processed",
            "improvement_plan": improvement_plan,
            "updated_approach": updated_approach
        }
```

### Database Context Handler
```python
# bmad-auto/src/agents/{agent_name}/context_handler.py - Database Context Processing (50-100 lines)
from ...services.database_context import DatabaseContextManager
from ...services.vector_storage import VectorEmbeddingManager
from ...services.json_protocol import JSONProtocolHandler
from datetime import datetime

class DatabaseContextHandler:
    """Handle database context storage and retrieval for agent coordination"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.db_manager = DatabaseContextManager()  # From services/
        self.vector_store = VectorEmbeddingManager()  # From services/
        self.json_protocol = JSONProtocolHandler()  # From services/

    async def store_agent_context(self, context_data: Dict[str, Any]) -> str:
        """Store agent context with vector embeddings for semantic retrieval"""
        # Generate vector embedding for semantic search
        context_embedding = await self.vector_store.generate_embedding(
            context_data
        )

        # Store in database with JSON protocol
        context_entry = {
            "agent_id": self.agent_id,
            "context_data": self.json_protocol.serialize(context_data),
            "vector_embedding": context_embedding,
            "timestamp": datetime.utcnow(),
            "context_type": context_data.get("type", "general")
        }

        context_id = await self.db_manager.store_context(context_entry)
        return context_id

    async def retrieve_relevant_context(self, query_context: Dict[str, Any],
                                      limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve contextually relevant information using vector similarity"""
        # Generate query embedding
        query_embedding = await self.vector_store.generate_embedding(query_context)

        # Find similar contexts
        similar_contexts = await self.vector_store.find_similar(
            query_embedding=query_embedding,
            agent_id=self.agent_id,
            limit=limit,
            similarity_threshold=0.7
        )

        # Deserialize and return relevant contexts
        relevant_contexts = []
        for context in similar_contexts:
            deserialized = self.json_protocol.deserialize(context.context_data)
            relevant_contexts.append({
                "context": deserialized,
                "similarity_score": context.similarity,
                "timestamp": context.timestamp
            })

        return relevant_contexts

    async def receive_pm_context_update(self, pm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Receive context update distributed by PM"""
        # Store PM-distributed context
        context_id = await self.store_agent_context({
            "type": "pm_distributed",
            "source": "john",
            "content": pm_context,
            "distribution_reason": pm_context.get("reason", "task_coordination")
        })

        # Update agent's working context
        updated_context = await self._integrate_pm_context_update(
            pm_context,
            self.current_working_context
        )

        return {
            "status": "context_updated",
            "context_id": context_id,
            "updated_working_context": updated_context
        }
```

## Shared Services Implementation

### Database Context Management Service
```python
# bmad-auto/src/services/database_context.py - Centralized Context Management
from typing import Dict, List, Optional, Any
import asyncpg
from datetime import datetime

class DatabaseContextManager:
    """Centralized database context management for all agents"""

    def __init__(self):
        self.db_pool = None
        self.connection_config = self._load_db_config()

    async def initialize(self):
        """Initialize database connection pool"""
        self.db_pool = await asyncpg.create_pool(
            host=self.connection_config.host,
            port=self.connection_config.port,
            database=self.connection_config.database,
            user=self.connection_config.user,
            password=self.connection_config.password,
            min_size=5,
            max_size=20
        )

    async def store_pm_task_assignment(self, task_context: Dict[str, Any]) -> str:
        """Store PM task assignment for agent coordination"""
        async with self.db_pool.acquire() as conn:
            task_id = await conn.fetchval(
                """
                INSERT INTO pm_task_assignments
                (pm_id, agent_id, task_data, boundaries, created_at)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING task_id
                """,
                task_context['pm_id'],
                task_context['agent_id'],
                task_context['task_data'],
                task_context['boundaries'],
                datetime.utcnow()
            )
            return task_id

    async def store_agent_decision(self, decision_context: Dict[str, Any]) -> str:
        """Store agent decision for PM review"""
        async with self.db_pool.acquire() as conn:
            decision_id = await conn.fetchval(
                """
                INSERT INTO agent_decisions
                (agent_id, task_id, decision_data, confidence_score, requires_pm_review, created_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING decision_id
                """,
                decision_context['agent_id'],
                decision_context['task_id'],
                decision_context['decision_data'],
                decision_context['confidence_score'],
                decision_context['requires_pm_review'],
                datetime.utcnow()
            )
            return decision_id

### Vector Storage Service
# bmad-auto/src/services/vector_storage.py - Agent Learning with Embeddings
class VectorEmbeddingManager:
    """Vector embedding storage for agent learning and context retrieval"""

    def __init__(self):
        self.embedding_model = self._initialize_embedding_model()
        self.vector_db = self._initialize_vector_database()

    async def store_agent_learning(self, agent_id: str, learning_context: Dict[str, Any]) -> str:
        """Store agent learning with vector embeddings for semantic retrieval"""
        # Generate embedding for learning context
        embedding = await self.embedding_model.generate_embedding(learning_context)

        # Store in vector database
        learning_id = await self.vector_db.store(
            collection=f"agent_learning_{agent_id}",
            embedding=embedding,
            metadata=learning_context,
            id_prefix=f"{agent_id}_learning_"
        )

        return learning_id

### Command Logging Service
# bmad-auto/src/services/command_logger.py - Action Logging for Audit
class CommandLogger:
    """Log all PM coordination and external API commands for audit and learning"""

    def __init__(self):
        self.log_storage = self._initialize_log_storage()

    async def log_pm_coordination_action(self, coordination_context: Dict[str, Any]):
        """Log PM coordination decisions and actions"""
        log_entry = {
            "timestamp": datetime.utcnow(),
            "action_type": "pm_coordination",
            "pm_id": "john",
            "coordination_data": coordination_context,
            "agents_involved": coordination_context.get('agents', []),
            "decision_rationale": coordination_context.get('reasoning', '')
        }

        await self.log_storage.store_log(log_entry)

    async def log_external_api_call(self, api_context: Dict[str, Any]):
        """Log external API calls (Linear, GitHub, etc.) coordinated through PM"""
        log_entry = {
            "timestamp": datetime.utcnow(),
            "action_type": "external_api",
            "service": api_context['service'],
            "operation": api_context['operation'],
            "coordinating_agent": api_context.get('agent_id', 'john'),
            "api_data": api_context['data'],
            "success": api_context.get('success', True)
        }

        await self.log_storage.store_log(log_entry)

    def validate_input(self, workflow: WorkflowState) -> Dict[str, Any]:
        """Validate workflow input for agent processing"""
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "quality_score": 0.0
        }

        # Check workflow context completeness
        context_score = self._validate_context_completeness(workflow.context)
        validation_results["quality_score"] += context_score * 0.3

        # Validate phase appropriateness
        phase_score = self._validate_phase_appropriateness(workflow.phase)
        validation_results["quality_score"] += phase_score * 0.2

        # Check agent workload capacity
        capacity_score = self._validate_agent_capacity(workflow)
        validation_results["quality_score"] += capacity_score * 0.2

        # Validate requirements clarity
        requirement_score = self._validate_requirement_clarity(workflow.context.requirements)
        validation_results["quality_score"] += requirement_score * 0.3

        # Overall validation
        if validation_results["quality_score"] < 0.7:
            validation_results["is_valid"] = False
            validation_results["errors"].append("Quality score below threshold")

        return validation_results

    def validate_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate agent output quality and completeness"""
        output_validation = {
            "is_valid": True,
            "completeness_score": 0.0,
            "quality_issues": [],
            "improvement_suggestions": []
        }

        # Check output completeness
        required_fields = self._get_required_output_fields()
        completeness = self._check_field_completeness(result, required_fields)
        output_validation["completeness_score"] = completeness

        # Validate confidence scores
        if "confidence_score" in result:
            confidence_validation = self._validate_confidence_score(result["confidence_score"])
            if not confidence_validation["is_valid"]:
                output_validation["quality_issues"].extend(confidence_validation["issues"])

        # Check for error indicators
        if "error" in result or "errors" in result:
            output_validation["is_valid"] = False
            output_validation["quality_issues"].append("Output contains error indicators")

        return output_validation
```

## BMAD Auto Integration Layer

### External Service Coordination
```python
# bmad-auto/src/integration/linear_mcp.py - Linear Integration via MCP
from ...services.command_logger import CommandLogger

class LinearMCP:
    """Linear integration using MCP when available, fallback to API"""

    def __init__(self):
        self.mcp_available = self._check_mcp_availability()
        self.command_logger = CommandLogger()
        if self.mcp_available:
            self.mcp_client = self._initialize_mcp_client()
        else:
            self.api_client = self._initialize_api_client()

    async def update_issue_via_pm(self, pm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Update Linear issue coordinated through PM"""
        # Log the coordination action
        await self.command_logger.log_external_api_call({
            "service": "linear",
            "operation": "issue_update",
            "agent_id": pm_context.get('agent_id', 'john'),
            "data": pm_context
        })

        if self.mcp_available:
            return await self._update_via_mcp(pm_context)
        else:
            return await self._update_via_api(pm_context)

# bmad-auto/src/integration/github_api.py - GitHub Integration
class GitHubAPI:
    """GitHub integration for development coordination"""

    def __init__(self):
        self.api_client = self._initialize_github_client()
        self.command_logger = CommandLogger()

    async def coordinate_pr_creation(self, pm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create PR coordinated through PM"""
        # Log GitHub operation
        await self.command_logger.log_external_api_call({
            "service": "github",
            "operation": "pr_creation",
            "agent_id": pm_context.get('agent_id', 'james'),
            "data": pm_context
        })

        return await self._create_pr_with_pm_validation(pm_context)

### AG UI Coordination Service
# bmad-auto/src/services/agui_coordinator.py - Human-AI Interface
class AGUICoordinator:
    """AG UI coordination for human-agent collaboration"""

    def __init__(self):
        self.agui_client = self._initialize_agui_client()
        self.command_logger = CommandLogger()

    async def request_human_approval(self, approval_context: Dict[str, Any]) -> Dict[str, Any]:
        """Request time-bounded human approval via AG UI"""
        # Log human collaboration request
        await self.command_logger.log_pm_coordination_action({
            "action": "human_approval_request",
            "context": approval_context,
            "timeout": approval_context.get('timeout', '2h'),
            "urgency": approval_context.get('urgency', 'normal')
        })

        return await self.agui_client.request_approval(
            approval_type=approval_context['type'],
            content=approval_context['content'],
            timeout=approval_context.get('timeout', '2h'),
            discussion_enabled=approval_context.get('discussion', True)
        )

    async def update_agent_monitoring_dashboard(self, agent_status: Dict[str, Any]):
        """Update AG UI monitoring dashboard with agent status"""
        await self.agui_client.update_dashboard({
            "agent_statuses": agent_status,
            "pm_coordination": agent_status.get('pm_activity', {}),
            "quality_gates": agent_status.get('quality_status', {}),
            "human_collaboration": agent_status.get('human_gates', {})
        })
```

### Collaboration Patterns
**Sequential Collaboration**:
- Workflow handoff with complete context transfer
- Quality validation before handoff acceptance
- Rollback capability for failed handoffs

**Parallel Collaboration**:
- Concurrent processing with synchronized checkpoints
- Conflict resolution for overlapping deliverables
- Resource coordination for efficient execution

### Decision Making Protocols
**Authority Matrix**:
- Domain-specific decision authority for each agent
- Escalation protocols for cross-domain decisions
- Consensus building for collaborative decisions
- Override capability for strategic interventions

## Performance Optimization

### Agent Performance Monitoring
**Metrics Collection**:
- Task completion time and success rate
- Quality score trends and improvement tracking
- Resource utilization and optimization opportunities
- Error frequency and resolution effectiveness

**Optimization Strategies**:
- Intelligent caching for repeated operations
- Load balancing across agent instances
- Context optimization for memory efficiency
- Predictive scaling based on workload patterns

### Continuous Improvement
**Learning Integration**:
- Pattern recognition for successful workflows
- Error analysis for improvement opportunities
- Capability enhancement based on usage patterns
- Quality standard evolution based on outcomes

---

*This BMAD Auto agent development guide provides the complete implementation structure for PM-centric 10-agent coordination using database context, command simulation, and AG UI human collaboration while preserving `.bmad-core` infrastructure integrity.*