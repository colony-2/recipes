"""Check a restarted receiver against the original job's retained merge evidence."""

import json
import subprocess
import tempfile
from pathlib import Path

from policy import is_hash


def inspect(command, job, *options):
    with tempfile.TemporaryDirectory() as scratch:
        output = Path(scratch) / "inspection.json"
        subprocess.run(["c2j", "job", command, job, *options, "--output", str(output)], check=True)
        return json.loads(output.read_bytes())


def pages(command, job, field, *options):
    args = []
    cursors = set()
    while True:
        page = inspect(command, job, "--json", "--limit", "50", *options, *args)
        if page["job"]["id"] != job:
            raise ValueError("Task inspection returned another receiver")
        yield from page.get(field, [])
        cursor = page.get("next_cursor")
        if not cursor:
            return
        if cursor in cursors:
            raise ValueError("Task inspection returned a repeated cursor")
        cursors.add(cursor)
        args = ["--cursor", cursor]


def assembly_receipts(rows, job, owner):
    receipts = set()
    for row in rows:
        if (row["status"] != "succeeded" or row["type"] != "extension_execution:extension_execution"
                or "adaptive3-merge-queue-replay/" not in row.get("path", "")):
            continue
        artifacts = row.get("artifacts", [])
        if row.get("inventory_truncated"):
            artifacts = pages("artifacts", job, "artifacts", "--task", row["id"], "--attempt", str(row["attempt"]))
        for artifact in artifacts:
            key = artifact.get("reference", {}).get("stored", {}).get("key", {})
            if artifact["name"] == "assembled.bundle" and key.get("jobId") == owner:
                receipts.add((row["id"], key["taskOrdinal"], key["name"]))
    return receipts


def confirm_restart(owner, repair, source):
    try:
        original = list(pages("log", owner, "tasks"))
        repaired = pages("log", repair, "tasks")
        if not assembly_receipts(original, owner, owner).intersection(assembly_receipts(repaired, repair, owner)):
            raise ValueError("The repair has no retained assembly from the original receiver")
        merges = [row for row in original if row["type"] == "merge:merge" and row["status"] == "succeeded"
                  and "adaptive3-merge-queue-land/install/" in row.get("path", "")]
        if len(merges) != 1:
            raise ValueError("The original queue merge is missing or ambiguous")
        row = merges[0]
        merge = inspect("log", owner, "--task", row["id"], "--attempt", str(row["attempt"]), "--field", "")
        if (not isinstance(source, dict) or not is_hash(source.get("merged_hash")) or not source.get("target_branch")
                or any(merge.get(key) != source[key] for key in ("merged_hash", "target_branch"))):
            raise ValueError("The repair refers to another publication source")
        return {"confirmed": True}
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        return {"confirmed": False, "summary": str(error)}
