# BMAD Auto Troubleshooting Guide

## Overview

This PM-centric troubleshooting guide provides systematic approaches to diagnosing and resolving issues within BMAD Auto's 10-agent orchestration system, covering PM coordination failures, command simulation issues, AG UI collaboration problems, and autonomous recovery procedures with human escalation patterns.

## System Health Diagnostics

### Health Check Procedures

#### PM-Centric System Status Check
```bash
#!/bin/bash
# scripts/pm-health-check.sh

echo "🔍 PM-Centric BMAD Auto Health Check"
echo "===================================="

# Check PM Integration Hub
echo "🎯 PM Integration Hub Status:"
curl -s http://pm-hub:8091/health/pm-coordination | jq '.' || echo "❌ PM Hub unreachable"

echo -e "\n🤖 10-Agent Ecosystem Status:"
curl -s http://agents:8092/health/agents | jq '.' || echo "❌ Agent ecosystem unreachable"

echo -e "\n👥 AG UI Collaboration Status:"
curl -s http://ag-ui:3001/health/collaboration | jq '.' || echo "❌ AG UI unreachable"

echo -e "\n📊 PM Context Database Status:"
curl -s http://pm-context-db-exporter:9187/health | jq '.' || echo "❌ PM Context DB check failed"

echo -e "\n📋 Command Simulation Database Status:"
curl -s http://command-db-exporter:9188/health | jq '.' || echo "❌ Command DB check failed"

echo -e "\n🗄️ PM Redis Cache Status:"
curl -s http://redis-exporter:9121/health | jq '.' || echo "❌ PM Redis check failed"

echo -e "\n📈 PM Coordination Metrics:"
curl -s http://pm-hub:8091/metrics/pm-coordination | head -10 || echo "❌ PM metrics unreachable"

echo -e "\n🐳 PM Service Container Status:"
docker ps --filter "name=pm-hub\|agents\|ag-ui" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo -e "\n📝 PM Coordination Logs:"
docker logs pm-hub --tail 5 --timestamps
docker logs agents --tail 5 --timestamps
docker logs ag-ui --tail 5 --timestamps

echo -e "\n🔄 PM Batch Processing Status:"
curl -s http://pm-hub:8091/metrics/batch-processing | jq '.pm_batch_processing_duration' || echo "❌ Batch processing metrics unavailable"

echo -e "\n🎭 Command Simulation Status:"
curl -s http://pm-hub:8091/health/command-simulation | jq '.' || echo "❌ Command simulation check failed"

echo -e "\n🧱 .bmad-core Integrity:"
if [ -d "/.bmad-core" ]; then
    echo "✅ .bmad-core directory preserved"
    ls -la /.bmad-core/ | head -3
else
    echo "❌ .bmad-core directory missing"
fi
```

