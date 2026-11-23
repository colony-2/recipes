import copy
import itertools
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "recipes" / "merge-queue"))

from git_work import Git, GitError, confirm_landed, install, reuse_verification
from policy import UnidentifiedContribution, caller_receipt, landing_results, plan_probes, publication_context, record_probes, screen_contributions, reusable_receipt


BASE = "a" * 40
HEAD = "b" * 40
BRANCH = "refs/heads/main"
REPOSITORY = "https://example.test/cell.git"
POLICY = {"version": 2, "require_verification": True, "target_directory": ".", "settings": {}}
OLDER, NEWER, YOUNGEST = (f"{number:027d}" for number in range(1, 4))


def evidence(results):
    return [{"ids": list(ids), "passed": passed} for ids, passed in results.items()]


def append(change_id, age, *, policy=POLICY, head=HEAD):
    bundle = {"kind": "stored", "stored": {"key": {"jobId": "producer", "taskOrdinal": 0, "name": "candidate.bundle", "sizeBytes": 1}}}
    return {
        "artifacts": [bundle],
        "content": {
            "version": 2, "changeid": change_id, "repository": REPOSITORY, "branch": BRANCH,
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
        publication = {"owner_job": "receiver", "source": {"merged_hash": HEAD, "target_branch": BRANCH},
                       "reason": "hook", "result": {"api_version": "c2.build-hook/v1", "status": "passed",
                                                    "summary": "Published.", "artifact_refs": {}}}
        receipt = {"version": 2, "branch": BRANCH, "requested": [OLDER, NEWER], "results": [other, own],
                   "publication": publication}
        self.assertEqual(caller_receipt(receipt, OLDER, BRANCH, "receiver"), {"own": own, "queue_publication": publication})
        self.assertEqual(caller_receipt(receipt, YOUNGEST, BRANCH, "receiver"), {})
        for changes in (
            {"version": 1},
            {"publication": dict(publication, owner_job="foreign")},
            {"publication": dict(publication, source={"merged_hash": "main", "target_branch": BRANCH})},
            {"publication": dict(publication, reason="no-new-merge")},
            {"publication": dict(publication, result=dict(publication["result"], status="unknown"))},
            {"branch": "refs/heads/other"},
            {"results": [own, own]},
            {"results": [own, dict(other, status="fail-validation")]},
            {"results": [dict(own, hash="invalid"), other]},
            {"requested": [OLDER, YOUNGEST]},
        ):
            with self.subTest(changes=changes):
                self.assertEqual(caller_receipt(dict(receipt, **changes), OLDER, BRANCH, "receiver"), {})

    def test_publication_comes_from_native_merge_and_only_accepted_documents(self):
        landing = {"merge": {"merged_hash": HEAD, "target_branch": BRANCH}, "base": BASE,
                   "verified_head": HEAD, "accepted": [OLDER]}
        contributions = [{"changeid": OLDER, "documents": {"review/note.md": {"stored": "accepted"}}},
                         {"changeid": NEWER, "documents": {"review/note.md": {"stored": "rejected"}}}]
        context = publication_context(landing, BRANCH, "receiver", contributions)
        self.assertEqual(context["source"], {"merged_hash": HEAD, "target_branch": BRANCH})
        self.assertEqual(context["documents"], {f"contributions/{OLDER}/review/note.md":
                                                {"stored": "accepted", "name": f"contributions/{OLDER}/review/note.md"}})
        for changes in ({"verified_head": BASE}, {"base": HEAD}, {"accepted": []},
                        {"merge": {"merged_hash": BASE, "target_branch": BRANCH}},
                        {"merge": {"merged_hash": HEAD, "target_branch": "refs/heads/other"}}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                publication_context(dict(landing, **changes), BRANCH, "receiver", contributions)
        skipped = publication_context({}, BRANCH, "receiver", [])
        self.assertIsNone(skipped["source"])
        self.assertEqual(skipped["result"]["status"], "skipped")

    def test_receipt_field_failures_are_independent_of_row_order(self):
        """R04c/QP06: each invalid field starts from a healthy unordered receipt."""
        receipt = {
            "version": 2, "branch": BRANCH, "requested": [OLDER, NEWER],
            "results": [{"changeid": NEWER, "status": "fail-conflict"},
                        {"changeid": OLDER, "status": "success", "hash": HEAD}],
            "publication": {"owner_job": "receiver", "reason": "hook",
                            "source": {"merged_hash": HEAD, "target_branch": BRANCH},
                            "result": {"api_version": "c2.build-hook/v1", "status": "passed",
                                       "summary": "Published.", "artifact_refs": {}}},
        }
        self.assertEqual(caller_receipt(receipt, OLDER, BRANCH, "receiver")["own"]["hash"], HEAD)
        mutations = [
            (("version",), None), (("version",), True), (("version",), 1),
            (("branch",), "refs/heads/foreign"), (("requested",), []),
            (("requested",), [OLDER, OLDER]), (("requested",), [OLDER, YOUNGEST]),
            (("results",), [receipt["results"][1]]),
            (("results", 0, "changeid"), OLDER), (("results", 0, "changeid"), YOUNGEST),
            (("results", 0, "status"), "unknown"), (("results", 0, "failure_logs"), {}),
            (("results", 0, "status"), "fail-validation"),
            (("results", 1, "hash"), "main"), (("results", 1, "hash"), HEAD[:8]),
            (("publication", "owner_job"), "foreign"),
            (("publication", "reason"), "unknown"), (("publication", "reason"), "no-new-merge"),
            (("publication", "source"), None),
            (("publication", "source", "target_branch"), "refs/heads/foreign"),
            (("publication", "source", "merged_hash"), "main"),
            (("publication", "result", "api_version"), "c2.build-hook/v2"),
            (("publication", "result", "status"), "unknown"),
            (("publication", "result", "summary"), " "),
            (("publication", "result", "artifact_refs"), []),
            (("publication", "result", "failure"), "not an envelope"),
            (("publication", "result", "unexpected"), "native receipt"),
        ]
        for path, value in mutations:
            with self.subTest(path=path, value=value):
                invalid = copy.deepcopy(receipt)
                parent = invalid
                for key in path[:-1]:
                    parent = parent[key]
                parent[path[-1]] = value
                self.assertEqual(caller_receipt(invalid, OLDER, BRANCH, "receiver"), {})
        for field in receipt:
            with self.subTest(missing=field):
                invalid = copy.deepcopy(receipt)
                del invalid[field]
                self.assertEqual(caller_receipt(invalid, OLDER, BRANCH, "receiver"), {})
        skipped = copy.deepcopy(receipt)
        skipped["publication"].update(reason="no-new-merge", source=None)
        skipped["publication"]["result"]["status"] = "skipped"
        self.assertIsNone(caller_receipt(skipped, OLDER, BRANCH, "receiver")["queue_publication"]["source"])
        skipped["publication"]["result"]["status"] = "passed"
        self.assertEqual(caller_receipt(skipped, OLDER, BRANCH, "receiver"), {})

    def test_duplicate_documents_and_versions_do_not_pool_authority(self):
        """QP05/QP06/QP08: duplicates cannot change document bytes or grants."""
        original = append(OLDER, "2026-11-18T12:00:00.000000001Z")
        ref = {"kind": "stored", "stored": {"key": {"jobId": "document", "index": 1}}}
        original["content"]["documents"] = {"review/note.txt": ref}
        original["artifacts"].append(ref)
        accepted, rejected = screen_contributions([original, copy.deepcopy(original)], REPOSITORY, BRANCH, POLICY)
        self.assertEqual(len(accepted), 1)
        self.assertFalse(rejected)
        for change in ("document", "alias", "bundle-owner", "contribution-version", "policy-version", "authority"):
            with self.subTest(change=change):
                duplicate = copy.deepcopy(original)
                if change == "document":
                    replacement = {"kind": "stored", "stored": {"key": {"jobId": "different", "index": 1}}}
                    duplicate["content"]["documents"] = {"review/note.txt": replacement}
                    duplicate["artifacts"][1] = replacement
                elif change == "alias":
                    duplicate["content"]["documents"]["review/second.txt"] = ref
                    duplicate["artifacts"].append(ref)
                elif change == "bundle-owner":
                    duplicate["content"]["job_id"] = "foreign"
                elif change == "contribution-version":
                    duplicate["content"]["version"] = 1
                elif change == "policy-version":
                    duplicate["content"]["verification_policy"]["version"] = 1
                else:
                    duplicate["content"]["verification_policy"]["perms"] = {"jobs": {"submit": True}}
                accepted, rejected = screen_contributions([original, duplicate], REPOSITORY, BRANCH, POLICY)
                self.assertEqual(accepted, [])
                self.assertIn(OLDER, rejected)

    def test_document_binding_and_policy_cannot_supply_authority(self):
        original = append(OLDER, "2026-11-18T12:00:00.000000001Z")
        document = {"kind": "stored", "stored": {"key": {"jobId": "document-owner", "index": 1}}}
        original["content"]["documents"] = {"review/note.md": document}
        original["artifacts"].append(document)
        accepted, rejected = screen_contributions([original], REPOSITORY, BRANCH, POLICY)
        self.assertFalse(rejected)
        self.assertEqual(accepted[0]["documents"], original["content"]["documents"])
        for name in ("../escape", "/absolute", "a/../b", "a\\b", "bad\x00name"):
            invalid = copy.deepcopy(original)
            invalid["content"]["documents"] = {name: document}
            self.assertIn(OLDER, screen_contributions([invalid], REPOSITORY, BRANCH, POLICY)[1])
        invalid = copy.deepcopy(original)
        invalid["artifacts"].pop()
        self.assertIn(OLDER, screen_contributions([invalid], REPOSITORY, BRANCH, POLICY)[1])
        invalid = copy.deepcopy(original)
        invalid["content"]["verification_policy"] = dict(POLICY, permissions={"secrets": ["unrelated"]})
        self.assertIn(OLDER, screen_contributions([invalid], REPOSITORY, BRANCH, POLICY)[1])

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

    def test_empty_selection_requires_failure_evidence_for_each_applied_change(self):
        with tempfile.TemporaryDirectory() as temporary:
            replay = [{"changeid": OLDER, "status": "applied"}]
            evidence = [{"ids": [NEWER], "passed": False}, {"ids": [], "passed": True}]
            with self.assertRaisesRegex(RuntimeError, f"Missing validation evidence for {OLDER}"):
                landing_results(Path(temporary), [], replay, {}, evidence)


class MergeQueueInstallTest(unittest.TestCase):
    def test_confirmation_requires_reachability_change_id_and_source_ancestry(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Git(Path(temporary))
            repo.run("init", "--quiet")
            repo.run("config", "user.name", "Queue Test")
            repo.run("config", "user.email", "queue@example.test")
            repo.run("commit", "--quiet", "--allow-empty", "-m", "Base")
            base = repo.head()
            repo.run("commit", "--quiet", "--allow-empty", "-m", "Own\n\nChange-Id: " + OLDER)
            own = repo.head()
            repo.run("commit", "--quiet", "--allow-empty", "-m", "Batch tip")
            tip = repo.head()
            repo.run("checkout", "--quiet", "--detach", base)
            repo.run("commit", "--quiet", "--allow-empty", "-m", "Unreachable\n\nChange-Id: " + OLDER)
            unreachable = repo.head()
            repo.run("checkout", "--quiet", "--detach", tip)
            source = {"merged_hash": tip, "target_branch": BRANCH}
            self.assertTrue(confirm_landed(repo, BRANCH, own, OLDER, source)["confirmed"])
            self.assertFalse(confirm_landed(repo, BRANCH, own, NEWER, source)["confirmed"])
            self.assertFalse(confirm_landed(repo, BRANCH, unreachable, OLDER, source)["confirmed"])
            self.assertFalse(confirm_landed(repo, BRANCH, own, OLDER,
                                          dict(source, merged_hash=base))["confirmed"])
            self.assertFalse(confirm_landed(repo, BRANCH, own, OLDER,
                                          dict(source, target_branch="refs/heads/other"))["confirmed"])
            self.assertFalse(confirm_landed(repo, BRANCH, own, OLDER,
                                          dict(source, merged_hash=unreachable))["confirmed"])
            self.assertFalse(confirm_landed(repo, BRANCH, own, OLDER,
                                          dict(source, merged_hash="f" * 40))["confirmed"])

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


def saved_receipt(content, policy=POLICY, status="passed"):
    return {
        "job_id": content["job_id"],
        "identity": {"candidate": content["head_hash"], "base": content["base_hash"],
                     "request": "Check the original request", "target_directory": policy["target_directory"],
                     "documents": {}, "settings": policy["settings"], "required": policy["require_verification"]},
        "result": {"api_version": "c2.build-hook/v1", "status": status,
                   "summary": "Original verification", "artifact_refs": {}},
        "artifacts": {},
    }


class ExactCommitReceiptTest(unittest.TestCase):
    def setUp(self):
        self.append = append(OLDER, "2026-11-18T12:00:00.000000001Z")
        self.append["content"]["verification"] = saved_receipt(self.append["content"])
        self.assembly = {"base": BASE, "head": HEAD,
                         "results": [{"changeid": OLDER, "status": "applied", "hash": HEAD}]}

    def select(self, appends=None, policy=POLICY, assembly=None):
        items, rejected = screen_contributions(appends or [self.append], REPOSITORY, BRANCH, policy)
        self.assertFalse(rejected)
        return reusable_receipt(assembly or self.assembly, items, policy)

    def test_exact_head_without_count_or_receipt_base_equality_gate(self):
        self.assertEqual(self.select(), self.append["content"]["verification"])
        assembly = copy.deepcopy(self.assembly)
        assembly["base"] = "c" * 40
        self.assertIsNotNone(self.select(assembly=assembly))
        second = append(NEWER, "2026-11-18T12:00:01.000000001Z", head="d" * 40)
        assembly["results"].append({"changeid": NEWER, "status": "applied", "hash": "d" * 40})
        self.assertIsNotNone(self.select([self.append, second], assembly=assembly))
        assembly["head"] = "d" * 40
        self.assertIsNone(self.select([self.append, second], assembly=assembly))

    def test_complete_original_identity_and_policy_are_required(self):
        receipt = self.append["content"]["verification"]
        for field in list(receipt["identity"]):
            with self.subTest(missing=field):
                candidate = copy.deepcopy(self.append)
                del candidate["content"]["verification"]["identity"][field]
                self.assertIsNone(self.select([candidate]))
        for field, value in {"candidate": "c" * 40, "base": "c" * 40, "required": False,
                             "target_directory": "other", "settings": {"changed": True},
                             "documents": [], "request": None}.items():
            with self.subTest(field=field):
                candidate = copy.deepcopy(self.append)
                candidate["content"]["verification"]["identity"][field] = value
                self.assertIsNone(self.select([candidate]))
        policy = dict(POLICY, settings={"b": {"y": 2, "x": 1}, "a": True})
        candidate = copy.deepcopy(self.append)
        candidate["content"]["verification"] = saved_receipt(candidate["content"], policy)
        candidate["content"]["verification"]["identity"]["settings"] = {"a": True, "b": {"x": 1, "y": 2}}
        candidate["content"]["verification_policy"] = policy
        self.assertIsNotNone(self.select([candidate], policy))

    def test_missing_malformed_and_failed_evidence_falls_back(self):
        for value in (None, {}, [], "passed", {"result": {"status": "passed"}}):
            with self.subTest(value=value):
                candidate = copy.deepcopy(self.append)
                candidate["content"]["verification"] = value
                self.assertIsNone(self.select([candidate]))
        for field, value in {"job_id": "foreign", "artifacts": [],
                             "result": {"status": "passed"}}.items():
            candidate = copy.deepcopy(self.append)
            candidate["content"]["verification"][field] = value
            self.assertIsNone(self.select([candidate]))
        for status in ("failed", "changes", "skipped", [], {}):
            candidate = copy.deepcopy(self.append)
            candidate["content"]["verification"]["result"]["status"] = status
            self.assertIsNone(self.select([candidate]))
        for field, value in (("failure", {}), ("artifact_refs", {"bad": {}})):
            candidate = copy.deepcopy(self.append)
            candidate["content"]["verification"]["result"][field] = value
            self.assertIsNone(self.select([candidate]))

    def test_optional_skip_stays_skipped(self):
        policy = dict(POLICY, require_verification=False)
        candidate = copy.deepcopy(self.append)
        candidate["content"]["verification_policy"] = policy
        candidate["content"]["verification"] = saved_receipt(candidate["content"], policy, "skipped")
        self.assertEqual(self.select([candidate], policy)["result"]["status"], "skipped")

    def test_duplicates_validate_each_producer_and_disable_conflicting_receipts(self):
        duplicate = copy.deepcopy(self.append)
        duplicate["content"]["job_id"] = "other-producer"
        duplicate["content"]["thinpack_ref"]["stored"]["key"]["jobId"] = "other-producer"
        duplicate["content"]["verification"]["job_id"] = "other-producer"
        duplicate["content"]["verification"]["result"]["summary"] = "Different log location"
        duplicate["content"]["verification"]["artifacts"] = {
            "test.log": {"kind": "stored", "stored": {"key": {"jobId": "other-producer", "taskOrdinal": 1, "name": "test.log", "sizeBytes": 1}}}}
        for pair in ([self.append, duplicate], [duplicate, self.append]):
            self.assertEqual(self.select(pair), pair[0]["content"]["verification"])
        for mutation in ("failed", "foreign", "identity", "malformed"):
            changed = copy.deepcopy(duplicate)
            receipt = changed["content"]["verification"]
            if mutation == "failed": receipt["result"]["status"] = "failed"
            if mutation == "foreign": receipt["job_id"] = "foreign"
            if mutation == "identity": receipt["identity"]["request"] = "Another request"
            if mutation == "malformed": del receipt["identity"]
            for pair in ([self.append, changed], [changed, self.append]):
                with self.subTest(mutation=mutation, first=pair[0]["content"]["job_id"]):
                    self.assertIsNone(self.select(pair))
        missing = copy.deepcopy(duplicate)
        del missing["content"]["verification"]
        for pair in ([missing, self.append], [self.append, missing]):
            self.assertEqual(self.select(pair), self.append["content"]["verification"])

    def test_accounting_and_exact_publication_identity_are_required(self):
        for rows in ([], [{"changeid": NEWER, "status": "applied", "hash": HEAD}],
                     [{"changeid": OLDER, "status": "fail-validation"}],
                     [{"changeid": OLDER, "status": "applied", "hash": BASE}]):
            self.assertIsNone(self.select(assembly=dict(self.assembly, results=rows)))
        for head in (BASE, "c" * 40):
            self.assertIsNone(self.select(assembly=dict(self.assembly, head=head)))
        rewritten = copy.deepcopy(self.assembly)
        rewritten["head"] = rewritten["results"][0]["hash"] = "c" * 40
        self.assertIsNone(self.select(assembly=rewritten))


class ExactCommitGitTest(unittest.TestCase):
    def test_git_checks_recompute_and_preserve_original_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = Git(root)
            repo.run("init", "--quiet")
            repo.run("config", "user.name", "Test")
            repo.run("config", "user.email", "test@example.test")
            repo.run("commit", "--quiet", "--allow-empty", "-m", "Base")
            base = repo.head()
            repo.run("commit", "--quiet", "--allow-empty", "-m", "Candidate")
            head = repo.head()
            item = append(OLDER, "2026-11-18T12:00:00.000000001Z")["content"]
            item.update(base_hash=base, head_hash=head)
            item["verification"] = saved_receipt(item)
            item["verification"]["artifacts"] = {"assembled.bundle": item["thinpack_ref"]}
            original = copy.deepcopy(item["verification"])
            assembly = {"base": base, "head": head,
                        "results": [{"changeid": OLDER, "status": "applied", "hash": head}]}
            result = reuse_verification(repo, assembly, [item], POLICY)
            self.assertTrue(result["reused"])
            self.assertEqual(result["receipt"], original)
            self.assertEqual(result["verification"]["status"], "passed")
            self.assertIn(head, result["verification"]["summary"])
            ref = result["artifacts"]["verification/producer/assembled.bundle"]
            self.assertEqual(ref["stored"], original["artifacts"]["assembled.bundle"]["stored"])
            (root / "dirty").write_text("dirty")
            with self.assertRaises(GitError): reuse_verification(repo, assembly, [item], POLICY)
            (root / "dirty").unlink()
            with self.assertRaises(GitError):
                reuse_verification(repo, dict(assembly, base="f" * 40), [item], POLICY)
            repo.run("checkout", "--quiet", "--detach", base)
            repo.run("commit", "--quiet", "--allow-empty", "-m", "Diverged")
            other = repo.head()
            repo.run("checkout", "--quiet", "--detach", head)
            self.assertFalse(reuse_verification(repo, dict(assembly, base=other), [item], POLICY)["reused"])
            repo.run("commit", "--quiet", "--allow-empty", "-m", "New candidate")
            new = repo.head()
            rewritten = {"base": base, "head": new,
                         "results": [{"changeid": OLDER, "status": "applied", "hash": new}]}
            self.assertFalse(reuse_verification(repo, rewritten, [item], POLICY)["reused"])
            with self.assertRaises(GitError): reuse_verification(repo, assembly, [item], POLICY)
