# /// script
# dependencies = ["jsonschema>=4.23,<5", "rfc3339-validator>=0.1.4,<0.2"]
# ///
"""Validate the proposed native review contract and handoff fixtures.

These are schema/fixture integration checks, not c2j runtime acceptance tests.
The pending native scenarios are listed in NATIVE_REVIEW_HANDOFF_PROPOSAL.md.
No database, model, or runtime is used.
"""
import hashlib
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/review"
SCHEMA = json.loads((CONTRACT / "v1.schema.json").read_text())


def fixture(name):
    return json.loads((CONTRACT / "examples" / (name + ".json")).read_text())


def validator(kind):
    return Draft202012Validator(
        {**SCHEMA, "$ref": "#/$defs/" + kind}, format_checker=FormatChecker()
    )


class ReviewContract(unittest.TestCase):
    def rejected(self, kind, value):
        self.assertTrue(list(validator(kind).iter_errors(value)), value)

    def test_schema_and_all_published_examples(self):
        Draft202012Validator.check_schema(SCHEMA)
        for kind, name in [
            ("ReviewSpec", "spec"), ("ReviewRequest", "request"),
            ("ReviewSubmission", "submission-approve"),
            ("ReviewSubmission", "submission-revise"), ("ReviewReceipt", "receipt"),
        ]:
            with self.subTest(name=name):
                validator(kind).validate(fixture(name))

    def test_documents_identify_exact_example_bytes(self):
        request = fixture("request")
        for file in request["files"]:
            key = file["artifact_ref"]["stored"]["key"]
            content = (CONTRACT / "examples" / key["name"]).read_bytes()
            self.assertEqual(file["sha256"], hashlib.sha256(content).hexdigest())
            self.assertEqual(key["sizeBytes"], len(content))
            self.assertIn(f'/tasks/{key["taskOrdinal"]}/artifacts/{key["name"]}', file["download_url"])

    def test_example_submission_and_receipt_retain_provenance(self):
        request, submission, receipt = (fixture(name) for name in ("request", "submission-revise", "receipt"))
        self.assertEqual(submission["review_id"], request["review_id"])
        self.assertIn(submission["decision"], [d["id"] for d in request["decisions"]])
        for annotation in submission["annotations"]:
            document = next(f for f in request["files"] if f["id"] == annotation["file_id"])
            self.assertEqual(annotation["base_sha256"], document["sha256"])
            self.assertEqual(document["annotations"], "criticmarkup")
        self.assertEqual(receipt["submission"], submission)
        self.assertEqual(set(receipt["artifact_refs"]["annotations"]), {a["file_id"] for a in submission["annotations"]})

    def test_all_criticmarkup_forms_and_unicode_survive_json(self):
        value = fixture("submission-revise")
        markdown = "# Café\r\n{++new++} {--old--} {~~before~>after~~} {>>note<<} {==highlight==}\r\n"
        value["annotations"][0]["markdown"] = markdown
        validator("ReviewSubmission").validate(value)
        self.assertEqual(json.loads(json.dumps(value))["annotations"][0]["markdown"], markdown)

    def test_required_fields_and_versions(self):
        for kind, name in [("ReviewSpec", "spec"), ("ReviewRequest", "request"), ("ReviewSubmission", "submission-revise"), ("ReviewReceipt", "receipt")]:
            for field in SCHEMA["$defs"][kind]["required"]:
                with self.subTest(kind=kind, missing=field):
                    value = fixture(name)
                    del value[field]
                    self.rejected(kind, value)
            value = fixture(name)
            value["schema"] = "c2.review-unknown/v2"
            self.rejected(kind, value)

    def test_unknown_fields_rejected_at_contract_boundaries(self):
        for kind, name in [("ReviewSpec", "spec"), ("ReviewRequest", "request"), ("ReviewSubmission", "submission-revise"), ("ReviewReceipt", "receipt")]:
            with self.subTest(kind=kind):
                value = fixture(name)
                value["unexpected"] = True
                self.rejected(kind, value)
        value = fixture("submission-revise")
        value["annotations"][0]["path"] = "../../AGENTS.md"
        self.rejected("ReviewSubmission", value)

    def test_recipe_cannot_choose_runtime_identity_hashes_or_urls(self):
        for key, extra in [("review_id", "chosen"), ("origin", {"job_id": "fake"})]:
            value = fixture("spec")
            value[key] = extra
            self.rejected("ReviewSpec", value)
        for key, extra in [("sha256", "a" * 64), ("download_url", "/fake")]:
            value = fixture("spec")
            value["files"][0][key] = extra
            self.rejected("ReviewSpec", value)

    def test_published_documents_require_hash_and_download(self):
        for field in ["sha256", "download_url", "artifact_ref"]:
            value = fixture("request")
            del value["files"][0][field]
            self.rejected("ReviewRequest", value)
        for digest in ["", "a" * 63, "z" * 64, "A" * 64]:
            value = fixture("request")
            value["files"][0]["sha256"] = digest
            self.rejected("ReviewRequest", value)
            value = fixture("submission-revise")
            value["annotations"][0]["base_sha256"] = digest
            self.rejected("ReviewSubmission", value)

    def test_worktree_paths_and_external_urls_are_not_stored_artifacts(self):
        for artifact in ["/tmp/op/inbox/design.md", {"path": "design.md"}, {"kind": "external", "external": {"url": "https://example.org/design.md"}}]:
            value = fixture("spec")
            value["files"][0]["artifact_ref"] = artifact
            self.rejected("ReviewSpec", value)
        for key, invalid in [("jobId", ""), ("taskOrdinal", -1), ("sizeBytes", -2), ("name", "")]:
            value = fixture("spec")
            value["files"][0]["artifact_ref"]["stored"]["key"][key] = invalid
            self.rejected("ReviewSpec", value)

    def test_only_markdown_can_allow_annotations(self):
        for media_type in ["application/json", "text/plain"]:
            value = fixture("spec")
            value["files"][0]["media_type"] = media_type
            self.rejected("ReviewSpec", value)
            value["files"][0]["annotations"] = "none"
            validator("ReviewSpec").validate(value)

    def test_feedback_only_reviews_and_immutable_subjects(self):
        value = fixture("spec")
        value["files"] = []
        value["subject"] = {"id": "github.com/example/cell", "version": "a" * 40}
        validator("ReviewSpec").validate(value)
        del value["subject"]["version"]
        self.rejected("ReviewSpec", value)

    def test_decisions_are_explicit_and_recipe_defined(self):
        value = fixture("spec")
        value["decisions"][0]["id"] = "satisfied"
        validator("ReviewSpec").validate(value)
        value["decisions"] = []
        self.rejected("ReviewSpec", value)
        for field in ["id", "label", "accepts_reviewed_content", "feedback_required"]:
            value = fixture("spec")
            del value["decisions"][0][field]
            self.rejected("ReviewSpec", value)

    def test_annotations_require_version_document_and_complete_text(self):
        for key in ["file_id", "base_sha256", "format", "markdown"]:
            value = fixture("submission-revise")
            del value["annotations"][0][key]
            self.rejected("ReviewSubmission", value)
        for key, invalid in [("format", "patch"), ("file_id", "../design.md"), ("markdown", "")]:
            value = fixture("submission-revise")
            value["annotations"][0][key] = invalid
            self.rejected("ReviewSubmission", value)

    def test_receipts_require_durable_artifacts_and_runtime_audit(self):
        value = fixture("receipt")
        value["submitted_at"] = "yesterday"
        self.rejected("ReviewReceipt", value)
        for key in ["request", "submission", "annotations"]:
            value = fixture("receipt")
            del value["artifact_refs"][key]
            self.rejected("ReviewReceipt", value)

    def test_client_cannot_assert_runtime_submitter_identity(self):
        for key, extra in [("user_id", "admin"), ("submitted_at", "2026-09-29T12:00:00Z")]:
            value = fixture("submission-revise")
            value[key] = extra
            self.rejected("ReviewSubmission", value)

    def test_membership_and_approval_checks_are_explicitly_runtime_owned(self):
        # These shapes are valid: a schema cannot compare a submission to a
        # separately stored request. Native negative coverage is NR-05/NR-06.
        # Keep this distinction visible instead of claiming schema validation
        # alone protects an approval boundary.
        for key, extra in [("review_id", "stale"), ("decision", "not-offered")]:
            value = fixture("submission-revise")
            value[key] = extra
            validator("ReviewSubmission").validate(value)
        value = fixture("submission-revise")
        value["decision"] = "approve"
        validator("ReviewSubmission").validate(value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
