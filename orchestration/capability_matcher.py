"""
BMAD Auto Capability Matching System
Agent-task capability matching algorithms and specialization analysis

This module provides sophisticated capability matching between tasks and agents,
analyzing specializations, availability, and efficiency to optimize assignments.

Integration:
- Used by TaskAssignmentEngine for capability analysis
- Integrates with agent specialization data structures
- Supports multi-criteria capability assessment
- Provides matching matrices for assignment optimization

Architecture:
- CapabilityMatcher: Main matching algorithm coordinator
- Specialization matching and scoring
- Availability and efficiency factor analysis
- Multi-dimensional capability matrix generation

Key Features:
- Primary and secondary specialization matching
- Real-time availability assessment
- Efficiency-weighted scoring algorithms
- Comprehensive capability matrix generation
"""

import logging
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json
from datetime import datetime, timedelta


class TaskComplexity(Enum):
    """Task complexity levels for assignment optimization"""
    TRIVIAL = "trivial"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class AgentSpecialization(Enum):
    """Agent specialization areas for capability matching"""
    PROJECT_MANAGEMENT = "project_management"
    ARCHITECTURE = "architecture"
    DEVELOPMENT = "development"
    QUALITY_ASSURANCE = "quality_assurance"
    USER_EXPERIENCE = "user_experience"
    BUSINESS_ANALYSIS = "business_analysis"
    RESEARCH = "research"
    COORDINATION = "coordination"


@dataclass
class TaskRequirement:
    """Individual task requirement specification"""
    task_id: str
    description: str
    complexity: TaskComplexity
    required_specializations: List[AgentSpecialization]
    estimated_effort_hours: float
    dependencies: List[str]  # Other task IDs
    priority: int  # 1-10 scale
    deadline: Optional[datetime] = None
    requires_human_approval: bool = False


@dataclass
class AgentCapability:
    """Agent capability and current status"""
    agent_id: str
    agent_name: str
    primary_specialization: AgentSpecialization
    secondary_specializations: List[AgentSpecialization]
    current_load_hours: float
    max_capacity_hours: float
    efficiency_score: float  # 0.0-1.0 performance multiplier
    availability_status: str  # "available", "busy", "blocked"
    last_task_completion: Optional[datetime] = None
    current_tasks: List[str] = None

    def __post_init__(self):
        if self.current_tasks is None:
            self.current_tasks = []

    @property
    def load_percentage(self) -> float:
        """Current workload as percentage of capacity"""
        return (self.current_load_hours / self.max_capacity_hours) * 100

    @property
    def available_capacity(self) -> float:
        """Available capacity in hours"""
        return max(0, self.max_capacity_hours - self.current_load_hours)