#### PM Database Context Diagnostic
```python
# scripts/pm_db_diagnostic.py
import asyncio
import asyncpg
import time
from typing import Dict, Any
import numpy as np

async def diagnose_pm_database_context(pm_context_db_url: str, command_db_url: str) -> Dict[str, Any]:
    """PM-centric database diagnostics for context and command storage"""
    diagnostic_results = {
        "pm_context_db": {
            "connection_test": False,
            "context_distribution_health": None,
            "agent_learning_storage": None,
            "vector_search_performance": None,
            "errors": []
        },
        "command_simulation_db": {
            "connection_test": False,
            "command_log_health": None,
            "simulation_audit_trail": None,
            "errors": []
        }
    }

    # Test PM Context Database
    try:
        pm_conn = await asyncpg.connect(pm_context_db_url)
        diagnostic_results["pm_context_db"]["connection_test"] = True

        # Test PM context distribution health
        context_stats = await pm_conn.fetchrow("""
            SELECT
                COUNT(*) as total_contexts,
                COUNT(DISTINCT agent_id) as agents_with_context,
                AVG(EXTRACT(EPOCH FROM (NOW() - created_at))) as avg_age_seconds
            FROM pm_agent_contexts
            WHERE created_at > NOW() - INTERVAL '1 hour'
        """)
        diagnostic_results["pm_context_db"]["context_distribution_health"] = dict(context_stats)

        # Test agent learning storage
        learning_stats = await pm_conn.fetchrow("""
            SELECT
                COUNT(*) as total_learning_entries,
                COUNT(DISTINCT agent_id) as learning_agents,
                AVG(confidence_score) as avg_confidence
            FROM agent_learning_entries
            WHERE created_at > NOW() - INTERVAL '24 hours'
        """)
        diagnostic_results["pm_context_db"]["agent_learning_storage"] = dict(learning_stats)

        # Test vector search performance
        if learning_stats['total_learning_entries'] > 0:
            start_time = time.time()
            await pm_conn.execute("""
                SELECT agent_id, context_vector <-> '[0.1,0.2,0.3]'::vector as distance
                FROM agent_learning_entries
                ORDER BY distance
                LIMIT 5
            """)
            diagnostic_results["pm_context_db"]["vector_search_performance"] = time.time() - start_time

        await pm_conn.close()

    except Exception as e:
        diagnostic_results["pm_context_db"]["errors"].append(str(e))

    # Test Command Simulation Database
    try:
        cmd_conn = await asyncpg.connect(command_db_url)
        diagnostic_results["command_simulation_db"]["connection_test"] = True

        # Test command logging health
        command_stats = await cmd_conn.fetchrow("""
            SELECT
                COUNT(*) as total_commands,
                COUNT(CASE WHEN success = true THEN 1 END) as successful_commands,
                COUNT(DISTINCT service) as services_coordinated,
                AVG(execution_time_ms) as avg_execution_time
            FROM pm_external_commands
            WHERE created_at > NOW() - INTERVAL '1 hour'
        """)
        diagnostic_results["command_simulation_db"]["command_log_health"] = dict(command_stats)

        # Test simulation audit trail
        integration_health = await cmd_conn.fetch("""
            SELECT
                service,
                method,
                COUNT(*) as usage_count,
                AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as success_rate
            FROM pm_external_commands
            WHERE created_at > NOW() - INTERVAL '24 hours'
            GROUP BY service, method
        """)
        diagnostic_results["command_simulation_db"]["simulation_audit_trail"] = [dict(row) for row in integration_health]

        await cmd_conn.close()

    except Exception as e:
        diagnostic_results["command_simulation_db"]["errors"].append(str(e))

        # Check active connections
        result = await conn.fetchval(
            "SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"
        )
        diagnostic_results["active_connections"] = result

        # Check table status
        tables = await conn.fetch("""
            SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del
            FROM pg_stat_user_tables
            WHERE schemaname = 'public'
        """)

        for table in tables:
            diagnostic_results["table_status"][table["tablename"]] = {
                "inserts": table["n_tup_ins"],
                "updates": table["n_tup_upd"],
                "deletes": table["n_tup_del"]
            }

        # Check index usage
        indexes = await conn.fetch("""
            SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
            FROM pg_stat_user_indexes
            WHERE schemaname = 'public'
        """)

        for index in indexes:
            diagnostic_results["index_health"][index["indexrelname"]] = {
                "scans": index["idx_scan"],
                "tuples_read": index["idx_tup_read"],
                "tuples_fetched": index["idx_tup_fetch"]
            }

        await conn.close()

    except Exception as e:
        diagnostic_results["errors"].append(str(e))

    return diagnostic_results

if __name__ == "__main__":
    import sys
    database_url = sys.argv[1] if len(sys.argv) > 1 else "postgresql://localhost/bmadauto"
    result = asyncio.run(diagnose_database_connection(database_url))
    print(json.dumps(result, indent=2))
```

## PM-Centric Common Issues and Solutions

### PM Coordination Failures

#### Problem: PM Batch Processing Deadlocks
**Symptoms:**
- PM coordination requests stuck in pending status
- Agent coordination effectiveness dropping below 0.7
- PM batch processing duration exceeding 300 seconds
- Multiple agents waiting for PM context distribution

