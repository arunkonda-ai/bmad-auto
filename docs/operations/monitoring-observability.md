# BMAD Auto Monitoring and Observability

## Overview

This guide provides comprehensive monitoring and observability implementation for BMAD Auto, covering metrics collection, logging, distributed tracing, alerting, and performance analysis across the autonomous product orchestration system.

## Monitoring Architecture

### Multi-Layer Observability Stack
```
┌─────────────────────────────────────────────────────────────────┐
│                        OBSERVABILITY LAYER                     │
│          (Dashboards, Alerts, Analytics, Reports)              │
├─────────────────────────────────────────────────────────────────┤
│                        ANALYSIS LAYER                          │
│        (Prometheus, Grafana, ELK Stack, Jaeger Tracing)       │
├─────────────────────────────────────────────────────────────────┤
│                       COLLECTION LAYER                         │
│         (Metrics, Logs, Traces, Events, Health Checks)         │
├─────────────────────────────────────────────────────────────────┤
│                      APPLICATION LAYER                         │
│       (BMAD Auto Services, Agents, Workflows, Integrations)    │
└─────────────────────────────────────────────────────────────────┘
```

### Core Monitoring Components
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboards
- **ELK Stack**: Centralized logging and analysis
- **Jaeger**: Distributed tracing for workflow analysis
- **AlertManager**: Intelligent alerting and escalation
- **Custom Metrics**: BMAD-specific performance indicators

## Metrics Collection Implementation

### Prometheus Configuration
```yaml
# monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'bmad-auto-production'
    replica: '1'

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  # BMAD Auto application metrics
  - job_name: 'bmad-auto'
    static_configs:
      - targets: ['bmad-auto:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
    scrape_timeout: 5s

  # Database metrics
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  # Redis metrics
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  # System metrics
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # Kubernetes metrics
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https
```

