"""
BMAD Auto Decision Capture System
PM reasoning capture with confidence scoring and cognitive enhancement

This module captures PM decision-making context and reasoning for cognitive
framework enhancement, storing complete decision trails with searchable context
and learning notes for future cognitive improvement.

Integration:
- Used by PMCoordinator for decision reasoning capture
- Stores decisions in coordination.db pm_decision_log table
- Provides decision analytics and pattern recognition
- Supports confidence scoring and learning feedback

Architecture:
- PMDecisionCapture: Main decision capture orchestrator
- DecisionContext: Decision data structure and validation
- DecisionAnalytics: Pattern analysis and insights
- ConfidenceScoring: PM confidence assessment utilities

Database Schema:
- pm_decision_log table with decision context and reasoning
- JSON storage for complex decision data structures
- Temporal tracking for decision evolution analysis
"""

import json
import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class DecisionType(Enum):
    """PM decision types for classification"""
    TASK_ASSIGNMENT = "task_assignment"
    QUALITY_GATE = "quality_gate"
    RESOURCE_ALLOCATION = "resource_allocation"
    ESCALATION = "escalation"
    WORKFLOW_SELECTION = "workflow_selection"
    AGENT_COORDINATION = "agent_coordination"


@dataclass
class DecisionContext:
    """Complete decision context data structure"""
    decision_id: str
    decision_type: DecisionType
    context_data: Dict[str, Any]
    reasoning_process: str
    outcome: str
    confidence_score: int  # 1-10 scale
    agent_assignments: Optional[Dict[str, str]] = None
    resource_optimization: Optional[Dict[str, Any]] = None
    learning_notes: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if not self.decision_id:
            self.decision_id = str(uuid.uuid4())


