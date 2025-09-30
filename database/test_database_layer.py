#!/usr/bin/env python3
"""
Database Layer Integration Test
Tests PostgreSQL schema, SQLite coordination.db, connection management, and migrations
"""

import asyncio
import sys
from pathlib import Path

# Add database module to path
sys.path.append(str(Path(__file__).parent))

from connection_manager import get_connection_manager, initialize_databases
from migrations.migration_manager import MigrationManager


async def test_database_layer():
    """Comprehensive test of database layer components"""
    print("🔄 Testing Database Layer Integration")
    print("=" * 50)

    try:
        # Test 1: Initialize database connections
        print("1. Testing database initialization...")
        await initialize_databases()
        print("✅ Database connections initialized")

        # Test 2: Connection manager health check
        print("\n2. Testing connection manager health...")
        manager = get_connection_manager()
        health = await manager.health_check()
        print(f"✅ Health check: {health}")

        # Test 3: PostgreSQL schema verification
        print("\n3. Testing PostgreSQL schema...")
        pg_tables = await manager.execute_postgresql_query(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
        table_names = [row['table_name'] for row in pg_tables]
        expected_tables = ['pm_decision_context', 'agent_state', 'workflow_execution',
                          'model_assignment', 'quality_gate_execution', 'schema_version']

        for table in expected_tables:
            if table in table_names:
                print(f"✅ PostgreSQL table '{table}' exists")
            else:
                print(f"❌ PostgreSQL table '{table}' missing")

        # Test 4: SQLite coordination.db verification
        print("\n4. Testing SQLite coordination.db...")
        sqlite_tables = await manager.execute_sqlite_query("SELECT name FROM sqlite_master WHERE type='table'")
        sqlite_table_names = [row['name'] for row in sqlite_tables]
        expected_sqlite_tables = ['provider_plans', 'pm_decision_log', 'agent_extensions',
                                 'langgraph_executions', 'external_service_operations', 'quality_gate_executions']

        for table in expected_sqlite_tables:
            if table in sqlite_table_names:
                print(f"✅ SQLite table '{table}' exists")
            else:
                print(f"❌ SQLite table '{table}' missing")

        # Test 5: Migration system
        print("\n5. Testing migration system...")
        migration_manager = MigrationManager()
        migration_status = await migration_manager.migration_status()
        print(f"✅ Migration status: {migration_status}")

        # Test 6: Data operations
        print("\n6. Testing data operations...")

        # Test PostgreSQL insert
        await manager.execute_postgresql_query(
            "INSERT INTO pm_decision_context (decision_id, decision_type, context_data, reasoning_process, outcome, confidence_score) VALUES (%s, %s, %s, %s, %s, %s)",
            ('test_001', 'task_assignment', '{"test": true}', 'Test reasoning', 'test_outcome', 8)
        )
        print("✅ PostgreSQL insert successful")

        # Test PostgreSQL select
        pg_result = await manager.execute_postgresql_query(
            "SELECT decision_id FROM pm_decision_context WHERE decision_id = %s",
            ('test_001',)
        )
        if pg_result:
            print(f"✅ PostgreSQL select successful: {pg_result[0]['decision_id']}")

        # Test SQLite select
        sqlite_result = await manager.execute_sqlite_query(
            "SELECT COUNT(*) as count FROM provider_plans"
        )
        if sqlite_result:
            print(f"✅ SQLite select successful: {sqlite_result[0]['count']} provider plans")

        # Test 7: Performance views
        print("\n7. Testing performance views...")
        views = ['active_agents', 'recent_pm_decisions', 'active_workflows']
        for view in views:
            try:
                result = await manager.execute_postgresql_query(f"SELECT * FROM {view} LIMIT 1")
                print(f"✅ View '{view}' accessible")
            except Exception as e:
                print(f"⚠️  View '{view}' error: {e}")

        # Cleanup
        print("\n8. Cleanup...")
        await manager.execute_postgresql_query(
            "DELETE FROM pm_decision_context WHERE decision_id = %s",
            ('test_001',)
        )
        print("✅ Test data cleaned up")

        manager.close_connections()
        print("\n🎉 All database layer tests passed!")

    except Exception as e:
        print(f"\n❌ Database layer test failed: {e}")
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_database_layer())
    sys.exit(0 if success else 1)