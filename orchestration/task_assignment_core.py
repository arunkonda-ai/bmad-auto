"""
BMAD Auto Task Assignment Core Engine
Central task assignment orchestration and execution logic

This module provides the core TaskAssignmentEngine that orchestrates
intelligent task distribution across the 10-agent ecosystem.

Integration:
- Used by PMCoordinator for intelligent agent assignment
- Coordinates with CapabilityMatcher and LoadBalancer
- Integrates with database for assignment persistence
- Supports optimization strategies and execution planning

Architecture:
- TaskAssignmentEngine: Main assignment orchestrator
- Task dependency analysis and execution planning
- Multi-criteria optimization coordination
- Assignment result generation and reporting

Key Features:
- Real-time task assignment orchestration
- Dependency analysis with critical path calculation
- Assignment optimization report generation
- Integration with capability matching and load balancing
"""

import logging
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json
from datetime import datetime, timedelta

from .capability_matcher import CapabilityMatcher, TaskRequirement, AgentCapability
from .load_balancer import LoadBalancer


@dataclass
class TaskAssignment:
    """Task assignment result with reasoning"""
    task_id: str
    assigned_agent_id: str
    assignment_confidence: float  # 0.0-1.0
    estimated_completion_time: datetime
    assignment_reasoning: str
    alternative_agents: List[Tuple[str, float]]  # (agent_id, confidence)
    dependencies_satisfied: bool
    parallel_opportunities: List[str]  # Task IDs that can run in parallel


