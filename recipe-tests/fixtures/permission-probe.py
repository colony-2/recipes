"""Exercise native task helpers with synthetic, case-local credentials."""
import json
import os
import subprocess


def run(*args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, **kwargs)


credential = run(
    "git", "credential", "fill",
    input="protocol=https\nhost=fixture.invalid\npath=repository.git\n\n",
)
assert credential.returncode == 0, "Git credential helper failed: " + credential.stderr
assert "password=" in credential.stdout, "Git credential helper returned no credential"
# Never print the helper's credential response or retain it in artifacts.
del credential

unrelated = run("c2j", "secret", "get", "unrelated_token")
assert unrelated.returncode != 0, "Unrelated secret access was granted"

submit = run(
    "c2j", "submit", "Permission regression probe",
    "--advanced-recipe-file", ".c2/recipes/noop.yaml", "--jobdb", "embed:///",
    "--cell", "root", "--from-workspace", "--json",
)
allow_submit = os.environ["ALLOW_SUBMIT"] == "true"
assert (submit.returncode == 0) == allow_submit, submit.stderr
if not allow_submit:
    assert any(word in submit.stderr.lower() for word in ("permission", "denied", "not authorized", "403 forbidden")), submit.stderr

create = run(
    "c2j", "cell", "create", "permission-probe-cell",
    "--repo", "fixture.invalid/permission-probe-cell", "--json",
)
allow_create = os.environ["ALLOW_CREATE"] == "true"
assert (create.returncode == 0) == allow_create, create.stderr
if not allow_create:
    assert any(word in create.stderr.lower() for word in ("permission", "denied", "not authorized", "403 forbidden")), create.stderr

print(json.dumps({
    "git_credential_resolved": True,
    "unrelated_secret_denied": True,
    "submission_allowed": allow_submit,
    "creation_allowed": allow_create,
}))
