# Clinical Trial External API MCP Server

MCP server for querying external pharmaceutical and clinical trial APIs.

## Features

- `search_clinical_trials`: Query ClinicalTrials.gov database for clinical studies
- `search_fda_drugs`: Search FDA openFDA API for drug labels and information

## APIs Used

- **ClinicalTrials.gov API v2**: Public clinical trial registry
- **FDA openFDA API**: Drug labels, adverse events, recalls

## Build and Run

```bash
go build -o mcp-external-api
./mcp-external-api
```

## Usage

The server communicates via stdio transport and provides access to public pharmaceutical databases.
