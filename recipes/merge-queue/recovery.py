"""Check a restarted receiver against the original job's retained merge evidence."""

import json
import subprocess
import tempfile
from pathlib import Path

from policy import is_hash


def inspect(job, *options):
    with tempfile.TemporaryDirectory() as scratch:
        output = Path(scratch) / "inspection.json"
        subprocess.run(["c2j", "job", "log", job, *options, "--output", str(output)], check=True)
        return json.loads(output.read_bytes())


def tasks(job):
    args = []
    cursors = set()
    while True:
        page = inspect(job, "--json", "--limit", "50", *args)
        if page["job"]["id"] != job:
            raise ValueError("Task inspection returned another receiver")
        yield from page.get("tasks", [])
        cursor = page.get("next_cursor")
        if not cursor:
            return
        if cursor in cursors:
            raise ValueError("Task inspection returned a repeated cursor")
        cursors.add(cursor)
        args = ["--cursor", cursor]


def assembly_receipts(rows, owner):
    return {
        (row["id"], key["taskOrdinal"], key["name"])
        for row in rows if row["status"] == "succeeded" and row["type"] == "extension_execution:extension_execution"
        and "adaptive3-merge-queue-replay/" in row.get("path", "")
        for artifact in row.get("artifacts", []) if artifact["name"] == "assembled.bundle"
        for key in [artifact.get("reference", {}).get("stored", {}).get("key", {})]
        if key.get("jobId") == owner
    }


def confirm_restart(owner, repair, source):
    try:
        original = list(tasks(owner))
        if not assembly_receipts(original, owner).intersection(assembly_receipts(tasks(repair), owner)):
            raise ValueError("The repair has no retained assembly from the original receiver")
        merges = [row for row in original if row["type"] == "merge:merge" and row["status"] == "succeeded"
                  and "adaptive3-merge-queue-land/install/" in row.get("path", "")]
        if len(merges) != 1:
            raise ValueError("The original queue merge is missing or ambiguous")
        row = merges[0]
        merge = inspect(owner, "--task", row["id"], "--attempt", str(row["attempt"]), "--field", "")
        if (not isinstance(source, dict) or not is_hash(source.get("merged_hash")) or not source.get("target_branch")
                or any(merge.get(key) != source[key] for key in ("merged_hash", "target_branch"))):
            raise ValueError("The repair refers to another publication source")
        return {"confirmed": True}
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        return {"confirmed": False, "summary": str(error)}
