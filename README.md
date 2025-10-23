# Clinical Trial Analysis Chat

AI-powered pharmaceutical clinical trial analysis application using Pydantic-AI, Golang MCP servers, FastAPI, and Svelte.

## Architecture

```
┌─────────────────┐
│  Svelte Frontend │ ◄──── AG-UI Protocol (SSE) ────► ┌──────────────────┐
│   (@ag-ui/client)│                                   │  FastAPI Backend │
└─────────────────┘                                   │  (Pydantic-AI)   │
                                                      └──────────────────┘
                                                             │
                                        ┌────────────────────┼────────────────────┐
                                        │                    │                    │
                                        ▼                    ▼                    ▼
                                  ┌──────────┐        ┌──────────┐        ┌──────────┐
                                  │ Database │        │Filesystem│        │External  │
                                  │   MCP    │        │   MCP    │        │ API MCP  │
                                  │  Server  │        │  Server  │        │  Server  │
                                  └──────────┘        └──────────┘        └──────────┘
                                  PostgreSQL          Documents/CSV       FDA/ClinicalTrials.gov
```

## Features

### AI Agent Capabilities
- **Data Querying**: Query clinical trial databases for patient data, adverse events, and outcomes
- **Statistical Analysis**: Calculate means, medians, standard deviations, confidence intervals
- **Compliance Checking**: Verify FDA 21 CFR Part 11 and ICH-GCP guidelines
- **Document Access**: Read and analyze clinical trial documents (PDF, CSV, Excel)
- **External Data**: Search ClinicalTrials.gov and FDA drug databases

### Technical Features
- **AG-UI Protocol**: Standards-compliant agent-user interaction with SSE streaming
- **MCP Integration**: Three Golang MCP servers for database, filesystem, and external APIs
- **Real-time Streaming**: Token-by-token response streaming in the UI
- **Data Encryption**: AES-256 encryption for sensitive pharmaceutical data
- **Rich Visualizations**: Data tables, statistical summaries, and charts

## Project Structure

```
clinical-trial-chat/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── agent/       # Pydantic-AI agent + MCP integration
│   │   ├── api/         # AG-UI endpoint (SSE streaming)
│   │   ├── models/      # Pydantic models
│   │   └── security/    # Encryption utilities
│   ├── main.py
│   └── requirements.txt
├── frontend/            # Svelte application
│   ├── src/
│   │   ├── components/  # Chat UI, tables, stats
│   │   ├── lib/         # AG-UI client
│   │   └── App.svelte
│   └── package.json
└── mcp-servers/         # Golang MCP servers
    ├── database/        # PostgreSQL queries
    ├── filesystem/      # Document access
    └── external-api/    # ClinicalTrials.gov, FDA
```

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Go 1.23+
- PostgreSQL (optional, for database features)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run backend
python main.py
```

Backend runs on `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

### 3. MCP Servers Setup

Build all MCP servers:

```bash
# Database server
cd mcp-servers/database
go build -o mcp-database

# Filesystem server
cd ../filesystem
go build -o mcp-filesystem

# External API server
cd ../external-api
go build -o mcp-external-api
```

The servers are automatically started by the backend via stdio transport.

## Configuration

### Environment Variables

Create `backend/.env`:

```bash
# Server
PORT=8000

# Database (optional)
DATABASE_URL=host=localhost port=5432 user=postgres password=postgres dbname=clinical_trials sslmode=disable

# MCP Server Paths
MCP_DATABASE_PATH=../mcp-servers/database/mcp-database
MCP_FILESYSTEM_PATH=../mcp-servers/filesystem/mcp-filesystem
MCP_EXTERNAL_API_PATH=../mcp-servers/external-api/mcp-external-api

# LLM API Keys (choose one)
OPENAI_API_KEY=your-openai-key
# ANTHROPIC_API_KEY=your-anthropic-key

# Encryption
ENCRYPTION_KEY=your-secure-32-byte-encryption-key
```

## Usage

1. Start the backend: `cd backend && python main.py`
2. Start the frontend: `cd frontend && npm run dev`
3. Open `http://localhost:5173` in your browser
4. Start chatting about clinical trial data!

### Example Queries

- "What are the statistical measures for patient age in the trial?"
- "Search ClinicalTrials.gov for diabetes studies"
- "Check compliance requirements for FDA 21 CFR Part 11"
- "Query the database for adverse events in the last month"
- "Calculate p-values for the treatment group outcomes"

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

### Git Workflow

This project uses focused, atomic commits:

```bash
git add <specific-files>
git commit -m "Brief description of change

- Detailed point 1
- Detailed point 2"
```

## Technology Stack

- **Frontend**: Svelte 5, Vite, @ag-ui/client, Chart.js
- **Backend**: Python, FastAPI, Pydantic-AI, MCP Client
- **MCP Servers**: Go, Official MCP SDK v1.0.0
- **Protocols**: AG-UI (agent-user interaction), MCP (model context protocol)
- **Security**: AES-256 encryption, PBKDF2 key derivation
- **APIs**: ClinicalTrials.gov v2, FDA openFDA

## License

MIT

## Contributing

This is a pharmaceutical clinical trial analysis tool. Contributions should maintain:
- HIPAA compliance considerations
- Data encryption for PHI/PII
- Accurate statistical calculations
- Proper regulatory citations
