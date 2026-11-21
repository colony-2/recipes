// Bounded client for the ask recipe's SQLite acceptance fixtures. No runtime mocks.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"os"
	"time"

	"github.com/colony-2/c2j/cmd/c2j/internal/c2jops"
	"github.com/colony-2/c2j/internal/celltest"
	"github.com/colony-2/c2j/internal/localruntime"
	"github.com/colony-2/c2j/pkg/artifacts"
	"github.com/colony-2/c2j/pkg/contextual"
	"github.com/colony-2/c2j/pkg/execution"
	"github.com/colony-2/c2j/pkg/executionruntime"
	"github.com/colony-2/c2j/pkg/input"
	"github.com/colony-2/c2j/pkg/jobdbschema"
	coreops "github.com/colony-2/c2j/pkg/ops"
	"github.com/colony-2/c2j/pkg/starter"
	"github.com/colony-2/c2j/pkg/worker/compiler"
	workerops "github.com/colony-2/c2j/pkg/worker/ops"
	workerworkflow "github.com/colony-2/c2j/pkg/worker/workflow"
	"github.com/colony-2/c2j/pkg/workflowctl"
	"github.com/colony-2/jobdb/pkg/jobdb"
	"github.com/colony-2/jobdb/pkg/jobdb/runtime/sqlite"
	jobworkflow "github.com/colony-2/jobdb/pkg/workflow"
)

