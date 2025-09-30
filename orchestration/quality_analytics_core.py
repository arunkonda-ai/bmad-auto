"""
BMAD Auto Quality Analytics Core Module
Rebuilt for BMAD compliance - Essential analytics only

Purpose: Core quality metrics and basic analytics
Size: <300 lines for BMAD compliance
Dependencies: Database coordination.db, analytics_metrics module
"""

import sqlite3
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics

from .analytics_metrics import QualityMetricsCalculator, QualityBenchmarkManager

logger = logging.getLogger(__name__)


@dataclass
class QualityReport:
    """Simplified quality report structure"""
    period: str
    total_gates: int
    passed_gates: int
    average_score: float
    trend: str
    generated_at: datetime


class QualityAnalyticsCore:
    """Core quality analytics with essential functionality"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.metrics_calculator = QualityMetricsCalculator(db_path)
        self.benchmark_manager = QualityBenchmarkManager(db_path)

    def generate_daily_report(self) -> Optional[QualityReport]:
        """Generate daily quality report"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get today's quality data
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

                # Simple trend calculation
                yesterday_avg = self._get_yesterday_average()
                trend = self._calculate_trend(avg_score, yesterday_avg)

                return QualityReport(
                    period="daily",
                    total_gates=total_gates,
                    passed_gates=passed_gates,
                    average_score=avg_score,
                    trend=trend,
                    generated_at=datetime.now()
                )

        except Exception as e:
            logger.error(f"Error generating daily report: {e}")
            return None

    def _get_yesterday_average(self) -> float:
        """Get yesterday's average quality score"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT AVG(quality_score)
                    FROM quality_gate_executions
                    WHERE date(created_at) = date('now', '-1 day')
                    AND quality_score IS NOT NULL
                """)

                result = cursor.fetchone()
                return result[0] if result[0] is not None else 0.0

        except Exception as e:
            logger.error(f"Error getting yesterday average: {e}")
            return 0.0

    def _calculate_trend(self, current: float, previous: float) -> str:
        """Calculate trend direction"""
        if previous == 0:
            return "stable"

        diff = current - previous
        if diff > 0.2:
            return "improving"
        elif diff < -0.2:
            return "declining"
        else:
            return "stable"

    def get_agent_quality_summary(self, agent_id: str, days: int = 7) -> Dict[str, Any]:
        """Get quality summary for specific agent"""
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
                    return {"agent_id": agent_id, "data_available": False}

                scores = [score for score, _ in results if score is not None]
                decisions = [decision for _, decision in results]

                return {
                    "agent_id": agent_id,
                    "data_available": True,
                    "total_reviews": len(results),
                    "average_score": statistics.mean(scores) if scores else 0.0,
                    "approval_rate": len([d for d in decisions if d == 'approved']) / len(decisions) if decisions else 0.0,
                    "period_days": days
                }

        except Exception as e:
            logger.error(f"Error getting agent quality summary: {e}")
            return {"agent_id": agent_id, "error": str(e)}

    def get_quality_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get quality trends over specified period"""
        try:
            trends = self.metrics_calculator.calculate_quality_trends(days)
            benchmarks = {
                "quality_score": self.benchmark_manager.get_benchmark("quality_score"),
                "completion_rate": self.benchmark_manager.get_benchmark("completion_rate")
            }

            return {
                "trends": trends,
                "benchmarks": benchmarks,
                "period_days": days,
                "generated_at": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting quality trends: {e}")
            return {"error": str(e)}

    def get_system_health_score(self) -> float:
        """Calculate simple system health score"""
        try:
            daily_report = self.generate_daily_report()
            if not daily_report or daily_report.total_gates == 0:
                return 0.0

            # Simple health calculation
            pass_rate = daily_report.passed_gates / daily_report.total_gates
            score_factor = min(daily_report.average_score / 10.0, 1.0)

            health_score = (pass_rate * 0.6) + (score_factor * 0.4)
            return min(health_score, 1.0)

        except Exception as e:
            logger.error(f"Error calculating health score: {e}")
            return 0.0

    def log_quality_insight(self, insight_type: str, description: str, confidence: float = 0.0):
        """Log quality insight to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO quality_insights
                    (insight_type, description, confidence, created_at)
                    VALUES (?, ?, ?, ?)
                """, (insight_type, description, confidence, datetime.now().isoformat()))
                conn.commit()

        except Exception as e:
            logger.error(f"Error logging quality insight: {e}")


class QualityDashboardProvider:
    """Provide data for quality dashboard"""

    def __init__(self, db_path: str):
        self.analytics_core = QualityAnalyticsCore(db_path)

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all data needed for quality dashboard"""
        try:
            return {
                "daily_summary": self.analytics_core.generate_daily_report(),
                "system_health": self.analytics_core.get_system_health_score(),
                "quality_trends": self.analytics_core.get_quality_trends(7),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    def get_agent_dashboard_data(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Get agent-specific dashboard data"""
        try:
            agent_data = {}
            for agent_id in agent_ids:
                agent_data[agent_id] = self.analytics_core.get_agent_quality_summary(agent_id)

            return {
                "agents": agent_data,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting agent dashboard data: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}


class QualityReportGenerator:
    """Generate various quality reports"""

    def __init__(self, db_path: str):
        self.analytics_core = QualityAnalyticsCore(db_path)

    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly quality report"""
        try:
            # Get 7-day trends
            trends = self.analytics_core.get_quality_trends(7)
            health_score = self.analytics_core.get_system_health_score()

            return {
                "report_type": "weekly",
                "period": "last_7_days",
                "health_score": health_score,
                "trends": trends,
                "generated_at": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating weekly report: {e}")
            return {"error": str(e)}

    def generate_agent_performance_report(self, agent_ids: List[str]) -> Dict[str, Any]:
        """Generate agent performance report"""
        try:
            agent_summaries = {}
            for agent_id in agent_ids:
                agent_summaries[agent_id] = self.analytics_core.get_agent_quality_summary(agent_id, 14)

            return {
                "report_type": "agent_performance",
                "period": "last_14_days",
                "agents": agent_summaries,
                "generated_at": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating agent performance report: {e}")
            return {"error": str(e)}