**PM Coordination Diagnostic Steps:**
```python
# Check PM coordination state
async def diagnose_pm_coordination_deadlocks():
    # Check PM coordination queue
    pending_coordinations = await pm_context_db.fetch("""
        SELECT coordination_id, coordination_type, target_agents, created_at
        FROM pm_task_coordination
        WHERE task_status = 'coordinating'
        AND created_at < NOW() - INTERVAL '5 minutes'
    """)

    for coordination in pending_coordinations:
        print(f"Stuck PM coordination: {coordination['coordination_id']}")
        print(f"Type: {coordination['coordination_type']}")
        print(f"Target agents: {coordination['target_agents']}")
        print(f"Created: {coordination['created_at']}")

    # Check PM batch processing status
    batch_status = await redis.hgetall("pm_batch_processing_state")
    print("PM Batch Status:", batch_status)

    # Check agent context sync status
    agent_sync_status = await pm_context_db.fetch("""
        SELECT agent_id,
               MAX(created_at) as last_context_sync,
               COUNT(*) as pending_contexts
        FROM pm_agent_contexts
        WHERE expires_at > NOW() OR expires_at IS NULL
        GROUP BY agent_id
    """)
    print("Agent Context Sync Status:", [dict(row) for row in agent_sync_status])
```

**PM Coordination Recovery Solutions:**

1. **PM Batch Processing Reset**
   ```python
   # Solution: Reset PM coordination state
   await redis.delete("pm_batch_processing_state")
   await redis.delete("pm_coordination_locks:*")
   await restart_pm_integration_hub()
   ```

2. **Context Distribution Cleanup**
   ```sql
   -- Clear expired contexts causing deadlocks
   DELETE FROM pm_agent_contexts
   WHERE expires_at < NOW()
   OR (created_at < NOW() - INTERVAL '10 minutes' AND expires_at IS NULL);

   -- Reset stuck coordination tasks
   UPDATE pm_task_coordination
   SET task_status = 'pending', updated_at = NOW()
   WHERE task_status = 'coordinating'
   AND updated_at < NOW() - INTERVAL '5 minutes';
   ```

3. **PM Integration Hub Recovery**
   ```bash
   # Restart PM coordination services
   kubectl rollout restart deployment/pm-hub -n bmad-auto
   kubectl wait --for=condition=ready pod -l app=pm-hub -n bmad-auto --timeout=120s

   # Verify PM coordination health
   curl -f http://pm-hub:8091/health/pm-coordination
   ```

#### Problem: 10-Agent Ecosystem Coordination Failures
**Symptoms:**
- Agents not receiving PM context distribution
- Agent independence boundary violations increasing
- Cross-agent context passing failures
- Agent-PM coordination latency exceeding 10 seconds

**10-Agent Ecosystem Diagnostic Procedure:**
```python
# bmad-auto/diagnostics/agent_ecosystem_diagnostics.py
async def diagnose_agent_ecosystem_coordination():
    """Diagnose 10-agent ecosystem coordination issues"""
    agents = ["mary", "john", "james", "quinn", "sally", "alex", "po", "sm", "bmad_orchestrator", "bmad_master"]

    ecosystem_results = {
        "pm_coordination_health": {},
        "agent_ecosystem_status": {},
        "context_distribution_effectiveness": {},
        "learning_storage_health": {}
    }

    for agent_id in agents:
        try:
            # Test PM-agent coordination
            start_time = time.time()
            pm_coordination_test = await test_pm_agent_coordination(agent_id)
            coordination_latency = time.time() - start_time

            # Test context distribution
            context_sync_status = await test_agent_context_sync(agent_id)

            # Test learning storage
            learning_status = await test_agent_learning_storage(agent_id)

            ecosystem_results["agent_ecosystem_status"][agent_id] = {
                "pm_coordination_responsive": pm_coordination_test.get("success", False),
                "coordination_latency_seconds": coordination_latency,
                "context_sync_healthy": context_sync_status.get("healthy", False),
                "learning_storage_accessible": learning_status.get("accessible", False),
                "independence_boundary_violations": await get_boundary_violations(agent_id)
            }

        except Exception as e:
            ecosystem_results["agent_ecosystem_status"][agent_id] = {
                "error": str(e),
                "ecosystem_position": get_agent_hierarchy_position(agent_id)
            }

    return ecosystem_results

async def test_pm_agent_coordination(agent_id: str) -> Dict[str, Any]:
    """Test PM coordination with specific agent"""
    coordination_message = {
        "type": "coordination_test",
        "pm_coordination_id": f"test_{int(time.time())}",
        "agent_id": agent_id,
        "test_context": {"test_key": "test_value"}
    }

    # Test through PM hub
    return await pm_hub.coordinate_agent_test(agent_id, coordination_message)

async def send_ping_to_agent(agent: AgentType) -> Dict[str, Any]:
    """Send ping message to agent"""
    message = {
        "type": "ping",
        "timestamp": time.time(),
        "sender": "diagnostic"
    }

    # Implementation depends on agent communication method
    return await agent_communicator.send_message(agent, message)
```

