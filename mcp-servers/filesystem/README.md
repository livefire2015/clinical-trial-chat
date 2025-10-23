# Clinical Trial Filesystem MCP Server

Filesystem MCP server for accessing clinical trial documents and data files.

## Features

- `read_file`: Read content of clinical trial documents (CSV, PDF, TXT, etc.)
- `list_files`: List files in a directory with optional glob pattern filtering

## Build and Run

```bash
go build -o mcp-filesystem
./mcp-filesystem
```

## Usage

The server communicates via stdio transport and provides file system access for the agent.
