"""Git worktree and artifact operations for the Adaptive3 merge queue."""

import posixpath
import re
import secrets
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from policy import UnidentifiedContribution, is_change_id, is_hash, screen_contributions, reusable_receipt


class GitError(RuntimeError):
    pass


class InvalidContribution(ValueError):
    pass


class Git:
    def __init__(self, path):
        self.path = path

    def run(self, *args, data=None, check=True):
        command = ["git", "-C", str(self.path), "-c", "core.hooksPath=/dev/null", *args]
        result = subprocess.run(command, input=data, capture_output=True)
        if check and result.returncode:
            detail = result.stderr.decode(errors="replace").strip()
            raise GitError(f"git {args[0]}: {detail or f'exited {result.returncode}'}")
        return result

    def read(self, *args, data=None):
        return self.run(*args, data=data).stdout

    def head(self):
        return self.read("rev-parse", "HEAD").decode().strip()

    def is_shallow(self):
        return self.read("rev-parse", "--is-shallow-repository").strip() == b"true"

    def deepen(self, branch):
        if self.is_shallow():
            self.run("fetch", "--unshallow", "--no-tags", "origin", branch)

    def require_clean(self, expected):
        git_dir = Path(self.read("rev-parse", "--absolute-git-dir").decode().rstrip("\n"))
        in_progress = (
            "CHERRY_PICK_HEAD", "REVERT_HEAD", "REBASE_HEAD", "MERGE_HEAD",
            "rebase-merge", "rebase-apply", "sequencer",
        )
        if (self.head() != expected or self.read("status", "--porcelain", "--untracked-files=all") or
                any((git_dir / name).exists() for name in in_progress)):
            raise GitError("Git workspace differs from the expected clean, inactive checkout")


def prepare_candidate(repo, base, message, previous):
    head = repo.head()
    changed = repo.read("rev-parse", base + "^{tree}") != repo.read("rev-parse", head + "^{tree}")
    existing = previous.get("head_hash") == head and previous.get("base_hash") == base
    result = {"changed": changed, "existing": existing}
    if changed and not existing:
        timestamp = (int(time.time()) - 1400000000).to_bytes(4, "big")
        value = int.from_bytes(timestamp + secrets.token_bytes(16), "big")
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        encoded = ""
        while value:
            value, remainder = divmod(value, 62)
            encoded = alphabet[remainder] + encoded
        change_id = encoded.rjust(27, "0")
        message = "\n".join(line for line in message.splitlines()
                            if not re.match(r"^Change-Id:", line, flags=re.I)).strip()
        result.update(changeid=change_id, message=f"{message}\n\nChange-Id: {change_id}")
    return result


def identify_submission(repo, base, expected_head, expected_base, ref, target_directory, submitted_at):
    if repo.head() != expected_head or base != expected_base:
        return {"verified": False}

    if re.fullmatch(r"[0-9a-fA-F]{40}", ref) or (ref.startswith("refs/") and not ref.startswith("refs/heads/")):
        raise ValueError("A merge queue requires a target branch")
    branch = ref if ref.startswith("refs/heads/") else "refs/heads/" + ref
    repo.run("check-ref-format", branch)
    directory = posixpath.normpath(target_directory)
    if directory.startswith(("/", "../")) or directory == ".." or "\\" in directory:
        raise ValueError("Verification directory must stay inside the cell")
    if not submitted_at:
        seconds, nanos = divmod(time.time_ns(), 1000000000)
        submitted_at = f"{time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(seconds))}.{nanos:09d}Z"
    return {"verified": True, "branch": branch, "directory": directory, "age": submitted_at}


def landed_hashes(repo, ids, base, branch):
    if not ids:
        return {}
    repo.deepen(branch)
    history = repo.read("log", "-z", "--format=%H%x00%(trailers:key=Change-Id,valueonly,separator=%x1f)", base)
    parts = history.split(b"\0")
    found = {}
    for commit, values in zip(parts[::2], parts[1::2]):
        for raw_id in values.strip().split(b"\x1f"):
            change_id = raw_id.decode(errors="replace")
            if change_id in ids:
                if change_id in found:
                    raise GitError(f"Upstream contains multiple Change-Id trailers for {change_id}")
                found[change_id] = commit.decode()
    if ids - found.keys() and repo.is_shallow():
        raise GitError("Incomplete published history cannot establish whether candidate IDs already landed")
    return found


def intake(repo, outbox, branch, repository, policy, appends):
    if not branch.startswith("refs/heads/"):
        raise ValueError("Queue requires a canonical branch ref")
    repo.run("check-ref-format", branch)
    base = repo.head()
    try:
        queued, rejected = screen_contributions(appends, repository, branch, policy)
    except UnidentifiedContribution as error:
        write_rejections(outbox, error.rejected)
        raise
    write_rejections(outbox, rejected)
    results = [{"changeid": change_id, "status": "fail-validation"} for change_id in rejected]
    landed = landed_hashes(repo, {item["changeid"] for item in queued}, base, branch)
    results.extend(
        {"changeid": change_id, "status": "success", "hash": commit}
        for change_id, commit in landed.items()
    )
    pending = [item for item in queued if item["changeid"] not in landed]
    return {"base": base, "pending": pending, "results": results}


