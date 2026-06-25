# c2j Authoring Reference

This directory is a Hugo Markdown site for c2j recipe authoring. It uses the
Relearn documentation theme through Hugo Modules.

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

When changing theme dependencies, run Hugo from this directory once to refresh
module metadata:

```bash
cd docs
hugo mod tidy
```

Local layout overrides under `docs/layouts` keep Relearn clear of Hugo 0.159
deprecation warnings. Remove them after an upstream Relearn release carries the
same `hugo.Sites`, `Language.Locale`, and `Language.Direction` changes.

The source site is under `docs/content`. Runnable recipe examples and test suites are under `docs/examples`. The guide migration audit is in `docs/data/guide-audit.yaml`.
