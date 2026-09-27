// An isolated, in-memory JobDB service for multi-process recipe integration tests.
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"

	"github.com/colony-2/jobdb/pkg/jobdb"
	"github.com/colony-2/jobdb/pkg/jobdb/runtime/remote"
	"github.com/colony-2/jobdb/pkg/jobdb/runtime/toy"
)

func main() {
	runtime := toy.New()
	mux := http.NewServeMux()
	mux.Handle("/", remote.NewServer(runtime))
	// Read-only inspection and deliberate cancellation for deterministic fixtures.
	mux.HandleFunc("/test/job", func(w http.ResponseWriter, r *http.Request) {
		result, err := runtime.GetJobRun(r.Context(), jobdb.GetJobRunRequest{
			JobKey:        jobdb.JobKey{TenantId: "test", JobId: r.URL.Query().Get("id")},
			IncludeInputs: true, IncludeAttemptInputs: true, IncludeOutputs: true, IncludeArtifacts: true,
		})
		if err != nil {
			http.Error(w, err.Error(), 500)
			return
		}
		json.NewEncoder(w).Encode(result)
	})
	mux.HandleFunc("/test/cancel", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			http.Error(w, "POST required", 405)
			return
		}
		err := runtime.CancelJob(r.Context(), jobdb.CancelJobRequest{
			JobKey: jobdb.JobKey{TenantId: "test", JobId: r.URL.Query().Get("id")}, Reason: "test cancellation",
		})
		if err != nil {
			http.Error(w, err.Error(), 500)
			return
		}
		w.WriteHeader(204)
	})
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("http://" + listener.Addr().String())
	log.Fatal(http.Serve(listener, mux))
}