**Solutions:**

1. **Network Connectivity Issues**
   ```bash
   # Check network connectivity between services
   kubectl exec -it bmad-auto-pod -- nslookup redis-service
   kubectl exec -it bmad-auto-pod -- telnet database-service 5432
   ```

2. **Agent Process Issues**
   ```bash
   # Restart agent processes
   docker restart bmad-auto-agents
   kubectl rollout restart deployment/bmad-auto-agents
   ```

3. **Message Queue Issues**
   ```python
   # Clear stuck messages
   await redis.flushdb()  # Use with caution
   await redis.delete("agent_message_queue:*")
   ```

### PM Quality Orchestration Failures

#### Problem: PM Quality Gate Coordination Issues
**Symptoms:**
- PM selecting wrong agents for quality validation
- Quality gate coordination duration exceeding 300 seconds
- PM quality decision accuracy below 0.8
- Human approval requests timing out in AG UI

**PM Quality Orchestration Diagnostic Steps:**
```python
# Check PM quality orchestration health
async def diagnose_pm_quality_orchestration():
    # Check PM quality gate coordination
    pm_quality_stats = await pm_context_db.fetch("""
        SELECT
            gate_type,
            selected_agents,
            pm_decision,
            COUNT(*) as coordination_count,
            AVG(EXTRACT(EPOCH FROM (approved_at - created_at))) as avg_coordination_time
        FROM pm_quality_gates
        WHERE created_at > NOW() - INTERVAL '2 hours'
        GROUP BY gate_type, selected_agents, pm_decision
    """)

    print("PM Quality Coordination Stats:")
    for stat in pm_quality_stats:
        print(f"Gate: {stat['gate_type']}")
        print(f"Selected agents: {stat['selected_agents']}")
        print(f"PM decision: {stat['pm_decision']}")
        print(f"Avg coordination time: {stat['avg_coordination_time']:.2f}s")

    # Check AG UI human approval patterns
    human_approval_stats = await command_db.fetch("""
        SELECT
            interaction_type,
            AVG(response_time_seconds) as avg_response_time,
            COUNT(CASE WHEN integration_result->>'approved' = 'true' THEN 1 END) as approvals,
            COUNT(*) as total_requests
        FROM human_collaboration_logs
        WHERE created_at > NOW() - INTERVAL '1 hour'
        GROUP BY interaction_type
    """)

    print("\nHuman Approval Patterns:")
    for stat in human_approval_stats:
        approval_rate = stat['approvals'] / stat['total_requests'] if stat['total_requests'] > 0 else 0
        print(f"Type: {stat['interaction_type']}")
        print(f"Avg response time: {stat['avg_response_time']:.2f}s")
        print(f"Approval rate: {approval_rate:.2%}")

    return pm_quality_stats, human_approval_stats
```

**Common Solutions:**

1. **Validation Criteria Too Strict**
   ```python
   # Adjust quality thresholds
   await update_quality_gate_config("code_coverage", {"minimum_coverage": 80})
   await update_quality_gate_config("performance", {"max_response_time": 2000})
   ```

2. **Test Environment Issues**
   ```bash
   # Reset test environment
   docker-compose -f docker-compose.test.yml down
   docker-compose -f docker-compose.test.yml up -d
   ```

3. **External Service Dependencies**
   ```python
   # Mock external services for testing
   await enable_mock_mode_for_quality_gates()
   ```

### Command Simulation and External Integration Issues

#### Problem: Command Simulation Failures
**Symptoms:**
- External API calls bypassing PM coordination
- Command interception failing for Linear/GitHub APIs
- .bmad-core integrity violations detected
- MCP integration failover loops

