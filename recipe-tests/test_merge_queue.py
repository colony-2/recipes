import copy
import itertools
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "recipes" / "merge-queue"))

from git_work import Git, install
from policy import UnidentifiedContribution, caller_receipt, landing_results, plan_probes, record_probes, screen_contributions


BASE = "a" * 40
HEAD = "b" * 40
BRANCH = "refs/heads/main"
REPOSITORY = "https://example.test/cell.git"
POLICY = {"version": 1, "require_verification": True, "target_directory": ".", "settings": {}}
OLDER, NEWER, YOUNGEST = (f"{number:027d}" for number in range(1, 4))


def evidence(results):
    return [{"ids": list(ids), "passed": passed} for ids, passed in results.items()]


def append(change_id, age, *, policy=POLICY, head=HEAD):
    bundle = {"kind": "stored", "stored": {"key": {"jobId": "producer", "index": 0}}}
    return {
        "artifacts": [bundle],
        "content": {
            "version": 1, "changeid": change_id, "repository": REPOSITORY, "branch": BRANCH,
            "base_hash": BASE, "head_hash": head, "initial_submitted_at": age,
            "thinpack_ref": bundle, "job_id": "producer", "verification_policy": policy,
        },
    }


class MergeQueuePolicyTest(unittest.TestCase):
    def test_screening_preserves_age_and_excludes_incompatible_or_ambiguous_changes(self):
        oldest = append(OLDER, "2026-11-18T12:00:00.000000001Z")
        newer = append(NEWER, "2026-11-18T12:00:00.000000010Z")
        reordered_policy = dict(reversed(list(POLICY.items())))
        eligible, rejected = screen_contributions([newer, oldest], REPOSITORY, BRANCH, reordered_policy)
        self.assertEqual([row["changeid"] for row in eligible], [OLDER, NEWER])
        self.assertEqual(rejected, {})

        other_policy = dict(POLICY, require_verification=False)
        ineligible = append(YOUNGEST, "2026-11-18T12:00:00.100000000Z", policy=other_policy)
        duplicate = append(NEWER, newer["content"]["initial_submitted_at"], head="c" * 40)
        eligible, rejected = screen_contributions(
            [newer, oldest, ineligible, duplicate], REPOSITORY, BRANCH, POLICY)
        self.assertEqual([row["changeid"] for row in eligible], [OLDER])
        self.assertIn("Duplicate Change-Id", rejected[NEWER])
        self.assertIn("differs from the batch policy", rejected[YOUNGEST])

        with self.assertRaises(UnidentifiedContribution) as unreadable:
            screen_contributions([ineligible, {}], REPOSITORY, BRANCH, POLICY)
        self.assertIn("differs from the batch policy", unreadable.exception.rejected[YOUNGEST])

    def test_plan_prefers_older_passing_change_over_larger_younger_stack(self):
        ids = [OLDER, NEWER, YOUNGEST]
        checked = evidence({
            (): True, tuple(ids): False, (OLDER,): True, (NEWER, YOUNGEST): True,
            (OLDER, NEWER): False, (OLDER, YOUNGEST): False,
        })
        self.assertEqual(plan_probes(ids, checked), {"probes": [], "selected": (OLDER,)})

    def test_plan_bounds_the_next_wave_and_stops_when_budget_is_exhausted(self):
        ids = list("abcdefgh")
        checked = evidence({(): True, tuple(ids): False, tuple(ids[:4]): False, tuple(ids[4:]): False})
        self.assertEqual(plan_probes(ids, checked)["probes"], [("a", "b"), ("c", "d"), ("e", "f"), ("g", "h")])

        ids = list("abcde")
        checked = evidence({
            group: not group
            for size in range(len(ids) + 1)
            for group in itertools.combinations(ids, size)
            if group != ("a", "b")
        })
        with self.assertRaisesRegex(RuntimeError, "subset search needs more evidence"):
            plan_probes(ids, checked)

    def test_record_rejects_missing_duplicate_or_mismatched_checks(self):
        check = {
            "key": "0", "status": "completed",
            "outputs": {
                "assembly": {"base": BASE, "head": HEAD, "results": [{"changeid": OLDER, "status": "applied"}]},
                "verified_head": HEAD, "policy": POLICY, "artifacts": {},
                "verification": {"status": "passed", "summary": "Checked the candidate."},
            },
        }
        records = record_probes([[OLDER]], [check], POLICY, BASE)["checks"]
        self.assertTrue(records[0]["passed"])
        self.assertEqual(records[0]["ids"], [OLDER])
        with self.assertRaisesRegex(ValueError, "Missing merge queue check"):
            record_probes([[OLDER]], [], POLICY, BASE)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            record_probes([[OLDER]], [check, check], POLICY, BASE)

        for key, value in {
            "verified_head": BASE,
            "policy": dict(POLICY, require_verification=False),
            "assembly": {"base": HEAD, "head": HEAD, "results": []},
            "verification": {"status": "changes", "failure": {"kind": "task_error"}},
        }.items():
            with self.subTest(key=key):
                rejected = copy.deepcopy(check)
                rejected["outputs"][key] = value
                with self.assertRaises(ValueError):
                    record_probes([[OLDER]], [rejected], POLICY, BASE)
        with self.assertRaisesRegex(ValueError, "did not account for"):
            record_probes([[NEWER]], [check], POLICY, BASE)

    def test_complete_receipt_releases_only_the_callers_own_result(self):
        own = {"changeid": OLDER, "status": "success", "hash": HEAD}
        other = {"changeid": NEWER, "status": "fail-conflict"}
        receipt = {"version": 1, "branch": BRANCH, "requested": [OLDER, NEWER], "results": [other, own]}
        self.assertEqual(caller_receipt(receipt, OLDER, BRANCH), {"own": own})
        self.assertEqual(caller_receipt(receipt, YOUNGEST, BRANCH), {})
        for changes in (
            {"branch": "refs/heads/other"},
            {"results": [own, own]},
            {"results": [own, dict(other, status="fail-validation")]},
            {"results": [dict(own, hash="invalid"), other]},
            {"requested": [OLDER, YOUNGEST]},
        ):
            with self.subTest(changes=changes):
                self.assertEqual(caller_receipt(dict(receipt, **changes), OLDER, BRANCH), {})

    def test_landing_results_attach_validation_evidence_without_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            outbox = Path(temporary)
            replay = [{"changeid": OLDER, "status": "applied"}, {"changeid": NEWER, "status": "fail-conflict"}]
            replay_logs = {f"{NEWER}.log": {"name": "conflict.log"}}
            failures = [
                {"ids": [OLDER], "passed": False, "summary": "Verifier failed.",
                 "logs": {"stdout.log": {"name": "stdout.log"}, "assembled.bundle": {"name": "assembled.bundle"}}},
                {"ids": [OLDER], "passed": False, "summary": "Verifier failed.", "logs": {}},
            ]
            rows = landing_results(outbox, [], replay, replay_logs, failures)["results"]
            self.assertEqual(rows[0]["failure_logs"], [{"name": "stdout.log"}])
            self.assertEqual((outbox / rows[0]["log_name"]).read_text(), "Verifier failed.\n")
            self.assertEqual(rows[1]["failure_logs"], [{"name": "conflict.log"}])


