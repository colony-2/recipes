# Review artifact annotations

Recipes attach presentation to review documents without changing their identities,
answers or approval rules. Adaptive uses native schema-v2 arrays and publishes
review annotations directly. The policy below applies only to the retained
creation helpers in `recipes/kernel/`, whose default remains **legacy**.

## Producer descriptors

Creation `files` keep required `path` and `description`. The shared provider
schema requires nullable metadata fields; invalid field types fail that schema.
The collector independently omits unusable presentation values:

```json
{"path":"decision.md","description":"Proposed behavior and acceptance evidence.","title":"Design decision brief","role":"primary","order":0,"source_paths":["design.md","tests.md"]}
```

Describe human purpose and decision relevance; do not mechanically derive titles
from filenames. Role is absent/empty neutral, primary, supporting or diagnostic.
Order is optional, including explicit zero. Source paths reference this producer's
declared outputs or bound inputs, in evidence order. They never attach new files.
Producers cannot designate overview, decide approval or activate presentation.

The required response/path checks remain unchanged. Invalid optional fields are
omitted independently, without whole-turn repair or editing the stored descriptor.
Valid descriptions supply presentation descriptions within the wire bounds. Empty
annotations do not imply importance, a title or an invented description.

## Collection and final binding

`artifact-annotations.yaml` exports a separate `annotations` list alongside refs:
originating job/invocation, original descriptor, immutable ref, delivery ID,
attachment lineage, and resolved source associations. `agent-turn` exports it;
phase records and consultation transcripts retain it; child results export it.
The public build/create/consultation APIs use native `annotations` arrays under
schema v2. Internal composites and child results pass typed lists. There is no
annotation JSON input or cross-job transport sidecar requirement. The retained
creation collector still filters internal tagged artifacts from review evidence.
This is a recipe contract, not a c2j ArtifactRef change.

Namespaces export an `attachment_map` and transform annotation lineage only for
attachments in that namespace. Bound inputs outside it retain their original
lineage. Final assembly accepts only exact IDs with matching immutable refs and
current lineage; equal refs elsewhere never redirect associations. Original keys
and collision rules are preserved. Brief/provenance IDs are reserved against all
original IDs before publishing. Internal context/feedback/conversation documents
are filtered before metadata. Sources retain declared order after duplicate/self
removal; unattached or ambiguous associations are omitted and disclosed.

The current attached decision brief is primary, order zero, and overview. Known
checkpoint documents get explicit titles/descriptions and orders 1..99. Other
valid producer roles/orders survive. Historical briefs cannot become current
overviews. Metadata is descriptive only; diagnostic classification never removes
material findings or original attachments.

The helper enforces text bounds (120/300 Unicode code points, valid UTF-8, no
ASCII controls), roles, integer orders 0..1000000 and at most 128 distinct attached
sources. More than 128 valid sources omits the whole source list, with incomplete
coverage disclosed. It does not truncate prose or silently claim complete coverage.

The presentation byte budget is 65536, measured as compact typed Go encoding/json
of present optional fields, including HTML and U+2028/U+2029 escaping. Local
canonical encoding must be verified against the authoritative typed c2j fixtures
before enabling it. Budget degradation omits producer entries in descending final
ID byte order, then supporting/diagnostic checkpoint entries, then other checkpoint
entries, retaining brief metadata/overview last. Unverifiable or oversized minimal
presentation omits both fields. Brief/provenance record coverage before freeze;
original documents and material content are never pruned to fit presentation.

Final assembly treats annotation records as ownership evidence, not chronological votes.
Competing producer origins, divergent lineage chains, or conflicting records at
the same occurrence and lineage omit producer metadata with an incomplete-coverage
notice. A longer lineage supersedes a shorter one only within the same producer
occurrence and when it extends the complete shorter chain. Matching source claims
must likewise share one extending chain; unresolved source ambiguity omits the
association. Original attachments and recipe-owned checkpoint presentation remain.

## Deployment policy and current release status

Operators package `recipes/kernel/review-presentation.yaml` with the single policy
interface `review_document_annotations: legacy|annotated_v1`. This is deployment
configuration, resolved before content generation, not a hook variable, ticket
input, producer output or human answer. The same packaged policy applies at every
shared review gateway, including repair and creation.
Pin the recipe revision consistently for workers and child recipe selectors;
custom deployment variants must preserve this operator interface and policy.

The delivered default is legacy. Missing/unknown values select legacy with a
configuration diagnostic. Legacy constructs forms omitting **both**
`document_metadata` and `overview_document_id`: no nulls or empty placeholders.
Ordinary brief/provenance/original attachments remain available.

On 2026-10-31, read-only inspection of c2j commit
`a501d923f05378adc54d04bd87a689ee291f7afb` found the complete metadata implementation
and authoritative fixtures in `pkg/input/document_metadata.go`,
`pkg/input/review_metadata_test.go` and `pkg/input/testdata/review-presentation.json`.
Its `GUIDE-Review-Recipe-Authors.md` explicitly labels the feature **unreleased**
and says the release workflow must publish the first supporting tag and delivered
commit. That source commit is **not** a minimum supporting release. The installed
CLI identifies itself as `v0.0.113-0.20261030062615-9aff0af49df3+dirty`; this likewise
is not eligibility evidence. No actual supporting release tag is currently
verified. **Annotated production activation is unavailable.** Do not replace this
status with HEAD or infer support from permissive decoding.

When c2j delivers the supporting release:

1. Record its actual first supporting tag and delivered commit here and in the
   packaged policy's `supporting_tag`/`supporting_commit`. Retain the release's
   authoritative validation, serialized transport and freeze/replay test evidence.
2. Verify the local canonical encoder against that release's typed fixtures,
   including byte limits and escaping; only then mark `canonical_verified` true.
3. Inventory executing workers and form-serving integrations. Upgrade and pin all
   to the delivered minimum or a later compatible release. Upgrade strict clients
   or explicitly exclude them from annotated reviews. Cortex independently pins
   its supporting dependency and verifies consumer selection/rendering.
4. Mark `release_verified` and `fleet_eligible` true only with these records, then
   package `review_document_annotations: annotated_v1` for new occurrences.
   Neither source inspection nor version probing sets these flags automatically.

The helper falls back to legacy if any eligibility condition is missing. The
flags document operator attestation; they are not a capability-discovery API.
Do not activate a variant based on fixture-only eligibility values used in tests.

## Replay, revision and rollback

Published presentation, mode, sources and refs are recorded in the occurrence's
provenance and durable outputs, then frozen with the input form. Replaying that
form does not rerun producers or rebuild metadata. Mode changes affect new
occurrences only. New feedback, uploads, candidates or sources follow existing
revision rules and obtain fresh occurrence-bound content. Uploaded annotations
request revision, never implicit approval.

Rollback selects legacy for new occurrences. Retain compatible workers and readers
for already frozen annotated forms; runtime downgrade retention is not guaranteed.
Routing, actors, prerequisite/consultation keys, actions, receipts, stale-candidate
checks and accounting gates retain their original meaning. No deprecation or
removal of legacy behavior is proposed.

See `recipe-tests/review-annotations-statements.md` for the additive acceptance plan.
Native producer tests and helper boundaries do not establish release, fleet or
Cortex visual acceptance; report those separately during delivery.