### Application Metrics Implementation
```python
# src/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Summary, CollectorRegistry, REGISTRY
from functools import wraps
import time
from typing import Dict, Any, Callable

# Custom registry for BMAD Auto metrics
BMAD_REGISTRY = CollectorRegistry()

# Workflow metrics
workflow_requests_total = Counter(
    'bmad_workflow_requests_total',
    'Total number of workflow requests',
    ['phase', 'agent', 'status'],
    registry=BMAD_REGISTRY
)

workflow_duration_seconds = Histogram(
    'bmad_workflow_duration_seconds',
    'Time spent processing workflows',
    ['phase', 'agent'],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 25.0, 60.0, 120.0, 300.0],
    registry=BMAD_REGISTRY
)

active_workflows = Gauge(
    'bmad_active_workflows',
    'Number of currently active workflows',
    ['phase', 'agent'],
    registry=BMAD_REGISTRY
)

# Agent metrics
agent_performance_score = Gauge(
    'bmad_agent_performance_score',
    'Agent performance score (0-1)',
    ['agent_type'],
    registry=BMAD_REGISTRY
)

agent_response_time = Histogram(
    'bmad_agent_response_time_seconds',
    'Agent response time',
    ['agent_type', 'operation'],
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
    registry=BMAD_REGISTRY
)

agent_error_rate = Counter(
    'bmad_agent_errors_total',
    'Total number of agent errors',
    ['agent_type', 'error_type'],
    registry=BMAD_REGISTRY
)

# Quality gate metrics
quality_gate_checks_total = Counter(
    'bmad_quality_gate_checks_total',
    'Total quality gate checks',
    ['gate_type', 'result'],
    registry=BMAD_REGISTRY
)

quality_gate_duration = Histogram(
    'bmad_quality_gate_duration_seconds',
    'Quality gate validation duration',
    ['gate_type'],
    buckets=[1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0],
    registry=BMAD_REGISTRY
)

# Integration metrics
external_api_requests = Counter(
    'bmad_external_api_requests_total',
    'External API requests',
    ['service', 'endpoint', 'status_code'],
    registry=BMAD_REGISTRY
)

external_api_duration = Histogram(
    'bmad_external_api_duration_seconds',
    'External API response time',
    ['service', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
    registry=BMAD_REGISTRY
)

# Business metrics
feature_completion_rate = Gauge(
    'bmad_feature_completion_rate',
    'Feature completion rate percentage',
    ['team', 'project'],
    registry=BMAD_REGISTRY
)

human_intervention_rate = Gauge(
    'bmad_human_intervention_rate',
    'Human intervention rate percentage',
    ['workflow_phase'],
    registry=BMAD_REGISTRY
)

class MetricsCollector:
    """Centralized metrics collection and reporting"""

    def __init__(self):
        self.start_time = time.time()

    def record_workflow_start(self, workflow_id: str, phase: str, agent: str):
        """Record workflow start metrics"""
        active_workflows.labels(phase=phase, agent=agent).inc()
        workflow_requests_total.labels(phase=phase, agent=agent, status='started').inc()

    def record_workflow_completion(self, workflow_id: str, phase: str,
                                 agent: str, duration: float, success: bool):
        """Record workflow completion metrics"""
        active_workflows.labels(phase=phase, agent=agent).dec()
        workflow_duration_seconds.labels(phase=phase, agent=agent).observe(duration)

        status = 'success' if success else 'failure'
        workflow_requests_total.labels(phase=phase, agent=agent, status=status).inc()

    def record_agent_performance(self, agent_type: str, operation: str,
                               response_time: float, success: bool, error_type: str = None):
        """Record agent performance metrics"""
        agent_response_time.labels(agent_type=agent_type, operation=operation).observe(response_time)

        if not success and error_type:
            agent_error_rate.labels(agent_type=agent_type, error_type=error_type).inc()

    def record_quality_gate(self, gate_type: str, duration: float, passed: bool):
        """Record quality gate metrics"""
        result = 'pass' if passed else 'fail'
        quality_gate_checks_total.labels(gate_type=gate_type, result=result).inc()
        quality_gate_duration.labels(gate_type=gate_type).observe(duration)

    def record_external_api_call(self, service: str, endpoint: str,
                                duration: float, status_code: int):
        """Record external API call metrics"""
        external_api_requests.labels(
            service=service,
            endpoint=endpoint,
            status_code=str(status_code)
        ).inc()
        external_api_duration.labels(service=service, endpoint=endpoint).observe(duration)

    def update_business_metrics(self, metrics_data: Dict[str, Any]):
        """Update business-level metrics"""
        if 'completion_rates' in metrics_data:
            for team_project, rate in metrics_data['completion_rates'].items():
                team, project = team_project.split(':')
                feature_completion_rate.labels(team=team, project=project).set(rate)

        if 'intervention_rates' in metrics_data:
            for phase, rate in metrics_data['intervention_rates'].items():
                human_intervention_rate.labels(workflow_phase=phase).set(rate)

# Decorator for automatic metrics collection
def monitor_performance(operation: str, agent_type: str = None):
    """Decorator to automatically monitor function performance"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            error_type = None

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                error_type = type(e).__name__
                raise
            finally:
                duration = time.time() - start_time
                metrics_collector.record_agent_performance(
                    agent_type or 'system',
                    operation,
                    duration,
                    success,
                    error_type
                )

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            error_type = None

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                error_type = type(e).__name__
                raise
            finally:
                duration = time.time() - start_time
                metrics_collector.record_agent_performance(
                    agent_type or 'system',
                    operation,
                    duration,
                    success,
                    error_type
                )

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Global metrics collector instance
metrics_collector = MetricsCollector()
```

## Distributed Tracing Implementation

