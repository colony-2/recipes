# Reusing adaptive3 activities

Use the normal build submission for a development assignment. Use a consultation
request for another owner's advice. These paths already provide cell workspaces,
validation, human decisions and recovery.

A small diagnostic job can run a specific check. Give it a title describing the
check and return a short explanation of what it found. A diagnostic that records
an import failure has completed its investigation; it has not repaired Python.
An acceptance check must fail when its required behavior fails.

## Including an activity from another repository

c2j trusts explicit secret inputs authored in the root recipe repository. Including
a recipe from another repository requires the caller to authorize its secret
inputs. An optional secret reference still needs authorization.

For example, this call authorizes the model input used by a read-only advice cycle:

```yaml
- id: advice
  include: git+https://github.com/colony-2/recipes.git//recipes/adaptive3/cycle.yaml@main
  perms:
    jobdb:
      secrets:
        resolve: [codex_api_key]
  inputs:
    purpose: advice
    request: Explain how saved drafts survive a restart.
```

The caller must handle the returned `result.status`, including `stuck`, and any
failure at the include boundary. Use the existing containing lifecycle/Backstop
when building a development workflow. `execute.yaml` alone is an internal activity;
it does not supply the surrounding correction and recovery behavior.

This grant authorizes the included recipe's model input. It does not automatically
grant every task permission to fetch the secret by name. It cannot override an
enclosing ceiling. Other capabilities, such as submitting jobs, need an appropriate
caller policy; do not copy this limited advice example as a complete build policy.
Use c2j's [node-permission guide](https://github.com/colony-2/c2j/blob/main/GUIDE-Node-Permissions.md)
for inheritance, ceilings and Git-profile behavior.

The native [reuse tests](../../recipe-tests/adaptive3/reuse-permissions.test.yaml)
create a distinct recipe repository and test trusted-root input resolution,
authorized and denied includes, a denied ceiling and a foreign operation default.
They use synthetic secrets and the actual permission evaluator. No production
secret or runtime implementation is changed.
