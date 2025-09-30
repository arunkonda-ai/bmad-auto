"""
BMAD Auto Quality Analytics Simple Module
Minimal analytics for BMAD compliance

Purpose: Essential quality analytics and reporting
Size: <300 lines for BMAD compliance
Dependencies: Database coordination.db only
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics

logger = logging.getLogger(__name__)


@dataclass
class QualityMetrics:
    """Simple quality metrics"""
    total_gates: int
    passed_gates: int
    average_score: float
    period: str
    generated_at: datetime


class QualityAnalyticsSimple:
    """Simplified quality analytics"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logger

    def get_daily_metrics(self) -> Optional[QualityMetrics]:
        """Get today's quality metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT quality_score, pm_decision
                    FROM quality_gate_executions
                    WHERE date(created_at) = date('now')
                """)

                results = cursor.fetchall()
                if not results:
                    return None

                scores = [score for score, _ in results if score is not None]
                decisions = [decision for _, decision in results]

                total_gates = len(results)
                passed_gates = len([d for d in decisions if d == 'approved'])
                avg_score = statistics.mean(scores) if scores else 0.0

                return QualityMetrics(
                    total_gates=total_gates,
                    passed_gates=passed_gates,
                    average_score=avg_score,
                    period="daily",
                    generated_at=datetime.now()
                )

        except Exception as e:
            self.logger.error(f"Error getting daily metrics: {e}")
            return None

    def get_weekly_metrics(self) -> Optional[QualityMetrics]:
        """Get this week's quality metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT quality_score, pm_decision
                    FROM quality_gate_executions
                    WHERE created_at >= datetime('now', '-7 days')
                """)

                results = cursor.fetchall()
                if not results:
                    return None

                scores = [score for score, _ in results if score is not None]
                decisions = [decision for _, decision in results]

                total_gates = len(results)
                passed_gates = len([d for d in decisions if d == 'approved'])
                avg_score = statistics.mean(scores) if scores else 0.0

                return QualityMetrics(
                    total_gates=total_gates,
                    passed_gates=passed_gates,
                    average_score=avg_score,
                    period="weekly",
                    generated_at=datetime.now()
                )

        except Exception as e:
            self.logger.error(f"Error getting weekly metrics: {e}")
            return None

    def get_agent_metrics(self, agent_id: str, days: int = 7) -> Dict[str, Any]:
        """Get metrics for specific agent"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT quality_score, pm_decision
                    FROM quality_gate_executions
                    WHERE agent_reviews LIKE ?
                    AND created_at >= datetime('now', '-{} days')
                """.format(days), (f'%{agent_id}%',))

                results = cursor.fetchall()
                if not results:
                    return {"agent_id": agent_id, "no_data": True}

                scores = [score for score, _ in results if score is not None]
                decisions = [decision for _, decision in results]

                total_reviews = len(results)
                avg_score = statistics.mean(scores) if scores else 0.0
                approval_rate = len([d for d in decisions if d == 'approved']) / total_reviews if total_reviews > 0 else 0.0

                return {
                    "agent_id": agent_id,
                    "total_reviews": total_reviews,
                    "average_score": round(avg_score, 2),
                    "approval_rate": round(approval_rate, 2),
                    "period_days": days
                }

        except Exception as e:
            self.logger.error(f"Error getting agent metrics: {e}")
            return {"agent_id": agent_id, "error": str(e)}

    def get_quality_trend(self, days: int = 30) -> Dict[str, Any]:
        """Get quality trend over specified period"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DATE(created_at) as date, AVG(quality_score) as avg_score
                    FROM quality_gate_executions
                    WHERE created_at >= datetime('now', '-{} days')
                    AND quality_score IS NOT NULL
                    GROUP BY DATE(created_at)
                    ORDER BY date
                """.format(days))

                results = cursor.fetchall()
                if len(results) < 2:
                    return {"trend": "insufficient_data", "period_days": days}

                # Simple trend calculation
                scores = [score for _, score in results]
                first_half = scores[:len(scores)//2]
                second_half = scores[len(scores)//2:]

                first_avg = statistics.mean(first_half) if first_half else 0
                second_avg = statistics.mean(second_half) if second_half else 0

                trend = "stable"
                if second_avg > first_avg + 0.5:
                    trend = "improving"
                elif second_avg < first_avg - 0.5:
                    trend = "declining"

                return {
                    "trend": trend,
                    "first_half_avg": round(first_avg, 2),
                    "second_half_avg": round(second_avg, 2),
                    "overall_avg": round(statistics.mean(scores), 2),
                    "period_days": days,
                    "data_points": len(results)
                }

        except Exception as e:
            self.logger.error(f"Error getting quality trend: {e}")
            return {"error": str(e)}

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics"""
        try:
            daily_metrics = self.get_daily_metrics()
            weekly_metrics = self.get_weekly_metrics()

            if not daily_metrics or not weekly_metrics:
                return {"status": "insufficient_data"}

            # Simple health calculation
            daily_pass_rate = daily_metrics.passed_gates / daily_metrics.total_gates if daily_metrics.total_gates > 0 else 0
            weekly_pass_rate = weekly_metrics.passed_gates / weekly_metrics.total_gates if weekly_metrics.total_gates > 0 else 0

            daily_score_norm = min(daily_metrics.average_score / 10.0, 1.0)
            weekly_score_norm = min(weekly_metrics.average_score / 10.0, 1.0)

            health_score = (daily_pass_rate * 0.3 + weekly_pass_rate * 0.3 +
                          daily_score_norm * 0.2 + weekly_score_norm * 0.2)

            status = "excellent" if health_score > 0.9 else \
                    "good" if health_score > 0.8 else \
                    "fair" if health_score > 0.7 else "poor"

            return {
                "status": status,
                "health_score": round(health_score, 3),
                "daily_pass_rate": round(daily_pass_rate, 3),
                "weekly_pass_rate": round(weekly_pass_rate, 3),
                "daily_avg_score": round(daily_metrics.average_score, 2),
                "weekly_avg_score": round(weekly_metrics.average_score, 2),
                "generated_at": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error getting system health: {e}")
            return {"status": "error", "error": str(e)}


class QualityReporter:
    """Generate quality reports"""

    def __init__(self, db_path: str):
        self.analytics = QualityAnalyticsSimple(db_path)

    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate daily quality report"""
        daily_metrics = self.analytics.get_daily_metrics()
        system_health = self.analytics.get_system_health()

        return {
            "report_type": "daily",
            "date": datetime.now().date().isoformat(),
            "metrics": daily_metrics.__dict__ if daily_metrics else None,
            "system_health": system_health,
            "generated_at": datetime.now().isoformat()
        }

    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly quality report"""
        weekly_metrics = self.analytics.get_weekly_metrics()
        quality_trend = self.analytics.get_quality_trend(7)
        system_health = self.analytics.get_system_health()

        return {
            "report_type": "weekly",
            "week_ending": datetime.now().date().isoformat(),
            "metrics": weekly_metrics.__dict__ if weekly_metrics else None,
            "trend": quality_trend,
            "system_health": system_health,
            "generated_at": datetime.now().isoformat()
        }

    def generate_agent_report(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Generate agent performance report"""
        agent_metrics = {}
        for agent_id in agent_ids:
            agent_metrics[agent_id] = self.analytics.get_agent_metrics(agent_id, 14)

        return {
            "report_type": "agent_performance",
            "period": "last_14_days",
            "agents": agent_metrics,
            "generated_at": datetime.now().isoformat()
        }


class QualityDashboard:
    """Provide dashboard data"""

    def __init__(self, db_path: str):
        self.analytics = QualityAnalyticsSimple(db_path)
        self.reporter = QualityReporter(db_path)

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all dashboard data"""
        return {
            "daily_metrics": self.analytics.get_daily_metrics(),
            "weekly_metrics": self.analytics.get_weekly_metrics(),
            "system_health": self.analytics.get_system_health(),
            "quality_trend": self.analytics.get_quality_trend(7),
            "timestamp": datetime.now().isoformat()
        }

    def get_agent_dashboard(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Get agent-specific dashboard"""
        agent_data = {}
        for agent_id in agent_ids:
            agent_data[agent_id] = self.analytics.get_agent_metrics(agent_id, 7)

        return {
            "agents": agent_data,
            "timestamp": datetime.now().isoformat()
        }