class PMDecisionCapture:
    """
    PM Decision Reasoning Capture System

    Captures complete PM decision-making context and reasoning for cognitive
    framework enhancement with confidence scoring and learning feedback.
    """

    def __init__(self, db_path: str = "coordination.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._ensure_database_connection()

    def _ensure_database_connection(self) -> None:
        """Ensure database connection and schema exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Verify pm_decision_log table exists
                cursor = conn.execute("""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name='pm_decision_log'
                """)
                if not cursor.fetchone():
                    raise Exception("pm_decision_log table not found in coordination.db")

            self.logger.info("Database connection verified")
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            raise

    def capture_decision(self, decision: DecisionContext) -> str:
        """
        Capture PM decision with complete reasoning and context

        Args:
            decision: Complete decision context and reasoning

        Returns:
            str: Decision ID for tracking
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO pm_decision_log (
                        decision_context, decision_type, reasoning_process,
                        outcome, confidence_score, learning_notes,
                        model_assignments, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    json.dumps(decision.context_data),
                    decision.decision_type.value,
                    decision.reasoning_process,
                    decision.outcome,
                    decision.confidence_score,
                    decision.learning_notes,
                    json.dumps({
                        "agent_assignments": decision.agent_assignments,
                        "resource_optimization": decision.resource_optimization
                    }),
                    decision.created_at.isoformat()
                ))

                self.logger.info(f"Decision captured: {decision.decision_id}")
                return decision.decision_id

        except Exception as e:
            self.logger.error(f"Failed to capture decision: {e}")
            raise

    def create_task_assignment_decision(
        self,
        user_prompt: str,
        task_breakdown: Dict[str, Any],
        agent_assignments: Dict[str, str],
        reasoning: str,
        confidence: int
    ) -> DecisionContext:
        """Create task assignment decision context"""

        context_data = {
            "user_prompt": user_prompt,
            "task_breakdown": task_breakdown,
            "available_agents": list(agent_assignments.keys()),
            "complexity_analysis": task_breakdown.get("complexity_scores", {}),
            "timeline_constraints": task_breakdown.get("timeline_estimate", 0)
        }

        return DecisionContext(
            decision_id=str(uuid.uuid4()),
            decision_type=DecisionType.TASK_ASSIGNMENT,
            context_data=context_data,
            reasoning_process=reasoning,
            outcome=f"Assigned {len(agent_assignments)} tasks to agents",
            confidence_score=confidence,
            agent_assignments=agent_assignments,
            learning_notes=f"Task assignment for: {user_prompt[:100]}..."
        )

    def create_quality_gate_decision(
        self,
        deliverable_id: str,
        quality_stage: str,
        pm_decision: str,
        reasoning: str,
        confidence: int,
        agent_reviews: Optional[Dict[str, Any]] = None
    ) -> DecisionContext:
        """Create quality gate decision context"""

        context_data = {
            "deliverable_id": deliverable_id,
            "quality_stage": quality_stage,
            "agent_reviews": agent_reviews or {},
            "validation_criteria": "Standard BMAD Auto quality gates",
            "escalation_required": pm_decision == "needs_human_review"
        }

        return DecisionContext(
            decision_id=str(uuid.uuid4()),
            decision_type=DecisionType.QUALITY_GATE,
            context_data=context_data,
            reasoning_process=reasoning,
            outcome=pm_decision,
            confidence_score=confidence,
            learning_notes=f"Quality gate {quality_stage} for {deliverable_id}"
        )

    def create_resource_allocation_decision(
        self,
        resource_request: Dict[str, Any],
        allocation_result: Dict[str, Any],
        reasoning: str,
        confidence: int
    ) -> DecisionContext:
        """Create resource allocation decision context"""

        context_data = {
            "resource_request": resource_request,
            "current_utilization": allocation_result.get("current_load", {}),
            "optimization_applied": allocation_result.get("optimizations", []),
            "budget_constraints": allocation_result.get("budget_impact", {})
        }

        return DecisionContext(
            decision_id=str(uuid.uuid4()),
            decision_type=DecisionType.RESOURCE_ALLOCATION,
            context_data=context_data,
            reasoning_process=reasoning,
            outcome=f"Allocated resources: {allocation_result.get('allocation_summary', 'Unknown')}",
            confidence_score=confidence,
            resource_optimization=allocation_result,
            learning_notes="Resource optimization decision with budget constraints"
        )

    def get_decision_history(
        self,
        decision_type: Optional[DecisionType] = None,
        days_back: int = 30,
        min_confidence: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve decision history for analysis"""

        where_clauses = ["created_at >= datetime('now', '-{} days')".format(days_back)]
        params = []

        if decision_type:
            where_clauses.append("decision_type = ?")
            params.append(decision_type.value)

        if min_confidence:
            where_clauses.append("confidence_score >= ?")
            params.append(min_confidence)

        where_clause = " AND ".join(where_clauses)

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(f"""
                    SELECT * FROM pm_decision_log
                    WHERE {where_clause}
                    ORDER BY created_at DESC
                """, params)

                decisions = []
                for row in cursor.fetchall():
                    decision = dict(row)
                    # Parse JSON fields
                    decision["decision_context"] = json.loads(decision["decision_context"])
                    decision["model_assignments"] = json.loads(decision["model_assignments"])
                    decisions.append(decision)

                return decisions

        except Exception as e:
            self.logger.error(f"Failed to retrieve decision history: {e}")
            return []

    def analyze_decision_patterns(self) -> Dict[str, Any]:
        """Analyze decision patterns for learning and optimization"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                # Confidence distribution by decision type
                confidence_analysis = {}
                cursor = conn.execute("""
                    SELECT decision_type, AVG(confidence_score) as avg_confidence,
                           COUNT(*) as total_decisions
                    FROM pm_decision_log
                    WHERE created_at >= datetime('now', '-30 days')
                    GROUP BY decision_type
                """)

                for row in cursor.fetchall():
                    confidence_analysis[row[0]] = {
                        "average_confidence": round(row[1], 2),
                        "total_decisions": row[2]
                    }

                # Recent decision trends
                cursor = conn.execute("""
                    SELECT DATE(created_at) as decision_date,
                           COUNT(*) as decisions_count,
                           AVG(confidence_score) as avg_confidence
                    FROM pm_decision_log
                    WHERE created_at >= datetime('now', '-7 days')
                    GROUP BY DATE(created_at)
                    ORDER BY decision_date DESC
                """)

                daily_trends = []
                for row in cursor.fetchall():
                    daily_trends.append({
                        "date": row[0],
                        "decisions_count": row[1],
                        "avg_confidence": round(row[2], 2)
                    })

                # Low confidence decisions for learning
                cursor = conn.execute("""
                    SELECT decision_type, reasoning_process, confidence_score
                    FROM pm_decision_log
                    WHERE confidence_score < 7
                    AND created_at >= datetime('now', '-30 days')
                    ORDER BY confidence_score ASC
                    LIMIT 10
                """)

                low_confidence_decisions = []
                for row in cursor.fetchall():
                    low_confidence_decisions.append({
                        "decision_type": row[0],
                        "reasoning": row[1][:100] + "...",
                        "confidence": row[2]
                    })

                return {
                    "confidence_by_type": confidence_analysis,
                    "daily_trends": daily_trends,
                    "low_confidence_decisions": low_confidence_decisions,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "total_decisions_analyzed": sum(
                        data["total_decisions"] for data in confidence_analysis.values()
                    )
                }

        except Exception as e:
            self.logger.error(f"Failed to analyze decision patterns: {e}")
            return {"error": str(e)}

    def get_confidence_score_guidance(
        self,
        decision_type: DecisionType,
        context_complexity: str = "medium"
    ) -> Tuple[int, str]:
        """
        Provide confidence score guidance based on decision type and complexity

        Returns:
            Tuple[int, str]: (suggested_score, reasoning)
        """

        base_scores = {
            DecisionType.TASK_ASSIGNMENT: 8,
            DecisionType.QUALITY_GATE: 9,
            DecisionType.RESOURCE_ALLOCATION: 7,
            DecisionType.ESCALATION: 6,
            DecisionType.WORKFLOW_SELECTION: 8,
            DecisionType.AGENT_COORDINATION: 7
        }

        complexity_modifiers = {
            "low": +1,
            "medium": 0,
            "high": -1,
            "very_high": -2
        }

        base_score = base_scores.get(decision_type, 7)
        modifier = complexity_modifiers.get(context_complexity, 0)
        suggested_score = max(1, min(10, base_score + modifier))

        reasoning = f"Base score {base_score} for {decision_type.value}, " \
                   f"adjusted by {modifier} for {context_complexity} complexity"

        return suggested_score, reasoning


class DecisionAnalytics:
    """Decision analytics and pattern recognition utilities"""

    def __init__(self, decision_capture: PMDecisionCapture):
        self.decision_capture = decision_capture
        self.logger = logging.getLogger(__name__)

    def generate_learning_insights(self) -> Dict[str, Any]:
        """Generate learning insights from decision patterns"""

        patterns = self.decision_capture.analyze_decision_patterns()
        insights = {
            "improvement_opportunities": [],
            "successful_patterns": [],
            "confidence_trends": {},
            "recommendations": []
        }

        # Analyze confidence trends
        confidence_data = patterns.get("confidence_by_type", {})
        for decision_type, data in confidence_data.items():
            avg_conf = data["average_confidence"]
            if avg_conf < 7:
                insights["improvement_opportunities"].append({
                    "area": decision_type,
                    "issue": f"Low average confidence ({avg_conf})",
                    "suggestion": "Review decision criteria and add more context"
                })
            elif avg_conf > 8.5:
                insights["successful_patterns"].append({
                    "area": decision_type,
                    "strength": f"High confidence ({avg_conf})",
                    "maintain": "Continue current decision patterns"
                })

        # Generate recommendations
        total_decisions = patterns.get("total_decisions_analyzed", 0)
        if total_decisions > 0:
            insights["recommendations"].extend([
                "Maintain decision logging for continuous improvement",
                "Review low-confidence decisions for pattern analysis",
                "Consider automating high-confidence decision types"
            ])

        return insights

    def export_decision_data(self, format_type: str = "json") -> str:
        """Export decision data for external analysis"""

        decisions = self.decision_capture.get_decision_history(days_back=90)

        if format_type == "json":
            return json.dumps(decisions, indent=2, default=str)
        elif format_type == "csv":
            # Simple CSV export (would need pandas for full implementation)
            csv_lines = ["decision_type,confidence_score,created_at,outcome"]
            for decision in decisions:
                csv_lines.append(
                    f"{decision['decision_type']},{decision['confidence_score']},"
                    f"{decision['created_at']},{decision['outcome'][:50]}"
                )
            return "\n".join(csv_lines)

        return str(decisions)