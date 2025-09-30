"""
Agent Extension Loader - Dynamic loading of .bmad-core agents with BMAD Auto enhancements.

This module provides the core infrastructure for loading base .bmad-core agents
and applying YAML extension overlays while maintaining absolute .bmad-core preservation.
"""

import os
import yaml
import hashlib
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentExtension:
    """Agent extension configuration."""
    agent_name: str
    extension_type: str
    base_agent_hash: str
    extension_config: Dict[str, Any]
    spec_kit_enabled: bool
    is_active: bool


class AgentExtensionLoader:
    """
    Dynamic loader for .bmad-core agents with BMAD Auto enhancements.

    Implements extension overlay pattern maintaining zero modifications to .bmad-core.
    """

    def __init__(self, bmad_core_path: str = ".bmad-core",
                 bmad_auto_path: str = ".bmad-auto"):
        self.bmad_core_path = Path(bmad_core_path)
        self.bmad_auto_path = Path(bmad_auto_path)
        self.loaded_extensions: Dict[str, AgentExtension] = {}
        self.integrity_cache: Dict[str, str] = {}

    def load_agent_with_extensions(
        self,
        agent_name: str,
        task_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Load agent with base .bmad-core definition + YAML extensions.

        Args:
            agent_name: Name of agent (pm, dev, architect, qa, ux, analyst)
            task_context: Optional task-specific context for dynamic loading

        Returns:
            Complete agent configuration with extensions applied
        """
        # Load base .bmad-core agent
        base_agent = self._load_base_agent(agent_name)

        # Validate .bmad-core integrity
        if not self._validate_core_integrity(agent_name):
            raise BMadCorePreservationError(
                f"Integrity check failed for .bmad-core agent: {agent_name}"
            )

        # Load extension configuration
        extension = self._load_extension_config(agent_name)

        # Merge base + extension
        enhanced_agent = self._merge_configurations(base_agent, extension, task_context)

        # Cache loaded extension
        self.loaded_extensions[agent_name] = extension

        return enhanced_agent

    def _load_base_agent(self, agent_name: str) -> Dict[str, Any]:
        """Load base .bmad-core agent definition (read-only)."""
        agent_file = self.bmad_core_path / "agents" / f"{agent_name}.md"

        if not agent_file.exists():
            raise AgentLoadError(f"Base agent not found: {agent_file}")

        with open(agent_file, 'r') as f:
            content = f.read()

        return {
            'agent_name': agent_name,
            'base_definition': content,
            'base_path': str(agent_file),
            'loaded_at': datetime.utcnow().isoformat()
        }

    def _load_extension_config(self, agent_name: str) -> AgentExtension:
        """Load YAML extension configuration from .bmad-auto/agents/."""
        extension_file = self.bmad_auto_path / "agents" / f"{agent_name}_extension.yaml"

        if not extension_file.exists():
            # Return minimal extension for agents without custom configs
            return AgentExtension(
                agent_name=agent_name,
                extension_type='basic',
                base_agent_hash=self._compute_agent_hash(agent_name),
                extension_config={},
                spec_kit_enabled=False,
                is_active=True
            )

        with open(extension_file, 'r') as f:
            config = yaml.safe_load(f)

        return AgentExtension(
            agent_name=agent_name,
            extension_type=config.get('extension_type', 'basic'),
            base_agent_hash=config.get('base_agent_hash', ''),
            extension_config=config.get('extension_config', {}),
            spec_kit_enabled=config.get('spec_kit_enabled', False),
            is_active=config.get('is_active', True)
        )

    def _merge_configurations(
        self,
        base_agent: Dict[str, Any],
        extension: AgentExtension,
        task_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Merge base agent + extension overlay + task context."""
        enhanced = {
            **base_agent,
            'extension_type': extension.extension_type,
            'enhanced_capabilities': extension.extension_config.get('capabilities', []),
            'spec_kit_enabled': extension.spec_kit_enabled,
            'bmad_auto_integration': True,
        }

        # Add task-specific context if provided
        if task_context:
            enhanced['task_context'] = task_context

        # Add extension-specific features
        if 'database_integration' in extension.extension_config:
            enhanced['database_features'] = extension.extension_config['database_integration']

        if 'spec_kit_commands' in extension.extension_config:
            enhanced['spec_kit_commands'] = extension.extension_config['spec_kit_commands']

        return enhanced

    def _validate_core_integrity(self, agent_name: str) -> bool:
        """Validate .bmad-core agent file has not been modified."""
        current_hash = self._compute_agent_hash(agent_name)

        # Check against cached hash if available
        if agent_name in self.integrity_cache:
            return current_hash == self.integrity_cache[agent_name]

        # First load - cache the hash
        self.integrity_cache[agent_name] = current_hash
        return True

    def _compute_agent_hash(self, agent_name: str) -> str:
        """Compute SHA-256 hash of base agent file for integrity checking."""
        agent_file = self.bmad_core_path / "agents" / f"{agent_name}.md"

        if not agent_file.exists():
            return ""

        with open(agent_file, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def validate_all_extensions(self) -> Dict[str, bool]:
        """Validate compatibility of all agent extensions."""
        results = {}
        agent_dir = self.bmad_auto_path / "agents"

        if not agent_dir.exists():
            return results

        for ext_file in agent_dir.glob("*_extension.yaml"):
            agent_name = ext_file.stem.replace('_extension', '')
            try:
                extension = self._load_extension_config(agent_name)
                results[agent_name] = self._validate_extension_compatibility(extension)
            except Exception as e:
                results[agent_name] = False

        return results

    def _validate_extension_compatibility(self, extension: AgentExtension) -> bool:
        """Validate extension configuration is compatible with base agent."""
        # Check base agent exists
        agent_file = self.bmad_core_path / "agents" / f"{extension.agent_name}.md"
        if not agent_file.exists():
            return False

        # Validate extension configuration structure
        required_fields = ['capabilities']
        if not all(field in extension.extension_config for field in required_fields):
            return False

        return True

    def get_loaded_extensions(self) -> List[str]:
        """Get list of currently loaded agent extensions."""
        return list(self.loaded_extensions.keys())

    def reload_extension(self, agent_name: str) -> bool:
        """Reload an agent extension (useful for development/testing)."""
        try:
            if agent_name in self.loaded_extensions:
                del self.loaded_extensions[agent_name]

            # Clear integrity cache to force re-validation
            if agent_name in self.integrity_cache:
                del self.integrity_cache[agent_name]

            # Reload with fresh configuration
            self.load_agent_with_extensions(agent_name)
            return True
        except Exception:
            return False


class BMadCorePreservationError(Exception):
    """Raised when .bmad-core integrity is threatened."""
    pass


class AgentLoadError(Exception):
    """Raised when agent loading fails."""
    pass