**Command Simulation Diagnostic Procedure:**
```python
# Test command simulation and PM coordination
async def test_command_simulation_integration():
    diagnostic_results = {
        "command_simulation_health": {},
        "pm_coordination_effectiveness": {},
        "external_integration_methods": {},
        "bmad_core_integrity": {}
    }

    try:
        # Test Linear integration through PM coordination
        linear_test = await test_pm_linear_coordination()
        diagnostic_results["pm_coordination_effectiveness"]["linear"] = linear_test

        # Test GitHub integration through PM coordination
        github_test = await test_pm_github_coordination()
        diagnostic_results["pm_coordination_effectiveness"]["github"] = github_test

        # Test AG UI collaboration
        agui_test = await test_agui_collaboration_session()
        diagnostic_results["pm_coordination_effectiveness"]["ag_ui"] = agui_test

        # Verify .bmad-core integrity
        bmad_integrity = await verify_bmad_core_integrity()
        diagnostic_results["bmad_core_integrity"] = bmad_integrity

        # Check integration method effectiveness
        integration_methods = await analyze_integration_method_effectiveness()
        diagnostic_results["external_integration_methods"] = integration_methods

        return diagnostic_results

    except Exception as e:
        diagnostic_results["error"] = str(e)
        return diagnostic_results

async def test_pm_linear_coordination():
    """Test Linear integration through PM coordination hub"""
    try:
        # Test MCP integration first
        if await check_linear_mcp_availability():
            mcp_result = await pm_hub.coordinate_external_action(
                action_context={
                    "action": "test_connection",
                    "requesting_agent": "diagnostic"
                },
                target_service="linear",
                integration_method="mcp"
            )
            return {"method": "mcp", "success": True, "result": mcp_result}
        else:
            # Fallback to direct API through PM
            api_result = await pm_hub.coordinate_external_action(
                action_context={
                    "action": "test_connection",
                    "requesting_agent": "diagnostic"
                },
                target_service="linear",
                integration_method="direct_api"
            )
            return {"method": "direct_api", "success": True, "result": api_result}

    except Exception as e:
        return {"success": False, "error": str(e)}

async def verify_bmad_core_integrity():
    """Verify .bmad-core directory integrity and preservation"""
    import os
    import hashlib

    bmad_core_path = "/.bmad-core"
    integrity_results = {
        "directory_exists": os.path.exists(bmad_core_path),
        "agents_preserved": False,
        "tasks_preserved": False,
        "workflows_preserved": False,
        "file_checksums": {}
    }

    if integrity_results["directory_exists"]:
        # Check key directories
        agents_path = os.path.join(bmad_core_path, "agents")
        tasks_path = os.path.join(bmad_core_path, "tasks")
        workflows_path = os.path.join(bmad_core_path, "workflows")

        integrity_results["agents_preserved"] = os.path.exists(agents_path)
        integrity_results["tasks_preserved"] = os.path.exists(tasks_path)
        integrity_results["workflows_preserved"] = os.path.exists(workflows_path)

        # Verify no unauthorized modifications
        if integrity_results["agents_preserved"]:
            agent_files = [f for f in os.listdir(agents_path) if f.endswith('.txt')]
            integrity_results["agent_count"] = len(agent_files)
            integrity_results["bmad_orchestrator_exists"] = "bmad-orchestrator.txt" in agent_files
            integrity_results["bmad_master_exists"] = "bmad-master.txt" in agent_files

    return integrity_results
```

**Common Solutions:**

1. **API Key Issues**
   ```bash
   # Verify API key
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"query": "query { viewer { id } }"}' \
        https://api.linear.app/graphql
   ```

2. **Rate Limiting**
   ```python
   # Implement exponential backoff
   await implement_rate_limiting(service="linear", requests_per_minute=60)
   ```

3. **Webhook Issues**
   ```python
   # Test webhook endpoint
   await test_webhook_endpoint("http://your-domain.com/webhooks/linear")
   ```

## Performance Issues

### High Memory Usage

#### Diagnostic Procedure
```python
# Memory usage analysis
import psutil
import gc

def analyze_memory_usage():
    """Analyze current memory usage"""
    process = psutil.Process()
    memory_info = process.memory_info()

    print(f"RSS Memory: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"VMS Memory: {memory_info.vms / 1024 / 1024:.2f} MB")

    # Python-specific memory analysis
    print(f"Objects in memory: {len(gc.get_objects())}")

    # Check for memory leaks
    import tracemalloc
    tracemalloc.start()

    # Run some operations
    await process_test_workflows()

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

    tracemalloc.stop()
```