### Jaeger Tracing Configuration
```python
# src/monitoring/tracing.py
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
import asyncio
from typing import Dict, Any, Optional
from contextvars import ContextVar

# Context variable for trace correlation
trace_context: ContextVar[Dict[str, Any]] = ContextVar('trace_context', default={})

class BMadTracer:
    """BMAD Auto distributed tracing implementation"""

    def __init__(self, service_name: str = "bmad-auto", jaeger_endpoint: str = "http://jaeger:14268/api/traces"):
        self.service_name = service_name

        # Configure tracer provider
        trace.set_tracer_provider(TracerProvider())
        self.tracer = trace.get_tracer(__name__)

        # Configure Jaeger exporter
        jaeger_exporter = JaegerExporter(
            agent_host_name="jaeger",
            agent_port=6831,
            collector_endpoint=jaeger_endpoint,
        )

        # Configure span processor
        span_processor = BatchSpanProcessor(jaeger_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

        # Auto-instrument FastAPI
        FastAPIInstrumentor.instrument()
        SQLAlchemyInstrumentor.instrument()
        RedisInstrumentor.instrument()

    def start_workflow_trace(self, workflow_id: str, phase: str, agent: str) -> trace.Span:
        """Start a new workflow trace"""
        span = self.tracer.start_span(
            name=f"workflow.{phase}",
            attributes={
                "workflow.id": workflow_id,
                "workflow.phase": phase,
                "workflow.agent": agent,
                "service.name": self.service_name
            }
        )

        # Store in context
        trace_context.set({
            "workflow_id": workflow_id,
            "phase": phase,
            "agent": agent,
            "span": span
        })

        return span

    def start_agent_trace(self, agent_type: str, operation: str,
                         workflow_id: str = None) -> trace.Span:
        """Start an agent operation trace"""
        current_context = trace_context.get({})

        span = self.tracer.start_span(
            name=f"agent.{agent_type}.{operation}",
            attributes={
                "agent.type": agent_type,
                "agent.operation": operation,
                "workflow.id": workflow_id or current_context.get("workflow_id"),
                "service.name": self.service_name
            }
        )

        return span

    def start_quality_gate_trace(self, gate_type: str, workflow_id: str = None) -> trace.Span:
        """Start a quality gate trace"""
        current_context = trace_context.get({})

        span = self.tracer.start_span(
            name=f"quality_gate.{gate_type}",
            attributes={
                "quality_gate.type": gate_type,
                "workflow.id": workflow_id or current_context.get("workflow_id"),
                "service.name": self.service_name
            }
        )

        return span

    def start_integration_trace(self, service: str, operation: str,
                              workflow_id: str = None) -> trace.Span:
        """Start an external integration trace"""
        current_context = trace_context.get({})

        span = self.tracer.start_span(
            name=f"integration.{service}.{operation}",
            attributes={
                "integration.service": service,
                "integration.operation": operation,
                "workflow.id": workflow_id or current_context.get("workflow_id"),
                "service.name": self.service_name
            }
        )

        return span

    def add_span_event(self, span: trace.Span, event_name: str, attributes: Dict[str, Any]):
        """Add an event to the current span"""
        span.add_event(event_name, attributes)

    def set_span_status(self, span: trace.Span, success: bool, error_message: str = None):
        """Set span status"""
        if success:
            span.set_status(trace.Status(trace.StatusCode.OK))
        else:
            span.set_status(trace.Status(
                trace.StatusCode.ERROR,
                error_message or "Operation failed"
            ))

# Global tracer instance
bmad_tracer = BMadTracer()

# Tracing decorator
def trace_operation(operation_name: str, service_type: str = "general"):
    """Decorator for automatic operation tracing"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with bmad_tracer.tracer.start_as_current_span(
                f"{service_type}.{operation_name}"
            ) as span:
                try:
                    result = await func(*args, **kwargs)
                    bmad_tracer.set_span_status(span, True)
                    return result
                except Exception as e:
                    bmad_tracer.set_span_status(span, False, str(e))
                    span.set_attribute("error.type", type(e).__name__)
                    span.set_attribute("error.message", str(e))
                    raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with bmad_tracer.tracer.start_as_current_span(
                f"{service_type}.{operation_name}"
            ) as span:
                try:
                    result = func(*args, **kwargs)
                    bmad_tracer.set_span_status(span, True)
                    return result
                except Exception as e:
                    bmad_tracer.set_span_status(span, False, str(e))
                    span.set_attribute("error.type", type(e).__name__)
                    span.set_attribute("error.message", str(e))
                    raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator
```

