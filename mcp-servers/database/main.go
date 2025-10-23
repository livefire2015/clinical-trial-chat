package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"os"

	_ "github.com/lib/pq"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type QueryArgs struct {
	SQL string `json:"sql"`
}

type QueryResult struct {
	Columns []string        `json:"columns"`
	Rows    [][]interface{} `json:"rows"`
	Count   int             `json:"count"`
}

var db *sql.DB

func executeQuery(ctx context.Context, args map[string]interface{}) (*mcp.CallToolResult, error) {
	// Parse arguments
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid arguments: %v", err)), nil
	}

	var queryArgs QueryArgs
	if err := json.Unmarshal(argsJSON, &queryArgs); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid query arguments: %v", err)), nil
	}

	// Execute query
	rows, err := db.QueryContext(ctx, queryArgs.SQL)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Query failed: %v", err)), nil
	}
	defer rows.Close()

	// Get column names
	columns, err := rows.Columns()
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to get columns: %v", err)), nil
	}

	// Fetch results
	var resultRows [][]interface{}
	for rows.Next() {
		// Create a slice of interface{} to hold each row
		values := make([]interface{}, len(columns))
		valuePtrs := make([]interface{}, len(columns))
		for i := range values {
			valuePtrs[i] = &values[i]
		}

		if err := rows.Scan(valuePtrs...); err != nil {
			return mcp.NewToolResultError(fmt.Sprintf("Failed to scan row: %v", err)), nil
		}

		resultRows = append(resultRows, values)
	}

	result := QueryResult{
		Columns: columns,
		Rows:    resultRows,
		Count:   len(resultRows),
	}

	resultJSON, err := json.Marshal(result)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to marshal result: %v", err)), nil
	}

	return mcp.NewToolResultText(string(resultJSON)), nil
}

func main() {
	// Get database connection string from environment
	connStr := os.Getenv("DATABASE_URL")
	if connStr == "" {
		connStr = "host=localhost port=5432 user=postgres password=postgres dbname=clinical_trials sslmode=disable"
	}

	// Connect to database
	var err error
	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	// Test connection
	if err = db.Ping(); err != nil {
		log.Printf("Warning: Database not reachable: %v", err)
	}

	// Create MCP server
	server := mcp.NewServer(mcp.ServerInfo{
		Name:    "clinical-trial-database",
		Version: "0.1.0",
	})

	// Register query tool
	server.AddTool(mcp.Tool{
		Name:        "execute_query",
		Description: "Execute SQL query on clinical trial database. Returns columns, rows, and count.",
		InputSchema: mcp.ToolInputSchema{
			Type: "object",
			Properties: map[string]interface{}{
				"sql": map[string]interface{}{
					"type":        "string",
					"description": "SQL SELECT query to execute",
				},
			},
			Required: []string{"sql"},
		},
	}, executeQuery)

	// Start stdio transport
	if err := server.ServeStdio(); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}
