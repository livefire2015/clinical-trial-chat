"""
Result truncation utilities for handling large MCP tool results.

This module provides utilities to intelligently truncate large tool results
to stay within token limits while preserving essential information for the
AI model and maintaining full results for UI display.
"""

import json
from typing import Any, Dict, List, Union
from dataclasses import dataclass


@dataclass
class TruncationResult:
    """Result of truncating tool output."""

    model_content: str  # Truncated content for AI model
    full_content: str  # Full content for UI display
    was_truncated: bool  # Whether truncation occurred
    original_size: int  # Original size in characters
    truncated_size: int  # Truncated size in characters
    metadata: Dict[str, Any]  # Additional metadata


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text.

    Uses a simple heuristic: ~4 characters per token for English text.
    This is a rough approximation but sufficient for truncation decisions.

    Args:
        text: The text to estimate tokens for

    Returns:
        Estimated token count
    """
    return len(text) // 4


def truncate_json_array(
    data: List[Any],
    max_items: int = 10,
    include_summary: bool = True
) -> Dict[str, Any]:
    """
    Truncate a JSON array to a maximum number of items with summary.

    Args:
        data: List to truncate
        max_items: Maximum number of items to include
        include_summary: Whether to include a summary of truncated items

    Returns:
        Dictionary with truncated items and summary
    """
    total_count = len(data)

    if total_count <= max_items:
        return {
            "items": data,
            "total_count": total_count,
            "showing": total_count,
            "truncated": False
        }

    result = {
        "items": data[:max_items],
        "total_count": total_count,
        "showing": max_items,
        "truncated": True
    }

    if include_summary:
        result["summary"] = f"Showing first {max_items} of {total_count} items. {total_count - max_items} items truncated."

    return result


def truncate_text(text: str, max_tokens: int = 2000) -> str:
    """
    Truncate text to approximately max_tokens.

    Args:
        text: Text to truncate
        max_tokens: Maximum tokens to allow

    Returns:
        Truncated text with ellipsis if truncated
    """
    max_chars = max_tokens * 4  # Approximate conversion

    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars]
    return truncated + f"\n\n... [Truncated. Original length: {len(text)} chars, showing first {max_chars} chars]"


def smart_truncate_result(
    result: Any,
    max_tokens: int = 2000,
    max_array_items: int = 10
) -> TruncationResult:
    """
    Intelligently truncate tool results based on their structure.

    Handles different result types:
    - JSON objects with arrays: Truncates arrays and preserves structure
    - Plain text: Character-based truncation
    - Already small results: Returns as-is

    Args:
        result: The tool result to truncate (can be str, dict, list, etc.)
        max_tokens: Maximum tokens for model content
        max_array_items: Maximum items to show in arrays

    Returns:
        TruncationResult with truncated and full content
    """
    # Convert result to string for processing
    if isinstance(result, str):
        result_str = result
        try:
            # Try to parse as JSON for structured truncation
            parsed = json.loads(result)
            is_json = True
        except (json.JSONDecodeError, TypeError):
            parsed = None
            is_json = False
    else:
        result_str = json.dumps(result, indent=2)
        parsed = result
        is_json = True

    original_size = len(result_str)
    estimated_tokens = estimate_tokens(result_str)

    # If already under limit, no truncation needed
    if estimated_tokens <= max_tokens:
        return TruncationResult(
            model_content=result_str,
            full_content=result_str,
            was_truncated=False,
            original_size=original_size,
            truncated_size=original_size,
            metadata={"estimated_tokens": estimated_tokens}
        )

    # Smart truncation for structured JSON data
    if is_json and parsed is not None:
        truncated_data = _truncate_json_structure(parsed, max_array_items)
        truncated_str = json.dumps(truncated_data, indent=2)

        # If still too large after array truncation, apply text truncation
        if estimate_tokens(truncated_str) > max_tokens:
            truncated_str = truncate_text(truncated_str, max_tokens)

        return TruncationResult(
            model_content=truncated_str,
            full_content=result_str,
            was_truncated=True,
            original_size=original_size,
            truncated_size=len(truncated_str),
            metadata={
                "truncation_type": "smart_json",
                "original_tokens": estimated_tokens,
                "truncated_tokens": estimate_tokens(truncated_str)
            }
        )

    # Fallback to simple text truncation
    truncated_str = truncate_text(result_str, max_tokens)

    return TruncationResult(
        model_content=truncated_str,
        full_content=result_str,
        was_truncated=True,
        original_size=original_size,
        truncated_size=len(truncated_str),
        metadata={
            "truncation_type": "text",
            "original_tokens": estimated_tokens,
            "truncated_tokens": estimate_tokens(truncated_str)
        }
    )


def _truncate_json_structure(data: Any, max_array_items: int) -> Any:
    """
    Recursively truncate arrays in JSON structure.

    Args:
        data: JSON data structure
        max_array_items: Maximum items per array

    Returns:
        Truncated JSON structure
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = _truncate_json_structure(value, max_array_items)
        return result

    elif isinstance(data, list):
        return truncate_json_array(data, max_array_items, include_summary=True)

    else:
        return data


def create_truncated_response(
    tool_name: str,
    original_result: Any,
    truncation_result: TruncationResult
) -> Dict[str, Any]:
    """
    Create a response object with both truncated and full results.

    This format allows the AI model to work with truncated content while
    the UI can access full results via metadata.

    Args:
        tool_name: Name of the tool that produced the result
        original_result: The original tool result
        truncation_result: The truncation result

    Returns:
        Response dictionary with model content and metadata
    """
    response = {
        "content": truncation_result.model_content,
        "metadata": {
            "tool_name": tool_name,
            "truncation": {
                "was_truncated": truncation_result.was_truncated,
                "original_size": truncation_result.original_size,
                "truncated_size": truncation_result.truncated_size,
                **truncation_result.metadata
            },
            "full_result": truncation_result.full_content if truncation_result.was_truncated else None
        }
    }

    return response
