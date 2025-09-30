"""
T016: Database Migration System
Purpose: Version-controlled schema evolution with rollback capabilities
Supports PostgreSQL and SQLite coordination.db with safe migration execution
File size compliance: <300 lines using modular design
"""

import os
import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

import sys
sys.path.append(str(Path(__file__).parent.parent))
from connection_manager import get_connection_manager


@dataclass
class Migration:
    """Represents a database migration"""
    version: str
    description: str
    up_sql: str
    down_sql: str
    database_type: str  # 'postgresql' or 'sqlite'
    file_path: Path


class MigrationManager:
    """
    Manages database migrations with version control and rollback capabilities
    Supports both PostgreSQL and SQLite coordination.db
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.migrations_dir = Path(__file__).parent
        self.connection_manager = get_connection_manager()

    def discover_migrations(self, database_type: str = "postgresql") -> List[Migration]:
        """
        Discover and parse migration files for specified database type
        Migration files follow pattern: {version}_{description}_{db_type}.sql
        """
        migrations = []
        pattern = f"*_{database_type}.sql"

        for migration_file in self.migrations_dir.glob(pattern):
            try:
                migration = self._parse_migration_file(migration_file, database_type)
                migrations.append(migration)
            except Exception as e:
                self.logger.error(f"Failed to parse migration {migration_file}: {e}")

        # Sort by version
        migrations.sort(key=lambda m: m.version)
        return migrations

    def _parse_migration_file(self, file_path: Path, database_type: str) -> Migration:
        """Parse migration file and extract UP/DOWN SQL"""
        content = file_path.read_text()

        # Extract version and description from filename
        # Pattern: v1_0_1_add_user_table_postgresql.sql
        filename = file_path.stem
        parts = filename.split('_')

        if len(parts) < 3:
            raise ValueError(f"Invalid migration filename format: {filename}")

        version = '_'.join(parts[:3])  # v1_0_1
        description = '_'.join(parts[3:-1])  # add_user_table

        # Split content by -- UP and -- DOWN markers
        up_match = re.search(r'-- UP\s*\n(.*?)(?=-- DOWN|\Z)', content, re.DOTALL)
        down_match = re.search(r'-- DOWN\s*\n(.*)', content, re.DOTALL)

        if not up_match:
            raise ValueError(f"Migration {filename} missing -- UP section")

        up_sql = up_match.group(1).strip()
        down_sql = down_match.group(1).strip() if down_match else ""

        return Migration(
            version=version,
            description=description,
            up_sql=up_sql,
            down_sql=down_sql,
            database_type=database_type,
            file_path=file_path
        )

    async def get_applied_migrations(self, database_type: str) -> List[str]:
        """Get list of applied migration versions"""
        if database_type == "postgresql":
            query = "SELECT version FROM schema_version ORDER BY applied_at"
            result = await self.connection_manager.execute_postgresql_query(query)
            return [row['version'] for row in result]

        elif database_type == "sqlite":
            # Create migrations table if it doesn't exist
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS migration_log (
                version TEXT PRIMARY KEY,
                description TEXT,
                applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            await self.connection_manager.execute_sqlite_query(create_table_sql)

            query = "SELECT version FROM migration_log ORDER BY applied_at"
            result = await self.connection_manager.execute_sqlite_query(query)
            return [row['version'] for row in result]

        else:
            raise ValueError(f"Unsupported database type: {database_type}")

    async def apply_migration(self, migration: Migration) -> bool:
        """Apply a single migration with error handling"""
        try:
            self.logger.info(f"Applying migration {migration.version}: {migration.description}")

            if migration.database_type == "postgresql":
                # Execute PostgreSQL migration
                async with self.connection_manager.get_postgresql_connection() as conn:
                    with conn.cursor() as cursor:
                        # Execute migration SQL
                        cursor.execute(migration.up_sql)

                        # Record migration
                        cursor.execute(
                            "INSERT INTO schema_version (version, description) VALUES (%s, %s)",
                            (migration.version, migration.description)
                        )

            elif migration.database_type == "sqlite":
                # Execute SQLite migration
                async with self.connection_manager.get_sqlite_connection() as conn:
                    cursor = conn.cursor()

                    # Execute migration SQL
                    cursor.executescript(migration.up_sql)

                    # Record migration
                    cursor.execute(
                        "INSERT INTO migration_log (version, description) VALUES (?, ?)",
                        (migration.version, migration.description)
                    )
                    conn.commit()

            self.logger.info(f"Migration {migration.version} applied successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to apply migration {migration.version}: {e}")
            return False

    async def rollback_migration(self, migration: Migration) -> bool:
        """Rollback a single migration using DOWN SQL"""
        if not migration.down_sql:
            self.logger.error(f"Migration {migration.version} has no rollback SQL")
            return False

        try:
            self.logger.info(f"Rolling back migration {migration.version}")

            if migration.database_type == "postgresql":
                async with self.connection_manager.get_postgresql_connection() as conn:
                    with conn.cursor() as cursor:
                        # Execute rollback SQL
                        cursor.execute(migration.down_sql)

                        # Remove migration record
                        cursor.execute(
                            "DELETE FROM schema_version WHERE version = %s",
                            (migration.version,)
                        )

            elif migration.database_type == "sqlite":
                async with self.connection_manager.get_sqlite_connection() as conn:
                    cursor = conn.cursor()

                    # Execute rollback SQL
                    cursor.executescript(migration.down_sql)

                    # Remove migration record
                    cursor.execute(
                        "DELETE FROM migration_log WHERE version = ?",
                        (migration.version,)
                    )
                    conn.commit()

            self.logger.info(f"Migration {migration.version} rolled back successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to rollback migration {migration.version}: {e}")
            return False

    async def migrate_to_latest(self, database_type: str = "postgresql") -> Dict[str, Any]:
        """Apply all pending migrations"""
        result = {
            "database_type": database_type,
            "applied_migrations": [],
            "failed_migrations": [],
            "total_migrations": 0,
            "success": True
        }

        try:
            # Get available and applied migrations
            available_migrations = self.discover_migrations(database_type)
            applied_versions = await self.get_applied_migrations(database_type)

            # Filter pending migrations
            pending_migrations = [
                m for m in available_migrations
                if m.version not in applied_versions
            ]

            result["total_migrations"] = len(pending_migrations)

            if not pending_migrations:
                self.logger.info(f"No pending migrations for {database_type}")
                return result

            # Apply pending migrations
            for migration in pending_migrations:
                if await self.apply_migration(migration):
                    result["applied_migrations"].append(migration.version)
                else:
                    result["failed_migrations"].append(migration.version)
                    result["success"] = False
                    break  # Stop on first failure

            self.logger.info(f"Migration complete for {database_type}: {len(result['applied_migrations'])} applied")

        except Exception as e:
            self.logger.error(f"Migration process failed for {database_type}: {e}")
            result["success"] = False
            result["error"] = str(e)

        return result

    async def rollback_to_version(self, target_version: str, database_type: str = "postgresql") -> Dict[str, Any]:
        """Rollback to specific version"""
        result = {
            "database_type": database_type,
            "rolled_back_migrations": [],
            "failed_rollbacks": [],
            "success": True
        }

        try:
            # Get applied migrations
            applied_versions = await self.get_applied_migrations(database_type)
            available_migrations = self.discover_migrations(database_type)

            # Find migrations to rollback (applied versions after target)
            migrations_to_rollback = []
            for version in reversed(applied_versions):
                if version == target_version:
                    break
                # Find migration object
                migration = next((m for m in available_migrations if m.version == version), None)
                if migration:
                    migrations_to_rollback.append(migration)

            # Execute rollbacks in reverse order
            for migration in migrations_to_rollback:
                if await self.rollback_migration(migration):
                    result["rolled_back_migrations"].append(migration.version)
                else:
                    result["failed_rollbacks"].append(migration.version)
                    result["success"] = False
                    break

        except Exception as e:
            self.logger.error(f"Rollback process failed: {e}")
            result["success"] = False
            result["error"] = str(e)

        return result

    async def migration_status(self) -> Dict[str, Any]:
        """Get migration status for both databases"""
        status = {}

        for db_type in ["postgresql", "sqlite"]:
            try:
                available_migrations = self.discover_migrations(db_type)
                applied_versions = await self.get_applied_migrations(db_type)

                pending_migrations = [
                    m.version for m in available_migrations
                    if m.version not in applied_versions
                ]

                status[db_type] = {
                    "total_available": len(available_migrations),
                    "applied_count": len(applied_versions),
                    "pending_count": len(pending_migrations),
                    "latest_applied": applied_versions[-1] if applied_versions else None,
                    "pending_migrations": pending_migrations
                }

            except Exception as e:
                status[db_type] = {"error": str(e)}

        return status


# Convenience functions
async def migrate_all():
    """Migrate both PostgreSQL and SQLite to latest"""
    manager = MigrationManager()

    pg_result = await manager.migrate_to_latest("postgresql")
    sqlite_result = await manager.migrate_to_latest("sqlite")

    return {"postgresql": pg_result, "sqlite": sqlite_result}


if __name__ == "__main__":
    # Test migration system
    import asyncio

    async def test_migrations():
        manager = MigrationManager()

        print("Checking migration status...")
        status = await manager.migration_status()
        print(f"Migration status: {status}")

        print("Testing migration discovery...")
        pg_migrations = manager.discover_migrations("postgresql")
        print(f"Found {len(pg_migrations)} PostgreSQL migrations")

        sqlite_migrations = manager.discover_migrations("sqlite")
        print(f"Found {len(sqlite_migrations)} SQLite migrations")

    asyncio.run(test_migrations())