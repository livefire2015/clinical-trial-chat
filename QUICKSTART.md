# Quick Start Guide

Get the Clinical Trial Analysis Chat app running in 5 minutes.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Go 1.23+
- OpenAI API key (or Anthropic API key)

## 1. Configure Environment

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add your API key:
```bash
OPENAI_API_KEY=sk-your-key-here
```

## 2. Start Backend

```bash
# From backend/ directory
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend will start on `http://localhost:8000`

## 3. Start Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend will start on `http://localhost:5173`

## 4. Build MCP Servers (Optional)

The MCP servers provide additional functionality. Build them when needed:

```bash
# Database server (for SQL queries)
cd mcp-servers/database
go build -o mcp-database

# Filesystem server (for document access)
cd ../filesystem
go build -o mcp-filesystem

# External API server (for ClinicalTrials.gov/FDA)
cd ../external-api
go build -o mcp-external-api
```

## 5. Try It Out!

Open `http://localhost:5173` and try these queries:

- "Calculate statistics for these values: 23, 45, 67, 89, 12, 34, 56"
- "Check compliance requirements for FDA 21 CFR Part 11"
- "What are the requirements for ICH-GCP compliance?"

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.11+)
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Clear cache: `rm -rf node_modules && npm install`

### MCP servers not working
- Build the servers first (see step 4)
- Check paths in backend/.env match your build output

### API errors
- Verify OPENAI_API_KEY is set in backend/.env
- Check backend logs for error messages

## What's Next?

- Set up PostgreSQL for database queries
- Add clinical trial data files
- Customize the agent prompt for your use case
- Deploy to production (see README.md)

## Architecture Overview

```
Svelte UI ──(AG-UI/SSE)──> FastAPI Backend ──(MCP/stdio)──> Go MCP Servers
                              ↓
                         Pydantic-AI Agent
```

For full documentation, see [README.md](README.md)
