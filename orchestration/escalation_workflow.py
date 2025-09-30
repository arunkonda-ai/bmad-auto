"""
BMAD Auto Escalation Workflow Module
Extracted from quality_escalation_core.py for BMAD compliance

Purpose: Escalation workflow orchestration and management
Size: Targeting <300 lines for BMAD compliance
Dependencies: Database coordination.db + PostgreSQL state
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class EscalationLevel(Enum):
    """Escalation severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EscalationStatus(Enum):
    """Escalation workflow status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    EXPERT_ASSIGNED = "expert_assigned"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    ESCALATED_FURTHER = "escalated_further"


@dataclass
class EscalationRequest:
    """Escalation request structure"""
    escalation_id: str
    deliverable_id: str
    issue_description: str
    current_level: EscalationLevel
    status: EscalationStatus
    requested_by: str
    created_at: datetime
    updated_at: datetime
    resolution_target: Optional[datetime] = None
    expert_assigned: Optional[str] = None
    resolution_notes: Optional[str] = None


@dataclass
class WorkflowStep:
    """Escalation workflow step"""
    step_id: str
    step_name: str
    description: str
    required_expertise: List[str]
    max_duration_hours: int
    auto_escalate: bool = True


class EscalationWorkflowManager:
    """Manage escalation workflows and routing"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.workflow_definitions = self._load_workflow_definitions()

    def _load_workflow_definitions(self) -> Dict[EscalationLevel, List[WorkflowStep]]:
        """Load escalation workflow definitions"""
        return {
            EscalationLevel.LOW: [
                WorkflowStep(
                    step_id="auto_review",
                    step_name="Automated Review",
                    description="Automated quality check and pattern matching",
                    required_expertise=["automation"],
                    max_duration_hours=1
                )
            ],
            EscalationLevel.MEDIUM: [
                WorkflowStep(
                    step_id="expert_review",
                    step_name="Expert Review",
                    description="Review by domain expert",
                    required_expertise=["domain_expert"],
                    max_duration_hours=8
                )
            ],
            EscalationLevel.HIGH: [
                WorkflowStep(
                    step_id="senior_review",
                    step_name="Senior Expert Review",
                    description="Senior specialist review",
                    required_expertise=["senior_expert"],
                    max_duration_hours=12
                )
            ],
            EscalationLevel.CRITICAL: [
                WorkflowStep(
                    step_id="emergency_review",
                    step_name="Emergency Review",
                    description="Immediate expert intervention",
                    required_expertise=["emergency_expert"],
                    max_duration_hours=2
                )
            ]
        }

    def create_escalation(self, deliverable_id: str, issue_description: str, level: EscalationLevel, requested_by: str) -> str:
        """Create new escalation request"""
        escalation_id = f"ESC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{deliverable_id[:8]}"

        # Calculate resolution target based on level
        target_hours = self._get_target_resolution_hours(level)
        resolution_target = datetime.now() + timedelta(hours=target_hours)

        escalation = EscalationRequest(
            escalation_id=escalation_id,
            deliverable_id=deliverable_id,
            issue_description=issue_description,
            current_level=level,
            status=EscalationStatus.PENDING,
            requested_by=requested_by,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            resolution_target=resolution_target
        )

        try:
            self._save_escalation(escalation)
            self._start_workflow(escalation)
            logger.info(f"Created escalation {escalation_id} for deliverable {deliverable_id}")
            return escalation_id

        except Exception as e:
            logger.error(f"Error creating escalation: {e}")
            raise

    def _get_target_resolution_hours(self, level: EscalationLevel) -> int:
        """Get target resolution time based on escalation level"""
        targets = {
            EscalationLevel.LOW: 24,
            EscalationLevel.MEDIUM: 48,
            EscalationLevel.HIGH: 12,
            EscalationLevel.CRITICAL: 4
        }
        return targets.get(level, 24)

    def _save_escalation(self, escalation: EscalationRequest):
        """Save escalation to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO escalation_requests
                    (escalation_id, deliverable_id, issue_description, current_level,
                     status, requested_by, created_at, updated_at, resolution_target)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    escalation.escalation_id,
                    escalation.deliverable_id,
                    escalation.issue_description,
                    escalation.current_level.value,
                    escalation.status.value,
                    escalation.requested_by,
                    escalation.created_at.isoformat(),
                    escalation.updated_at.isoformat(),
                    escalation.resolution_target.isoformat() if escalation.resolution_target else None
                ))
                conn.commit()

        except Exception as e:
            logger.error(f"Error saving escalation: {e}")
            raise

    def _start_workflow(self, escalation: EscalationRequest):
        """Start escalation workflow"""
        workflow_steps = self.workflow_definitions.get(escalation.current_level, [])
        if not workflow_steps:
            logger.warning(f"No workflow defined for level {escalation.current_level}")
            return

        # Start with first step
        first_step = workflow_steps[0]
        self._execute_workflow_step(escalation.escalation_id, first_step)

    def _execute_workflow_step(self, escalation_id: str, step: WorkflowStep):
        """Execute a workflow step"""
        try:
            # Update escalation status
            self._update_escalation_status(escalation_id, EscalationStatus.IN_PROGRESS)

            # Log workflow step start
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO escalation_workflow_log
                    (escalation_id, step_id, step_name, status, started_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    escalation_id,
                    step.step_id,
                    step.step_name,
                    "started",
                    datetime.now().isoformat()
                ))
                conn.commit()

            logger.info(f"Started workflow step {step.step_name} for escalation {escalation_id}")

        except Exception as e:
            logger.error(f"Error executing workflow step: {e}")

    def _update_escalation_status(self, escalation_id: str, status: EscalationStatus):
        """Update escalation status"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE escalation_requests
                    SET status = ?, updated_at = ?
                    WHERE escalation_id = ?
                """, (status.value, datetime.now().isoformat(), escalation_id))
                conn.commit()

        except Exception as e:
            logger.error(f"Error updating escalation status: {e}")

    def check_overdue_escalations(self) -> List[str]:
        """Check for overdue escalations"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT escalation_id, current_level
                    FROM escalation_requests
                    WHERE status NOT IN ('resolved', 'escalated_further')
                    AND resolution_target < ?
                """, (datetime.now().isoformat(),))

                overdue = cursor.fetchall()

                for escalation_id, level in overdue:
                    self._handle_overdue_escalation(escalation_id, EscalationLevel(level))

                return [esc_id for esc_id, _ in overdue]

        except Exception as e:
            logger.error(f"Error checking overdue escalations: {e}")
            return []

    def _handle_overdue_escalation(self, escalation_id: str, current_level: EscalationLevel):
        """Handle overdue escalation by escalating to next level"""
        level_progression = {
            EscalationLevel.LOW: EscalationLevel.MEDIUM,
            EscalationLevel.MEDIUM: EscalationLevel.HIGH,
            EscalationLevel.HIGH: EscalationLevel.CRITICAL,
            EscalationLevel.CRITICAL: EscalationLevel.CRITICAL
        }

        next_level = level_progression.get(current_level)
        if next_level and next_level != current_level:
            self.escalate_to_next_level(escalation_id, next_level)

    def escalate_to_next_level(self, escalation_id: str, new_level: EscalationLevel):
        """Escalate to next level"""
        try:
            target_hours = self._get_target_resolution_hours(new_level)
            new_target = datetime.now() + timedelta(hours=target_hours)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE escalation_requests
                    SET current_level = ?, resolution_target = ?,
                        status = ?, updated_at = ?
                    WHERE escalation_id = ?
                """, (
                    new_level.value,
                    new_target.isoformat(),
                    EscalationStatus.PENDING.value,
                    datetime.now().isoformat(),
                    escalation_id
                ))
                conn.commit()

        except Exception as e:
            logger.error(f"Error escalating to next level: {e}")
