"""
Toolset wrapper that automatically truncates large tool results.

This module provides a WrapperToolset subclass that intercepts tool calls
and intelligently truncates results to stay within token limits while
preserving full results for UI display.
"""

from dataclasses import dataclass
from typing import Any, Dict
from pydantic_ai import RunContext, WrapperToolset, ToolsetTool
from .result_truncation import smart_truncate_result, create_truncated_response


@dataclass
class TruncatingToolset(WrapperToolset):
    """
    Toolset wrapper that truncates large tool results.

    This wrapper intercepts all tool calls and applies smart truncation
    to results that exceed token limits. The truncated content is sent
    to the AI model, while full results are preserved in metadata for
    UI display.

    Example:
        >>> from pydantic_ai.toolsets.fastmcp import FastMCPToolset
        >>> from app.agent.truncating_toolset import TruncatingToolset
        >>>
        >>> # Load MCP servers
        >>> mcp_toolset = FastMCPToolset.from_config("mcp_config.json")
        >>>
        >>> # Wrap with truncation
        >>> truncating_toolset = TruncatingToolset(
        ...     wrapped=mcp_toolset,
        ...     max_tokens=2000,
        ...     max_array_items=10
        ... )
        >>>
        >>> # Use in agent
        >>> agent = Agent(model, toolsets=[truncating_toolset])
    """

    max_tokens: int = 2000
    max_array_items: int = 10
    enabled_tools: set[str] | None = None

    async def call_tool(
        self,
        name: str,
        tool_args: Dict[str, Any],
        ctx: RunContext,
        tool: ToolsetTool
    ) -> Any:
        """
        Intercept tool calls and truncate large results.

        Args:
            name: Tool name
            tool_args: Validated tool arguments
            ctx: Run context
            tool: Tool definition

        Returns:
            Truncated result if result is large, otherwise original result
        """
        # Call the underlying tool
        result = await super().call_tool(name, tool_args, ctx, tool)

        # Check if truncation should be applied to this tool
        if self.enabled_tools is not None and name not in self.enabled_tools:
            return result

        # Apply smart truncation
        truncation_result = smart_truncate_result(
            result,
            max_tokens=self.max_tokens,
            max_array_items=self.max_array_items
        )

        # If no truncation occurred, return original result
        if not truncation_result.was_truncated:
            return result

        # Return truncated content as string
        # The AI model will receive the truncated version
        # Full results are available in the TruncationResult object if needed
        return truncation_result.model_content


@dataclass
class VerboseTruncatingToolset(TruncatingToolset):
    """
    Truncating toolset that includes truncation metadata in responses.

    This variant returns a structured response with both truncated content
    and metadata about the truncation, including the full result.

    This is useful when you want to preserve full results in the response
    for downstream processing or UI display.

    Example:
        >>> truncating_toolset = VerboseTruncatingToolset(
        ...     mcp_toolset,
        ...     max_tokens=2000
        ... )
        >>>
        >>> # Results will include metadata:
        >>> # {
        >>> #     "content": "<truncated content>",
        >>> #     "metadata": {
        >>> #         "tool_name": "search_clinical_trials",
        >>> #         "truncation": {...},
        >>> #         "full_result": "<full content>"
        >>> #     }
        >>> # }
    """

    async def call_tool(
        self,
        name: str,
        tool_args: Dict[str, Any],
        ctx: RunContext,
        tool: ToolsetTool
    ) -> Any:
        """
        Intercept tool calls and return structured response with metadata.

        Args:
            name: Tool name
            tool_args: Validated tool arguments
            ctx: Run context
            tool: Tool definition

        Returns:
            Dictionary with truncated content and metadata
        """
        # Call the underlying tool
        result = await super(TruncatingToolset, self).call_tool(name, tool_args, ctx, tool)

        # Check if truncation should be applied to this tool
        if self.enabled_tools is not None and name not in self.enabled_tools:
            return result

        # Apply smart truncation
        truncation_result = smart_truncate_result(
            result,
            max_tokens=self.max_tokens,
            max_array_items=self.max_array_items
        )

        # If no truncation occurred, return original result
        if not truncation_result.was_truncated:
            return result

        # Return structured response with metadata
        return create_truncated_response(name, result, truncation_result)
