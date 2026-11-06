# Adaptive gap closure

Each statement concerns observable recipe behavior. All are integration tests;
dependencies: c2j embedded runtime and fixture model responses; package tests also
require Python, yq, and uv.

| ID | Importance | Statement | Files |
| --- | --- | --- | --- |
| GC01 | critical | Independent consultation and execution requests can share one response without a correction turn. | agent.yaml, coordinate.yaml, develop.yaml |
| GC02 | critical | Repeating execution of an agreed request reuses its goal and consumes the successful attempt. | coordinate.yaml |
| GC03 | critical | Legacy response fields and job-only dependency targets are rejected. | agent.yaml, validation-goals.yaml |
| GC04 | critical | Unfinished required goals prevent final acceptance; advisory agreements do not create implementation obligations. | develop.yaml |
| GC05 | critical | Exhausted correction, consultation, and execution bounds stop the attempt without asking a product reviewer. | response-repair.yaml, consultation.yaml, develop.yaml |
| GC06 | critical | Explicit product decisions retain clear review questions and exact returned feedback. | review.yaml, develop.yaml |
| GC07 | critical | Reviews exclude stale decision briefs and unrelated accumulated documents while retaining explicitly selected evidence. | review.yaml, consultation.yaml |
| GC08 | critical | Repeated identical package refusals do not prompt again or install tools. | packages.yaml, develop.yaml |
| GC09 | critical | Approved identical package proposals reuse authorization and their validation goal; changed probes require fresh approval. | packages.yaml |
| GC10 | critical | Failed package validation supplies real diagnostic files and preserves the parent configuration. | packages.yaml, await-goal.yaml |
| GC11 | critical | Preparation failure after adoption preserves setup diagnostics and exposes goal recovery without another product review. | agent-turn.yaml, packages.yaml |
| GC12 | high | Two requests to one owner retain separate agreements; root creation uses its authorized cell and goal. | coordinate.yaml, route-target.yaml, create-request.yaml |
