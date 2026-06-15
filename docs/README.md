# c2j Authoring Reference

This directory is a Hugo Markdown site for c2j recipe authoring.

Useful commands from the repository root:

```bash
docs/scripts/validate-docs.sh
```

```bash
hugo --source docs --destination public
```

If `hugo` is not on `PATH`, set `HUGO_BIN`:

```bash
HUGO_BIN=/tmp/c2j-docs-bin/hugo docs/scripts/validate-docs.sh
```

The source site is under `docs/content`. Runnable recipe examples and test suites are under `docs/examples`. The guide migration audit is in `docs/data/guide-audit.yaml`.

