# c2j feature request: resolve approximate artifact paths

Status: implemented in c2j main `94484c909de14a2fe2b2a62dfbd82d31595b5b75`
(not yet released). See [the usage guide](GUIDE-Path-Matching.md).
The requirements below record the requested contract.
Requested by: recipes cell. Implementation owner: c2j.
Date: 2026-10-21.

## Problem and outcome

An agent can produce the correct document but refer to it using a filesystem
path instead of its artifact name. This should not stop an otherwise valid job.

In job `3L1FpMQOeRx2d4wnIdvHi93z0X3`, Codex completed successfully with a
schema-valid response naming `outbox/design.md`. Task 358 persisted the document
as `design.md`. The build recipe rejected the reference and failed before review.
The source recipe was `85627faa57a0e1ca5175dab4114c67b48752e94a`.

Provide deterministic matching against a caller-supplied inventory. Resolve
unique references automatically and return ambiguity or absence as data so a
recipe can request correction without failing expression evaluation.

## Recommended interface: an expression function

Add a pure CEL/template helper, provisionally:

```text
path_match(reference: string, candidates: list<string>) -> map
```

This is a function because it compares supplied values. It needs no filesystem,
network, model invocation, durable task, or side effects. An op would add an
execution boundary without adding a capability. Keep it generic enough to match
other explicit path inventories; artifact selection is its first consumer.

Always return the same fields:

```json
{"status":"matched","path":"design.md","candidates":["design.md"]}
```

- `status`: `matched`, `not_found`, `ambiguous`, or `invalid`.
- `path`: the exact original candidate string when matched; otherwise empty.
- `candidates`: matching candidates at the strongest matching level, sorted
  lexically and deduplicated; empty for `not_found` or `invalid`.

Ordinary absent, ambiguous, or malformed path references must not raise CEL
errors. Incorrect argument types remain normal expression errors.

## Matching rules

1. Prefer an exact candidate string match, even if other candidates share its
   filename. Deduplicate identical candidate strings.
2. Otherwise compare complete trailing path components, starting with the most
   specific suffix of the reference and progressively dropping leading
   components. A candidate matches when it ends in that complete suffix.
3. At the first level with matches, return the sole candidate or `ambiguous`.
   Do not break ties by input order, shorter paths, or additional heuristics.
4. If no suffix matches, return `not_found`.

Use case-sensitive component equality. Do not use edit distance, substring
matching, extension substitution, or semantic filename guesses. Thus `sign.md`
does not match `design.md`, and a longer directory suffix beats a shared basename.

For the reference, accept absolute paths, repeated `/` separators, and `.`
components through lexical normalization. Require a filename; empty references,
trailing directory separators, NULs, backslashes, and `..` components return
`invalid`. Never expand `~`, environment variables, URIs, or symlinks. The initial
contract uses `/` separators, matching c2j artifact names.

Candidates must be canonical relative file names: nonempty components separated
by `/`, with no absolute prefix, trailing separator, `.`, `..`, NUL, or backslash.
An invalid candidate inventory returns `invalid`, rather than silently dropping
entries. An empty inventory returns `not_found` for a valid reference.

## Acceptance examples

These are unit-level expectations for the c2j expression helper. Also exercise
the helper through native recipe expression evaluation; no external services are
required.

| Reference | Candidate inventory | Expected result |
| --- | --- | --- |
| `design.md` | `design.md`, `archive/design.md` | Match `design.md` exactly. |
| `outbox/design.md` | `design.md` | Match `design.md`. |
| `/scratch/job/outbox/design.md` | `design.md` | Match `design.md`. |
| `./outbox//design.md` | `design.md` | Match `design.md`. |
| `feature.md` | `iter1/consultant/feature.md` | Match the unique nested file. |
| `outbox/iter2/consultant/reply.md` | `iter1/consultant/reply.md`, `iter2/consultant/reply.md` | Match the iteration-two file. |
| `reply.md` | `iter1/reply.md`, `iter2/reply.md` | Ambiguous; return both candidates. |
| `outbox/design.md` | `outbox/design.md`, `design.md` | Preserve the exact match. |
| `missing.md` | `design.md` | Not found. |
| `sign.md` or `Design.md` | `design.md` | Not found. |
| `../design.md` or empty string | `design.md` | Invalid reference. |

Reordering candidates must not change the result. Duplicate identical candidates
must not cause ambiguity. Matching must never read the referenced filesystem
path or mutate the supplied inventory.

## Recipe integration and repair

The recipes cell owns the consuming workflow. Match against the current turn's
eligible published artifact names, not every artifact ever produced by the job.
Use the returned name to look up the existing artifact reference; preserve its
storage identity and content. Resolve linked references consistently, including
creation `purpose_path` values and their corresponding `files` entries.

After matching, retain normal semantic checks: required documents, permitted
iteration prefixes, duplicate references, review requirements, and approval
gates. A unique filename match does not authorize a transition by itself.

For unresolved references or other correctable agent-result errors, the shared
recipe kernel should resume the originating agent session with specific
diagnostics, candidate names, its previous response, and preserved documents.
The agent can disambiguate, correct its response, or supply missing documents.
Reapply matching and validation after the repair turn. Bound repair attempts and
escalate exhaustion to human review with the work preserved. Repair must not
reset consultation limits or bypass approvals, submit jobs, or repeat publication.

The repair loop is a separate recipe change. The requested c2j function only
returns a deterministic match result; it does not invoke agents or select workflow
policy. This request adds no second JSON-schema validator.
