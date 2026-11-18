"""Merge queue decisions over contributions and recorded verification."""

import datetime
import json
import posixpath
import re


class UnidentifiedContribution(ValueError):
    def __init__(self, rejected):
        super().__init__("Queue append does not identify a usable Change-Id")
        self.rejected = rejected


def is_hash(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def is_change_id(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9A-Za-z]{27}", value) is not None


def policy_key(policy):
    if (type(policy) is not dict or set(policy) !=
            {"version", "require_verification", "target_directory", "settings"} or
            type(policy["version"]) is not int or policy["version"] != 1 or
            type(policy["require_verification"]) is not bool or type(policy["settings"]) is not dict):
        raise ValueError("Invalid verification policy")
    directory = policy["target_directory"]
    if (not isinstance(directory, str) or not directory or posixpath.normpath(directory) != directory or
            directory.startswith(("/", "../")) or directory == ".." or "\0" in directory or "\\" in directory):
        raise ValueError("Verification directory must be normalized and inside the cell")
    return json.dumps(policy, sort_keys=True, separators=(",", ":"))


def validate_contribution(append, content, repository, branch, authority):
    if type(content.get("version")) is not int or content["version"] != 1:
        raise ValueError("Unknown merge queue contribution version")
    if content.get("repository") != repository or content.get("branch") != branch:
        raise ValueError("Contribution target differs from the batch target")
    if policy_key(content.get("verification_policy")) != authority:
        raise ValueError("Contribution verification policy differs from the batch policy")
    if any(not is_hash(content.get(key)) for key in ("base_hash", "head_hash")):
        raise ValueError("Contribution requires full Git hashes")
    age = content.get("initial_submitted_at")
    if not isinstance(age, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{9}Z", age):
        raise ValueError("Contribution is missing its initial UTC submission time")
    datetime.datetime.fromisoformat(age[:19])

    refs = append.get("artifacts", [])
    ref = content.get("thinpack_ref")
    stored = ref.get("stored") if isinstance(ref, dict) else None
    key = stored.get("key") if isinstance(stored, dict) else None
    owner = key.get("jobId") if isinstance(key, dict) else None
    if (not isinstance(refs, list) or len(refs) != 1 or not isinstance(refs[0], dict) or
            not owner or owner != content.get("job_id") or ref.get("kind") != "stored" or
            refs[0].get("stored") != stored):
        raise ValueError("Contribution bundle must be bound to its originating job")


def screen_contributions(appends, repository, branch, policy):
    """Return eligible contributions and the reasons for per-change rejection."""
    authority = policy_key(policy)
    accepted = {}
    rejected = {}
    source_fields = ("repository", "base_hash", "head_hash", "initial_submitted_at")
    for append in appends:
        content = append.get("content") if isinstance(append, dict) else None
        change_id = content.get("changeid") if isinstance(content, dict) else None
        if not is_change_id(change_id):
            raise UnidentifiedContribution(rejected)
        try:
            validate_contribution(append, content, repository, branch, authority)
            previous = accepted.get(change_id)
            if previous and any(previous[key] != content[key] for key in source_fields):
                raise ValueError("Duplicate Change-Id names different source commits or submission times")
            accepted.setdefault(change_id, {key: content[key] for key in
                                           ("changeid", *source_fields, "thinpack_ref")})
        except ValueError as error:
            rejected[change_id] = str(error)

    eligible = [item for change_id, item in accepted.items() if change_id not in rejected]
    eligible.sort(key=lambda item: (item["initial_submitted_at"], item["changeid"]))
    return eligible, rejected


def plan_probes(ids, evidence):
    """Find the next bounded set of probes, or select the oldest passing work."""
    full = tuple(ids)
    checks = {tuple(check["ids"]): check["passed"] for check in evidence}

    def priority(group):
        return tuple(item in group for item in ids)

    def unseen(groups):
        return sorted(set(groups) - checks.keys(), key=priority, reverse=True)

    def split(group):
        if group not in checks:
            yield group
        elif not checks[group] and len(group) > 1:
            middle = len(group) // 2
            yield from split(group[:middle])
            yield from split(group[middle:])

    def combine(left, right):
        return tuple(item for item in ids if item in left or item in right)

    probes = unseen(split(full))[:4]
    if not probes:
        passing = [group for group, passed in checks.items() if passed]
        best = max(passing, key=priority)
        trials = []
        for offset, item in enumerate(ids):
            if item in best:
                continue
            older = tuple(previous for previous in ids[:offset] if previous in best)
            support = [(item,)] + [group for group in passing if item in group]
            for group in support:
                trials.extend((combine(best, group), combine(older, group)))
        probes = unseen(group for group in trials if priority(group) > priority(best))[:4]
        if not probes:
            return {"probes": [], "selected": best}

    if len(checks) + len(probes) > 4 * len(ids) + 1:
        raise RuntimeError("Bounded merge queue subset search needs more evidence")
    return {"probes": probes}


def record_probes(cases, children, policy, base):
    """Turn one complete wave of native child receipts into planner evidence."""
    expected = {str(index): ids for index, ids in enumerate(cases)}
    records = {}
    authority = policy_key(policy)
    for child in children:
        key = child.get("key")
        if key not in expected or key in records or child.get("status") != "completed":
            raise ValueError("Missing, duplicate or incomplete merge queue check")
        ids = expected[key]
        output = child["outputs"]
        assembly = output["assembly"]
        verification = output["verification"]
        head = assembly["head"]
        if policy_key(output["policy"]) != authority or assembly["base"] != base:
            raise ValueError("Merge queue check used a different base or verification policy")
        if not is_hash(head) or (head != base and output.get("verified_head") != head):
            raise ValueError("Merge queue check did not verify its assembled head")
        if [row["changeid"] for row in assembly["results"]] != ids:
            raise ValueError("Merge queue check did not account for its requested changes")
        if "failure" in verification or verification["status"] not in {"passed", "skipped", "changes"}:
            raise ValueError("Merge queue check returned an operational failure")
        records[key] = {
            "ids": ids,
            "passed": (
                verification["status"] in {"passed", "skipped"} and
                all(row["status"] == "applied" for row in assembly["results"])
            ),
            "logs": output["artifacts"],
            "summary": verification["summary"],
        }
    if records.keys() != expected.keys():
        raise ValueError("Missing merge queue check receipts")
    return {"checks": [records[key] for key in expected]}


def caller_receipt(receipt, own, branch):
    """Return one caller's result only after validating the whole receipt."""
    if not isinstance(receipt, dict) or type(receipt.get("version")) is not int:
        return {}
    if receipt["version"] != 1 or receipt.get("branch") != branch:
        return {}

    requested = receipt.get("requested")
    rows = receipt.get("results")
    if not isinstance(requested, list) or not isinstance(rows, list) or len(requested) != len(rows):
        return {}
    if not all(is_change_id(change_id) for change_id in requested):
        return {}

    by_id = {}
    for row in rows:
        if not isinstance(row, dict) or not is_change_id(row.get("changeid")):
            return {}
        change_id, status = row["changeid"], row.get("status")
        if change_id in by_id:
            return {}
        if status == "success":
            if not is_hash(row.get("hash")):
                return {}
        elif status in ("fail-conflict", "fail-validation"):
            logs = row.get("failure_logs", [])
            if not isinstance(logs, list) or (status == "fail-validation" and not logs):
                return {}
        else:
            return {}
        by_id[change_id] = row
    if sorted(by_id) != requested or own not in by_id:
        return {}
    return {"own": by_id[own]}


def landing_results(outbox, landed, replay, replay_logs, evidence):
    """Collect per-change receipts and write any new short diagnostic logs."""
    results = list(landed)
    landed_ids = {row["changeid"] for row in landed}
    for row in replay:
        change_id = row["changeid"]
        if change_id in landed_ids:
            continue
        if not is_change_id(change_id):
            raise ValueError("Invalid Change-Id in the assembly result")
        name = f"{change_id}.log"
        status = row["status"]
        if status in ("fail-conflict", "fail-validation"):
            results.append({"changeid": change_id, "status": status, "failure_logs": [replay_logs[name]]})
            continue
        if status != "applied":
            raise ValueError(f"Unknown replay result for {change_id}: {status}")

        failures = [probe for probe in evidence if not probe["passed"] and change_id in probe["ids"]]
        if not failures:
            raise RuntimeError(f"Missing validation evidence for {change_id}")
        summaries = dict.fromkeys(probe["summary"] for probe in failures)
        (outbox / name).write_text("\n".join(summaries) + "\n", encoding="utf-8")
        logs = [ref for probe in failures for key, ref in probe["logs"].items() if key != "assembled.bundle"]
        results.append({
            "changeid": change_id,
            "status": "fail-validation",
            "failure_logs": logs,
            "log_name": name,
        })
    return {"results": results}
