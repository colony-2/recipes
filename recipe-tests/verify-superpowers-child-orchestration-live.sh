#!/usr/bin/env bash
set -euo pipefail

WORK_DIR="/tmp/superpowers-child-orchestration-live"
C2J_BIN="${C2J_BIN:-c2j}"
TENANT_ID="recipe-tests"

rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

prepare_cell_repo() {
  local cell_repo="$WORK_DIR/cell-repo"
  git init -b main "$cell_repo" >/dev/null
  git -C "$cell_repo" config user.email c2j-smoke@example.com
  git -C "$cell_repo" config user.name "c2j smoke"
  mkdir -p "$cell_repo/.c2j/recipes"

  cat >"$cell_repo/.c2j/config.yaml" <<EOF_CONFIG
self:
  repo: $cell_repo
  ref: main
EOF_CONFIG

  cat >"$cell_repo/.c2j/recipes/child-fails.yaml" <<'EOF_CHILD_FAILS'
id: child-fails
version: "1.0"
sequence:
  - id: fail_task
    op: command_execution
    inputs:
      timeout: 10s
      run: |
        set -euo pipefail
        echo "intentional child failure"
        exit 7
EOF_CHILD_FAILS

  cat >"$cell_repo/.c2j/recipes/parent-soft-child-status.yaml" <<'EOF_PARENT_SOFT'
id: parent-soft-child-status
version: "1.0"
sequence:
  - id: start_child
    op: recipes.run
    inputs:
      git_ref: "{{ context.git.ref }}"
      recipes:
        - name: child-fails
          inputs: {}
          artifacts: []

  - id: await_child
    op: recipe.await_result_soft
    inputs:
      job_id: "${{ sequence.start_child.outputs.job_ids[0] }}"
      return_when: terminal

  - id: child_status_gate
    op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
    inputs:
      rules:
        - id: child_required_completed
          type: child_status
          status: "${{ sequence.await_child.outputs }}"
          allow_statuses:
            - completed
          message: Failed child jobs should be policy data for the planner.

  - id: probe
    op: command_execution
    inputs:
      timeout: 10s
      env:
        CHILD_STATUS: "{{ sequence.await_child.outputs.status }}"
        CHILD_TERMINAL: '${{ sequence.await_child.outputs.terminal ? "true" : "false" }}'
        GATE_OK_FALSE: '${{ !sequence.child_status_gate.outputs.ok ? "true" : "false" }}'
        GATE_FAILED_ID_PRESENT: '${{ "child_required_completed" in sequence.child_status_gate.outputs.failed_rule_ids ? "true" : "false" }}'
      run: |
        set -euo pipefail
        python3 - <<'PY'
        import json
        import os

        assert os.environ["CHILD_STATUS"] == "failed", os.environ["CHILD_STATUS"]
        assert os.environ["CHILD_TERMINAL"] == "true", os.environ["CHILD_TERMINAL"]
        assert os.environ["GATE_OK_FALSE"] == "true", os.environ["GATE_OK_FALSE"]
        assert os.environ["GATE_FAILED_ID_PRESENT"] == "true", os.environ["GATE_FAILED_ID_PRESENT"]

        print("soft-child-status assertions passed")
        PY

outputs:
  child_status: "{{ sequence.await_child.outputs.status }}"
  child_failed_routeable: "${{ !sequence.child_status_gate.outputs.ok }}"
EOF_PARENT_SOFT

  cat >"$cell_repo/.c2j/recipes/child-review-pass.yaml" <<'EOF_REVIEW_PASS'
id: child-review-pass
version: "1.0"
input_schema:
  review:
    type: string
    required: false
sequence:
  - id: write_review
    op: command_execution
    inputs:
      timeout: 10s
      run: |
        set -euo pipefail
        mkdir -p "{{ context.environment.op.outbox }}/review"
        cat > "{{ context.environment.op.outbox }}/review/result.json" <<JSON
        {
          "review": "${{ inputs.?review.orValue("review") }}",
          "verdict": "pass",
          "blocking_issues": [],
          "warnings": []
        }
        JSON
outputs:
  verdict: pass
  summary: "Review passed."
  blocking_issues: []
  warnings: []
EOF_REVIEW_PASS

  cat >"$cell_repo/.c2j/recipes/child-review-fail.yaml" <<'EOF_REVIEW_FAIL'
id: child-review-fail
version: "1.0"
input_schema:
  review:
    type: string
    required: false
sequence:
  - id: write_review
    op: command_execution
    inputs:
      timeout: 10s
      run: |
        set -euo pipefail
        mkdir -p "{{ context.environment.op.outbox }}/review"
        cat > "{{ context.environment.op.outbox }}/review/result.json" <<JSON
        {
          "review": "${{ inputs.?review.orValue("review") }}",
          "verdict": "fail",
          "blocking_issues": ["${{ inputs.?review.orValue("review") }} blocker"],
          "warnings": []
        }
        JSON

  - id: fail_review
    op: command_execution
    inputs:
      timeout: 10s
      run: |
        set -euo pipefail
        echo "intentional review failure"
        exit 3
EOF_REVIEW_FAIL

  cat >"$cell_repo/.c2j/recipes/parent-child-group-review.yaml" <<'EOF_PARENT_GROUP'
id: parent-child-group-review
version: "1.0"
sequence:
  - id: reviews
    child_group:
      mode: run_and_get_result
      children:
        - key: spec
          recipe: child-review-pass
          required: true
          inputs:
            review: spec
        - key: quality
          recipe: child-review-fail
          required: true
          inputs:
            review: quality
        - key: advisory
          recipe: child-review-fail
          required: false
          inputs:
            review: advisory
      aggregate:
        shape: review_pack
        artifact: review/review-pack.json

  - id: gate
    op: git+https://github.com/colony-2/c2ops.git//rule_gate@main
    inputs:
      rules:
        - id: review_group_failure_shape
          type: assert
          value: "${{ !sequence.reviews.outputs.ok && sequence.reviews.outputs.summary.failed_required == 1 && sequence.reviews.outputs.summary.failed_optional == 1 }}"
          message: Required and optional reviewer failures should remain distinguishable.

  - id: probe
    op: command_execution
    artifacts:
      review-pack.json: '${{ sequence.reviews.artifacts["review/review-pack.json"] }}'
    inputs:
      timeout: 10s
      env:
        INBOX: "{{ context.environment.op.inbox }}"
        GROUP_OK_FALSE: '${{ !sequence.reviews.outputs.ok ? "true" : "false" }}'
        FAILED_REQUIRED_ONE: '${{ sequence.reviews.outputs.summary.failed_required == 1 ? "true" : "false" }}'
        FAILED_OPTIONAL_ONE: '${{ sequence.reviews.outputs.summary.failed_optional == 1 ? "true" : "false" }}'
        GATE_OK: '${{ sequence.gate.outputs.ok ? "true" : "false" }}'
      run: |
        set -euo pipefail
        python3 - <<'PY'
        import json
        import os
        from pathlib import Path

        pack_path = Path(os.environ["INBOX"]) / "review-pack.json"
        pack = json.loads(pack_path.read_text())

        assert os.environ["GROUP_OK_FALSE"] == "true", os.environ["GROUP_OK_FALSE"]
        assert os.environ["FAILED_REQUIRED_ONE"] == "true", os.environ["FAILED_REQUIRED_ONE"]
        assert os.environ["FAILED_OPTIONAL_ONE"] == "true", os.environ["FAILED_OPTIONAL_ONE"]
        assert os.environ["GATE_OK"] == "true", os.environ["GATE_OK"]
        assert isinstance(pack, dict), pack

        print("child-group-review assertions passed")
        PY

outputs:
  group_ok: "{{ sequence.reviews.outputs.ok }}"
  failed_required: "{{ sequence.reviews.outputs.summary.failed_required }}"
  failed_optional: "{{ sequence.reviews.outputs.summary.failed_optional }}"
  gate_ok: "{{ sequence.gate.outputs.ok }}"
EOF_PARENT_GROUP

  cat >"$cell_repo/README.md" <<'EOF_README'
# Superpowers Child Orchestration Smoke Cell
EOF_README

  git -C "$cell_repo" add .
  git -C "$cell_repo" commit -m "seed superpowers child orchestration smoke cell" >/dev/null
  printf '%s\n' "$cell_repo"
}