class TaskAssignmentEngine:
    """
    Intelligent Task Assignment Engine

    Provides sophisticated algorithms for matching tasks to agent capabilities,
    optimizing workload distribution, and identifying parallel execution
    opportunities across the 10-agent ecosystem.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.capability_matcher = CapabilityMatcher()
        self.load_balancer = LoadBalancer()

    def assign_tasks(
        self,
        tasks: List[TaskRequirement],
        agents: List[AgentCapability],
        optimization_strategy: str = "balanced"
    ) -> Tuple[List[TaskAssignment], Dict[str, Any]]:
        """
        Assign multiple tasks to agents with optimization

        Args:
            tasks: List of tasks to assign
            agents: Available agents with capabilities
            optimization_strategy: "speed", "quality", "balanced", "load_balance"

        Returns:
            Tuple of (assignments, optimization_report)
        """
        try:
            # Analyze task dependencies and identify execution order
            execution_plan = self._analyze_task_dependencies(tasks)

            # Get agent capability matrix
            capability_matrix = self.capability_matcher.build_capability_matrix(
                tasks, agents
            )

            # Optimize assignments based on strategy
            assignments = self._optimize_assignments(
                tasks, agents, capability_matrix, optimization_strategy
            )

            # Balance load across agents
            balanced_assignments = self.load_balancer.balance_workload(
                assignments, agents
            )

            # Generate optimization report
            optimization_report = self._generate_optimization_report(
                balanced_assignments, agents, execution_plan
            )

            self.logger.info(f"Successfully assigned {len(tasks)} tasks to agents")
            return balanced_assignments, optimization_report

        except Exception as e:
            self.logger.error(f"Task assignment failed: {e}")
            raise

    def _analyze_task_dependencies(
        self,
        tasks: List[TaskRequirement]
    ) -> Dict[str, Any]:
        """Analyze task dependencies and create execution plan"""

        task_map = {task.task_id: task for task in tasks}
        dependency_graph = {}
        parallel_groups = []

        # Build dependency graph
        for task in tasks:
            dependency_graph[task.task_id] = {
                "dependencies": task.dependencies,
                "dependents": []
            }

        # Find dependents
        for task_id, deps in dependency_graph.items():
            for dep_id in deps["dependencies"]:
                if dep_id in dependency_graph:
                    dependency_graph[dep_id]["dependents"].append(task_id)

        # Identify parallel execution opportunities
        independent_tasks = [
            task_id for task_id, deps in dependency_graph.items()
            if not deps["dependencies"]
        ]

        if len(independent_tasks) > 1:
            parallel_groups.append(independent_tasks)

        return {
            "dependency_graph": dependency_graph,
            "parallel_groups": parallel_groups,
            "execution_order": self._topological_sort(dependency_graph),
            "critical_path": self._find_critical_path(task_map, dependency_graph)
        }

    def _topological_sort(self, dependency_graph: Dict) -> List[str]:
        """Topological sort for task execution order"""

        in_degree = {task_id: len(deps["dependencies"])
                    for task_id, deps in dependency_graph.items()}
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            current = queue.pop(0)
            result.append(current)

            for dependent in dependency_graph[current]["dependents"]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        return result

    def _find_critical_path(
        self,
        task_map: Dict[str, TaskRequirement],
        dependency_graph: Dict
    ) -> List[str]:
        """Find critical path through task dependencies"""

        # Simplified critical path calculation
        path_times = {}
        for task_id, task in task_map.items():
            path_times[task_id] = task.estimated_effort_hours

        # Return longest single task as critical path
        critical_task = max(path_times, key=path_times.get)
        return [critical_task]

    def _optimize_assignments(
        self,
        tasks: List[TaskRequirement],
        agents: List[AgentCapability],
        capability_matrix: Dict[str, Dict[str, float]],
        strategy: str
    ) -> List[TaskAssignment]:
        """Optimize task assignments based on strategy"""

        assignments = []

        # Sort tasks by priority and complexity
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (t.priority, t.complexity.value),
            reverse=True
        )

        for task in sorted_tasks:
            assignment = self._optimize_single_assignment(
                task, agents, capability_matrix, strategy
            )
            assignments.append(assignment)

        return assignments

    def _optimize_single_assignment(
        self,
        task: TaskRequirement,
        agents: List[AgentCapability],
        capability_matrix: Dict[str, Dict[str, float]],
        strategy: str
    ) -> TaskAssignment:
        """Optimize assignment for single task"""

        task_capabilities = capability_matrix.get(task.task_id, {})
        agent_scores = {}

        for agent in agents:
            if agent.availability_status == "blocked":
                continue

            capability_score = task_capabilities.get(agent.agent_id, 0)

            if strategy == "speed":
                score = capability_score * agent.efficiency_score
            elif strategy == "quality":
                score = capability_score * (2 - agent.load_percentage / 100)
            else:  # balanced or load_balance
                score = capability_score * agent.efficiency_score * (1 - agent.load_percentage / 100)

            agent_scores[agent.agent_id] = score

        if not agent_scores:
            raise Exception(f"No available agents for task {task.task_id}")

        best_agent_id = max(agent_scores, key=agent_scores.get)
        best_score = agent_scores[best_agent_id]

        alternatives = sorted(
            [(agent_id, score) for agent_id, score in agent_scores.items()
             if agent_id != best_agent_id],
            key=lambda x: x[1], reverse=True
        )[:3]

        best_agent = next(a for a in agents if a.agent_id == best_agent_id)
        estimated_completion = datetime.now() + timedelta(
            hours=task.estimated_effort_hours / best_agent.efficiency_score
        )

        return TaskAssignment(
            task_id=task.task_id,
            assigned_agent_id=best_agent_id,
            assignment_confidence=best_score,
            estimated_completion_time=estimated_completion,
            assignment_reasoning=f"Selected based on {strategy} strategy",
            alternative_agents=alternatives,
            dependencies_satisfied=True,
            parallel_opportunities=[]
        )

    def _generate_optimization_report(
        self,
        assignments: List[TaskAssignment],
        agents: List[AgentCapability],
        execution_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate optimization report"""

        total_effort = sum(self._estimate_task_effort(a.task_id, assignments) for a in assignments)
        avg_confidence = sum(a.assignment_confidence for a in assignments) / len(assignments)

        return {
            "total_tasks_assigned": len(assignments),
            "total_estimated_effort": total_effort,
            "average_assignment_confidence": round(avg_confidence, 3),
            "parallel_execution_opportunities": len(execution_plan.get("parallel_groups", [])),
            "critical_path_length": len(execution_plan.get("critical_path", [])),
            "optimization_timestamp": datetime.now().isoformat()
        }

    def _estimate_task_effort(self, task_id: str, assignments: List[TaskAssignment]) -> float:
        """Estimate task effort based on assignment confidence"""
        assignment = next(a for a in assignments if a.task_id == task_id)

        if assignment.assignment_confidence > 0.8:
            return 2.0
        elif assignment.assignment_confidence > 0.6:
            return 4.0
        elif assignment.assignment_confidence > 0.4:
            return 6.0
        else:
            return 8.0