**Solutions:**

1. **Implement Memory Optimization**
   ```python
   # Clear workflow context periodically
   async def cleanup_workflow_contexts():
       await workflow_context_cache.cleanup_expired()
       gc.collect()

   # Schedule cleanup
   schedule.every(10).minutes.do(cleanup_workflow_contexts)
   ```

2. **Database Connection Pooling**
   ```python
   # Optimize database connections
   engine = create_async_engine(
       database_url,
       pool_size=10,  # Reduced from 20
       max_overflow=5,  # Reduced from 30
       pool_recycle=3600
   )
   ```

### High CPU Usage

#### Diagnostic Procedure
```bash
# CPU profiling
py-spy top --pid $(pgrep -f "bmad-auto")
py-spy record -o profile.svg --pid $(pgrep -f "bmad-auto") --duration 60
```

**Solutions:**

1. **Optimize Async Operations**
   ```python
   # Implement proper async batching
   async def process_workflows_batch(workflows: List[WorkflowState]):
       semaphore = asyncio.Semaphore(5)  # Limit concurrency

       async def process_single(workflow):
           async with semaphore:
               return await process_workflow(workflow)

       tasks = [process_single(w) for w in workflows]
       return await asyncio.gather(*tasks)
   ```

2. **Cache Frequently Accessed Data**
   ```python
   # Implement intelligent caching
   @lru_cache(maxsize=1000)
   async def get_agent_capabilities(agent_type: AgentType):
       return await load_agent_capabilities(agent_type)
   ```

## Error Recovery Procedures

### Workflow Recovery
```python
# Recover stuck or failed workflows
async def recover_failed_workflows():
    """Recover workflows that are in error states"""

    # Find workflows stuck in error states
    stuck_workflows = await db.fetch("""
        SELECT workflow_id, phase, status, error_count, last_error
        FROM workflow_states
        WHERE status IN ('failed', 'escalated')
        AND updated_at < NOW() - INTERVAL '10 minutes'
        AND error_count < 3
    """)

    for workflow_data in stuck_workflows:
        workflow_id = workflow_data["workflow_id"]

        try:
            # Reset workflow state
            await db.execute("""
                UPDATE workflow_states
                SET status = 'pending',
                    error_count = error_count + 1,
                    retry_attempts = retry_attempts + 1,
                    updated_at = NOW()
                WHERE workflow_id = $1
            """, workflow_id)

            # Clear any locks
            await redis.delete(f"workflow_lock:{workflow_id}")

            # Re-queue workflow
            await workflow_queue.put(workflow_id)

            logger.info(f"Recovered workflow: {workflow_id}")

        except Exception as e:
            logger.error(f"Failed to recover workflow {workflow_id}: {e}")
```

### Database Recovery
```python
# Database consistency check and repair
async def check_database_consistency():
    """Check and repair database consistency issues"""

    checks = {}

    # Check for orphaned records
    orphaned_checkpoints = await db.fetchval("""
        SELECT COUNT(*) FROM workflow_checkpoints wc
        LEFT JOIN workflow_states ws ON wc.workflow_id = ws.workflow_id
        WHERE ws.workflow_id IS NULL
    """)
    checks["orphaned_checkpoints"] = orphaned_checkpoints

    # Check for inconsistent agent assignments
    inconsistent_assignments = await db.fetchval("""
        SELECT COUNT(*) FROM workflow_states
        WHERE current_agent IS NOT NULL
        AND status = 'pending'
    """)
    checks["inconsistent_assignments"] = inconsistent_assignments

    # Repair if necessary
    if orphaned_checkpoints > 0:
        await db.execute("""
            DELETE FROM workflow_checkpoints
            WHERE workflow_id NOT IN (SELECT workflow_id FROM workflow_states)
        """)
        logger.info(f"Cleaned up {orphaned_checkpoints} orphaned checkpoints")

    if inconsistent_assignments > 0:
        await db.execute("""
            UPDATE workflow_states
            SET current_agent = NULL
            WHERE status = 'pending' AND current_agent IS NOT NULL
        """)
        logger.info(f"Fixed {inconsistent_assignments} inconsistent assignments")

    return checks
```

