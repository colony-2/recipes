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
            type(policy["version"]) is not int or policy["version"] != 2 or
            type(policy["require_verification"]) is not bool or type(policy["settings"]) is not dict):
        raise ValueError("Invalid verification policy")
    directory = policy["target_directory"]
    if (not isinstance(directory, str) or not directory or posixpath.normpath(directory) != directory or
            directory.startswith(("/", "../")) or directory == ".." or "\0" in directory or "\\" in directory):
        raise ValueError("Verification directory must be normalized and inside the cell")
    return json.dumps(policy, sort_keys=True, separators=(",", ":"))


def artifact_ref(ref):
    if type(ref) is not dict:
        return False
    if ref.get("kind") == "value":
        return ("value" in ref and ref.get("format") in ("json", "text") and
                (ref["format"] == "json" or isinstance(ref["value"], str)))
    if ref.get("kind") != "stored" or type(ref.get("stored")) is not dict:
        return False
    key = ref["stored"].get("key")
    return (type(key) is dict and isinstance(key.get("jobId"), str) and bool(key["jobId"]) and
            type(key.get("taskOrdinal")) is int and key["taskOrdinal"] >= 0 and
            isinstance(key.get("name"), str) and bool(key["name"]) and
            type(key.get("sizeBytes")) is int and key["sizeBytes"] >= 0)


def artifact_map(value):
    return (type(value) is dict and all(
        isinstance(name, str) and name and not name.startswith("/") and
        ".." not in name.split("/") and artifact_ref(ref) for name, ref in value.items()))


def receipt_key(receipt, contribution, policy):
    """Validate optional saved evidence before deduplication, preserving its producer."""
    if type(receipt) is not dict or set(receipt) != {"job_id", "identity", "result", "artifacts"}:
        return None
    identity, result = receipt["identity"], receipt["result"]
    if (not isinstance(receipt["job_id"], str) or
            re.fullmatch(r"[A-Za-z0-9_-]+", receipt["job_id"]) is None or
            receipt["job_id"] != contribution["job_id"] or type(identity) is not dict or
            set(identity) != {"candidate", "base", "request", "target_directory", "documents", "settings", "required"} or
            identity["candidate"] != contribution["head_hash"] or
            identity["base"] != contribution["base_hash"] or
            not isinstance(identity["request"], str) or not artifact_map(identity["documents"]) or
            type(identity["required"]) is not bool or identity["required"] != policy["require_verification"] or
            identity["target_directory"] != policy["target_directory"] or
            type(identity["settings"]) is not dict or
            json.dumps(identity["settings"], sort_keys=True) != json.dumps(policy["settings"], sort_keys=True) or
            type(result) is not dict or result.get("api_version") != "c2.build-hook/v1" or
            result.get("status") not in ("passed", "failed", "skipped", "changes") or
            not isinstance(result.get("summary"), str) or not result["summary"] or
            not artifact_map(result.get("artifact_refs")) or not artifact_map(receipt["artifacts"])):
        return None
    # Log names, summaries and producers may differ between equivalent checks.
    return json.dumps([identity, result["status"], "failure" in result], sort_keys=True)


def reusable_receipt(assembly, contributions, policy):
    """Select evidence only for an accounted, applied, exact supplied publication head."""
    policy_key(policy)
    rows = assembly["results"]
    if ([row["changeid"] for row in rows] != [item["changeid"] for item in contributions] or
            assembly["head"] == assembly["base"]):
        return None
    for item, row in zip(contributions, rows):
        receipt = item.get("verification")
        if (row["status"] == "applied" and row.get("hash") == assembly["head"] == item["head_hash"] and
                receipt_key(receipt, item, policy) is not None and
                "failure" not in receipt["result"] and
                (receipt["result"]["status"] == "passed" or
                 (receipt["result"]["status"] == "skipped" and not policy["require_verification"]))):
            return receipt
    return None


def validate_contribution(append, content, repository, branch, authority):
    if type(content.get("version")) is not int or content["version"] != 2:
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
    documents = content.get("documents", {})
    if not isinstance(documents, dict):
        raise ValueError("Contribution documents must be named artifact references")
    for name, document in documents.items():
        if (not safe_name(name) or not isinstance(document, dict) or
                document.get("kind") != "stored" or not isinstance(document.get("stored"), dict)):
            raise ValueError("Contribution document needs a safe alias and stored reference")
    expected = [ref, *documents.values()]
    identities = [json.dumps(item.get("stored"), sort_keys=True) for item in expected
                  if isinstance(item, dict)]
    if len(identities) != len(set(identities)):
        raise ValueError("Bundle and document references must not be duplicated")
    if (not isinstance(refs, list) or not owner or owner != content.get("job_id") or
            ref.get("kind") != "stored" or len(refs) != len(expected) or
            any(not isinstance(item, dict) for item in refs) or
            sorted(json.dumps(item.get("stored"), sort_keys=True) for item in refs) !=
            sorted(json.dumps(item.get("stored"), sort_keys=True) for item in expected)):
        raise ValueError("Contribution bundle and documents must be bound to their originating references")


