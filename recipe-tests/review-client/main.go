// Test client using the public input library against a separately running JobDB.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/colony-2/c2j/pkg/artifacts"
	"github.com/colony-2/c2j/pkg/input"
	"github.com/colony-2/c2j/pkg/worker/workflow"
	"github.com/colony-2/jobdb/pkg/jobdb"
	"github.com/colony-2/jobdb/pkg/jobdb/runtime/remote"
	jobworkflow "github.com/colony-2/jobdb/pkg/workflow"
)

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
func run() error {
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
	defer cancel()
	rt, err := remote.New(os.Args[1], &http.Client{Timeout: 15 * time.Second})
	if err != nil {
		return err
	}
	engine, err := jobworkflow.NewEngineBuilder().WithRuntime(rt).BuildEngine()
	if err != nil {
		return err
	}
	ctl := &workflow.SWFWorkflowControl{Engine: engine}
	client, err := input.NewRuntime(ctl, nil)
	if err != nil {
		return err
	}
	job := os.Args[2]
	var result any
	switch os.Args[3] {
	case "get":
		result, err = client.GetForm(ctx, "test", job)
	case "read":
		var ref artifacts.Ref
		if err = json.NewDecoder(os.Stdin).Decode(&ref); err != nil {
			return err
		}
		key, ok := ref.StoredKey()
		if !ok {
			return fmt.Errorf("stored reference required")
		}
		var content []byte
		content, err = ctl.GetArtifactLazy(ctx, "test", key).Bytes(ctx)
		result = map[string]string{"content": string(content)}
	case "submit":
		var request struct {
			RequestID    string         `json:"request_id"`
			SubmissionID string         `json:"submission_id"`
			Fields       map[string]any `json:"fields"`
			Uploads      map[string]struct {
				Name    string `json:"name"`
				Content string `json:"content"`
			} `json:"uploads"`
		}
		if err = json.NewDecoder(os.Stdin).Decode(&request); err != nil {
			return err
		}
		if request.Fields == nil {
			request.Fields = map[string]any{}
		}
		for field, upload := range request.Uploads {
			request.Fields[field] = jobdb.NewArtifactFromBytes(upload.Name, []byte(upload.Content))
		}
		result, err = client.SubmitFormResponse(ctx, "test", job, input.FormSubmission{RequestID: request.RequestID, SubmissionID: request.SubmissionID, Fields: request.Fields}, input.Actor{ID: "recipe-reviewer", Kind: "human"})
	default:
		return fmt.Errorf("unknown action")
	}
	if err != nil {
		return err
	}
	return json.NewEncoder(os.Stdout).Encode(result)
}