## Monitoring and Alerting

### Custom Alert Scripts
```python
# Custom alerting for BMAD-specific issues
class BMadAlertManager:
    """Custom alert manager for BMAD Auto specific issues"""

    async def check_workflow_health(self):
        """Check workflow processing health"""

        # Check for workflow bottlenecks
        pending_count = await db.fetchval("""
            SELECT COUNT(*) FROM workflow_states
            WHERE status = 'pending'
            AND created_at < NOW() - INTERVAL '5 minutes'
        """)

        if pending_count > 10:
            await self.send_alert(
                severity="warning",
                message=f"High number of pending workflows: {pending_count}",
                recommended_action="Check agent availability and orchestration service"
            )

        # Check for quality gate failures
        recent_failures = await db.fetchval("""
            SELECT COUNT(*) FROM quality_gate_results
            WHERE passed = false
            AND created_at > NOW() - INTERVAL '10 minutes'
        """)

        if recent_failures > 5:
            await self.send_alert(
                severity="critical",
                message=f"High quality gate failure rate: {recent_failures} failures",
                recommended_action="Review quality gate configuration and test environment"
            )

    async def send_alert(self, severity: str, message: str, recommended_action: str):
        """Send alert to configured channels"""
        alert_data = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "service": "bmad-auto",
            "message": message,
            "recommended_action": recommended_action
        }

        # Send to monitoring systems
        await self.send_to_prometheus_alertmanager(alert_data)
        await self.send_to_slack(alert_data)
        await self.send_to_email(alert_data)
```

## Emergency Procedures

### System Shutdown
```bash
#!/bin/bash
# Emergency shutdown procedure

echo "🚨 Emergency BMAD Auto Shutdown"

# Graceful shutdown
echo "Attempting graceful shutdown..."
kubectl scale deployment/bmad-auto --replicas=0 -n bmad-auto

# Wait for pods to terminate
kubectl wait --for=delete pod -l app=bmad-auto -n bmad-auto --timeout=60s

# Force shutdown if necessary
echo "Force stopping remaining processes..."
docker stop $(docker ps -q --filter "name=bmad-auto")

# Backup current state
echo "Backing up current state..."
kubectl create backup bmad-auto-emergency-backup -n bmad-auto

echo "Emergency shutdown complete"
```

### System Recovery
```bash
#!/bin/bash
# Emergency recovery procedure

echo "🔧 BMAD Auto Emergency Recovery"

# Restore from backup
echo "Restoring from latest backup..."
kubectl restore bmad-auto-emergency-backup -n bmad-auto

# Start core services
echo "Starting core services..."
kubectl scale deployment/bmad-auto --replicas=3 -n bmad-auto

# Wait for health checks
echo "Waiting for services to be healthy..."
kubectl wait --for=condition=ready pod -l app=bmad-auto -n bmad-auto --timeout=300s

# Verify system health
echo "Verifying system health..."
curl -f http://bmad-auto-service/health || exit 1

# Run consistency checks
echo "Running consistency checks..."
python scripts/db_consistency_check.py

echo "Recovery complete"
```

## PM-Centric Emergency Recovery Procedures

