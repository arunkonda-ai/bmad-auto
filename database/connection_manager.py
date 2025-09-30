"""
T015: Database Connection Management
Purpose: PostgreSQL connection pooling + SQLite coordination.db management
Handles concurrent 10-agent access patterns with production-ready error handling
File size compliance: <300 lines with modular architecture
"""

import sqlite3
import logging
import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor


@dataclass
class ConnectionConfig:
    """Database connection configuration"""
    # PostgreSQL settings
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_database: str = "bmad_auto"
    pg_user: str = "apple"  # Default user
    pg_password: Optional[str] = None
    pg_min_connections: int = 5
    pg_max_connections: int = 20

    # SQLite settings
    sqlite_path: str = ".bmad-auto/intercept/coordination.db"
    sqlite_timeout: float = 30.0
    sqlite_check_same_thread: bool = False


class DatabaseConnectionManager:
    """
    Manages PostgreSQL connection pool and SQLite coordination.db connections
    Supports concurrent 10-agent operations with proper error handling
    """

    def __init__(self, config: Optional[ConnectionConfig] = None):
        self.config = config or ConnectionConfig()
        self._pg_pool: Optional[psycopg2.pool.ThreadedConnectionPool] = None
        self._sqlite_lock = asyncio.Lock()
        self.logger = logging.getLogger(__name__)

    def initialize_postgresql_pool(self) -> None:
        """Initialize PostgreSQL connection pool"""
        try:
            # Build connection string
            conn_params = {
                'host': self.config.pg_host,
                'port': self.config.pg_port,
                'database': self.config.pg_database,
                'user': self.config.pg_user,
            }

            if self.config.pg_password:
                conn_params['password'] = self.config.pg_password

            # Create threaded connection pool for concurrent agent access
            self._pg_pool = psycopg2.pool.ThreadedConnectionPool(
                self.config.pg_min_connections,
                self.config.pg_max_connections,
                **conn_params
            )

            self.logger.info(f"PostgreSQL pool initialized: {self.config.pg_min_connections}-{self.config.pg_max_connections} connections")

        except Exception as e:
            self.logger.error(f"Failed to initialize PostgreSQL pool: {e}")
            raise

    @asynccontextmanager
    async def get_postgresql_connection(self) -> AsyncGenerator[psycopg2.extensions.connection, None]:
        """
        Get PostgreSQL connection from pool with automatic cleanup
        Supports concurrent agent access patterns
        """
        if not self._pg_pool:
            self.initialize_postgresql_pool()

        connection = None
        try:
            # Get connection from pool (thread-safe)
            connection = self._pg_pool.getconn()
            if connection is None:
                raise Exception("No PostgreSQL connections available in pool")

            # Set autocommit for most operations
            connection.autocommit = True

            self.logger.debug("PostgreSQL connection acquired from pool")
            yield connection

        except Exception as e:
            if connection:
                connection.rollback()
            self.logger.error(f"PostgreSQL connection error: {e}")
            raise
        finally:
            if connection:
                # Return connection to pool
                self._pg_pool.putconn(connection)
                self.logger.debug("PostgreSQL connection returned to pool")

    @asynccontextmanager
    async def get_sqlite_connection(self) -> AsyncGenerator[sqlite3.Connection, None]:
        """
        Get SQLite connection to coordination.db with proper locking
        Handles concurrent agent access to coordination data
        """
        async with self._sqlite_lock:  # Serialize SQLite access
            connection = None
            try:
                sqlite_path = Path(self.config.sqlite_path)
                if not sqlite_path.exists():
                    raise FileNotFoundError(f"coordination.db not found at {sqlite_path}")

                connection = sqlite3.connect(
                    str(sqlite_path),
                    timeout=self.config.sqlite_timeout,
                    check_same_thread=self.config.sqlite_check_same_thread
                )

                # Enable row factory for dict-like access
                connection.row_factory = sqlite3.Row

                # Enable WAL mode for better concurrent access
                connection.execute("PRAGMA journal_mode=WAL")
                connection.execute("PRAGMA synchronous=NORMAL")
                connection.execute("PRAGMA cache_size=10000")

                self.logger.debug("SQLite connection acquired")
                yield connection

            except Exception as e:
                if connection:
                    connection.rollback()
                self.logger.error(f"SQLite connection error: {e}")
                raise
            finally:
                if connection:
                    connection.close()
                    self.logger.debug("SQLite connection closed")

    async def execute_postgresql_query(self, query: str, params: Optional[tuple] = None) -> list:
        """Execute PostgreSQL query with connection management"""
        async with self.get_postgresql_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    return cursor.fetchall()
                return []

    async def execute_sqlite_query(self, query: str, params: Optional[tuple] = None) -> list:
        """Execute SQLite query with connection management"""
        async with self.get_sqlite_connection() as conn:
            cursor = conn.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                return []

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on both database connections
        Returns status for monitoring and alerting
        """
        health_status = {
            "postgresql": {"status": "unknown", "pool_size": 0, "error": None},
            "sqlite": {"status": "unknown", "path": self.config.sqlite_path, "error": None}
        }

        # Check PostgreSQL
        try:
            await self.execute_postgresql_query("SELECT 1 as test")
            if self._pg_pool:
                # Get pool statistics (approximate)
                health_status["postgresql"]["pool_size"] = self._pg_pool.minconn
            health_status["postgresql"]["status"] = "healthy"
        except Exception as e:
            health_status["postgresql"]["status"] = "error"
            health_status["postgresql"]["error"] = str(e)

        # Check SQLite
        try:
            await self.execute_sqlite_query("SELECT 1 as test")
            health_status["sqlite"]["status"] = "healthy"
        except Exception as e:
            health_status["sqlite"]["status"] = "error"
            health_status["sqlite"]["error"] = str(e)

        return health_status

    def close_connections(self) -> None:
        """Close all database connections and clean up resources"""
        try:
            if self._pg_pool:
                self._pg_pool.closeall()
                self.logger.info("PostgreSQL connection pool closed")
        except Exception as e:
            self.logger.error(f"Error closing PostgreSQL pool: {e}")

        self.logger.info("Database connections closed")


# Global connection manager instance
_connection_manager: Optional[DatabaseConnectionManager] = None


def get_connection_manager() -> DatabaseConnectionManager:
    """Get global connection manager instance (singleton pattern)"""
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = DatabaseConnectionManager()
    return _connection_manager


async def initialize_databases() -> None:
    """Initialize both PostgreSQL and SQLite connections"""
    manager = get_connection_manager()
    manager.initialize_postgresql_pool()

    # Verify both databases are accessible
    health = await manager.health_check()

    if health["postgresql"]["status"] != "healthy":
        raise Exception(f"PostgreSQL not healthy: {health['postgresql']['error']}")

    if health["sqlite"]["status"] != "healthy":
        raise Exception(f"SQLite not healthy: {health['sqlite']['error']}")

    logging.info("Database connections initialized successfully")


# Convenience functions for common operations
async def get_pg_connection():
    """Convenience function to get PostgreSQL connection"""
    manager = get_connection_manager()
    return manager.get_postgresql_connection()


async def get_sqlite_connection():
    """Convenience function to get SQLite connection"""
    manager = get_connection_manager()
    return manager.get_sqlite_connection()


if __name__ == "__main__":
    # Test the connection manager
    import asyncio

    async def test_connections():
        await initialize_databases()
        manager = get_connection_manager()

        print("Testing PostgreSQL connection...")
        result = await manager.execute_postgresql_query("SELECT current_database()")
        print(f"PostgreSQL test: {result}")

        print("Testing SQLite connection...")
        result = await manager.execute_sqlite_query("SELECT COUNT(*) as count FROM provider_plans")
        print(f"SQLite test: {result}")

        print("Health check...")
        health = await manager.health_check()
        print(f"Health status: {health}")

        manager.close_connections()

    asyncio.run(test_connections())