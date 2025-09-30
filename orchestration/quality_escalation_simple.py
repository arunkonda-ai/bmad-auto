"""
BMAD Auto Quality Escalation Simple Module
Rebuilt for BMAD compliance - Essential escalation only

Purpose: Simple quality escalation coordination
Size: <300 lines for BMAD compliance
Dependencies: Database coordination.db, escalation_workflow module
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from .escalation_workflow import EscalationWorkflowManager, EscalationLevel, EscalationStatus

logger = logging.getLogger(__name__)


class EscalationTrigger(Enum):
    """Quality escalation trigger types"""
    QUALITY_FAILURE = "quality_failure"
    TIMEOUT = "timeout"
    EXPERT_REQUEST = "expert_request"
    MANUAL = "manual"


@dataclass
class EscalationConfig:
    """Escalation configuration"""
    trigger_type: EscalationTrigger
    quality_threshold: float
    timeout_hours: int
    escalation_level: EscalationLevel
    auto_escalate: bool = True


class QualityEscalationSimple:
    """Simplified quality escalation manager"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.workflow_manager = EscalationWorkflowManager(db_path)
        self.escalation_configs = self._load_escalation_configs()

    def _load_escalation_configs(self) -> Dict[str, EscalationConfig]:
        """Load escalation configuration"""
        return {
            "low_quality": EscalationConfig(
                trigger_type=EscalationTrigger.QUALITY_FAILURE,
                quality_threshold=6.0,
                timeout_hours=24,
                escalation_level=EscalationLevel.LOW
            ),
            "medium_quality": EscalationConfig(
                trigger_type=EscalationTrigger.QUALITY_FAILURE,
                quality_threshold=4.0,
                timeout_hours=12,
                escalation_level=EscalationLevel.MEDIUM
            ),
            "high_quality": EscalationConfig(
                trigger_type=EscalationTrigger.QUALITY_FAILURE,
                quality_threshold=2.0,
                timeout_hours=4,
                escalation_level=EscalationLevel.HIGH
            ),
            "timeout": EscalationConfig(
                trigger_type=EscalationTrigger.TIMEOUT,
                quality_threshold=0.0,
                timeout_hours=48,
                escalation_level=EscalationLevel.MEDIUM
            )
        }

    def check_escalation_needed(self, deliverable_id: str, quality_score: float, hours_pending: int = 0) -> Optional[str]:
        """Check if escalation is needed and trigger if so"""
        try:
            # Check quality-based escalation
            escalation_level = self._determine_escalation_level(quality_score)
            if escalation_level:
                return self._trigger_escalation(deliverable_id, f"Quality score {quality_score}", escalation_level, "quality_failure")

            # Check timeout-based escalation
            if hours_pending > 24:
                return self._trigger_escalation(deliverable_id, f"Timeout after {hours_pending} hours", EscalationLevel.MEDIUM, "timeout")

            return None

        except Exception as e:
            logger.error(f"Error checking escalation for {deliverable_id}: {e}")
            return None

    def _determine_escalation_level(self, quality_score: float) -> Optional[EscalationLevel]:
        """Determine escalation level based on quality score"""
        if quality_score <= 2.0:
            return EscalationLevel.HIGH
        elif quality_score <= 4.0:
            return EscalationLevel.MEDIUM
        elif quality_score <= 6.0:
            return EscalationLevel.LOW
        else:
            return None

    def _trigger_escalation(self, deliverable_id: str, issue_description: str, level: EscalationLevel, trigger_type: str) -> str:
        """Trigger escalation workflow"""
        try:
            escalation_id = self.workflow_manager.create_escalation(
                deliverable_id=deliverable_id,
                issue_description=issue_description,
                level=level,
                requested_by=f"system_{trigger_type}"
            )

            # Log escalation trigger
            self._log_escalation_trigger(escalation_id, deliverable_id, trigger_type, level)

            logger.info(f"Triggered {level.value} escalation {escalation_id} for deliverable {deliverable_id}")
            return escalation_id

        except Exception as e:
            logger.error(f"Error triggering escalation: {e}")
            raise

    def _log_escalation_trigger(self, escalation_id: str, deliverable_id: str, trigger_type: str, level: EscalationLevel):
        """Log escalation trigger event"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO escalation_triggers
                    (escalation_id, deliverable_id, trigger_type, escalation_level, triggered_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (escalation_id, deliverable_id, trigger_type, level.value, datetime.now().isoformat()))
                conn.commit()

        except Exception as e:
            logger.error(f"Error logging escalation trigger: {e}")

    def get_active_escalations(self) -> List[Dict[str, Any]]:
        """Get all active escalations"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT escalation_id, deliverable_id, current_level, status,
                           issue_description, created_at, resolution_target
                    FROM escalation_requests
                    WHERE status NOT IN ('resolved', 'escalated_further')
                    ORDER BY created_at DESC
                """)

                results = cursor.fetchall()
                escalations = []

                for row in results:
                    escalations.append({
                        "escalation_id": row[0],
                        "deliverable_id": row[1],
                        "level": row[2],
                        "status": row[3],
                        "description": row[4],
                        "created_at": row[5],
                        "resolution_target": row[6]
                    })

                return escalations

        except Exception as e:
            logger.error(f"Error getting active escalations: {e}")
            return []

    def resolve_escalation(self, escalation_id: str, resolution_notes: str, resolved_by: str) -> bool:
        """Resolve an escalation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE escalation_requests
                    SET status = ?, resolution_notes = ?, resolved_by = ?, resolved_at = ?, updated_at = ?
                    WHERE escalation_id = ?
                """, (
                    EscalationStatus.RESOLVED.value,
                    resolution_notes,
                    resolved_by,
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    escalation_id
                ))
                conn.commit()

                logger.info(f"Resolved escalation {escalation_id} by {resolved_by}")
                return True

        except Exception as e:
            logger.error(f"Error resolving escalation {escalation_id}: {e}")
            return False

    def get_escalation_metrics(self, days: int = 7) -> Dict[str, Any]:
        """Get escalation metrics for specified period"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get escalation counts by level
                cursor.execute("""
                    SELECT current_level, COUNT(*) as count
                    FROM escalation_requests
                    WHERE created_at >= datetime('now', '-{} days')
                    GROUP BY current_level
                """.format(days))

                level_counts = dict(cursor.fetchall())

                # Get resolution times
                cursor.execute("""
                    SELECT
                        AVG(JULIANDAY(resolved_at) - JULIANDAY(created_at)) * 24 as avg_hours
                    FROM escalation_requests
                    WHERE status = 'resolved'
                    AND created_at >= datetime('now', '-{} days')
                """.format(days))

                avg_resolution_time = cursor.fetchone()[0] or 0.0

                # Get current active count
                cursor.execute("""
                    SELECT COUNT(*) FROM escalation_requests
                    WHERE status NOT IN ('resolved', 'escalated_further')
                """)

                active_count = cursor.fetchone()[0] or 0

                return {
                    "period_days": days,
                    "escalations_by_level": level_counts,
                    "average_resolution_hours": round(avg_resolution_time, 2),
                    "active_escalations": active_count,
                    "generated_at": datetime.now().isoformat()
                }

        except Exception as e:
            logger.error(f"Error getting escalation metrics: {e}")
            return {"error": str(e)}

    def check_overdue_escalations(self) -> List[str]:
        """Check for overdue escalations and auto-escalate"""
        try:
            return self.workflow_manager.check_overdue_escalations()

        except Exception as e:
            logger.error(f"Error checking overdue escalations: {e}")
            return []


