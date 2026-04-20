"""
Configuration module for AutoGen Interview Platform Workflow

This module manages all configuration settings including API keys,
model selection, and agent parameters.

NOTE: This module now uses the shared configuration from the root directory.
Environment variables should be set in the root .env file, not in the autogen directory.

Usage:
    from config import Config

    # Validate configuration before running
    if not Config.validate_setup():
        exit(1)

    # Get AutoGen-compatible configuration
    config_list = Config.get_config_list()
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path to import shared_config
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared_config import Config as SharedConfig


class Config(SharedConfig):
    """
    AutoGen-specific configuration class that extends the shared configuration.

    This class extends the shared configuration with AutoGen-specific settings
    while maintaining compatibility with the shared .env file.
    """

    # AutoGen-specific settings
    HUMAN_INPUT_MODE = "NEVER"  # Agents operate autonomously
    MAX_RETRIES = 2  # Retry failed API calls

    # Output Settings
    OUTPUT_DIR = str(Path(__file__).parent)
    SAVE_OUTPUTS = True
    CREATE_SUMMARY = True

    @classmethod
    def get_config_list(cls) -> List[Dict[str, Any]]:
        """
        Get LLM configuration list for AutoGen.

        Returns:
            List[Dict[str, Any]]: Configuration list compatible with AutoGen
        """
        config = {
            "model": cls.OPENAI_MODEL,
            "api_key": cls.API_KEY,
            "base_url": cls.API_BASE,
        }

        return [config]

    @classmethod
    def validate_setup(cls) -> bool:
        """
        Validate that all required configurations are set.

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        # Use the parent class validation
        if not cls.validate():
            return False

        if cls.VERBOSE:
            print(f"✓ Configuration loaded: {cls.OPENAI_MODEL}")

        return True

    @classmethod
    def get_summary(cls) -> str:
        """Get a summary of current configuration"""
        return f"""
Configuration Summary:
- Model: {cls.OPENAI_MODEL}
- Temperature: {cls.AGENT_TEMPERATURE}
- Output Directory: {cls.OUTPUT_DIR}
- Verbose Mode: {cls.VERBOSE}
- API Base: {cls.API_BASE}
- Timeout: {cls.AGENT_TIMEOUT}s
- Max Tokens: {cls.AGENT_MAX_TOKENS}
"""


class AgentConfig:
    """Configuration for individual agents"""

    RESEARCH_AGENT = {
        "name": "ResearchAgent",
        "role": "Market Researcher",
    }

    ANALYSIS_AGENT = {
        "name": "AnalysisAgent",
        "role": "Product Analyst",
    }

    BLUEPRINT_AGENT = {
        "name": "BlueprintAgent",
        "role": "Product Designer",
    }

    REVIEWER_AGENT = {
        "name": "ReviewerAgent",
        "role": "Product Reviewer",
    }

    @classmethod
    def get_agent_config(cls, agent_type: str) -> Dict[str, Any]:
        """Get configuration for a specific agent type"""
        agents = {
            "research": cls.RESEARCH_AGENT,
            "analysis": cls.ANALYSIS_AGENT,
            "blueprint": cls.BLUEPRINT_AGENT,
            "reviewer": cls.REVIEWER_AGENT,
        }
        return agents.get(agent_type, {})


class WorkflowConfig:
    """Configuration for workflow parameters"""

    # Workflow phases
    PHASES = [
        "research",
        "analysis",
        "blueprint",
        "review",
    ]

    # Phase descriptions
    PHASE_DESCRIPTIONS = {
        "research": "Market Research & Competitive Analysis",
        "analysis": "Market Gap Analysis & Opportunities",
        "blueprint": "Product Blueprint Creation",
        "review": "Strategic Review & Recommendations",
    }

    # Task descriptions
    TASK_DESCRIPTIONS = {
        "research": "Conduct market analysis for AI-powered interview platforms",
        "analysis": "Identify 3 key market opportunities and gaps",
        "blueprint": "Create product blueprint with features and user flows",
        "review": "Review blueprint and provide strategic recommendations",
    }

    @classmethod
    def get_phase_description(cls, phase: str) -> str:
        """Get description for a specific phase"""
        return cls.PHASE_DESCRIPTIONS.get(phase, "Unknown Phase")

    @classmethod
    def get_task_description(cls, phase: str) -> str:
        """Get task description for a specific phase"""
        return cls.TASK_DESCRIPTIONS.get(phase, "Unknown Task")
