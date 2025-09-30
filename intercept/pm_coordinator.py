"""
BMAD Auto PM Coordinator - Central 10-Agent Coordination Hub
Implements autonomous task breakdown, agent assignment, and quality orchestration
"""

import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from .decision_capture import PMDecisionCapture


class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AgentStatus(Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"


@dataclass
class TaskBreakdown:
    task_id: str
    parent_task: str
    subtasks: List[Dict[str, Any]]
    agent_assignments: Dict[str, str]
    priority: TaskPriority
    estimated_duration: int  # minutes
    dependencies: List[str]
    quality_gates: List[str]
    created_at: datetime


@dataclass
class AgentCapability:
    agent_name: str
    capabilities: List[str]
    current_load: float  # 0.0 to 1.0
    avg_response_time: float  # seconds
    success_rate: float  # 0.0 to 1.0
    last_activity: datetime


class PMCoordinator:
    """Central coordination hub for BMAD Auto 10-agent ecosystem"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or self._get_default_db_path()
        self.decision_capture = PMDecisionCapture(self.db_path)
        self.agent_capabilities = self._initialize_agent_capabilities()
        self.active_workflows = {}
        self._setup_logging()

    def _get_default_db_path(self) -> str:
        """Get default coordination.db path"""
        import os
        return os.path.join(
            os.path.dirname(__file__),
            'coordination.db'
        )

    def _setup_logging(self):
        """Setup structured logging for PM coordination"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - PM_COORDINATOR - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _initialize_agent_capabilities(self) -> Dict[str, AgentCapability]:
        """Initialize the 10-agent capability matrix"""
        return {
            'john_pm': AgentCapability(
                agent_name='john_pm',
                capabilities=['task_breakdown', 'coordination', 'quality_gates', 'strategic_decisions'],
                current_load=0.0,
                avg_response_time=1.0,
                success_rate=0.95,
                last_activity=datetime.now()
            ),
            'alex_architect': AgentCapability(
                agent_name='alex_architect',
                capabilities=['system_design', 'technical_architecture', 'performance_optimization'],
                current_load=0.0,
                avg_response_time=2.5,
                success_rate=0.92,
                last_activity=datetime.now()
            ),
            'james_developer': AgentCapability(
                agent_name='james_developer',
                capabilities=['code_implementation', 'debugging', 'testing', 'integration'],
                current_load=0.0,
                avg_response_time=3.0,
                success_rate=0.88,
                last_activity=datetime.now()
            ),
            'quinn_qa': AgentCapability(
                agent_name='quinn_qa',
                capabilities=['quality_validation', 'testing', 'automation', 'performance_testing'],
                current_load=0.0,
                avg_response_time=2.8,
                success_rate=0.94,
                last_activity=datetime.now()
            ),
            'sally_ux': AgentCapability(
                agent_name='sally_ux',
                capabilities=['user_experience', 'design_validation', 'accessibility', 'user_research'],
                current_load=0.0,
                avg_response_time=2.2,
                success_rate=0.91,
                last_activity=datetime.now()
            ),
            'mary_analyst': AgentCapability(
                agent_name='mary_analyst',
                capabilities=['research', 'analysis', 'documentation', 'market_intelligence'],
                current_load=0.0,
                avg_response_time=1.8,
                success_rate=0.93,
                last_activity=datetime.now()
            )
        }

    def coordinate_task(self, user_prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main coordination entry point - autonomous task breakdown and agent assignment

        Args:
            user_prompt: User's task description
            context: Additional context (project, priority, etc.)

        Returns:
            Coordination result with task breakdown and assignments
        """
        try:
            self.logger.info(f"Starting task coordination for: {user_prompt[:100]}...")

            # Step 1: Autonomous task breakdown
            task_breakdown = self._decompose_task(user_prompt, context or {})

            # Step 2: Capability-based agent assignment
            assignments = self._assign_agents(task_breakdown)

            # Step 3: Quality gate configuration
            quality_config = self._configure_quality_gates(task_breakdown)

            # Step 4: Capture PM decision reasoning
            decision_id = self.decision_capture.capture_decision(
                decision_type='task_assignment',
                context_data={
                    'user_prompt': user_prompt,
                    'context': context,
                    'task_breakdown': asdict(task_breakdown),
                    'agent_assignments': assignments
                },
                reasoning_process=self._generate_reasoning(task_breakdown, assignments),
                outcome=f"Task decomposed into {len(task_breakdown.subtasks)} subtasks",
                confidence_score=self._calculate_confidence(task_breakdown),
                model_assignments=self._determine_model_assignments(assignments)
            )

            # Step 5: Register workflow in database
            workflow_id = self._register_workflow(task_breakdown, assignments, decision_id)

            # Step 6: Update agent status
            self._update_agent_status(assignments)

            coordination_result = {
                'workflow_id': workflow_id,
                'decision_id': decision_id,
                'task_breakdown': asdict(task_breakdown),
                'agent_assignments': assignments,
                'quality_gates': quality_config,
                'estimated_completion': self._estimate_completion_time(task_breakdown),
                'next_actions': self._generate_next_actions(assignments)
            }

            self.logger.info(f"Task coordination completed - Workflow ID: {workflow_id}")
            return coordination_result

        except Exception as e:
            self.logger.error(f"Task coordination failed: {e}")
            raise

    def _decompose_task(self, user_prompt: str, context: Dict[str, Any]) -> TaskBreakdown:
        """Autonomous task decomposition with PM logic"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Analyze task complexity and determine breakdown strategy
        complexity_score = self._analyze_task_complexity(user_prompt, context)

        if complexity_score < 3:
            # Simple task - single agent
            subtasks = [{'description': user_prompt, 'type': 'implementation', 'estimated_hours': 2}]
            priority = TaskPriority.MEDIUM
        elif complexity_score < 7:
            # Medium complexity - multi-agent coordination
            subtasks = self._generate_medium_complexity_breakdown(user_prompt, context)
            priority = TaskPriority.HIGH
        else:
            # Complex task - full workflow orchestration
            subtasks = self._generate_complex_breakdown(user_prompt, context)
            priority = TaskPriority.CRITICAL

        return TaskBreakdown(
            task_id=task_id,
            parent_task=user_prompt,
            subtasks=subtasks,
            agent_assignments={},  # Will be filled by _assign_agents
            priority=priority,
            estimated_duration=sum(st.get('estimated_hours', 1) * 60 for st in subtasks),
            dependencies=self._extract_dependencies(subtasks),
            quality_gates=self._determine_quality_gates(subtasks),
            created_at=datetime.now()
        )

    def _assign_agents(self, task_breakdown: TaskBreakdown) -> Dict[str, str]:
        """Capability-based agent assignment with load balancing"""
        assignments = {}

        for i, subtask in enumerate(task_breakdown.subtasks):
            required_capabilities = self._extract_required_capabilities(subtask)
            best_agent = self._find_best_agent(required_capabilities)

            if best_agent:
                assignments[f"subtask_{i}"] = best_agent
                # Update agent load
                self.agent_capabilities[best_agent].current_load += 0.1
            else:
                self.logger.warning(f"No suitable agent found for subtask: {subtask['description']}")
                assignments[f"subtask_{i}"] = 'james_developer'  # Default fallback

        return assignments

    def _find_best_agent(self, required_capabilities: List[str]) -> Optional[str]:
        """Find the best agent based on capabilities, load, and performance"""
        best_agent = None
        best_score = -1

        for agent_name, capability in self.agent_capabilities.items():
            # Calculate capability match score
            match_score = len(set(required_capabilities) & set(capability.capabilities))
            if match_score == 0:
                continue

            # Factor in current load (prefer less loaded agents)
            load_penalty = capability.current_load * 0.5

            # Factor in success rate and response time
            performance_score = capability.success_rate - (capability.avg_response_time / 10)

            total_score = match_score + performance_score - load_penalty

            if total_score > best_score:
                best_score = total_score
                best_agent = agent_name

        return best_agent

    def _extract_required_capabilities(self, subtask: Dict[str, Any]) -> List[str]:
        """Extract required capabilities from subtask description"""
        description = subtask.get('description', '').lower()
        task_type = subtask.get('type', '').lower()

        capabilities = []

        # Map keywords to capabilities
        if any(word in description for word in ['implement', 'code', 'develop', 'build']):
            capabilities.append('code_implementation')
        if any(word in description for word in ['test', 'quality', 'validate']):
            capabilities.append('quality_validation')
        if any(word in description for word in ['design', 'architect', 'structure']):
            capabilities.append('system_design')
        if any(word in description for word in ['research', 'analyze', 'investigate']):
            capabilities.append('research')
        if any(word in description for word in ['ui', 'ux', 'user', 'interface']):
            capabilities.append('user_experience')
        if any(word in description for word in ['coordinate', 'manage', 'oversee']):
            capabilities.append('coordination')

        return capabilities or ['code_implementation']  # Default capability

    def notify_agent(self, agent_name: str, message: str, context: Dict[str, Any] = None) -> bool:
        """Notify specific agent with task assignment or update"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO coordination_log (agent, command, context, status, pm_decision)
                    VALUES (?, ?, ?, ?, ?)
                ''', (agent_name, 'notification', json.dumps(context or {}), 'sent', message))

            self.logger.info(f"Notification sent to {agent_name}: {message[:50]}...")
            return True

        except Exception as e:
            self.logger.error(f"Failed to notify {agent_name}: {e}")
            return False

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status for PM dashboard"""
        try:
            status = {
                'timestamp': datetime.now().isoformat(),
                'agents': {},
                'active_workflows': len(self.active_workflows),
                'system_health': 'healthy'
            }

            # Get agent status from database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT agent, status, current_task, last_activity, coordination_count
                    FROM agent_status
                ''')

                for row in cursor.fetchall():
                    agent, agent_status, current_task, last_activity, coord_count = row
                    status['agents'][agent] = {
                        'status': agent_status,
                        'current_task': current_task,
                        'last_activity': last_activity,
                        'coordination_count': coord_count,
                        'capabilities': self.agent_capabilities.get(agent, {}).capabilities if agent in self.agent_capabilities else []
                    }

            return status

        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}

    def _register_workflow(self, task_breakdown: TaskBreakdown, assignments: Dict[str, str], decision_id: str) -> str:
        """Register workflow in database for tracking"""
        workflow_id = f"wf_{task_breakdown.task_id}"

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO workflow_state (id, workflow_type, agents_involved, current_stage, status, context)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    workflow_id,
                    'pm_coordinated_task',
                    json.dumps(list(assignments.values())),
                    'task_assignment',
                    'active',
                    json.dumps({
                        'task_breakdown': asdict(task_breakdown),
                        'assignments': assignments,
                        'decision_id': decision_id
                    })
                ))

            self.active_workflows[workflow_id] = {
                'task_breakdown': task_breakdown,
                'assignments': assignments,
                'status': 'active',
                'created_at': datetime.now()
            }

            return workflow_id

        except Exception as e:
            self.logger.error(f"Failed to register workflow: {e}")
            raise

    def _update_agent_status(self, assignments: Dict[str, str]):
        """Update agent status in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                for subtask, agent in assignments.items():
                    conn.execute('''
                        INSERT OR REPLACE INTO agent_status
                        (agent, last_activity, current_task, status, coordination_count, updated_at)
                        VALUES (
                            ?, ?, ?, ?,
                            COALESCE((SELECT coordination_count FROM agent_status WHERE agent = ?) + 1, 1),
                            ?
                        )
                    ''', (
                        agent,
                        datetime.now().isoformat(),
                        subtask,
                        'busy',
                        agent,
                        datetime.now().isoformat()
                    ))

        except Exception as e:
            self.logger.error(f"Failed to update agent status: {e}")

    # Helper methods for task analysis
    def _analyze_task_complexity(self, user_prompt: str, context: Dict[str, Any]) -> int:
        """Analyze task complexity on scale 1-10"""
        complexity = 1

        # Length-based complexity
        if len(user_prompt) > 200:
            complexity += 2
        elif len(user_prompt) > 100:
            complexity += 1

        # Keyword-based complexity
        complex_keywords = ['integrate', 'orchestrate', 'coordinate', 'multiple', 'system', 'architecture']
        complexity += sum(1 for word in complex_keywords if word in user_prompt.lower())

        # Context-based complexity
        if context.get('priority') == 'critical':
            complexity += 2
        if context.get('agents_required', 1) > 3:
            complexity += 2

        return min(complexity, 10)

    def _generate_medium_complexity_breakdown(self, user_prompt: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate breakdown for medium complexity tasks"""
        return [
            {'description': f"Research and analysis for: {user_prompt}", 'type': 'research', 'estimated_hours': 2},
            {'description': f"Design approach for: {user_prompt}", 'type': 'design', 'estimated_hours': 3},
            {'description': f"Implementation of: {user_prompt}", 'type': 'implementation', 'estimated_hours': 5},
            {'description': f"Quality validation for: {user_prompt}", 'type': 'validation', 'estimated_hours': 2}
        ]

    def _generate_complex_breakdown(self, user_prompt: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate breakdown for complex tasks"""
        return [
            {'description': f"Requirements analysis for: {user_prompt}", 'type': 'analysis', 'estimated_hours': 3},
            {'description': f"System architecture design for: {user_prompt}", 'type': 'architecture', 'estimated_hours': 4},
            {'description': f"Technical specification for: {user_prompt}", 'type': 'specification', 'estimated_hours': 3},
            {'description': f"Core implementation for: {user_prompt}", 'type': 'implementation', 'estimated_hours': 8},
            {'description': f"Integration testing for: {user_prompt}", 'type': 'testing', 'estimated_hours': 4},
            {'description': f"UX validation for: {user_prompt}", 'type': 'ux_validation', 'estimated_hours': 2},
            {'description': f"Quality gates validation for: {user_prompt}", 'type': 'quality', 'estimated_hours': 2}
        ]

    def _extract_dependencies(self, subtasks: List[Dict[str, Any]]) -> List[str]:
        """Extract task dependencies"""
        dependencies = []
        task_types = [st.get('type') for st in subtasks]

        if 'research' in task_types and 'design' in task_types:
            dependencies.append('research -> design')
        if 'design' in task_types and 'implementation' in task_types:
            dependencies.append('design -> implementation')
        if 'implementation' in task_types and 'testing' in task_types:
            dependencies.append('implementation -> testing')

        return dependencies

    def _determine_quality_gates(self, subtasks: List[Dict[str, Any]]) -> List[str]:
        """Determine quality gates for task"""
        gates = ['task_completion_validation']

        task_types = [st.get('type') for st in subtasks]

        if 'implementation' in task_types:
            gates.append('code_quality_gate')
        if 'testing' in task_types:
            gates.append('test_validation_gate')
        if any(t in task_types for t in ['design', 'architecture']):
            gates.append('design_review_gate')

        return gates

    def _configure_quality_gates(self, task_breakdown: TaskBreakdown) -> Dict[str, Any]:
        """Configure quality gates for the task"""
        return {
            'gates': task_breakdown.quality_gates,
            'criteria': {
                'code_quality_gate': {'coverage': 85, 'complexity': 'low'},
                'test_validation_gate': {'pass_rate': 95},
                'design_review_gate': {'approval_required': True}
            },
            'escalation_rules': {
                'failure_threshold': 2,
                'human_escalation': True
            }
        }

    def _generate_reasoning(self, task_breakdown: TaskBreakdown, assignments: Dict[str, str]) -> str:
        """Generate PM reasoning for decision capture"""
        return f"""
        Task Analysis:
        - Complexity: {len(task_breakdown.subtasks)} subtasks identified
        - Priority: {task_breakdown.priority.value}
        - Estimated duration: {task_breakdown.estimated_duration} minutes

        Agent Assignment Logic:
        - Capability matching performed for each subtask
        - Load balancing considered
        - Success rates factored into assignments

        Quality Gates:
        - {len(task_breakdown.quality_gates)} quality gates configured
        - Dependencies: {', '.join(task_breakdown.dependencies)}
        """

    def _calculate_confidence(self, task_breakdown: TaskBreakdown) -> int:
        """Calculate PM confidence score 1-10"""
        base_confidence = 8

        # Adjust based on complexity
        if len(task_breakdown.subtasks) > 5:
            base_confidence -= 1
        if task_breakdown.priority == TaskPriority.CRITICAL:
            base_confidence -= 1
        if len(task_breakdown.dependencies) > 3:
            base_confidence -= 1

        return max(base_confidence, 5)

    def _determine_model_assignments(self, assignments: Dict[str, str]) -> Dict[str, str]:
        """Determine AI model assignments for each agent"""
        model_assignments = {}

        for subtask, agent in assignments.items():
            if 'architect' in agent:
                model_assignments[agent] = 'claude-sonnet-4'  # Complex reasoning
            elif 'analyst' in agent:
                model_assignments[agent] = 'glm-4.5'  # Research tasks
            else:
                model_assignments[agent] = 'glm-4.5-air'  # Routine tasks

        return model_assignments

    def _estimate_completion_time(self, task_breakdown: TaskBreakdown) -> str:
        """Estimate task completion time"""
        completion_time = datetime.now() + timedelta(minutes=task_breakdown.estimated_duration)
        return completion_time.isoformat()

    def _generate_next_actions(self, assignments: Dict[str, str]) -> List[str]:
        """Generate next actions for the workflow"""
        return [
            f"Notify {agent} of {subtask} assignment"
            for subtask, agent in assignments.items()
        ]