class ExpertCoordinator:
    """Coordinate expert assignment for escalations"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def assign_expert(self, escalation_id: str, expert_id: str, expertise_area: str) -> bool:
        """Assign expert to escalation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE escalation_requests
                    SET expert_assigned = ?, status = ?, updated_at = ?
                    WHERE escalation_id = ?
                """, (expert_id, EscalationStatus.EXPERT_ASSIGNED.value, datetime.now().isoformat(), escalation_id))

                # Log expert assignment
                cursor.execute("""
                    INSERT INTO expert_assignments
                    (escalation_id, expert_id, expertise_area, assigned_at)
                    VALUES (?, ?, ?, ?)
                """, (escalation_id, expert_id, expertise_area, datetime.now().isoformat()))

                conn.commit()
                logger.info(f"Assigned expert {expert_id} to escalation {escalation_id}")
                return True

        except Exception as e:
            logger.error(f"Error assigning expert: {e}")
            return False

    def get_available_experts(self, expertise_area: str) -> List[Dict[str, Any]]:
        """Get available experts for specific expertise area"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT expert_id, name, expertise_areas, current_workload
                    FROM experts
                    WHERE expertise_areas LIKE ?
                    AND is_available = 1
                    ORDER BY current_workload ASC
                """, (f'%{expertise_area}%',))

                results = cursor.fetchall()
                experts = []

                for row in results:
                    experts.append({
                        "expert_id": row[0],
                        "name": row[1],
                        "expertise_areas": row[2].split(','),
                        "workload": row[3]
                    })

                return experts

        except Exception as e:
            logger.error(f"Error getting available experts: {e}")
            return []