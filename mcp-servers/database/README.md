# Clinical Trial Database MCP Server

PostgreSQL MCP server for querying clinical trial data.

## Features

- `execute_query`: Execute SELECT queries on clinical trial database

## Configuration

Set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="host=localhost port=5432 user=postgres password=postgres dbname=clinical_trials sslmode=disable"
```

## Build and Run

```bash
go build -o mcp-database
./mcp-database
```

## Usage with MCP Client

The server communicates via stdio transport and can be used with any MCP client.
