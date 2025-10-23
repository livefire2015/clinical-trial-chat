package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type ClinicalTrialsSearchArgs struct {
	Query    string `json:"query"`
	MaxItems int    `json:"max_items,omitempty"`
}

type FDADrugSearchArgs struct {
	DrugName string `json:"drug_name"`
}

func searchClinicalTrials(ctx context.Context, args map[string]interface{}) (*mcp.CallToolResult, error) {
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid arguments: %v", err)), nil
	}

	var searchArgs ClinicalTrialsSearchArgs
	if err := json.Unmarshal(argsJSON, &searchArgs); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid search arguments: %v", err)), nil
	}

	if searchArgs.MaxItems == 0 {
		searchArgs.MaxItems = 10
	}

	// Build ClinicalTrials.gov API request
	baseURL := "https://clinicaltrials.gov/api/v2/studies"
	params := url.Values{}
	params.Add("query.term", searchArgs.Query)
	params.Add("pageSize", fmt.Sprintf("%d", searchArgs.MaxItems))
	params.Add("format", "json")

	apiURL := fmt.Sprintf("%s?%s", baseURL, params.Encode())

	// Make HTTP request
	resp, err := http.Get(apiURL)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to query ClinicalTrials.gov: %v", err)), nil
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to read response: %v", err)), nil
	}

	// Parse and return results
	var apiResponse map[string]interface{}
	if err := json.Unmarshal(body, &apiResponse); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to parse API response: %v", err)), nil
	}

	result := map[string]interface{}{
		"query":    searchArgs.Query,
		"count":    apiResponse["totalCount"],
		"studies":  apiResponse["studies"],
	}

	resultJSON, err := json.Marshal(result)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to marshal result: %v", err)), nil
	}

	return mcp.NewToolResultText(string(resultJSON)), nil
}

func searchFDADrugs(ctx context.Context, args map[string]interface{}) (*mcp.CallToolResult, error) {
	argsJSON, err := json.Marshal(args)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid arguments: %v", err)), nil
	}

	var drugArgs FDADrugSearchArgs
	if err := json.Unmarshal(argsJSON, &drugArgs); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Invalid drug arguments: %v", err)), nil
	}

	// Build FDA openFDA API request
	baseURL := "https://api.fda.gov/drug/label.json"
	params := url.Values{}
	params.Add("search", fmt.Sprintf("openfda.brand_name:\"%s\"", drugArgs.DrugName))
	params.Add("limit", "5")

	apiURL := fmt.Sprintf("%s?%s", baseURL, params.Encode())

	// Make HTTP request
	resp, err := http.Get(apiURL)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to query FDA API: %v", err)), nil
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to read response: %v", err)), nil
	}

	// Parse and return results
	var apiResponse map[string]interface{}
	if err := json.Unmarshal(body, &apiResponse); err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Failed to parse API response: %v", err)), nil
	}

	result := map[string]interface{}{
		"drug_name": drugArgs.DrugName,
		"results":   apiResponse["results"],
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
		Name:    "clinical-trial-external-api",
		Version: "0.1.0",
	})

	// Register ClinicalTrials.gov search tool
	server.AddTool(mcp.Tool{
		Name:        "search_clinical_trials",
		Description: "Search ClinicalTrials.gov database for clinical studies",
		InputSchema: mcp.ToolInputSchema{
			Type: "object",
			Properties: map[string]interface{}{
				"query": map[string]interface{}{
					"type":        "string",
					"description": "Search query (e.g., disease name, intervention, sponsor)",
				},
				"max_items": map[string]interface{}{
					"type":        "number",
					"description": "Maximum number of results to return (default: 10)",
				},
			},
			Required: []string{"query"},
		},
	}, searchClinicalTrials)

	// Register FDA drug search tool
	server.AddTool(mcp.Tool{
		Name:        "search_fda_drugs",
		Description: "Search FDA drug database for drug labels and information",
		InputSchema: mcp.ToolInputSchema{
			Type: "object",
			Properties: map[string]interface{}{
				"drug_name": map[string]interface{}{
					"type":        "string",
					"description": "Drug brand name to search for",
				},
			},
			Required: []string{"drug_name"},
		},
	}, searchFDADrugs)

	// Start stdio transport
	if err := server.ServeStdio(); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}
