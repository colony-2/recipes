# Submit an approved package check

`package-probe.yaml` accepts optional string `prompt` and `title` context, both
empty by default. Existing include and native-child callers can omit them.
`config` and `requests` remain required. A missing or conflicting `approved`
binding still returns `changes` before writing configuration or running checks.
Context never selects commands: only the approved request argument arrays run.

Use the installed CLI's `--advanced-recipe-file` for a local candidate, or
`--advanced-recipe` with a published Git selector. `c2j submit` supplies the
positional prompt and optional `--title`. No wrapper, model credentials or
permission override is needed. A successful submission is only a job identity;
inspect its completed result and probe task before claiming the tools work.

## Recover the retained approval

Request `58ee6156-3ae8-4723-be3d-16c082b92551` accepted the exact task-61
`review/config.yaml` from job `8xRJD69dht1XxepXxYA0p6rTRhL`. Its SHA-256 is
`cc73e1755f86d5fa03bc3f174e027625ed0ea1c6325be79a62dc60d6d4bc441a`.
Keep its stored reference, bytes, versions and check arrays unchanged. A copied
review attachment has a different identity and cannot substitute for that reference.

That approval covers the two private pnpm references below, including direct,
transitive and selected optional dependency builds, mutable transitives, and
repeated preparation after failures, worker changes or cache loss. Changed scope
or requests require applicable authority; withdrawal, cancellation and newer
human direction prevail. A validator binding records content and baseline; it
does not create human approval. Standing cell policy and baseline dependencies
are separate authority.

Create the input file in scratch outside the checkout:

```sh
scratch=$(mktemp -d)
python3 - "$scratch/validator-inputs.json" <<'PY'
import json, sys
reference = {
    "kind": "stored", "name": "review/config.yaml",
    "stored": {"key": {
        "jobId": "8xRJD69dht1XxepXxYA0p6rTRhL", "taskOrdinal": 61,
        "name": "review/config.yaml", "sizeBytes": 96
    }}
}
requests = [
    {"reference": "pnpm:@openai/codex@0.112.0", "check": ["codex", "--version"]},
    {"reference": "pnpm:@agentclientprotocol/claude-agent-acp@0.109.0",
     "check": ["claude-agent-acp", "--version"]}
]
with open(sys.argv[1], "w") as stream:
    json.dump({"check": "package_config", "write": False,
               "documents": {"review/config.yaml": reference}, "requests": requests}, stream)
PY
c2j submit 'Validate the retained approved tool configuration without writing it' \
  --cell acp-plus-session \
  --advanced-recipe-file ./recipes/adaptive3/tools.yaml \
  --inputs-file "$scratch/validator-inputs.json" \
  --title 'Validate retained Codex and Claude package approval' --json
```

Normal workers run the submitted job against the target cell's current baseline.
Do not add `--from-workspace-now`: that selects a caller candidate instead.
`tools.yaml` declares its existing validator inputs so it can run directly as a
root recipe as well as through existing includes.

After the validator completes, replace `VALIDATOR_JOB` with its returned ID:

```sh
c2j job result VALIDATOR_JOB --json
c2j job result VALIDATOR_JOB --field /approved --output "$scratch/approved.json"
c2j job log VALIDATOR_JOB --json
```

Require successful completion, `result.status: passed`, a nonempty binding and
`written: false` in the exact validator task's stdout. Discover that task's ID
from `job log`; use `job log --task TASK --field '' --output FILE` for its full
output. `job snapshot VALIDATOR_JOB --task TASK --output FILE` records the actual
target repository, ref and commit. Compare its observed configuration with the
returned baseline, rather than assuming the historical configuration is still absent.
The read-only task must leave that configuration unchanged.

If outputs are unavailable, recover the exact validator task output using
`job fields` and `job log`; never reconstruct a binding with a guessed baseline.
A changed baseline that makes the retained proposal incompatible stops recovery.
Do not alter approved bytes or regenerate authority to bypass a conflict.

Create the probe inputs from the returned binding without editing it:

```sh
python3 - "$scratch/validator-inputs.json" "$scratch/approved.json" "$scratch/probe-inputs.json" <<'PY'
import json, sys
original = json.load(open(sys.argv[1]))
approved = json.load(open(sys.argv[2]))
assert approved["config"] == original["documents"]["review/config.yaml"]
assert approved["requests"] == original["requests"]
assert approved["sha256"] == "cc73e1755f86d5fa03bc3f174e027625ed0ea1c6325be79a62dc60d6d4bc441a"
assert approved["proposed"] == {"packages": [item["reference"] for item in original["requests"]]}
with open(sys.argv[3], "w") as stream:
    json.dump({"config": approved["config"], "requests": approved["requests"],
               "approved": approved}, stream)
PY
c2j submit 'Check the tools authorized by request 58ee6156-3ae8-4723-be3d-16c082b92551' \
  --cell acp-plus-session \
  --advanced-recipe-file ./recipes/adaptive3/package-probe.yaml \
  --inputs-file "$scratch/probe-inputs.json" \
  --title 'Check retained Codex and Claude package versions' --json
```

Require completed success and recipe `status: passed`, then read the separate
probe task's output for both exact version commands. The preceding task writes
the bounded configuration; only the following fresh task prepares and probes it.
A completed job returning `changes` fails this availability check. If the baseline
changes incompatibly between validation and writing, the existing guard rejects it.
These checks do not implement or qualify provider sessions; `acp-plus-session`
retains both-provider implementation and qualification, excluding app servers.

After normal adaptive3 publication, select the published repair in each command
by replacing its local file option with the corresponding selector:

```sh
--advanced-recipe "git+https://github.com/colony-2/recipes.git//recipes/adaptive3/tools.yaml@${REPAIR_REV}"
--advanced-recipe "git+https://github.com/colony-2/recipes.git//recipes/adaptive3/package-probe.yaml@${REPAIR_REV}"
```

`REPAIR_REV` must contain both input-contract fixes. Restarting an old diagnostic
reuses its old recipe and does not validate this repair.