## Centralized Logging Implementation

### ELK Stack Configuration
```yaml
# monitoring/elasticsearch/elasticsearch.yml
cluster.name: bmad-auto-logging
node.name: elasticsearch-node-1
network.host: 0.0.0.0
http.port: 9200
transport.port: 9300

discovery.type: single-node

# Security
xpack.security.enabled: false

# Performance
indices.memory.index_buffer_size: 20%
thread_pool.write.queue_size: 1000
```

```yaml
# monitoring/logstash/logstash.yml
http.host: "0.0.0.0"
xpack.monitoring.elasticsearch.hosts: ["http://elasticsearch:9200"]

# Pipeline configuration
path.config: /usr/share/logstash/pipeline
```

```yaml
# monitoring/logstash/pipeline/bmad-auto.conf
input {
  beats {
    port => 5044
  }

  http {
    port => 8080
    codec => json
  }
}

filter {
  if [fields][service] == "bmad-auto" {
    # Parse JSON logs
    if [message] =~ /^{.*}$/ {
      json {
        source => "message"
      }
    }

    # Add workflow correlation
    if [workflow_id] {
      mutate {
        add_field => { "correlation_id" => "%{workflow_id}" }
      }
    }

    # Parse log levels
    if [level] {
      mutate {
        uppercase => [ "level" ]
      }
    }

    # Add timestamps
    date {
      match => [ "timestamp", "ISO8601" ]
    }

    # Grok patterns for structured logs
    grok {
      match => {
        "message" => "%{TIMESTAMP_ISO8601:log_timestamp} \[%{WORD:log_level}\] %{DATA:logger_name}: %{GREEDYDATA:log_message}"
      }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "bmad-auto-logs-%{+YYYY.MM.dd}"
  }

  stdout {
    codec => rubydebug
  }
}
```

