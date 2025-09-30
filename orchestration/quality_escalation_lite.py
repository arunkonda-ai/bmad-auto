"""
BMAD Auto Quality Escalation Lite Module
Minimal escalation functionality for BMAD compliance

Purpose: Essential quality escalation coordination only
Size: <300 lines for BMAD compliance
Dependencies: Database coordination.db only
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class EscalationLevel(Enum):
    """Quality escalation severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EscalationStatus(Enum):
    """Escalation workflow status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


@dataclass
class SimpleEscalation:
    """Simple escalation record"""
    escalation_id: str
    deliverable_id: str
    level: EscalationLevel
    status: EscalationStatus
    description: str
    created_at: datetime
    resolved_at: Optional[datetime] = None


class QualityEscalationLite:
    """Lightweight quality escalation manager"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logger

    def create_escalation(self, deliverable_id: str, quality_score: float, description: str) -> str:
        """Create new escalation based on quality score"""
        level = self._determine_level(quality_score)
        escalation_id = f"ESC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{deliverable_id[:8]}"

        escalation = SimpleEscalation(
            escalation_id=escalation_id,
            deliverable_id=deliverable_id,
            level=level,
            status=EscalationStatus.PENDING,
            description=description,
            created_at=datetime.now()
        )

        try:
            self._save_escalation(escalation)
            self.logger.info(f"Created {level.value} escalation {escalation_id}")
            return escalation_id
        except Exception as e:
            self.logger.error(f"Error creating escalation: {e}")
            raise

    def _determine_level(self, quality_score: float) -> EscalationLevel:
        """Determine escalation level from quality score"""
        if quality_score <= 2.0:
            return EscalationLevel.CRITICAL
        elif quality_score <= 4.0:
            return EscalationLevel.HIGH
        elif quality_score <= 6.0:
            return EscalationLevel.MEDIUM
        else:
            return EscalationLevel.LOW

    def _save_escalation(self, escalation: SimpleEscalation):
        """Save escalation to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO simple_escalations
                    (escalation_id, deliverable_id, level, status, description, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    escalation.escalation_id,
                    escalation.deliverable_id,
                    escalation.level.value,
                    escalation.status.value,
                    escalation.description,
                    escalation.created_at.isoformat()
                ))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Error saving escalation: {e}")
            raise

    def resolve_escalation(self, escalation_id: str, resolution_notes: str) -> bool:
        """Resolve an escalation"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE simple_escalations
                    SET status = ?, resolved_at = ?, resolution_notes = ?
                    WHERE escalation_id = ?
                """, (
                    EscalationStatus.RESOLVED.value,
                    datetime.now().isoformat(),
                    resolution_notes,
                    escalation_id
                ))
                conn.commit()
                self.logger.info(f"Resolved escalation {escalation_id}")
                return True
        except Exception as e:
            self.logger.error(f"Error resolving escalation: {e}")
            return False

    def get_active_escalations(self) -> List[SimpleEscalation]:
        """Get all active escalations"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT escalation_id, deliverable_id, level, status, description, created_at, resolved_at
                    FROM simple_escalations
                    WHERE status != 'resolved'
                    ORDER BY created_at DESC
                """)

                results = cursor.fetchall()
                escalations = []

                for row in results:
                    escalations.append(SimpleEscalation(
                        escalation_id=row[0],
                        deliverable_id=row[1],
                        level=EscalationLevel(row[2]),
                        status=EscalationStatus(row[3]),
                        description=row[4],
                        created_at=datetime.fromisoformat(row[5]),
                        resolved_at=datetime.fromisoformat(row[6]) if row[6] else None
                    ))

                return escalations

        except Exception as e:
            self.logger.error(f"Error getting active escalations: {e}")
            return []

    def get_escalation_metrics(self, days: int = 7) -> Dict[str, Any]:
        """Get basic escalation metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Count by level
                cursor.execute("""
                    SELECT level, COUNT(*) as count
                    FROM simple_escalations
                    WHERE created_at >= datetime('now', '-{} days')
                    GROUP BY level
                """.format(days))

                level_counts = dict(cursor.fetchall())

                # Count active
                cursor.execute("""
                    SELECT COUNT(*) FROM simple_escalations
                    WHERE status != 'resolved'
                """)

                active_count = cursor.fetchone()[0] or 0

                # Average resolution time
                cursor.execute("""
                    SELECT AVG(JULIANDAY(resolved_at) - JULIANDAY(created_at)) * 24 as avg_hours
                    FROM simple_escalations
                    WHERE status = 'resolved'
                    AND created_at >= datetime('now', '-{} days')
                """.format(days))

                avg_resolution = cursor.fetchone()[0] or 0.0

                return {
                    "period_days": days,
                    "by_level": level_counts,
                    "active_count": active_count,
                    "avg_resolution_hours": round(avg_resolution, 2),
                    "generated_at": datetime.now().isoformat()
                }

        except Exception as e:
            self.logger.error(f"Error getting metrics: {e}")
            return {"error": str(e)}

    def check_overdue_escalations(self) -> List[str]:
        """Check for overdue escalations"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Define timeout thresholds by level
                thresholds = {
                    EscalationLevel.CRITICAL: 4,    # 4 hours
                    EscalationLevel.HIGH: 12,       # 12 hours
                    EscalationLevel.MEDIUM: 24,     # 24 hours
                    EscalationLevel.LOW: 48          # 48 hours
                }

                overdue_escalations = []

                for level, timeout_hours in thresholds.items():
                    cursor.execute("""
                        SELECT escalation_id
                        FROM simple_escalations
                        WHERE level = ? AND status != 'resolved'
                        AND created_at < datetime('now', '-{} hours')
                    """.format(timeout_hours), (level.value,))

                    overdue = [row[0] for row in cursor.fetchall()]
                    overdue_escalations.extend(overdue)

                # Log overdue escalations
                for escalation_id in overdue_escalations:
                    self.logger.warning(f"Escalation {escalation_id} is overdue")

                return overdue_escalations

        except Exception as e:
            self.logger.error(f"Error checking overdue escalations: {e}")
            return []

    def escalate_to_higher_level(self, escalation_id: str) -> bool:
        """Escalate to the next higher level"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get current level
                cursor.execute("""
                    SELECT level FROM simple_escalations
                    WHERE escalation_id = ?
                """, (escalation_id,))

                result = cursor.fetchone()
                if not result:
                    return False

                current_level = EscalationLevel(result[0])

                # Determine next level
                level_progression = {
                    EscalationLevel.LOW: EscalationLevel.MEDIUM,
                    EscalationLevel.MEDIUM: EscalationLevel.HIGH,
                    EscalationLevel.HIGH: EscalationLevel.CRITICAL,
                    EscalationLevel.CRITICAL: EscalationLevel.CRITICAL  # Stay at critical
                }

                next_level = level_progression.get(current_level)
                if next_level == current_level:
                    return False  # Already at highest level

                # Update escalation level
                cursor.execute("""
                    UPDATE simple_escalations
                    SET level = ?, status = ?
                    WHERE escalation_id = ?
                """, (next_level.value, EscalationStatus.PENDING.value, escalation_id))

                conn.commit()
                self.logger.info(f"Escalated {escalation_id} from {current_level.value} to {next_level.value}")
                return True

        except Exception as e:
            self.logger.error(f"Error escalating {escalation_id}: {e}")
            return False


class EscalationTrigger:
    """Handle escalation triggers from quality gates"""

    def __init__(self, db_path: str):
        self.escalation_manager = QualityEscalationLite(db_path)

    def check_quality_gate_result(self, deliverable_id: str, quality_score: float, pm_decision: str) -> Optional[str]:
        """Check if quality gate result requires escalation"""
        if pm_decision == "rejected" or quality_score < 5.0:
            description = f"Quality gate failure: score {quality_score}, decision {pm_decision}"
            return self.escalation_manager.create_escalation(deliverable_id, quality_score, description)
        return None

    def check_timeout(self, deliverable_id: str, hours_pending: int) -> Optional[str]:
        """Check if pending time requires escalation"""
        if hours_pending > 24:
            description = f"Timeout escalation: {hours_pending} hours pending"
            return self.escalation_manager.create_escalation(deliverable_id, 5.0, description)
        return None