def write_rejections(outbox, rejected):
    for change_id, reason in rejected.items():
        (outbox / f"{change_id}.log").write_text(reason + "\n", encoding="utf-8")


def source_parts(repo, source, parent, change_id):
    raw = repo.read("cat-file", "commit", source)
    headers, message = raw.split(b"\n\n", 1)
    lines = headers.split(b"\n")
    if [line for line in lines if line.startswith(b"parent ")] != [b"parent " + parent.encode()]:
        raise InvalidContribution("Advertised source must have the declared base as its sole parent")
    trailers = repo.read("interpret-trailers", "--parse", data=message).splitlines()
    keys = [line for line in trailers if line.lower().startswith(b"change-id:")]
    if keys != [b"Change-Id: " + change_id.encode()]:
        raise InvalidContribution("Source commit must carry exactly one matching Change-Id trailer")
    metadata = [line for line in lines if line.startswith((b"author ", b"committer ", b"encoding "))]
    return metadata, message


def replay(repo, published, previous, contribution, repository, inbox, outbox):
    source, base, change_id = (contribution[key] for key in ("head_hash", "base_hash", "changeid"))
    if contribution["repository"] != repository or not is_hash(source) or not is_hash(base):
        raise InvalidContribution("Repository or source hashes do not match the contribution contract")
    if repo.read("cat-file", "-t", base) != b"commit\n":
        raise InvalidContribution("Declared base must be a commit")
    ancestry = repo.run("merge-base", "--is-ancestor", base, published, check=False)
    if ancestry.returncode == 1:
        raise InvalidContribution("Source base is outside the pinned branch history")
    if ancestry.returncode:
        raise GitError("Could not establish source base history")
    bundle = inbox / "contributions" / f"{change_id}.bundle"
    with bundle.open("rb"):
        advertised = repo.run("bundle", "list-heads", str(bundle), check=False)
    heads = advertised.stdout.splitlines()
    if advertised.returncode or len(heads) != 1 or heads[0].split(b" ", 1)[0] != source.encode():
        raise InvalidContribution("Bundle must advertise exactly the declared source commit")
    repo.run("bundle", "verify", str(bundle))
    repo.run("bundle", "unbundle", str(bundle))
    if repo.read("cat-file", "-t", source) != b"commit\n":
        raise InvalidContribution("Advertised source is not a commit")
    metadata, message = source_parts(repo, source, base, change_id)

    repaired = contribution.get("repair_base") == previous
    if repaired:
        patch = inbox / "repairs" / f"{change_id}.diff"
        if patch.stat().st_size:
            repo.run("apply", "--index", "--binary", str(patch))
    else:
        picked = repo.run("cherry-pick", "--no-commit", source, check=False)
        if picked.returncode:
            if not repo.read("ls-files", "--unmerged", "-z"):
                detail = picked.stderr.decode(errors="replace").strip()
                raise GitError(f"Replay failed without Git conflict entries: {detail}")
            (outbox / f"{change_id}.log").write_bytes(
                picked.stdout + picked.stderr + b"\n" + repo.read("status", "--porcelain=v1"))
            (outbox / f"{change_id}.diff").write_bytes(repo.read(
                "diff", "--binary", "--full-index", "--no-ext-diff", "--no-textconv", base, source, "--"))
            (outbox / f"{change_id}.paths").write_bytes(
                repo.read("diff", "--name-only", "--no-renames", "-z", base, source, "--"))
            repo.run("reset", "--hard", previous)
            repo.require_clean(previous)
            return {"changeid": change_id, "status": "fail-conflict", "previous_head": previous}

    tree = repo.read("write-tree").strip()
    parent_tree = repo.read("rev-parse", previous + "^{tree}").strip()
    # Retain the original author, committer, encoding, and message bytes.
    commit = b"\n".join([b"tree " + tree, b"parent " + previous.encode(), *metadata])
    applied = repo.read("hash-object", "-t", "commit", "-w", "--stdin",
                        data=commit + b"\n\n" + message).decode().strip()
    repo.run("reset", "--hard", applied)
    repo.require_clean(applied)
    return {
        "changeid": change_id, "status": "applied", "previous_head": previous,
        "source_head": source, "hash": applied, "empty": tree == parent_tree, "repaired": repaired,
    }


