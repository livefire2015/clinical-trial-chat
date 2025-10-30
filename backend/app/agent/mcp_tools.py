"""
DEPRECATED: MCP Tool Integration for Pydantic-AI Agent

This module is no longer used. MCP servers are now managed directly by Pydantic AI
through the load_mcp_servers() function and passed as toolsets to the Agent.

See mcp_config.json for MCP server configuration and clinical_agent.py for the
new implementation using Pydantic AI's built-in MCP support.

This approach resolves the anyio.ClosedResourceError that occurred with manual
session management and provides better integration with Pydantic AI's lifecycle.
"""

# Deprecation notice for any code that might still import this
import warnings

warnings.warn(
    "mcp_tools module is deprecated. MCP servers are now loaded via "
    "pydantic_ai.mcp.load_mcp_servers() and passed as toolsets to the Agent. "
    "See clinical_agent.py for the new implementation.",
    DeprecationWarning,
    stacklevel=2
)
