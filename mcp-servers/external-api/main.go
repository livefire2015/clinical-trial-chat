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
	Query    string `json:"query" jsonschema:"description=Search query (e.g., disease name, intervention, sponsor)"`
	MaxItems int    `json:"max_items,omitempty" jsonschema:"description=Maximum number of results to return (default: 10)"`
}

type FDADrugSearchArgs struct {
	DrugName string `json:"drug_name" jsonschema:"description=Drug brand name to search for"`
}

func searchClinicalTrials(ctx context.Context, req *mcp.CallToolRequest, args ClinicalTrialsSearchArgs) (*mcp.CallToolResult, any, error) {

	if args.MaxItems == 0 {
		args.MaxItems = 10
	}

	// Build ClinicalTrials.gov API request
	baseURL := "https://clinicaltrials.gov/api/v2/studies"
	params := url.Values{}
	params.Add("query.term", args.Query)
	params.Add("pageSize", fmt.Sprintf("%d", args.MaxItems))
	params.Add("format", "json")

	apiURL := fmt.Sprintf("%s?%s", baseURL, params.Encode())

	// Make HTTP request
	resp, err := http.Get(apiURL)
	if err != nil {
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: fmt.Sprintf("Failed to query ClinicalTrials.gov: %v", err)},
			},
			IsError: true,
		}, nil, nil
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: fmt.Sprintf("Failed to read response: %v", err)},
			},
			IsError: true,
		}, nil, nil
	}

	// Parse and return results
	var apiResponse map[string]interface{}
	if err := json.Unmarshal(body, &apiResponse); err != nil {
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: fmt.Sprintf("Failed to parse API response: %v", err)},
			},
			IsError: true,
		}, nil, nil
	}

	result := map[string]interface{}{
		"query":   args.Query,
		"count":   apiResponse["totalCount"],
		"studies": apiResponse["studies"],
	}

	resultJSON, err := json.Marshal(result)
	if err != nil {
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: fmt.Sprintf("Failed to marshal result: %v", err)},
			},
			IsError: true,
		}, nil, nil
	}

	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{Text: string(resultJSON)},
		},
	}, nil, nil
}

func searchFDADrugs(ctx context.Context, req *mcp.CallToolRequest, args FDADrugSearchArgs) (*mcp.CallToolResult, any, error) {

	// Build FDA openFDA API request
	baseURL := "https://api.fda.gov/drug/label.json"
	params := url.Values{}
	params.Add("search", fmt.Sprintf("openfda.brand_name:\"%s\"", args.DrugName))
	params.Add("limit", "5")

	apiURL := fmt.Sprintf("%s?%s", baseURL, params.Encode())

	// Make HTTP request
	resp, err := http.Get(apiURL)
	if err != nil {
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: fmt.Sprintf("Failed to query FDA API: %v", err)},
			},
			IsError: true,
		}, nil, nil
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: fmt.Sprintf("Failed to read response: %v", err)},
			},
			IsError: true,
		}, nil, nil
	}

	// Parse and return results
	var apiResponse map[string]interface{}
	if err := json.Unmarshal(body, &apiResponse); err != nil {
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: fmt.Sprintf("Failed to parse API response: %v", err)},
			},
			IsError: true,
		}, nil, nil
	}

	result := map[string]interface{}{
		"drug_name": args.DrugName,
		"results":   apiResponse["results"],
	}

	resultJSON, err := json.Marshal(result)
	if err != nil {
		return &mcp.CallToolResult{
			Content: []mcp.Content{
				&mcp.TextContent{Text: fmt.Sprintf("Failed to marshal result: %v", err)},
			},
			IsError: true,
		}, nil, nil
	}

	return &mcp.CallToolResult{
		Content: []mcp.Content{
			&mcp.TextContent{Text: string(resultJSON)},
		},
	}, nil, nil
}

func main() {
	// Create MCP server
	server := mcp.NewServer(&mcp.Implementation{
		Name:    "clinical-trial-external-api",
		Version: "0.1.0",
	}, nil)

	// Register ClinicalTrials.gov search tool
	mcp.AddTool(server, &mcp.Tool{
		Name:        "search_clinical_trials",
		Description: "Search ClinicalTrials.gov database for clinical studies",
	}, searchClinicalTrials)

	// Register FDA drug search tool
	mcp.AddTool(server, &mcp.Tool{
		Name:        "search_fda_drugs",
		Description: "Search FDA drug database for drug labels and information",
	}, searchFDADrugs)

	// Start stdio transport
	if err := server.Run(context.Background(), &mcp.StdioTransport{}); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}
