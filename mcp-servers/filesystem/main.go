package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type ReadFileArgs struct {
	Path string `json:"path"`
}

type ListFilesArgs struct {
	Directory string `json:"directory"`
	Pattern   string `json:"pattern,omitempty"`
}

func readFile(ctx context.Context, args map[string]interface{}) (*mcp.CallToolResult, error) {
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid arguments: %v", err)), nil
	}

	var fileArgs ReadFileArgs
	if err := json.Unmarshal(argsJSON, &fileArgs); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid file arguments: %v", err)), nil
	}

	// Read file content
	content, err := os.ReadFile(fileArgs.Path)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to read file: %v", err)), nil
	}

	result := map[string]interface{}{
		"path":    fileArgs.Path,
		"content": string(content),
		"size":    len(content),
	}

	resultJSON, err := json.Marshal(result)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to marshal result: %v", err)), nil
	}

	return mcp.NewToolResultText(string(resultJSON)), nil
}

func listFiles(ctx context.Context, args map[string]interface{}) (*mcp.CallToolResult, error) {
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid arguments: %v", err)), nil
	}

	var listArgs ListFilesArgs
	if err := json.Unmarshal(argsJSON, &listArgs); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid list arguments: %v", err)), nil
	}

	var files []map[string]interface{}

	// Walk directory
	err = filepath.Walk(listArgs.Directory, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Apply pattern filter if specified
		if listArgs.Pattern != "" {
			matched, matchErr := filepath.Match(listArgs.Pattern, filepath.Base(path))
			if matchErr != nil || !matched {
				return nil
			}
		}

		files = append(files, map[string]interface{}{
			"path":    path,
			"name":    info.Name(),
			"size":    info.Size(),
			"is_dir":  info.IsDir(),
			"mod_time": info.ModTime().Format("2006-01-02 15:04:05"),
		})

		return nil
	})

	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to list files: %v", err)), nil
	}

	result := map[string]interface{}{
		"directory": listArgs.Directory,
		"files":     files,
		"count":     len(files),
	}

	resultJSON, err := json.Marshal(result)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to marshal result: %v", err)), nil
	}

	return mcp.NewToolResultText(string(resultJSON)), nil
}

func main() {
	// Create MCP server
	server := mcp.NewServer(mcp.ServerInfo{
		Name:    "clinical-trial-filesystem",
		Version: "0.1.0",
	})

	// Register read_file tool
	server.AddTool(mcp.Tool{
		Name:        "read_file",
		Description: "Read content of a clinical trial document or data file",
		InputSchema: mcp.ToolInputSchema{
			Type: "object",
			Properties: map[string]interface{}{
				"path": map[string]interface{}{
					"type":        "string",
					"description": "Path to the file to read",
				},
			},
			Required: []string{"path"},
		},
	}, readFile)

	// Register list_files tool
	server.AddTool(mcp.Tool{
		Name:        "list_files",
		Description: "List files in a directory, optionally filtered by pattern",
		InputSchema: mcp.ToolInputSchema{
			Type: "object",
			Properties: map[string]interface{}{
				"directory": map[string]interface{}{
					"type":        "string",
					"description": "Directory path to list",
				},
				"pattern": map[string]interface{}{
					"type":        "string",
					"description": "Optional glob pattern to filter files (e.g., '*.csv', '*.pdf')",
				},
			},
			Required: []string{"directory"},
		},
	}, listFiles)

	// Start stdio transport
	if err := server.ServeStdio(); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}
