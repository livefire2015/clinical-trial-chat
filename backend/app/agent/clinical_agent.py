"""
Clinical Trial Analysis Agent using Pydantic-AI
"""
from typing import Any
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.anthropic import AnthropicModel
from .mcp_tools import mcp_db_client

# Create the agent
clinical_agent = Agent(
    model=AnthropicModel('claude-3-5-sonnet-20241022'),
    instructions=(
        "You are an expert clinical trial analyst specializing in pharmaceutical research. "
        "You help researchers analyze clinical trial data, perform statistical analyses, "
        "and ensure regulatory compliance.\n\n"
        "Your capabilities include:\n"
        "- Querying clinical trial databases for patient data, adverse events, and outcomes\n"
        "- Performing statistical analysis (means, medians, p-values, confidence intervals)\n"
        "- Checking compliance with FDA 21 CFR Part 11 and ICH-GCP guidelines\n"
        "- Analyzing trial documents and data files\n\n"
        "Always provide clear, accurate, and well-structured responses. "
        "When presenting statistical results, include proper context and interpretation. "
        "For compliance checks, cite specific regulatory requirements."
    ),
    retries=2,
)


@clinical_agent.tool
async def query_database(ctx: RunContext[Any], sql: str) -> dict:
    """
    Execute a SQL query on the clinical trial database.

    Args:
        sql: SELECT query to execute

    Returns:
        Query results with columns, rows, and count
    """
    result = await mcp_db_client.execute_query(sql)
    return result


@clinical_agent.tool
async def calculate_statistics(ctx: RunContext[Any], values: list[float]) -> dict:
    """
    Calculate basic statistics for a dataset.

    Args:
        values: List of numeric values

    Returns:
        Statistical measures including mean, median, std, etc.
    """
    import numpy as np
    from scipy import stats

    arr = np.array(values)

    return {
        "count": len(values),
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr, ddof=1)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "q25": float(np.percentile(arr, 25)),
        "q75": float(np.percentile(arr, 75)),
    }


@clinical_agent.tool
async def check_compliance(ctx: RunContext[Any], regulation: str, data_description: str) -> dict:
    """
    Check compliance with pharmaceutical regulations.

    Args:
        regulation: Regulation to check (e.g., "FDA 21 CFR Part 11", "ICH-GCP")
        data_description: Description of the data or process to check

    Returns:
        Compliance assessment with requirements and recommendations
    """
    # This is a placeholder - in production, this would check against actual regulatory requirements
    compliance_rules = {
        "FDA 21 CFR Part 11": {
            "requirements": [
                "Electronic signatures must be unique and linked to records",
                "Audit trails must be maintained for all data changes",
                "Systems must be validated for accuracy and reliability",
                "Access controls must be implemented"
            ],
            "description": "Electronic Records and Electronic Signatures"
        },
        "ICH-GCP": {
            "requirements": [
                "Informed consent must be obtained before trial procedures",
                "Protocol amendments must be documented and approved",
                "Adverse events must be reported according to timelines",
                "Source data must be accurate, complete, and verifiable"
            ],
            "description": "Good Clinical Practice Guidelines"
        }
    }

    if regulation not in compliance_rules:
        return {
            "status": "unknown",
            "message": f"Regulation '{regulation}' not found in knowledge base"
        }

    return {
        "status": "informational",
        "regulation": regulation,
        "description": compliance_rules[regulation]["description"],
        "requirements": compliance_rules[regulation]["requirements"],
        "assessment": f"Review required for: {data_description}"
    }


def get_agent() -> Agent:
    """Get the clinical trial analysis agent"""
    return clinical_agent
