"""
BMAD Auto Quality Gate Simple Module
Optimized for BMAD compliance - Essential gate processing only

Purpose: Essential quality gate validation and processing
Size: <300 lines for BMAD compliance
Dependencies: Database coordination.db only
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class QualityStage(Enum):
    """Simplified quality gate stages"""
    INPUT_VALIDATION = "input_validation"
    CONTENT_REVIEW = "content_review"
    PM_APPROVAL = "pm_approval"


class QualityDecision(Enum):
    """Quality gate decision outcomes"""
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


@dataclass
class SimpleQualityResult:
    """Simplified quality gate result"""
    deliverable_id: str
    stage: QualityStage
    decision: QualityDecision
    quality_score: float
    pm_reasoning: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class QualityGateSimple:
    """Simplified quality gate processor for BMAD compliance"""

    def __init__(self, db_path: str = "intercept/coordination.db"):
        self.db_path = db_path
        self.logger = logger
        self.quality_thresholds = {
            QualityStage.INPUT_VALIDATION: 6.0,
            QualityStage.CONTENT_REVIEW: 7.0,
            QualityStage.PM_APPROVAL: 8.0
        }

    def execute_gate(self, deliverable_id: str, content: Dict[str, Any], stage: QualityStage) -> SimpleQualityResult:
        """Execute simplified quality gate validation"""
        try:
            self.logger.info(f"Executing quality gate {stage.value} for {deliverable_id}")

            # Simple quality assessment
            quality_score = self._assess_quality(content, stage)

            # Make decision based on threshold
            decision = self._make_decision(quality_score, stage)

            # Create result
            result = SimpleQualityResult(
                deliverable_id=deliverable_id,
                stage=stage,
                decision=decision,
                quality_score=quality_score,
                pm_reasoning=f"Automated assessment for {stage.value}"
            )

            # Store result
            self._store_result(result)

            return result

        except Exception as e:
            self.logger.error(f"Quality gate execution failed: {e}")
            raise

    def _assess_quality(self, content: Dict[str, Any], stage: QualityStage) -> float:
        """Simple quality assessment based on stage"""

        if stage == QualityStage.INPUT_VALIDATION:
            return self._validate_input(content)
        elif stage == QualityStage.CONTENT_REVIEW:
            return self._review_content(content)
        elif stage == QualityStage.PM_APPROVAL:
            return self._pm_assessment(content)

        return 5.0  # Default score

    def _validate_input(self, content: Dict[str, Any]) -> float:
        """Input validation scoring"""
        score = 8.0  # Base score

        required_fields = content.get("required_fields", [])
        provided_fields = list(content.keys())

        if len(provided_fields) >= len(required_fields):
            score += 1.0
        else:
            score -= 2.0

        return max(0.0, min(10.0, score))

    def _review_content(self, content: Dict[str, Any]) -> float:
        """Content review scoring"""
        accuracy = content.get("accuracy_score", 7.0)
        completeness = content.get("completeness_score", 7.0)

        return (accuracy + completeness) / 2.0

    def _pm_assessment(self, content: Dict[str, Any]) -> float:
        """PM approval assessment"""
        return content.get("pm_score", 8.0)

    def _make_decision(self, score: float, stage: QualityStage) -> QualityDecision:
        """Make quality gate decision"""
        threshold = self.quality_thresholds.get(stage, 7.0)

        if score >= threshold:
            return QualityDecision.APPROVED
        elif score >= (threshold - 2.0):
            return QualityDecision.NEEDS_REVISION
        else:
            return QualityDecision.REJECTED

    def _store_result(self, result: SimpleQualityResult):
        """Store quality gate result"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO quality_gate_executions (
                        deliverable_id, quality_stage, pm_decision,
                        quality_score, pm_reasoning, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    result.deliverable_id, result.stage.value, result.decision.value,
                    result.quality_score, result.pm_reasoning, result.created_at.isoformat()
                ))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to store quality result: {e}")
            raise

    def get_results(self, deliverable_id: str) -> List[SimpleQualityResult]:
        """Get quality gate results for deliverable"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT deliverable_id, quality_stage, pm_decision,
                           quality_score, pm_reasoning, created_at
                    FROM quality_gate_executions
                    WHERE deliverable_id = ?
                    ORDER BY created_at DESC
                """, (deliverable_id,))

                results = []
                for row in cursor.fetchall():
                    results.append(SimpleQualityResult(
                        deliverable_id=row[0],
                        stage=QualityStage(row[1]),
                        decision=QualityDecision(row[2]),
                        quality_score=row[3],
                        pm_reasoning=row[4],
                        created_at=datetime.fromisoformat(row[5])
                    ))

                return results

        except Exception as e:
            self.logger.error(f"Error getting quality results: {e}")
            return []


class QualityBatch:
    """Batch quality gate processing"""

    def __init__(self, db_path: str):
        self.gate_processor = QualityGateSimple(db_path)

    def process_batch(self, deliverables: List[Dict[str, Any]], stage: QualityStage) -> List[SimpleQualityResult]:
        """Process multiple deliverables through quality gate"""
        results = []

        for deliverable in deliverables:
            deliverable_id = deliverable.get("id", f"batch_{datetime.now().timestamp()}")
            content = deliverable.get("content", {})

            try:
                result = self.gate_processor.execute_gate(deliverable_id, content, stage)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch processing failed for {deliverable_id}: {e}")
                # Create failure result
                results.append(SimpleQualityResult(
                    deliverable_id=deliverable_id,
                    stage=stage,
                    decision=QualityDecision.REJECTED,
                    quality_score=0.0,
                    pm_reasoning=f"Processing error: {str(e)}"
                ))

        return results