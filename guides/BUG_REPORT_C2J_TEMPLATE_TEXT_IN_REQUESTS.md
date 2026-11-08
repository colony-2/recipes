# Literal template-looking request text fails at a hook boundary

Observed while testing the self-improvement entrypoint on November 8, 2026 with
c2j **0.0.124**, source `33e2a4de4e99d3a577a38dca4b8de33d43a099ce`.

**Expected:** request text remains data when passed through includes and hook
inputs. For example, a request can discuss the literal text `{{ scope_name }}`
without defining a recipe variable named `scope_name`.

**Observed:** a request containing that literal fails during configuration,
before classification or any agent turn. The outer error says:

```text
[build.workflow.adaptive-build.configure.adaptive-hook-configure]
failed to resolve sequence outputs: failed to resolve input 'artifact_refs':
failed to evaluate CEL expression: no such key: invoke_hook
```

Some runs name `settings_artifact` instead of `artifact_refs`. That missing output
obscures why the hook invocation failed.

The initial reproduction passed this constraint through the new prompt include:

```text
Preserve 100% of scope and literal {{ scope_name }}.
Do not modify audited jobs.
```

Replacing the braces with ordinary text allowed the same workflow to finish.
A second reproduction used **the existing root `build.yaml` directly**, with
`prompt: 'Keep {{ scope_name }} as literal example text.'`; it failed at the same
configure boundary. The local trace contains only `initial_candidate`, before
Jev or Codex. The reproduction log is
`/tmp/self-improvement-template-repro2.log`. The initial diagnostic test also
reported an unused Jev mock because execution never reached that operation.

**Requested investigation, owned by c2j:** determine where supplied request text
is treated as a template again during hook/include input resolution, preserve
literal data through that boundary, and retain the original invocation error
instead of replacing it with a missing-output error. The exact internal cause
has not been established; no runtime source change was made here.

For current audits, put raw recipe/prompt excerpts in evidence files and keep
inline job-selection instructions as prose. This also avoids large inline
payloads and is the existing artifact-based audit convention. No escaping layer
or alternate workflow was added to the recipes to conceal this runtime issue.