def safe_name(name):
    return (isinstance(name, str) and bool(name) and name not in {".", ".."} and
            not name.startswith(("/", "../")) and "\\" not in name and
            all(ord(char) >= 32 and ord(char) != 127 for char in name) and
            posixpath.normpath(name) == name)


def screen_contributions(appends, repository, branch, policy):
    """Return eligible contributions and the reasons for per-change rejection."""
    authority = policy_key(policy)
    accepted = {}
    rejected = {}
    evidence = {}
    ambiguous = set()
    source_fields = ("repository", "base_hash", "head_hash", "initial_submitted_at", "documents")
    for append in appends:
        content = append.get("content") if isinstance(append, dict) else None
        change_id = content.get("changeid") if isinstance(content, dict) else None
        if not is_change_id(change_id):
            raise UnidentifiedContribution(rejected)
        try:
            validate_contribution(append, content, repository, branch, authority)
            content = dict(content, documents=content.get("documents", {}))
            previous = accepted.get(change_id)
            if previous and any(previous[key] != content[key] for key in source_fields):
                raise ValueError("Duplicate Change-Id names different source commits or submission times")
            item = accepted.setdefault(change_id, {key: content[key] for key in
                                                  ("changeid", *source_fields, "thinpack_ref", "job_id")})
            if "verification" in content:
                receipt = content["verification"]
                key = receipt_key(receipt, content, policy)
                if key is None or (change_id in evidence and evidence[change_id] != key):
                    ambiguous.add(change_id)
                elif change_id not in evidence:
                    evidence[change_id] = key
                    item["verification"] = receipt
                    # Evidence remains bound to its producer even if the first append had none.
                    item["job_id"] = content["job_id"]
        except ValueError as error:
            rejected[change_id] = str(error)

    eligible = [item for change_id, item in accepted.items() if change_id not in rejected]
    for item in eligible:
        if item["changeid"] in ambiguous:
            item.pop("verification", None)
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


def caller_receipt(receipt, own, branch, owner_job):
    """Return one caller's result only after validating the whole receipt."""
    if not isinstance(receipt, dict) or type(receipt.get("version")) is not int:
        return {}
    if receipt["version"] != 2 or receipt.get("branch") != branch:
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
    publication = receipt.get("publication")
    if not valid_publication(publication, branch, owner_job):
        return {}
    return {"own": by_id[own], "queue_publication": publication}


def valid_publication(publication, branch, owner_job):
    if not isinstance(publication, dict) or not owner_job or publication.get("owner_job") != owner_job:
        return False
    result = publication.get("result")
    if (not isinstance(result, dict) or not set(result) <= {"api_version", "status", "summary", "artifact_refs", "failure"} or
            ("failure" in result and not isinstance(result["failure"], dict)) or
            result.get("api_version") != "c2.build-hook/v1" or
            result.get("status") not in {"passed", "skipped", "failed"} or
            not isinstance(result.get("summary"), str) or not result["summary"].strip() or len(result["summary"]) > 8192 or
            not isinstance(result.get("artifact_refs"), dict)):
        return False
    source = publication.get("source")
    if publication.get("reason") == "no-new-merge":
        return source is None and result["status"] == "skipped"
    return (publication.get("reason") == "hook" and isinstance(source, dict) and
            set(source) == {"merged_hash", "target_branch"} and is_hash(source.get("merged_hash")) and source.get("target_branch") == branch)


def publication_context(landing, branch, owner_job, contributions):
    """Bind the hook to the recorded final native merge, never receipt-row order."""
    merge = landing.get("merge", {})
    if not merge:
        return {"owner_job": owner_job, "source": None, "reason": "no-new-merge",
                "result": {"api_version": "c2.build-hook/v1", "status": "skipped",
                           "summary": "No new merge; no publication hook ran.", "artifact_refs": {}}}
    head, base = landing.get("verified_head"), landing.get("base")
    if (not owner_job or not is_hash(base) or not is_hash(head) or head == base or
            merge.get("merged_hash") != head or merge.get("target_branch") != branch):
        raise ValueError("Native merge does not match the verified publication source and branch")
    accepted = landing.get("accepted", [])
    if not accepted or not all(is_change_id(item) for item in accepted) or len(accepted) != len(set(accepted)):
        raise ValueError("Publication requires accepted contribution identities")
    by_id = {item["changeid"]: item for item in contributions}
    if not set(accepted) <= by_id.keys():
        raise ValueError("Publication identifies an unknown contribution")
    documents = {f"contributions/{change_id}/{name}": dict(ref, name=f"contributions/{change_id}/{name}")
                 for change_id in accepted for name, ref in by_id[change_id].get("documents", {}).items()}
    return {"owner_job": owner_job, "source": {"merged_hash": head, "target_branch": branch},
            "reason": "hook", "base": base, "merge": merge, "accepted": accepted,
            "request": f"Publish merged batch on {branch}: " + ", ".join(accepted), "documents": documents}



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
