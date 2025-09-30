"""
BMAD Auto Load Balancing System
Agent workload balancing and resource optimization algorithms

This module provides sophisticated load balancing across the 10-agent ecosystem,
ensuring optimal resource utilization and preventing agent overload through
dynamic workload redistribution and capacity management.

Integration:
- Used by TaskAssignmentEngine for workload optimization
- Monitors agent capacity and current loads
- Provides alternative agent recommendations
- Supports dynamic load redistribution strategies

Architecture:
- LoadBalancer: Main workload balancing coordinator
- Capacity monitoring and overload detection
- Alternative agent discovery and assignment
- Resource optimization and efficiency tracking

Key Features:
- Real-time capacity monitoring across all agents
- Dynamic workload redistribution to prevent overload
- Alternative agent discovery with capability matching
- Efficiency-based load balancing optimization
"""

import logging
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

from .capability_matcher import AgentCapability, TaskRequirement


@dataclass
class LoadBalancingResult:
    """Result of load balancing operation"""
    original_agent_id: str
    new_agent_id: str
    reason: str
    confidence_change: float
    estimated_effort: float


class LoadBalancer:
    """
    Agent Workload Load Balancing System

    Provides sophisticated algorithms for balancing workload across agents,
    preventing overload, and optimizing resource utilization through
    dynamic assignment redistribution.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.overload_threshold = 0.9  # 90% capacity threshold
        self.optimal_load_range = (0.4, 0.8)  # 40-80% optimal range

    def balance_workload(
        self,
        assignments: List,  # TaskAssignment objects
        agents: List[AgentCapability]
    ) -> List:  # Returns List[TaskAssignment]
        """
        Balance workload across agents to prevent overload

        Args:
            assignments: Initial task assignments
            agents: Available agents with current capacity information

        Returns:
            Balanced task assignments with load redistribution
        """
        try:
            # Calculate current loads after assignments
            agent_loads = {agent.agent_id: agent.current_load_hours for agent in agents}
            agent_map = {agent.agent_id: agent for agent in agents}
            balanced_assignments = []
            rebalancing_actions = []

            self.logger.info(f"Starting load balancing for {len(assignments)} assignments")

            for assignment in assignments:
                agent = agent_map[assignment.assigned_agent_id]
                estimated_effort = self._estimate_effort_from_assignment(assignment)

                # Check if agent would be overloaded
                projected_load = agent_loads[assignment.assigned_agent_id] + estimated_effort
                load_percentage = (projected_load / agent.max_capacity_hours)

                if load_percentage > self.overload_threshold:
                    self.logger.warning(
                        f"Agent {assignment.assigned_agent_id} would be overloaded "
                        f"({load_percentage:.1%} capacity)"
                    )

                    # Try to find alternative agent
                    alternative_result = self._find_alternative_agent(
                        assignment, agents, agent_loads
                    )

                    if alternative_result:
                        self.logger.info(
                            f"Reassigning task {assignment.task_id} from "
                            f"{assignment.assigned_agent_id} to {alternative_result.new_agent_id}"
                        )

                        assignment.assigned_agent_id = alternative_result.new_agent_id
                        assignment.assignment_reasoning += f" (Load balanced: {alternative_result.reason})"
                        assignment.assignment_confidence *= (1 + alternative_result.confidence_change)

                        rebalancing_actions.append(alternative_result)

                # Update load tracking
                agent_loads[assignment.assigned_agent_id] += estimated_effort
                balanced_assignments.append(assignment)

            # Generate load balancing report
            self._log_load_balancing_results(rebalancing_actions, agent_loads, agents)

            return balanced_assignments

        except Exception as e:
            self.logger.error(f"Load balancing failed: {e}")
            raise

    def _estimate_effort_from_assignment(self, assignment) -> float:
        """
        Estimate effort required for assignment based on confidence and complexity

        Lower confidence typically indicates higher complexity/effort required.
        """

        # Base effort estimation from assignment confidence
        if assignment.assignment_confidence > 0.8:
            base_effort = 2.0  # High confidence = straightforward task
        elif assignment.assignment_confidence > 0.6:
            base_effort = 4.0  # Medium confidence = moderate complexity
        elif assignment.assignment_confidence > 0.4:
            base_effort = 6.0  # Lower confidence = higher complexity
        else:
            base_effort = 8.0  # Very low confidence = complex task

        # Adjust based on alternative agents available
        # More alternatives typically means task is more flexible (less effort)
        alternative_factor = max(0.8, 1.0 - (len(assignment.alternative_agents) * 0.05))

        return base_effort * alternative_factor

    def _find_alternative_agent(
        self,
        assignment,
        agents: List[AgentCapability],
        current_loads: Dict[str, float]
    ) -> Optional[LoadBalancingResult]:
        """
        Find alternative agent for load balancing

        Prioritizes agents with:
        1. Available capacity
        2. Good capability match (from alternatives)
        3. Optimal load range
        """

        estimated_effort = self._estimate_effort_from_assignment(assignment)
        original_agent_id = assignment.assigned_agent_id

        # Check alternative agents from assignment
        for agent_id, confidence in assignment.alternative_agents:
            agent = next((a for a in agents if a.agent_id == agent_id), None)
            if not agent:
                continue

            # Check if agent has capacity
            projected_load = current_loads[agent_id] + estimated_effort
            load_percentage = projected_load / agent.max_capacity_hours

            if load_percentage <= self.overload_threshold and confidence > 0.5:
                # Calculate confidence change
                original_confidence = assignment.assignment_confidence
                confidence_change = (confidence - original_confidence) / original_confidence

                reason = self._generate_rebalancing_reason(
                    agent, load_percentage, confidence, estimated_effort
                )

                self.logger.debug(
                    f"Found alternative agent {agent_id} for task {assignment.task_id}: "
                    f"load {load_percentage:.1%}, confidence {confidence:.3f}"
                )

                return LoadBalancingResult(
                    original_agent_id=original_agent_id,
                    new_agent_id=agent_id,
                    reason=reason,
                    confidence_change=confidence_change,
                    estimated_effort=estimated_effort
                )

        # If no alternatives from assignment, try to find underutilized agents
        return self._find_underutilized_agent(
            assignment, agents, current_loads, estimated_effort
        )

    def _find_underutilized_agent(
        self,
        assignment,
        agents: List[AgentCapability],
        current_loads: Dict[str, float],
        estimated_effort: float
    ) -> Optional[LoadBalancingResult]:
        """Find underutilized agent as last resort"""

        for agent in agents:
            if (agent.agent_id != assignment.assigned_agent_id and
                agent.availability_status != "blocked"):

                projected_load = (current_loads[agent.agent_id] + estimated_effort) / agent.max_capacity_hours

                if projected_load <= self.overload_threshold:
                    return LoadBalancingResult(
                        original_agent_id=assignment.assigned_agent_id,
                        new_agent_id=agent.agent_id,
                        reason=f"Load balanced (load: {projected_load:.1%})",
                        confidence_change=-0.1,
                        estimated_effort=estimated_effort
                    )

        return None

    def _generate_rebalancing_reason(
        self,
        agent: AgentCapability,
        load_percentage: float,
        confidence: float,
        effort: float
    ) -> str:
        """Generate rebalancing reason"""
        return f"Load balanced: {load_percentage:.1%} load, {confidence:.2f} confidence"

    def _log_load_balancing_results(
        self,
        rebalancing_actions: List[LoadBalancingResult],
        final_loads: Dict[str, float],
        agents: List[AgentCapability]
    ):
        """Log load balancing results"""

        if rebalancing_actions:
            self.logger.info(f"Performed {len(rebalancing_actions)} load balancing actions")

        overloaded_count = sum(
            1 for agent in agents
            if (final_loads[agent.agent_id] / agent.max_capacity_hours) > self.overload_threshold
        )

        if overloaded_count == 0:
            self.logger.info("Load balancing successful - no agents overloaded")
        else:
            self.logger.warning(f"Still {overloaded_count} agents overloaded after balancing")

    def get_load_distribution_report(
        self,
        agents: List[AgentCapability],
        current_loads: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Generate load distribution report"""

        if current_loads is None:
            current_loads = {agent.agent_id: agent.current_load_hours for agent in agents}

        total_capacity = sum(agent.max_capacity_hours for agent in agents)
        total_used = sum(current_loads.values())
        overloaded_count = sum(
            1 for agent in agents
            if (current_loads.get(agent.agent_id, 0) / agent.max_capacity_hours) > self.overload_threshold
        )

        return {
            "total_agents": len(agents),
            "overall_utilization_percentage": round((total_used / total_capacity) * 100, 1),
            "overloaded_agents": overloaded_count,
            "load_balance_status": "balanced" if overloaded_count == 0 else "unbalanced",
            "generated_at": datetime.now().isoformat()
        }