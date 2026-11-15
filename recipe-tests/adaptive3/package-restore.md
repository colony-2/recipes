# Package validation against a retained candidate

`package-restore.test.yaml` runs the production `package_config` command. A native
write commits the candidate configuration and marker. An independent child writes
and persists a different proposal workspace and three linked review documents.
The candidate has a setting and existing portable package absent from upstream;
the proposal workspace has a different setting and marker.

The fixture uses the existing artifact-namespace helper to carry the candidate's
collection alongside the proposal's collection. It changes delivery prefixes only;
the runtime-generated restore filenames, stored keys and pack bytes remain intact.
Both distinct producer packs reach the validation include. The candidate is also
supplied by native workspace restoration. This is deliberate: merely supplying a
foreign proposal pack does not reproduce the original duplicate-restore error.

`package_restore_control.py` derives a temporary source variant from the current
production file, reverting exactly its document binding. It runs the same graph
and data, requiring `multiple workspace restore artifacts`, distinct nonempty
native producer packs, and no validator command entry. A bundle-prerequisite or
artifact-destination error fails this control. The temporary sources are removed.
CI runs this control separately before normal suite discovery.

The corrected case checks the actual validator input files, candidate HEAD at
command entry, candidate settings and marker, parsed result, materialized validator
log, exact review bytes, a clean checkout and unchanged final HEAD. A review-only
control preserves the same behavior. `tools.test.yaml` additionally checks that
the same proposal fails against upstream or the proposal workspace settings.

Run from the repository root:

```sh
python3 recipe-tests/checks/package_restore_control.py --out-dir /tmp/package-validator-results/unfiltered
c2j test run --file recipe-tests/adaptive3/package-restore.test.yaml --out-dir /tmp/package-validator-results/restore
c2j test run --file recipe-tests/adaptive3/tools.test.yaml --out-dir /tmp/package-validator-results/tools
c2j test run --file recipe-tests/adaptive3/packages.test.yaml --out-dir /tmp/package-validator-results/packages
c2j test run --file recipe-tests/adaptive3/package-probe.test.yaml --out-dir /tmp/package-validator-results/probe
```

Model choices and the child-submission selector are scripted. Workspace persistence,
restore preparation, storage, commands, reviews, child execution and terminal waits
run natively in disposable cells. Portable proposal cases never activate the
proposed configuration. The existing successful probe cases execute pytest in
disposable cells; none changes or installs dependencies in the application job.