class MergeQueueInstallTest(unittest.TestCase):
    def test_install_checks_the_advertised_head_before_changing_the_workspace(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            worktree = root / "git"
            worktree.mkdir()
            repo = Git(worktree)
            repo.run("init", "--quiet")
            repo.run("config", "user.name", "Merge Queue Test")
            repo.run("config", "user.email", "merge-queue@example.test")
            repo.run("commit", "--quiet", "--allow-empty", "-m", "Base")
            base = repo.head()
            binary = worktree / "program"
            binary.write_bytes(b"\x00\xfe\xff\x00")
            binary.chmod(0o755)
            repo.run("add", "program")
            repo.run("commit", "--quiet", "-m", "Candidate")
            head = repo.head()
            ref = "refs/heads/merge-queue-assembled"
            repo.run("update-ref", ref, head)
            repo.run("bundle", "create", str(root / "assembled.bundle"), ref, "^" + base)
            repo.run("checkout", "--quiet", "--detach", base)

            with self.assertRaisesRegex(ValueError, "does not advertise"):
                install(repo, root, base, "f" * 40)
            repo.require_clean(base)
            self.assertFalse(binary.exists())
            self.assertEqual(install(repo, root, base, head), {"head": head})
            self.assertEqual(binary.read_bytes(), b"\x00\xfe\xff\x00")
            self.assertTrue(binary.stat().st_mode & 0o100)
            repo.require_clean(head)
