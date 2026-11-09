"""Export actual native-trial artifacts; never rewrite generated documents."""

import argparse
import hashlib
import json
from pathlib import Path


def export(report: Path, destination: Path, producer_files: Path | None = None) -> None:
    run = json.loads(report.read_text())["run"]
    files = {}
    destination.mkdir(parents=True, exist_ok=True)

    def retain(name, body, source):
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe artifact name: {name}")
        if name.startswith(("_c2j/", "__c2j_objects__/")):
            return
        content = body.encode() if isinstance(body, str) else body
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        files[name] = {
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "source": source,
        }

    # The final native command materializes the recipe's selected artifact map.
    # Its recorded inbox retains producer bytes even after fixture cleanup.
    capture_calls = [
        call for call in run["runtime"]["calls"]
        if call["node_path"].endswith(("/retain_review_packet", "/read_documents"))
        and call.get("artifacts")
    ]
    if not capture_calls:
        raise ValueError("No complete packet capture; retain this as a failed trial.")
    for call in capture_calls:
        for name, content in call["artifacts"].items():
            retain(name, content, {
                "consumer_job": call["job_id"],
                "consumer_task": call["node_path"],
                "binding": name,
                "producer": run.get("outputs", {}).get("artifact_refs", {}).get(name),
            })

    # Native call traces omit files over 64 KiB and represent bodies as text.
    # Prefer retained observations, or an untouched producer snapshot when supplied,
    # for missing/invalid-sized bodies. Never silently publish a partial packet.
    for name, ref in run.get("outputs", {}).get("artifact_refs", {}).items():
        expected = ref.get("stored", {}).get("key", {}).get("sizeBytes")
        if name in files and (expected is None or files[name]["bytes"] == expected):
            continue
        content = None
        source = None
        for observation in run["runtime"].get("observation_artifacts", []):
            if observation.get("status") == "retained" and observation.get("ref") == ref:
                content = (report.parent / observation["path"]).read_bytes()
                source = {"observation": observation, "producer": ref}
        if content is None and producer_files:
            candidate = (producer_files / name).resolve()
            if candidate.is_relative_to(producer_files.resolve()) and candidate.is_file():
                content = candidate.read_bytes()
                source = {"producer_snapshot": str(candidate), "producer": ref}
        if content is None or (expected is not None and len(content) != expected):
            raise ValueError(f"Missing intact artifact body: {name}")
        retain(name, content, source)

    forms = [
        {"task": call["node_path"], "form": call["inputs"]["form"]}
        for call in run["runtime"]["calls"] if call["op"] == "input"
    ]
    metadata = {
        "case": run["case_id"],
        "case_hash": run["case_hash"],
        "status": run["status"],
        "duration_ms": run["duration_ms"],
        "runtime": "c2j 0.0.124 (33e2a4de4e99d3a577a38dca4b8de33d43a099ce)",
        "baseline": "33f6474 plus adaptive2 changes in this checkout",
        "native_report": str(report),
        "review_forms": forms,
        "files": files,
        "note": (
            "Live model outputs copied without editorial changes. Disposable native "
            "test runtime: job IDs are not retained production jobs. Direction trials "
            "use a scripted cancel response to export the packet without implementation. "
            "This is not human approval or a human evaluation of document quality."
        ),
    }
    (destination / "run-metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"{destination}: {len(files)} original artifacts")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--producer-files", type=Path,
                        help="Untouched producer snapshot for bodies the native trace did not retain")
    args = parser.parse_args()
    export(args.report, args.destination, args.producer_files)
