# Runtime recipe tests cannot prepare mocked ops with optional secret defaults

Date: 2026-10-16 UTC
Status: Resolved; verified with c2j `6a25847a90d0` on 2026-10-16.
Owner: c2j native recipe test runtime / tenant configuration fixtures

## Resolution

Installed the latest GitHub main with
`go install github.com/colony-2/c2j/cmd/c2j@main`, yielding
`v0.0.79-0.20261016052546-6a25847a90d0` in `/home/shai/go/bin/c2j`.

The full `recipe-tests/build-cell-setup.test.yaml` case now passes with no
`runtime.secrets` or `runtime.config` fixtures. It completes all 14 mocked model
decisions, real schema gates, four review responses, the child mandate merge,
native parent refresh, and the parent feature merge. The parent sees the mandate
before its design phase, and the fixture repository contains both merged commits.
No production defaults or native Git operations were bypassed.

The runtime supplies an isolated empty secret provider and configuration store
by default, shared with child jobs. Optional missing values therefore use their
normal fallbacks. See [the testing guide](../GUIDE-Native-Recipe-Testing.md) for
explicit synthetic fixtures when a case needs present values.

The eight setup cases and native-default refresh regression also pass on this
version. The historical failure and diagnosis below describe the earlier build.

## Original impact

The native mandate-refresh tests now pass with c2j
`v0.0.78-0.20261016014732-ee1420b12dee`. On that version, the full build integration
test could not reach its mocked Codex decisions: preparing the published Codex
operation failed with `secret resolution unavailable`.

This is separate from the resolved `thinpackrebase` defects. The recipe keeps
the native refresh and normal operation defaults. No production secret defaults
were disabled to get the test past preparation.

## Reproduce

With Nix, flakes, and the trusted colony2 cache configured, from the recipes repo:

```sh
c2j test run \
  --file recipe-tests/build-cell-setup.test.yaml \
  --case-timeout 5m \
  --out-dir /tmp/build-cell-setup
```

This suite mocks every Codex response by selector and cell, while using real
child jobs, reviews, schema gates, Git persistence, and native refresh. The
model should never run or require real credentials.

The failure was observed with the CLI above and published Codex store output
`/nix/store/n3xl51kv5l5k8xndji9n0ay6y6wri12l-c2ops-codex-0.1.0`.
Nix evaluation and package retrieval succeeded using Nix 2.20.6 through a
user-local nix-portable installation. This supersedes the earlier environment
failure where Nix was missing.

```text
executing op op=nix:github:colony-2/c2ops/published#codex
failed to execute op ... err="secret resolution unavailable"
```

The child fails before the model mock returns. The parent consequently cannot
complete initialization; retries reproduce the preparation error.

## Evidence and likely cause

The published Codex manifest has optional tenant defaults for its proxy settings:

```text
base_url: ${{ context.config.?codex_api_base_url.orValue(null) }}
api_key:  ${{ context.secrets.?codex_api_key.orValue(null) }}
```

`pkg/recipetest/runtime.go` constructs a toy runtime, engine, workflow control,
and service dependencies. It intercepts operation invocation for mocks, but
does not configure a tenant secret/configuration fixture provider. Preparation
still materializes the operation's defaults before that interception.

`pkg/secrets/session.go` reports `secret resolution unavailable` when no provider
exists. The fallback tests explicitly distinguish a missing key from an absent
provider: an optional reference's `orValue(null)` is not intended to hide a
provider outage. That production distinction should be preserved.

These code paths explain the observed failure; the test runtime's appropriate
provider/fixture integration belongs to c2j. Configuration defaults may need the
same fixture treatment once secret resolution is available.

## Expected behavior

- Runtime tests have an isolated tenant secret/configuration provider, with
  absent optional keys represented as missing keys rather than provider outages.
- Suites can explicitly supply fixture values when testing present keys.
- Mocked model operations can prepare with absent optional tenant settings
  without accessing real tenant credentials or making model requests.
- Required missing values and actual provider outages still fail.
- The existing full build case reaches its model mocks, four review responses,
  child merge, native parent refresh, and final parent merge without changing
  production recipes to suppress tenant defaults.

The eight `recipe-tests/cell-setup.test.yaml` cases, the minimal native-default
reproduction, and its live embedded submission pass independently of this issue.
