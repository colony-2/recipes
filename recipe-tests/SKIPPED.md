# Temporarily excluded recipe tests

| Test ID | Suite | Reason and re-enable instructions |
| --- | --- | --- |
| `heavy-accepts-successful-unmerged-child` | [build-dependency-disposition.disabled.yaml](build-dependency-disposition.disabled.yaml) | [c2j clean hook pin requires an unnecessary child snapshot](../guides/BUG_C2J_HOOK_PIN_CHILD_SNAPSHOT.md) |

These cases retain their original assertions. The runner has no per-case skip flag;
`.disabled.yaml` excludes a suite from directory discovery while permitting explicit
`c2j test run --file ...` execution. Restore `.test.yaml` after the linked issue is fixed.