func must(err error) {
	if err != nil {
		panic(err)
	}
}
func emit(v any) { must(json.NewEncoder(os.Stdout).Encode(v)) }
func main() {
	slog.SetDefault(slog.New(slog.NewTextHandler(os.Stderr, &slog.HandlerOptions{Level: slog.LevelWarn})))
	ctx := celltest.Context(context.Background())
	var config struct {
		DB, Action, Job, Source, Consumer, Hash string
		Inputs                                  map[string]any
		Response                                map[string]any
	}
	must(json.NewDecoder(os.Stdin).Decode(&config))
	repo := celltest.Repo(config.Consumer)
	db, err := sqlite.NewFromConfig(ctx, sqlite.Config{DBPath: config.DB})
	must(err)
	defer func() { must(db.Close(ctx)) }()
	c2jops.Register()
	rt := localruntime.New(db)
	sdk, err := jobworkflow.NewEngineBuilder().WithRuntime(rt).WithWorkerTenantId("ask-fixture").BuildEngine()
	must(err)
	engine := jobdbschema.WorkflowEngine{Engine: sdk, Registry: db}
	ctl := &workerworkflow.SWFWorkflowControl{Engine: engine, PreferRuntimeRecipeResolution: true}
	deps := coreops.NewServiceDepsBuilder().WithWorkflowControl(ctl).Build()
	registry, err := workerops.NewActivityRegistry()
	must(err)
	registry.SetDependencies(deps)
	workers, err := compiler.NewRecipeWorkerWithOptions(deps, registry, compiler.RecipeJobWorkerOptions{RootSourceResolver: compiler.NewRecipeSourceResolver(compiler.RecipeSourceResolverOptions{})})
	must(err)
	must(engine.RegisterWorkers(workers))
	guard := executionruntime.New(rt, execution.Allocation{SchemaVersion: 1})
	var tasks []jobworkflow.TaskWorker
	for _, w := range workers.TaskWorkers {
		tasks = append(tasks, guard.WrapTaskWorker(w))
	}
	key := jobdb.JobKey{TenantId: "ask-fixture", JobId: config.Job}
	var last any
	run := func() {
		runnable, err := jobworkflow.GetJobForRun(ctx, guard, jobworkflow.GetJobForRunRequest{JobKey: key, JobWorker: workers.JobWorker, TaskWorkers: tasks, WorkerID: "ask-fixture", LeaseDuration: time.Minute})
		must(err)
		if outcome, ok := runnable.Outcome(); ok {
			last = outcome
		} else {
			outcome, err := runnable.Run(nil)
			must(err)
			last = outcome
		}
	}
	native, err := input.NewRuntime(ctl, nil)
	must(err)
	switch config.Action {
	case "start", "complete":
		_, err := rt.CreateCell(ctx, jobdb.CreateCellRequest{TenantID: key.TenantId, Name: "consumer", Repo: repo, RequestID: "consumer"})
		must(err)
		jobctx := contextual.JobContext{Workflow: contextual.WorkflowContext{CellName: "consumer"}, GitBase: contextual.GitBaseContext{BaseRepo: "file://" + config.Consumer, BaseRef: config.Hash, ResolvedBaseHash: config.Hash}}
		_, err = starter.StartRecipeJob(ctx, workflowctl.StartJob{TenantId: key.TenantId, JobID: key.JobId, RecipeName: config.Source, Inputs: config.Inputs, JobContext: jobctx, GitRef: config.Hash, Cell: "consumer", CellRepo: repo}, engine)
		must(err)
		run()
		if config.Action == "complete" {
			form, err := native.GetForm(ctx, key.TenantId, key.JobId)
			must(err)
			out, err := native.SubmitStructuredResponse(ctx, key.TenantId, key.JobId, input.StructuredSubmission{RequestID: form.RequestID, SubmissionID: "fixture-reply", Response: config.Response}, input.Actor{ID: "fixture-person", Kind: "human"})
			must(err)
			run()
			emit(map[string]any{"accepted": out, "form": form})
		} else {
			emit(map[string]any{"started": key.JobId, "outcome": last})
		}
	case "run":
		run()
		emit(map[string]any{"ran": key.JobId, "outcome": last})
	case "form":
		form, err := native.GetForm(ctx, key.TenantId, key.JobId)
		must(err)
		task, err := ctl.GetWaitingTask(ctx, key)
		must(err)
		emit(map[string]any{"form": form, "ordinal": task.TaskOrdinalToComplete()})
	case "respond":
		form, err := native.GetForm(ctx, key.TenantId, key.JobId)
		must(err)
		out, err := native.SubmitStructuredResponse(ctx, key.TenantId, key.JobId, input.StructuredSubmission{RequestID: form.RequestID, SubmissionID: "fixture-reply", Response: config.Response}, input.Actor{ID: "fixture-person", Kind: "human"})
		if err != nil {
			emit(map[string]any{"rejected": err.Error()})
			return
		}
		emit(out)
	case "cancel":
		must(ctl.Cancel(ctx, key))
		emit(map[string]any{"cancelled": key.JobId})
	case "history":
		history, err := input.NewHistoryService(input.HistoryConfig{Reader: ctl})
		must(err)
		page, err := history.ListJobInputStory(ctx, input.ListJobInputStoryRequest{TenantID: key.TenantId, JobID: key.JobId})
		must(err)
		emit(page)
	case "result":
		data, err := ctl.JobResult(ctx, key)
		must(err)
		raw, err := data.GetData()
		must(err)
		var values map[string]any
		must(json.Unmarshal(raw, &values))
		if wrapped, ok := values["output"].(map[string]any); ok {
			values = wrapped
		}
		materialized := map[string]string{}
		if refs, ok := values["artifact_refs"].(map[string]any); ok {
			for name, value := range refs {
				raw, err := json.Marshal(value)
				must(err)
				var ref artifacts.Ref
				must(json.Unmarshal(raw, &ref))
				key, ok := ref.StoredKey()
				if !ok {
					panic("expected stored reference")
				}
				stream, err := ctl.GetArtifactLazy(ctx, "ask-fixture", key).Open()
				must(err)
				body, err := io.ReadAll(stream)
				must(err)
				must(stream.Close())
				materialized[name] = string(body)
			}
		}
		emit(map[string]any{"outputs": values, "bytes": materialized})
	default:
		panic(fmt.Sprintf("unknown action %q", config.Action))
	}
}