### Structured Logging Implementation
```python
# src/monitoring/logging_setup.py
import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from contextvars import ContextVar
from pythonjsonlogger import jsonlogger

# Context variable for log correlation
log_context: ContextVar[Dict[str, Any]] = ContextVar('log_context', default={})

class BMadJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for BMAD Auto logging"""

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Add standard fields
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['service'] = 'bmad-auto'
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

        # Add correlation fields from context
        context = log_context.get({})
        if context:
            log_record.update(context)

        # Add trace information if available
        if hasattr(record, 'trace_id'):
            log_record['trace_id'] = record.trace_id
        if hasattr(record, 'span_id'):
            log_record['span_id'] = record.span_id

class BMadLogger:
    """Enhanced logger with workflow correlation and structured logging"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self._setup_logging()

    def _setup_logging(self):
        """Setup structured logging configuration"""
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Create console handler with JSON formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = BMadJsonFormatter(
            fmt='%(timestamp)s %(level)s %(logger)s %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Set level
        self.logger.setLevel(logging.INFO)

    def set_workflow_context(self, workflow_id: str, phase: str = None, agent: str = None):
        """Set workflow context for log correlation"""
        context = {"workflow_id": workflow_id}
        if phase:
            context["workflow_phase"] = phase
        if agent:
            context["agent"] = agent

        log_context.set(context)

    def set_agent_context(self, agent_type: str, operation: str = None):
        """Set agent context for log correlation"""
        context = log_context.get({}).copy()
        context["agent_type"] = agent_type
        if operation:
            context["agent_operation"] = operation

        log_context.set(context)

    def clear_context(self):
        """Clear correlation context"""
        log_context.set({})

    def info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message with context"""
        self.logger.info(message, extra=extra or {})

    def warning(self, message: str, extra: Dict[str, Any] = None):
        """Log warning message with context"""
        self.logger.warning(message, extra=extra or {})

    def error(self, message: str, extra: Dict[str, Any] = None, exc_info: bool = False):
        """Log error message with context"""
        self.logger.error(message, extra=extra or {}, exc_info=exc_info)

    def debug(self, message: str, extra: Dict[str, Any] = None):
        """Log debug message with context"""
        self.logger.debug(message, extra=extra or {})

    def workflow_started(self, workflow_id: str, phase: str, agent: str, context: Dict[str, Any] = None):
        """Log workflow start with structured data"""
        self.set_workflow_context(workflow_id, phase, agent)
        self.info(
            f"Workflow started: {workflow_id}",
            extra={
                "event_type": "workflow_started",
                "workflow_context": context or {}
            }
        )

    def workflow_completed(self, workflow_id: str, success: bool, duration: float,
                          result: Dict[str, Any] = None):
        """Log workflow completion with structured data"""
        self.info(
            f"Workflow {'completed' if success else 'failed'}: {workflow_id}",
            extra={
                "event_type": "workflow_completed",
                "success": success,
                "duration_seconds": duration,
                "result": result or {}
            }
        )

    def agent_action(self, agent_type: str, action: str, result: Dict[str, Any] = None):
        """Log agent action with structured data"""
        self.set_agent_context(agent_type, action)
        self.info(
            f"Agent action: {agent_type}.{action}",
            extra={
                "event_type": "agent_action",
                "action_result": result or {}
            }
        )

    def quality_gate(self, gate_type: str, passed: bool, duration: float,
                    details: Dict[str, Any] = None):
        """Log quality gate validation"""
        self.info(
            f"Quality gate {'passed' if passed else 'failed'}: {gate_type}",
            extra={
                "event_type": "quality_gate",
                "gate_type": gate_type,
                "passed": passed,
                "duration_seconds": duration,
                "details": details or {}
            }
        )

    def external_api_call(self, service: str, endpoint: str, status_code: int,
                         duration: float, request_id: str = None):
        """Log external API call"""
        self.info(
            f"External API call: {service}/{endpoint}",
            extra={
                "event_type": "external_api_call",
                "service": service,
                "endpoint": endpoint,
                "status_code": status_code,
                "duration_seconds": duration,
                "request_id": request_id
            }
        )

def get_logger(name: str) -> BMadLogger:
    """Get a configured BMAD logger instance"""
    return BMadLogger(name)
```

## Grafana Dashboard Configuration

### Workflow Performance Dashboard
```json
{
  "dashboard": {
    "id": null,
    "title": "BMAD Auto - Workflow Performance",
    "tags": ["bmad-auto", "workflows"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Active Workflows",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(bmad_active_workflows)",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 10},
                {"color": "red", "value": 20}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Workflow Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(bmad_workflow_requests_total{status=\"success\"}[5m]) / rate(bmad_workflow_requests_total[5m]) * 100",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "min": 0,
            "max": 100,
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "yellow", "value": 80},
                {"color": "green", "value": 95}
              ]
            }
          }
        }
      },
      {
        "id": 3,
        "title": "Workflow Duration by Phase",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(bmad_workflow_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile",
            "refId": "A"
          },
          {
            "expr": "histogram_quantile(0.50, rate(bmad_workflow_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile",
            "refId": "B"
          }
        ],
        "yAxes": [
          {
            "unit": "s",
            "min": 0
          }
        ]
      },
      {
        "id": 4,
        "title": "Agent Performance",
        "type": "table",
        "targets": [
          {
            "expr": "bmad_agent_performance_score",
            "format": "table",
            "refId": "A"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
```

## Alerting Rules Configuration

