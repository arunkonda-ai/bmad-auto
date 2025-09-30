"""
BMAD Auto Expert Assignment and Management System
Expert matching, assignment, and coordination for quality escalations

This module provides expert management capabilities for quality escalations,
including expert discovery, skill matching, and assignment optimization
for the BMAD Auto autonomous orchestration system.

Integration:
- Used by QualityEscalationManager for expert assignment
- Integrates with human oversight and AG-UI Protocol
- Supports quality escalation workflow coordination

Architecture:
- ExpertMatcher: Expert discovery and assignment logic
- Expert database integration and skill matching
- Assignment optimization and workload balancing

Key Features:
- Expert skill matching with required expertise areas
- Workload balancing and availability management
- Assignment optimization based on multiple criteria
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExpertAssignment:
    """Expert assignment for quality escalation"""
    expert_id: str
    expertise_areas: List[str]
    current_workload: int
    availability_status: str
    response_time_hours: float
    success_rate: float


class ExpertMatcher:
    """
    Expert Matching and Assignment System

    Provides expert discovery, skill matching, and assignment optimization
    for quality escalations in the BMAD Auto system.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def find_matching_experts(
        self,
        required_expertise: List[str],
        preferences: Optional[List[str]] = None
    ) -> List[ExpertAssignment]:
        """
        Find experts matching required expertise areas

        Args:
            required_expertise: Required skill areas
            preferences: Preferred expert IDs

        Returns:
            List of matching expert assignments
        """
        try:
            # Get expert database (mock implementation)
            available_experts = self._get_expert_database()

            # Filter by expertise match
            matching_experts = []
            for expert in available_experts:
                if self._has_required_expertise(expert, required_expertise):
                    if expert.availability_status == "available":
                        matching_experts.append(expert)

            # Prioritize preferred experts if specified
            if preferences:
                matching_experts.sort(
                    key=lambda x: 0 if x.expert_id in preferences else 1
                )

            self.logger.info(f"Found {len(matching_experts)} matching experts")
            return matching_experts

        except Exception as e:
            self.logger.error(f"Expert matching failed: {e}")
            return []

    def select_best_expert(
        self,
        available_experts: List[ExpertAssignment],
        required_expertise: List[str]
    ) -> ExpertAssignment:
        """
        Select optimal expert from available options

        Args:
            available_experts: Available expert candidates
            required_expertise: Required expertise areas

        Returns:
            Best expert assignment
        """
        if not available_experts:
            raise Exception("No available experts")

        # Score experts based on multiple criteria
        expert_scores = []
        for expert in available_experts:
            score = self._calculate_expert_score(expert, required_expertise)
            expert_scores.append((expert, score))

        # Select expert with highest score
        best_expert = max(expert_scores, key=lambda x: x[1])[0]

        self.logger.info(f"Selected expert {best_expert.expert_id}")
        return best_expert

    def get_expert_workload_status(self) -> Dict[str, Any]:
        """
        Get current expert workload status

        Returns:
            Expert workload summary
        """
        experts = self._get_expert_database()

        workload_summary = {
            "total_experts": len(experts),
            "available_experts": len([e for e in experts if e.availability_status == "available"]),
            "average_workload": sum(e.current_workload for e in experts) / len(experts) if experts else 0,
            "high_workload_experts": len([e for e in experts if e.current_workload > 5])
        }

        return workload_summary

    def _get_expert_database(self) -> List[ExpertAssignment]:
        """Get expert database (mock implementation)"""

        # In production, this would connect to actual expert database
        return [
            ExpertAssignment(
                expert_id="expert_qa_001",
                expertise_areas=["quality_assurance", "testing", "standards_compliance"],
                current_workload=2,
                availability_status="available",
                response_time_hours=2.0,
                success_rate=0.95
            ),
            ExpertAssignment(
                expert_id="expert_arch_001",
                expertise_areas=["software_architecture", "system_integration", "performance_engineering"],
                current_workload=1,
                availability_status="available",
                response_time_hours=3.0,
                success_rate=0.92
            ),
            ExpertAssignment(
                expert_id="expert_sec_001",
                expertise_areas=["security_engineering", "compliance", "regulatory_compliance"],
                current_workload=3,
                availability_status="available",
                response_time_hours=1.5,
                success_rate=0.98
            ),
            ExpertAssignment(
                expert_id="expert_perf_001",
                expertise_areas=["performance_engineering", "optimization", "system_tuning"],
                current_workload=4,
                availability_status="busy",
                response_time_hours=6.0,
                success_rate=0.94
            )
        ]

    def _has_required_expertise(
        self,
        expert: ExpertAssignment,
        required_expertise: List[str]
    ) -> bool:
        """Check if expert has required expertise"""

        expertise_overlap = set(expert.expertise_areas) & set(required_expertise)
        return len(expertise_overlap) > 0

    def _calculate_expert_score(
        self,
        expert: ExpertAssignment,
        required_expertise: List[str]
    ) -> float:
        """Calculate expert suitability score"""

        # Expertise match score (0-1)
        expertise_match = len(set(expert.expertise_areas) & set(required_expertise))
        expertise_score = min(1.0, expertise_match / len(required_expertise))

        # Availability score (0-1, lower workload is better)
        availability_score = max(0, 1.0 - (expert.current_workload / 10))

        # Response time score (0-1, faster is better)
        response_score = max(0, 1.0 - (expert.response_time_hours / 24))

        # Combine scores with weights
        total_score = (
            expertise_score * 0.5 +
            availability_score * 0.3 +
            response_score * 0.2
        ) * expert.success_rate

        return total_score