# Excluded tests

Live suites require explicit `--include-live` and configured model credentials.
There are no retained disabled legacy build cases; those workflows and their
fixtures were removed. See [the cleanup assessment](../guides/ASSESSMENT_LEGACY_WORKFLOW_REMOVAL.md)
for deterministic results. Eighteen full-creation cases currently fail at the
known fixture identity boundary; they are enabled, not skipped. The user requested
a documented c2j requirement for that support.
