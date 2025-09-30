"""
Synchronous Wrappers for Agent State Manager.

Provides synchronous interfaces for CLI and testing usage.
For async contexts (FastAPI, LangGraph), use agent_manager.py directly.

All methods use asyncio.run() to call corresponding async methods.
"""

import asyncio
from typing import Dict, Any, Optional, List
from .agent_manager import AgentStateManager, AgentStatus, AgentState


class AgentStateManagerSync:
    """
    Synchronous wrapper interface for AgentStateManager.

    Use this class for CLI operations and testing.
    For async contexts, use AgentStateManager directly.
    """

    def __init__(self, db_connection=None):
        """Initialize with wrapped async manager."""
        self.manager = AgentStateManager(db_connection)

    def register_agent(
        self,
        agent_id: str,
        agent_name: str,
        capabilities: List[str]
    ) -> bool:
        """
        Synchronous wrapper for register_agent.

        Use this method for CLI operations and testing.
        For async contexts, use AgentStateManager.register_agent() directly.
        """
        return asyncio.run(self.manager.register_agent(agent_id, agent_name, capabilities))

    def update_agent_status(
        self,
        agent_id: str,
        status: AgentStatus,
        current_task: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Synchronous wrapper for update_agent_status.

        Use this method for CLI operations and testing.
        For async contexts, use AgentStateManager.update_agent_status() directly.
        """
        return asyncio.run(
            self.manager.update_agent_status(agent_id, status, current_task, error_message)
        )

    def get_agent_status(self, agent_id: str) -> Optional[AgentState]:
        """
        Synchronous wrapper for get_agent_status.

        Use this method for CLI operations and testing.
        For async contexts, use AgentStateManager.get_agent_status() directly.
        """
        return asyncio.run(self.manager.get_agent_status(agent_id))

    def get_all_agent_states(self) -> Dict[str, AgentState]:
        """
        Synchronous wrapper for get_all_agent_states.

        Use this method for CLI operations and testing.
        For async contexts, use AgentStateManager.get_all_agent_states() directly.
        """
        return asyncio.run(self.manager.get_all_agent_states())

    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message_type: str,
        content: Dict[str, Any]
    ) -> bool:
        """
        Synchronous wrapper for send_message.

        Use this method for CLI operations and testing.
        For async contexts, use AgentStateManager.send_message() directly.
        """
        return asyncio.run(
            self.manager.send_message(from_agent, to_agent, message_type, content)
        )

    def get_messages(
        self,
        agent_id: str,
        unread_only: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Synchronous wrapper for get_messages.

        Use this method for CLI operations and testing.
        For async contexts, use AgentStateManager.get_messages() directly.
        """
        return asyncio.run(self.manager.get_messages(agent_id, unread_only))

    def check_agent_health(self, agent_id: str) -> bool:
        """
        Synchronous wrapper for check_agent_health.

        Use this method for CLI operations and testing.
        For async contexts, use AgentStateManager.check_agent_health() directly.
        """
        return asyncio.run(self.manager.check_agent_health(agent_id))