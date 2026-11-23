"""Check diagnostics materialized through the submitting job's returned errors map."""
import json
from pathlib import Path
import shutil
import sys


def check(inbox, outbox):
    returned = json.loads((inbox / "returned.json").read_text())

    def find(name):
        matches = [(alias, ref) for alias, ref in returned.items()
                   if ref["stored"]["key"]["name"] == name]
        assert len(matches) == 1, f"Expected exactly one returned {name}: {matches}"
        alias, ref = matches[0]
        assert ref["name"] == alias, (alias, ref)
        return inbox / "errors" / alias, ref["stored"]["key"]

    origin_path, manifest_key = find("diagnostic-origin.json")
    original = json.loads(origin_path.read_text())
    expected = {
        "restoration.log": b"Expected an activity selector.\n",
        "input-failure.log": b"Expected an artifact error.\n",
    }
    assert set(original) == set(expected), original
    matched = {}
    for name, body in expected.items():
        path, key = find(name)
        assert path.read_bytes() == body, f"Diagnostic bytes differ: {name}"
        assert key == original[name]["stored"]["key"], f"Producer key differs: {name}"
        assert key["jobId"] == manifest_key["jobId"], (key, manifest_key)
        assert key["taskOrdinal"] != manifest_key["taskOrdinal"], (key, manifest_key)
        assert key["sizeBytes"] == len(body), key
        matched[name] = key

    # The separately generated summary must survive alongside the original logs.
    change_id = (inbox / "change-id.txt").read_text().strip()
    summary_path, summary_key = find(change_id + ".log")
    assert summary_key["jobId"] == manifest_key["jobId"], summary_key
    assert all(summary_key["taskOrdinal"] != key["taskOrdinal"] for key in matched.values())
    summary = summary_path.read_bytes()
    assert b"Checked worker health." in summary, summary

    outbox.mkdir(parents=True, exist_ok=True)
    (outbox / "delivery.json").write_text(json.dumps({
        "original": original, "returned": returned, "matched": matched,
        "manifest_key": manifest_key, "bytes_verified": True,
    }, indent=2) + "\n")
    # Retain the tiny materialized inputs for independent assertion-sensitivity checks.
    shutil.copytree(inbox, outbox / "delivered", dirs_exist_ok=True)
    print("Read both original diagnostics and summary; complete producer keys match.")


if __name__ == "__main__":
    check(Path(sys.argv[1]), Path(sys.argv[2]))
