"""
Capability Registry - Standard capability definitions for BMAD Auto agents.

Extracted from capability_manager.py for BMAD size compliance.
"""

from enum import Enum


class CapabilityType(Enum):
    """Agent capability categories."""
    ORCHESTRATION = "orchestration"
    DEVELOPMENT = "development"
    ARCHITECTURE = "architecture"
    QUALITY_ASSURANCE = "quality_assurance"
    USER_EXPERIENCE = "user_experience"
    ANALYSIS = "analysis"
    RESEARCH = "research"
    TESTING = "testing"
    INTEGRATION = "integration"
    AUTOMATION = "automation"


def get_standard_capabilities() -> dict:
    """Get standard capability definitions for all agents."""
    return {
        # PM capabilities
        'task_decomposition': CapabilityType.ORCHESTRATION,
        'agent_coordination': CapabilityType.ORCHESTRATION,
        'quality_gate_management': CapabilityType.ORCHESTRATION,
        'decision_reasoning': CapabilityType.ORCHESTRATION,

        # Developer capabilities
        'code_implementation': CapabilityType.DEVELOPMENT,
        'debugging': CapabilityType.DEVELOPMENT,
        'refactoring': CapabilityType.DEVELOPMENT,
        'api_development': CapabilityType.DEVELOPMENT,

        # Architect capabilities
        'system_design': CapabilityType.ARCHITECTURE,
        'technical_specification': CapabilityType.ARCHITECTURE,
        'integration_patterns': CapabilityType.ARCHITECTURE,
        'performance_optimization': CapabilityType.ARCHITECTURE,

        # QA capabilities
        'test_automation': CapabilityType.TESTING,
        'quality_validation': CapabilityType.QUALITY_ASSURANCE,
        'performance_testing': CapabilityType.TESTING,
        'security_testing': CapabilityType.TESTING,

        # UX capabilities
        'ui_design': CapabilityType.USER_EXPERIENCE,
        'accessibility_validation': CapabilityType.USER_EXPERIENCE,
        'user_research': CapabilityType.USER_EXPERIENCE,

        # Analyst capabilities
        'market_research': CapabilityType.RESEARCH,
        'competitive_analysis': CapabilityType.ANALYSIS,
        'data_analysis': CapabilityType.ANALYSIS,
    }