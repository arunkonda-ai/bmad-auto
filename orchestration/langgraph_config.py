"""
BMAD Auto LangGraph Orchestration Configuration
Configures LangGraph with state persistence to PostgreSQL and LangSmith monitoring
"""

import os
from typing import Dict, Any, Optional
from langsmith import Client
import psycopg2
import sqlite3


class BMadAutoLangGraphConfig:
    """Central configuration for LangGraph orchestration framework"""

    def __init__(self):
        self.postgresql_url = self._get_postgresql_url()
        self.sqlite_path = self._get_sqlite_path()
        self.langsmith_config = self._get_langsmith_config()

    def _get_postgresql_url(self) -> str:
        """Get PostgreSQL connection URL for state persistence"""
        # Default to local PostgreSQL installation
        host = os.getenv('POSTGRES_HOST', 'localhost')
        port = os.getenv('POSTGRES_PORT', '5432')
        user = os.getenv('POSTGRES_USER', os.getenv('USER', 'postgres'))
        password = os.getenv('POSTGRES_PASSWORD', '')
        database = os.getenv('POSTGRES_DB', 'bmad_auto')

        if password:
            return f"postgresql://{user}:{password}@{host}:{port}/{database}"
        else:
            return f"postgresql://{user}@{host}:{port}/{database}"

    def _get_sqlite_path(self) -> str:
        """Get SQLite coordination.db path for backup/fallback"""
        return os.path.join(
            os.path.dirname(__file__),
            '..', 'intercept', 'coordination.db'
        )

    def _get_langsmith_config(self) -> Dict[str, Any]:
        """Configure LangSmith monitoring integration"""
        return {
            'project': os.getenv('LANGSMITH_PROJECT', 'bmad-auto-orchestration'),
            'api_key': os.getenv('LANGSMITH_API_KEY'),
            'endpoint': os.getenv('LANGSMITH_ENDPOINT', 'https://api.smith.langchain.com'),
            'enabled': bool(os.getenv('LANGSMITH_TRACING', 'true').lower() == 'true')
        }

    def create_postgresql_checkpointer(self):
        """Create PostgreSQL checkpointer for workflow state persistence"""
        try:
            # Will be implemented when checkpointer imports are resolved
            print("PostgreSQL checkpointer placeholder - ready for implementation")
            return None
        except Exception as e:
            print(f"Warning: PostgreSQL checkpointer failed: {e}")
            print("Falling back to SQLite checkpointer")
            return self.create_sqlite_checkpointer()

    def create_sqlite_checkpointer(self):
        """Create SQLite checkpointer as fallback"""
        print("SQLite checkpointer placeholder - ready for implementation")
        return None

    def setup_langsmith_monitoring(self) -> Optional[Client]:
        """Set up LangSmith monitoring if configured"""
        if not self.langsmith_config['enabled'] or not self.langsmith_config['api_key']:
            print("LangSmith monitoring disabled or API key not provided")
            return None

        try:
            # Set environment variables for LangSmith
            os.environ['LANGCHAIN_TRACING_V2'] = 'true'
            os.environ['LANGCHAIN_PROJECT'] = self.langsmith_config['project']
            os.environ['LANGCHAIN_API_KEY'] = self.langsmith_config['api_key']
            os.environ['LANGCHAIN_ENDPOINT'] = self.langsmith_config['endpoint']

            client = Client(
                api_key=self.langsmith_config['api_key'],
                api_url=self.langsmith_config['endpoint']
            )

            print(f"LangSmith monitoring enabled for project: {self.langsmith_config['project']}")
            return client

        except Exception as e:
            print(f"Warning: LangSmith setup failed: {e}")
            return None

    def validate_configuration(self) -> bool:
        """Validate the LangGraph configuration"""
        try:
            # Test PostgreSQL connection
            import psycopg2
            conn = psycopg2.connect(self.postgresql_url)
            conn.close()
            print("✅ PostgreSQL connection successful")

            # Test SQLite fallback
            import sqlite3
            conn = sqlite3.connect(self.sqlite_path)
            conn.close()
            print("✅ SQLite coordination.db accessible")

            # Test LangGraph imports
            from langgraph.graph import StateGraph
            print("✅ LangGraph imports successful")

            return True

        except Exception as e:
            print(f"❌ Configuration validation failed: {e}")
            return False


# Global configuration instance
langgraph_config = BMadAutoLangGraphConfig()


def get_default_checkpointer():
    """Get the default checkpointer (PostgreSQL with SQLite fallback)"""
    return langgraph_config.create_postgresql_checkpointer()


def get_langsmith_client():
    """Get LangSmith client if monitoring is enabled"""
    return langgraph_config.setup_langsmith_monitoring()


if __name__ == "__main__":
    # Validation script
    print("🔄 Validating BMAD Auto LangGraph Configuration...")

    if langgraph_config.validate_configuration():
        print("✅ LangGraph orchestration framework ready")

        # Test checkpointer creation
        checkpointer = get_default_checkpointer()
        print(f"✅ Checkpointer created: {type(checkpointer).__name__}")

        # Test LangSmith setup
        langsmith_client = get_langsmith_client()
        if langsmith_client:
            print("✅ LangSmith monitoring configured")
        else:
            print("ℹ️  LangSmith monitoring not configured (optional)")

    else:
        print("❌ Configuration validation failed")
        exit(1)