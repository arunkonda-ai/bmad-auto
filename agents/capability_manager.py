"""
Agent Capability Management - Dynamic capability assignment and performance tracking.

Manages agent capabilities, skill matching, performance optimization,
and resource allocation across the 10-agent ecosystem.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from .capability_registry import CapabilityType, get_standard_capabilities


@dataclass
class Capability:
    """Agent capability definition."""
    name: str
    category: CapabilityType
    proficiency_level: float  # 0.0 to 1.0
    usage_count: int = 0
    success_rate: float = 1.0
    last_used: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CapabilityRequirement:
    """Task capability requirements."""
    required_capabilities: List[str]
    optional_capabilities: List[str] = field(default_factory=list)
    minimum_proficiency: float = 0.7
    task_complexity: float = 0.5  # 0.0 to 1.0


@dataclass
class AgentPerformance:
    """Agent performance metrics."""
    agent_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    average_completion_time: float = 0.0
    quality_score: float = 1.0
    resource_efficiency: float = 1.0
    last_updated: datetime = field(default_factory=datetime.utcnow)


class CapabilityManager:
    """
    Dynamic agent capability management and performance optimization.

    Handles capability matching, performance tracking, and resource
    allocation for optimal agent coordination.
    """

    def __init__(self):
        self.agent_capabilities: Dict[str, List[Capability]] = {}
        self.agent_performance: Dict[str, AgentPerformance] = {}
        self.capability_registry: Dict[str, CapabilityType] = get_standard_capabilities()

    def register_agent_capabilities(
        self,
        agent_id: str,
        capabilities: List[str],
        proficiency_levels: Optional[Dict[str, float]] = None
    ) -> bool:
        """Register agent with capability profile."""
        agent_caps = []

        for cap_name in capabilities:
            if cap_name not in self.capability_registry:
                continue

            proficiency = proficiency_levels.get(cap_name, 0.8) if proficiency_levels else 0.8

            capability = Capability(
                name=cap_name,
                category=self.capability_registry[cap_name],
                proficiency_level=proficiency
            )
            agent_caps.append(capability)

        self.agent_capabilities[agent_id] = agent_caps

        # Initialize performance tracking
        if agent_id not in self.agent_performance:
            self.agent_performance[agent_id] = AgentPerformance(agent_id=agent_id)

        return True

    def match_agent_to_task(
        self,
        requirement: CapabilityRequirement,
        available_agents: List[str]
    ) -> List[tuple[str, float]]:
        """
        Match agents to task requirements with scoring.

        Returns list of (agent_id, match_score) sorted by best match.
        """
        matches = []

        for agent_id in available_agents:
            if agent_id not in self.agent_capabilities:
                continue

            score = self._calculate_match_score(
                agent_id,
                requirement
            )

            if score >= 0.5:  # Minimum 50% match threshold
                matches.append((agent_id, score))

        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def _calculate_match_score(
        self,
        agent_id: str,
        requirement: CapabilityRequirement
    ) -> float:
        """Calculate capability match score for agent."""
        agent_caps = self.agent_capabilities[agent_id]
        agent_cap_names = {cap.name for cap in agent_caps}

        # Check required capabilities
        required_match = sum(
            1 for cap in requirement.required_capabilities
            if cap in agent_cap_names
        )

        if required_match < len(requirement.required_capabilities):
            return 0.0  # Must have all required capabilities

        # Calculate proficiency score
        proficiency_scores = []
        for cap_name in requirement.required_capabilities:
            cap = next((c for c in agent_caps if c.name == cap_name), None)
            if cap:
                proficiency_scores.append(cap.proficiency_level)

        avg_proficiency = sum(proficiency_scores) / len(proficiency_scores) if proficiency_scores else 0

        # Bonus for optional capabilities
        optional_match = sum(
            1 for cap in requirement.optional_capabilities
            if cap in agent_cap_names
        )
        optional_bonus = optional_match * 0.1

        # Performance factor
        performance = self.agent_performance.get(agent_id)
        performance_factor = performance.quality_score if performance else 1.0

        # Final score calculation
        score = (avg_proficiency * 0.6 +
                performance_factor * 0.3 +
                optional_bonus)

        return min(score, 1.0)

    def update_capability_usage(
        self,
        agent_id: str,
        capability_name: str,
        success: bool
    ) -> None:
        """Update capability usage statistics."""
        if agent_id not in self.agent_capabilities:
            return

        for cap in self.agent_capabilities[agent_id]:
            if cap.name == capability_name:
                cap.usage_count += 1
                cap.last_used = datetime.utcnow()

                # Update success rate with exponential moving average
                alpha = 0.1
                cap.success_rate = (alpha * (1.0 if success else 0.0) +
                                  (1 - alpha) * cap.success_rate)
                break

    def update_agent_performance(
        self,
        agent_id: str,
        task_completed: bool,
        completion_time: float,
        quality_score: float
    ) -> None:
        """Update agent performance metrics."""
        if agent_id not in self.agent_performance:
            self.agent_performance[agent_id] = AgentPerformance(agent_id=agent_id)

        perf = self.agent_performance[agent_id]

        if task_completed:
            perf.tasks_completed += 1
        else:
            perf.tasks_failed += 1

        # Update average completion time
        total_tasks = perf.tasks_completed + perf.tasks_failed
        perf.average_completion_time = (
            (perf.average_completion_time * (total_tasks - 1) + completion_time) /
            total_tasks
        )

        # Update quality score with exponential moving average
        alpha = 0.2
        perf.quality_score = alpha * quality_score + (1 - alpha) * perf.quality_score

        perf.last_updated = datetime.utcnow()

    def get_agent_capabilities(self, agent_id: str) -> List[Capability]:
        """Get all capabilities for agent."""
        return self.agent_capabilities.get(agent_id, [])

    def get_agent_performance(self, agent_id: str) -> Optional[AgentPerformance]:
        """Get performance metrics for agent."""
        return self.agent_performance.get(agent_id)

    def get_performance_leaderboard(self) -> List[tuple[str, AgentPerformance]]:
        """Get agents ranked by performance."""
        agents = list(self.agent_performance.items())
        agents.sort(key=lambda x: x[1].quality_score, reverse=True)
        return agents

    def recommend_capability_training(self, agent_id: str) -> List[str]:
        """Recommend capabilities for agent improvement."""
        if agent_id not in self.agent_capabilities:
            return []

        recommendations = []
        agent_caps = self.agent_capabilities[agent_id]

        for cap in agent_caps:
            # Recommend training if low proficiency or low success rate
            if cap.proficiency_level < 0.7 or cap.success_rate < 0.8:
                recommendations.append(cap.name)

        return recommendations