### PM Coordination Emergency Recovery
```bash
#!/bin/bash
# Emergency PM coordination recovery

echo "🚨 PM Coordination Emergency Recovery"

# Step 1: Stop PM coordination gracefully
echo "Stopping PM coordination..."
kubectl scale deployment/pm-hub --replicas=0 -n bmad-auto

# Step 2: Clear PM coordination state
echo "Clearing PM coordination state..."
kubectl exec -it redis-pod -n bmad-auto -- redis-cli FLUSHDB

# Step 3: Reset PM context database
echo "Resetting PM context distribution..."
kubectl exec -it pm-context-db-pod -n bmad-auto -- psql -c "
DELETE FROM pm_agent_contexts WHERE expires_at < NOW();
UPDATE pm_task_coordination SET task_status = 'pending' WHERE task_status = 'coordinating';
"

# Step 4: Restart PM coordination services
echo "Restarting PM coordination..."
kubectl scale deployment/pm-hub --replicas=2 -n bmad-auto
kubectl wait --for=condition=ready pod -l app=pm-hub -n bmad-auto --timeout=120s

# Step 5: Restart agent ecosystem
echo "Restarting agent ecosystem..."
kubectl rollout restart deployment/agents -n bmad-auto
kubectl wait --for=condition=ready pod -l app=agents -n bmad-auto --timeout=180s

# Step 6: Restart AG UI collaboration
echo "Restarting AG UI collaboration..."
kubectl rollout restart deployment/ag-ui -n bmad-auto
kubectl wait --for=condition=ready pod -l app=ag-ui -n bmad-auto --timeout=60s

# Step 7: Verify PM coordination health
echo "Verifying PM coordination health..."
curl -f http://pm-hub-service:8091/health/pm-coordination || exit 1
curl -f http://agents-service:8092/health/agents || exit 1
curl -f http://ag-ui-service:3001/health/collaboration || exit 1

echo "PM coordination emergency recovery complete"
```

### .bmad-core Integrity Recovery
```bash
#!/bin/bash
# Emergency .bmad-core integrity recovery

echo "🧱 .bmad-core Integrity Recovery"

# Step 1: Verify .bmad-core corruption
if [ ! -d "/.bmad-core" ]; then
    echo "❌ .bmad-core directory missing - restoring from backup"

    # Restore from backup
    kubectl create job bmad-core-restore --image=bmad-backup-restore:latest \
        --restart=Never -- /scripts/restore-bmad-core.sh

    kubectl wait --for=condition=complete job/bmad-core-restore --timeout=300s
fi

# Step 2: Verify agent files
agent_files=("bmad-orchestrator.txt" "bmad-master.txt" "mary.txt" "john.txt" "james.txt" "quinn.txt" "sally.txt" "alex.txt" "po.txt" "sm.txt")
for agent_file in "${agent_files[@]}"; do
    if [ ! -f "/.bmad-core/agents/$agent_file" ]; then
        echo "❌ Missing agent file: $agent_file"
        # Restore specific agent file
        kubectl exec -it backup-pod -- cp "/backup/.bmad-core/agents/$agent_file" "/.bmad-core/agents/"
    fi
done

# Step 3: Set read-only permissions
chmod -R 444 /.bmad-core/
chown -R root:root /.bmad-core/

# Step 4: Restart command simulation layer
echo "Restarting command simulation..."
kubectl rollout restart deployment/pm-hub -n bmad-auto

echo ".bmad-core integrity recovery complete"
```

### AG UI Collaboration Session Recovery
```python
# Emergency AG UI collaboration recovery
async def recover_agui_collaboration_sessions():
    """Recover corrupted AG UI collaboration sessions"""

    # Find stuck collaboration sessions
    stuck_sessions = await command_db.fetch("""
        SELECT collaboration_session_id, interaction_type, pm_analysis
        FROM human_collaboration_logs
        WHERE created_at > NOW() - INTERVAL '30 minutes'
        AND integration_result IS NULL
    """)

    recovery_results = []

    for session in stuck_sessions:
        try:
            session_id = session['collaboration_session_id']

            # Attempt session recovery
            recovery_result = await agui_coordinator.recover_collaboration_session(
                session_id=session_id,
                recovery_mode="graceful_timeout"
            )

            # Log recovery attempt
            await command_db.execute("""
                UPDATE human_collaboration_logs
                SET integration_result = $1,
                    response_time_seconds = $2
                WHERE collaboration_session_id = $3
            """,
            {"recovered": True, "recovery_method": "emergency_timeout"},
            30,  # Default timeout response
            session_id)

            recovery_results.append({
                "session_id": session_id,
                "recovery_status": "success",
                "method": "graceful_timeout"
            })

        except Exception as e:
            recovery_results.append({
                "session_id": session_id,
                "recovery_status": "failed",
                "error": str(e)
            })

    return recovery_results
```

---

*This PM-centric troubleshooting guide provides systematic approaches to diagnosing and resolving issues in BMAD Auto's 10-agent orchestration system, ensuring reliable PM coordination, command simulation integrity, and AG UI human collaboration recovery.*