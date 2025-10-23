"""
MCP Tool Integration for Pydantic-AI Agent
"""
import os
import json
from typing import Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPDatabaseClient:
    """MCP client for database server"""

    def __init__(self):
        self.server_path = os.getenv(
            "MCP_DATABASE_PATH",
            "../mcp-servers/database/mcp-database"
        )
        self.session: ClientSession | None = None

    async def connect(self):
        """Connect to MCP database server"""
        server_params = StdioServerParameters(
            command=self.server_path,
            args=[],
            env={"DATABASE_URL": os.getenv("DATABASE_URL", "")}
        )

        # Initialize stdio client
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self.session = session

    async def execute_query(self, sql: str) -> dict[str, Any]:
        """
        Execute SQL query via MCP server

        Args:
            sql: SQL SELECT query

        Returns:
            Query results with columns, rows, and count
        """
        if not self.session:
            await self.connect()

        result = await self.session.call_tool("execute_query", {"sql": sql})

        # Parse result
        if result.content and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return json.loads(content.text)

        return {"columns": [], "rows": [], "count": 0}


# Global MCP client instance
mcp_db_client = MCPDatabaseClient()
