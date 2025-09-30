"""
BMAD Auto Analytics Metrics Module
Extracted from quality_analytics.py for BMAD compliance

Purpose: Quality metrics calculation and performance tracking
Size: Targeting <300 lines for BMAD compliance
Dependencies: Database coordination.db + PostgreSQL state
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import statistics
import logging

logger = logging.getLogger(__name__)


@dataclass
class MetricResult:
    """Quality metric calculation result"""
    metric_name: str
    value: float
    trend: str  # 'improving', 'declining', 'stable'
    benchmark: Optional[float] = None
    confidence: float = 0.0


@dataclass
class PerformanceSnapshot:
    """Agent performance snapshot"""
    agent_id: str
    quality_score: float
    completion_rate: float
    error_rate: float
    avg_response_time: float
    timestamp: datetime


class QualityMetricsCalculator:
    """Calculate quality metrics from validation data"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.baseline_days = 30

    def calculate_quality_trends(self, days: int = 7) -> Dict[str, MetricResult]:
        """Calculate quality trend metrics over specified period"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get quality scores for trend analysis
                cursor.execute("""
                    SELECT quality_score, created_at
                    FROM quality_gate_executions
                    WHERE created_at >= datetime('now', '-{} days')
                    ORDER BY created_at
                """.format(days))

                scores = [(score, datetime.fromisoformat(timestamp))
                         for score, timestamp in cursor.fetchall()]

                if not scores:
                    return {}

                return self._analyze_score_trends(scores)

        except Exception as e:
            logger.error(f"Error calculating quality trends: {e}")
            return {}

    def _analyze_score_trends(self, scores: List[Tuple[float, datetime]]) -> Dict[str, MetricResult]:
        """Analyze score trends and calculate metrics"""
        if len(scores) < 2:
            return {}

        values = [score for score, _ in scores]

        # Calculate basic statistics
        avg_score = statistics.mean(values)
        recent_half = values[len(values)//2:]
        early_half = values[:len(values)//2]

        recent_avg = statistics.mean(recent_half) if recent_half else avg_score
        early_avg = statistics.mean(early_half) if early_half else avg_score

        # Determine trend
        trend_diff = recent_avg - early_avg
        if trend_diff > 0.1:
            trend = 'improving'
        elif trend_diff < -0.1:
            trend = 'declining'
        else:
            trend = 'stable'

        return {
            'overall_quality': MetricResult(
                metric_name='overall_quality',
                value=avg_score,
                trend=trend,
                benchmark=8.0,
                confidence=min(len(scores) / 10.0, 1.0)
            )
        }

    def calculate_agent_performance(self, agent_id: str, days: int = 7) -> Optional[PerformanceSnapshot]:
        """Calculate agent-specific performance metrics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get agent performance data
                cursor.execute("""
                    SELECT quality_score, pm_decision, created_at
                    FROM quality_gate_executions
                    WHERE agent_reviews LIKE ?
                    AND created_at >= datetime('now', '-{} days')
                """.format(days), (f'%{agent_id}%',))

                results = cursor.fetchall()
                if not results:
                    return None

                scores = [score for score, _, _ in results if score is not None]
                decisions = [decision for _, decision, _ in results]

                # Calculate metrics
                avg_quality = statistics.mean(scores) if scores else 0.0
                completion_rate = len([d for d in decisions if d == 'approved']) / len(decisions) if decisions else 0.0
                error_rate = len([d for d in decisions if d == 'rejected']) / len(decisions) if decisions else 0.0

                return PerformanceSnapshot(
                    agent_id=agent_id,
                    quality_score=avg_quality,
                    completion_rate=completion_rate,
                    error_rate=error_rate,
                    avg_response_time=2.5,  # Default - would need actual timing data
                    timestamp=datetime.now()
                )

        except Exception as e:
            logger.error(f"Error calculating agent performance for {agent_id}: {e}")
            return None


class QualityBenchmarkManager:
    """Manage quality benchmarks and targets"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.default_benchmarks = {
            'quality_score': 8.0,
            'completion_rate': 0.95,
            'error_rate': 0.05,
            'response_time': 2.0
        }

    def get_benchmark(self, metric_name: str) -> float:
        """Get benchmark value for metric"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT benchmark_value FROM quality_benchmarks
                    WHERE metric_name = ?
                """, (metric_name,))

                result = cursor.fetchone()
                if result:
                    return result[0]

                return self.default_benchmarks.get(metric_name, 0.0)

        except Exception as e:
            logger.error(f"Error getting benchmark for {metric_name}: {e}")
            return self.default_benchmarks.get(metric_name, 0.0)

    def update_benchmark(self, metric_name: str, value: float, rationale: str = ""):
        """Update benchmark value"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO quality_benchmarks
                    (metric_name, benchmark_value, rationale, updated_at)
                    VALUES (?, ?, ?, ?)
                """, (metric_name, value, rationale, datetime.now().isoformat()))

                conn.commit()
                logger.info(f"Updated benchmark {metric_name} to {value}")

        except Exception as e:
            logger.error(f"Error updating benchmark {metric_name}: {e}")


class TrendAnalyzer:
    """Analyze quality and performance trends"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def analyze_system_trends(self, days: int = 30) -> Dict[str, Any]:
        """Analyze overall system quality trends"""
        try:
            calculator = QualityMetricsCalculator(self.db_path)
            benchmark_mgr = QualityBenchmarkManager(self.db_path)

            # Get quality trends
            quality_trends = calculator.calculate_quality_trends(days)

            # Get benchmarks
            benchmarks = {
                metric: benchmark_mgr.get_benchmark(metric)
                for metric in ['quality_score', 'completion_rate', 'error_rate']
            }

            # Calculate system health score
            health_score = self._calculate_health_score(quality_trends, benchmarks)

            return {
                'quality_trends': quality_trends,
                'benchmarks': benchmarks,
                'health_score': health_score,
                'analysis_date': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error analyzing system trends: {e}")
            return {}

    def _calculate_health_score(self, trends: Dict[str, MetricResult], benchmarks: Dict[str, float]) -> float:
        """Calculate overall system health score"""
        if not trends:
            return 0.0

        scores = []
        for metric_name, metric_result in trends.items():
            benchmark = benchmarks.get(metric_name, 0.0)
            if benchmark > 0:
                score = min(metric_result.value / benchmark, 1.0)
                scores.append(score)

        return statistics.mean(scores) if scores else 0.0