"""c2j extension entry point. Requests and results travel as JSON."""

import functools
import json
import sys
from pathlib import Path

import git_work
import policy
import recovery


def main():
    invocation = json.load(sys.stdin)
    action = invocation["action"]
    repo = git_work.Git(Path(invocation["worktree"]))
    inbox = Path(invocation["inbox"])
    outbox = Path(invocation["outbox"])
    actions = {
        "prepare": functools.partial(git_work.prepare_candidate, repo),
        "identify": functools.partial(git_work.identify_submission, repo),
        "intake": functools.partial(git_work.intake, repo, outbox),
        "assemble": functools.partial(git_work.assemble, repo, inbox, outbox),
        "install": functools.partial(git_work.install, repo, inbox),
        "reuse_verification": functools.partial(git_work.reuse_verification, repo),
        "capture_repair": functools.partial(git_work.capture_repair, repo, inbox, outbox),
        "plan_probes": policy.plan_probes,
        "record_probes": policy.record_probes,
        "landing_results": functools.partial(policy.landing_results, outbox),
        "caller_receipt": policy.caller_receipt,
        "confirm_restart": recovery.confirm_restart,
        "publication_context": policy.publication_context,
        "confirm_landed": functools.partial(git_work.confirm_landed, repo),
    }
    try:
        result = actions[action](**invocation["request"])
    except (OSError, RuntimeError, ValueError) as error:
        if action == "assemble":
            (outbox / "replay-error.log").write_text(str(error) + "\n", encoding="utf-8")
        print(error, file=sys.stderr)
        return 1
    json.dump({"output": {"result": result}}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