### Prometheus Alert Rules
```yaml
# monitoring/prometheus/rules/bmad-auto-alerts.yml
groups:
  - name: bmad-auto-critical
    rules:
      - alert: WorkflowHighFailureRate
        expr: rate(bmad_workflow_requests_total{status="failure"}[5m]) / rate(bmad_workflow_requests_total[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
          service: bmad-auto
        annotations:
          summary: "High workflow failure rate detected"
          description: "Workflow failure rate is {{ $value | humanizePercentage }} over the last 5 minutes"

      - alert: QualityGateHighFailureRate
        expr: rate(bmad_quality_gate_checks_total{result="fail"}[5m]) / rate(bmad_quality_gate_checks_total[5m]) > 0.2
        for: 2m
        labels:
          severity: critical
          service: bmad-auto
        annotations:
          summary: "High quality gate failure rate"
          description: "Quality gate failure rate is {{ $value | humanizePercentage }} for gate type {{ $labels.gate_type }}"

      - alert: AgentHighErrorRate
        expr: rate(bmad_agent_errors_total[5m]) > 5
        for: 2m
        labels:
          severity: critical
          service: bmad-auto
        annotations:
          summary: "High agent error rate"
          description: "Agent {{ $labels.agent_type }} error rate is {{ $value }} errors per second"

  - name: bmad-auto-warning
    rules:
      - alert: WorkflowSlowProcessing
        expr: histogram_quantile(0.95, rate(bmad_workflow_duration_seconds_bucket[5m])) > 300
        for: 5m
        labels:
          severity: warning
          service: bmad-auto
        annotations:
          summary: "Slow workflow processing detected"
          description: "95th percentile workflow duration is {{ $value }}s for phase {{ $labels.phase }}"

      - alert: ExternalAPIHighLatency
        expr: histogram_quantile(0.95, rate(bmad_external_api_duration_seconds_bucket[5m])) > 10
        for: 3m
        labels:
          severity: warning
          service: bmad-auto
        annotations:
          summary: "High external API latency"
          description: "95th percentile API latency for {{ $labels.service }} is {{ $value }}s"

      - alert: HumanInterventionRateHigh
        expr: bmad_human_intervention_rate > 50
        for: 5m
        labels:
          severity: warning
          service: bmad-auto
        annotations:
          summary: "High human intervention rate"
          description: "Human intervention rate for {{ $labels.workflow_phase }} is {{ $value }}%"
```

### AlertManager Configuration
```yaml
# monitoring/alertmanager/alertmanager.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@bmad-auto.com'

route:
  group_by: ['alertname', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
  routes:
    - match:
        severity: critical
      receiver: 'critical-alerts'
      group_wait: 0s
      repeat_interval: 5m
    - match:
        severity: warning
      receiver: 'warning-alerts'

receivers:
  - name: 'web.hook'
    webhook_configs:
      - url: 'http://webhook-handler:5000/alerts'

  - name: 'critical-alerts'
    email_configs:
      - to: 'oncall@bmad-auto.com'
        subject: 'CRITICAL: BMAD Auto Alert'
        body: |
          Alert: {{ .GroupLabels.alertname }}
          Severity: {{ .CommonLabels.severity }}
          Description: {{ range .Alerts }}{{ .Annotations.description }}{{ end }}

    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        channel: '#alerts'
        title: 'CRITICAL: BMAD Auto Alert'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'warning-alerts'
    email_configs:
      - to: 'team@bmad-auto.com'
        subject: 'WARNING: BMAD Auto Alert'
        body: |
          Alert: {{ .GroupLabels.alertname }}
          Severity: {{ .CommonLabels.severity }}
          Description: {{ range .Alerts }}{{ .Annotations.description }}{{ end }}
```

---

*This monitoring and observability implementation provides comprehensive visibility into BMAD Auto operations with real-time metrics, distributed tracing, centralized logging, and intelligent alerting for maintaining system reliability and performance.*