def assemble(receiving, inbox, outbox, base, branch, repository, contributions):
    if not is_hash(base):
        raise ValueError("Expected a full, pinned base hash")
    ids = [contribution["changeid"] for contribution in contributions]
    if not all(is_change_id(value) for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("Replay requires unique, validated change IDs")
    receiving.require_clean(base)
    if any(item["base_hash"] != base for item in contributions):
        receiving.deepen(branch)

    results = []
    previous = base
    with tempfile.TemporaryDirectory(prefix="merge-queue-") as scratch:
        path = Path(scratch) / "assembly"
        receiving.run("clone", "--quiet", "--shared", "--no-checkout", str(receiving.path), str(path))
        repo = Git(path)
        repo.run("checkout", "--quiet", "--detach", base)
        for contribution in contributions:
            change_id = contribution["changeid"]
            try:
                result = replay(repo, base, previous, contribution, repository, inbox, outbox)
            except InvalidContribution as error:
                (outbox / f"{change_id}.log").write_text(str(error) + "\n", encoding="utf-8")
                result = {"changeid": change_id, "status": "fail-validation"}
            if result["status"] == "fail-conflict":
                result["prefix"] = [entry["changeid"] for entry in results if entry["status"] == "applied"]
            if result["status"] == "applied":
                previous = result["hash"]
            results.append(result)
        if previous != base:
            ref = "refs/heads/merge-queue-assembled"
            repo.run("update-ref", ref, previous)
            repo.run("bundle", "create", str(outbox / "assembled.bundle"), ref, "^" + base)
    receiving.require_clean(base)
    return {"base": base, "head": previous, "results": results}


def install(repo, inbox, base, head):
    if not is_hash(base) or not is_hash(head):
        raise ValueError("Merge queue installation requires full Git commit hashes")
    repo.require_clean(base)
    bundle = str(inbox / "assembled.bundle")
    if repo.read("bundle", "list-heads", bundle).splitlines() != [f"{head} refs/heads/merge-queue-assembled".encode()]:
        raise ValueError("Assembled bundle does not advertise the expected head")
    repo.run("bundle", "verify", bundle)
    repo.run("bundle", "unbundle", bundle)
    repo.run("merge-base", "--is-ancestor", base, head)

    def interrupted(signum, _frame):
        raise InterruptedError(f"Merge queue installation interrupted by signal {signum}")

    signals = (signal.SIGINT, signal.SIGTERM)
    handlers = {signum: signal.signal(signum, interrupted) for signum in signals}
    try:
        repo.run("reset", "--hard", head)
        repo.require_clean(head)
    except BaseException:
        repo.run("reset", "--hard", base)
        repo.require_clean(base)
        raise
    finally:
        for signum, handler in handlers.items():
            signal.signal(signum, handler)
    return {"head": head}


def reuse_verification(repo, assembly, contributions, policy):
    base, head = assembly["base"], assembly["head"]
    if not is_hash(base) or not is_hash(head):
        raise ValueError("Verification reuse requires full Git commit hashes")
    repo.require_clean(head)
    for commit in (base, head):
        if repo.read("cat-file", "-t", commit) != b"commit\n":
            raise GitError("Verification reuse requires readable commits")
    ancestry = repo.run("merge-base", "--is-ancestor", base, head, check=False)
    if ancestry.returncode not in (0, 1):
        raise GitError("Could not establish fast-forward ancestry")
    receipt = reusable_receipt(assembly, contributions, policy)
    if ancestry.returncode or receipt is None:
        return {"reused": False}
    prefix = f"verification/{receipt['job_id']}/"
    artifacts = {prefix + name: dict(ref, name=prefix + name) for name, ref in receipt["artifacts"].items()}
    result = dict(receipt["result"], summary=(
        f"Reused verification from job {receipt['job_id']} for exact commit {head}. " + receipt["result"]["summary"]))
    return {"reused": True, "receipt": receipt, "verified_head": head,
            "verification": result, "artifacts": artifacts}


def capture_repair(repo, inbox, outbox, prefix, summary):
    permitted = set((inbox / "original.paths").read_bytes().split(b"\0"))
    touched = set(repo.read("diff", "--no-renames", "--name-only", "-z", prefix, "HEAD", "--").split(b"\0"))
    if not touched <= permitted or repo.run("merge-base", "--is-ancestor", prefix, "HEAD", check=False).returncode:
        return {}
    patch = repo.read("diff", "--binary", "--full-index", "--no-renames", "--no-ext-diff", "--no-textconv",
                      prefix, "HEAD", "--")
    (outbox / "repair.diff").write_bytes(patch)
    (outbox / "repair.txt").write_text(summary + "\n", encoding="utf-8")
    return {}


def confirm_landed(repo, branch, landed, change_id):
    try:
        if landed != repo.head():
            repo.deepen(branch)
        repo.run("merge-base", "--is-ancestor", landed, "HEAD")
        trailers = repo.read("log", "-1", "--format=%(trailers:key=Change-Id,valueonly)", landed)
    except GitError as error:
        print(error, file=sys.stderr)
        return {"confirmed": False}
    return {"confirmed": trailers.strip() == change_id.encode()}