fail_with_logs() {
  local message="$1"
  echo "$message"
  find "$WORK_DIR" -maxdepth 1 -type f -name '*.log' -print | sort | while read -r log; do
    echo "== ${log##*/} =="
    tail -120 "$log"
  done
  exit 1
}

run_child_once() {
  local child_id="$1"
  local log="$WORK_DIR/child-${child_id}.log"
  set +e
  "$C2J_BIN" run one \
    --embed \
    --tenant-id "$TENANT_ID" \
    --job-id "$child_id" \
    --lease-duration 2m \
    --wait-timeout 2m >"$log" 2>&1
  set -e
}

run_parent_to_completion() {
  local parent_id="$1"
  local label="$2"
  local seen="$WORK_DIR/${label}.seen"
  : >"$seen"

  for attempt in $(seq 1 12); do
    local log="$WORK_DIR/${label}-parent-${attempt}.log"
    set +e
    "$C2J_BIN" run one \
      --embed \
      --tenant-id "$TENANT_ID" \
      --job-id "$parent_id" \
      --lease-duration 2m \
      --wait-timeout 45s \
      --on-not-ready fail-on-pending-jobs >"$log" 2>&1
    local rc=$?
    set -e

    if [[ "$rc" -eq 0 ]]; then
      return 0
    fi

    mapfile -t child_ids < <(rg -o 'wait_for=[A-Za-z0-9,]+' "$log" | sed 's/^wait_for=//' | tr ',' '\n' | rg -v '^$' | sort -u)
    if [[ "${#child_ids[@]}" -eq 0 ]]; then
      fail_with_logs "TS-049/TS-050 failed: parent $label stopped without child wait information"
    fi

    local started_new=false
    for child_id in "${child_ids[@]}"; do
      if ! rg -q "^${child_id}$" "$seen"; then
        printf '%s\n' "$child_id" >>"$seen"
        run_child_once "$child_id"
        started_new=true
      fi
    done

    if [[ "$started_new" != "true" ]]; then
      sleep 1
    fi
  done

  fail_with_logs "TS-049/TS-050 failed: parent $label did not complete"
}

submit_job() {
  local cell_repo="$1"
  local recipe="$2"
  local job_json
  job_json="$("$C2J_BIN" submit \
    --cell "$cell_repo" \
    --recipe "$recipe" \
    --embed \
    --tenant-id "$TENANT_ID" \
    --json)"
  printf '%s\n' "$job_json" | jq -r .job_id
}

CELL_REPO="$(prepare_cell_repo)"
export C2J_EMBED_ROOT="$WORK_DIR/embed"

SOFT_PARENT_ID="$(submit_job "$CELL_REPO" parent-soft-child-status)"
run_parent_to_completion "$SOFT_PARENT_ID" "soft-child-status"

GROUP_PARENT_ID="$(submit_job "$CELL_REPO" parent-child-group-review)"
run_parent_to_completion "$GROUP_PARENT_ID" "child-group-review"

if rg -q 'lease is required|replay cache miss|workflow state conflict|chapter ordinal|duplicate submitted artifact' "$WORK_DIR"/*.log; then
  fail_with_logs "TS-049/TS-050 failed: child orchestration logs contain known c2j state/story signatures"
fi

echo "TS-049 and TS-050 passed"