class CapabilityMatcher:
    """
    Agent Capability Matching System

    Provides sophisticated algorithms for matching tasks to agent capabilities,
    analyzing specializations, availability, and efficiency to generate
    optimal assignment recommendations.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def build_capability_matrix(
        self,
        tasks: List[TaskRequirement],
        agents: List[AgentCapability]
    ) -> Dict[str, Dict[str, float]]:
        """
        Build comprehensive task-agent capability matching matrix

        Args:
            tasks: List of tasks requiring assignment
            agents: Available agents with capabilities

        Returns:
            Matrix with task_id -> agent_id -> match_score mapping
        """
        try:
            matrix = {}

            for task in tasks:
                matrix[task.task_id] = {}

                for agent in agents:
                    match_score = self._calculate_match_score(task, agent)
                    matrix[task.task_id][agent.agent_id] = match_score

            self.logger.debug(f"Built capability matrix for {len(tasks)} tasks and {len(agents)} agents")
            return matrix

        except Exception as e:
            self.logger.error(f"Failed to build capability matrix: {e}")
            raise

    def _calculate_match_score(
        self,
        task: TaskRequirement,
        agent: AgentCapability
    ) -> float:
        """
        Calculate comprehensive match score between task and agent

        Evaluates:
        - Primary specialization alignment
        - Secondary specialization coverage
        - Agent availability and workload
        - Efficiency and performance factors

        Returns:
            Match score from 0.0 to 1.0
        """
        score = 0.0

        # Primary specialization match (highest weight)
        if agent.primary_specialization in task.required_specializations:
            score += 0.5
            self.logger.debug(f"Primary match: {agent.agent_id} -> {task.task_id}")

        # Secondary specialization matches (medium weight)
        secondary_matches = sum(
            1 for spec in agent.secondary_specializations
            if spec in task.required_specializations
        )
        secondary_score = min(0.3, secondary_matches * 0.1)
        score += secondary_score

        if secondary_matches > 0:
            self.logger.debug(f"Secondary matches ({secondary_matches}): {agent.agent_id} -> {task.task_id}")

        # Availability factor (important for real-time assignment)
        availability_score = self._calculate_availability_score(agent)
        score += availability_score

        # Efficiency factor (applies as multiplier)
        score *= agent.efficiency_score

        # Complexity alignment factor
        complexity_alignment = self._calculate_complexity_alignment(task, agent)
        score *= complexity_alignment

        final_score = min(1.0, max(0.0, score))

        self.logger.debug(
            f"Match score: {agent.agent_id} -> {task.task_id} = {final_score:.3f} "
            f"(availability: {availability_score:.2f}, efficiency: {agent.efficiency_score:.2f})"
        )

        return final_score

    def _calculate_availability_score(self, agent: AgentCapability) -> float:
        """Calculate availability score based on agent status and load"""

        if agent.availability_status == "available":
            # Available agents get full availability score
            if agent.load_percentage < 50:
                return 0.2  # Lightly loaded
            elif agent.load_percentage < 80:
                return 0.15  # Moderately loaded
            else:
                return 0.1  # Heavily loaded but available

        elif agent.availability_status == "busy":
            # Busy agents can still take on work if not overloaded
            if agent.load_percentage < 80:
                return 0.1  # Can still handle additional work
            else:
                return 0.05  # Overloaded, minimal availability

        else:  # "blocked" or other status
            return 0.0  # No availability

    def _calculate_complexity_alignment(
        self,
        task: TaskRequirement,
        agent: AgentCapability
    ) -> float:
        """
        Calculate how well agent capabilities align with task complexity

        Higher efficiency agents are better suited for complex tasks,
        while simpler tasks can be handled by any available agent.
        """

        complexity_factors = {
            TaskComplexity.TRIVIAL: 0.9,      # Any agent can handle
            TaskComplexity.LOW: 0.95,         # Slight preference for efficiency
            TaskComplexity.MEDIUM: 1.0,       # Neutral
            TaskComplexity.HIGH: 1.1,         # Prefer high-efficiency agents
            TaskComplexity.VERY_HIGH: 1.2     # Strong preference for top performers
        }

        base_factor = complexity_factors.get(task.complexity, 1.0)

        # Adjust based on agent efficiency
        if task.complexity in [TaskComplexity.HIGH, TaskComplexity.VERY_HIGH]:
            # Complex tasks benefit more from high-efficiency agents
            return base_factor * agent.efficiency_score
        else:
            # Simple tasks don't require top efficiency
            return base_factor * min(1.0, agent.efficiency_score + 0.2)

    def get_agent_specializations(self, agent_id: str, agents: List[AgentCapability]) -> Dict[str, Any]:
        """Get detailed specialization information for specific agent"""

        agent = next((a for a in agents if a.agent_id == agent_id), None)
        if not agent:
            return {}

        return {
            "agent_id": agent.agent_id,
            "agent_name": agent.agent_name,
            "primary_specialization": agent.primary_specialization.value,
            "secondary_specializations": [spec.value for spec in agent.secondary_specializations],
            "efficiency_score": agent.efficiency_score,
            "current_load": {
                "hours": agent.current_load_hours,
                "percentage": agent.load_percentage,
                "available_capacity": agent.available_capacity
            },
            "availability_status": agent.availability_status,
            "last_task_completion": agent.last_task_completion.isoformat() if agent.last_task_completion else None
        }

    def find_best_matches(
        self,
        task: TaskRequirement,
        agents: List[AgentCapability],
        max_results: int = 5
    ) -> List[Tuple[str, float, str]]:
        """Find best agent matches for a specific task"""

        matches = []

        for agent in agents:
            if agent.availability_status == "blocked":
                continue

            match_score = self._calculate_match_score(task, agent)
            reasoning = f"Score: {match_score:.2f}, Load: {agent.load_percentage:.0f}%"
            matches.append((agent.agent_id, match_score, reasoning))

        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:max_results]