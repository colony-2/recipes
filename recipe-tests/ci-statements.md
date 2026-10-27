# Recipe CI test statements

Defined before implementing `.github/workflows/recipes.yml`.

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / GitHub Actions | `.github/workflows/recipes.yml` | Pushes to main and pull requests run deterministic recipe tests on Linux. |
| Critical | Integration / npm, GitHub Releases | `.github/workflows/recipes.yml` | Each run installs the latest published c2j npm package and records the selected version. |
| Critical | Integration / c2j, Nix, public Cachix cache | `.github/workflows/recipes.yml` | Repository-wide discovery executes recipe cases with their declared tools and requires no live model credentials. |
| Critical | Integration / c2j, GitHub Actions | `.github/workflows/recipes.yml` | A required recipe failure fails CI; logs and test reports remain available for diagnosis. |
| High | Integration / c2j | `.github/workflows/recipes.yml` | Live suites remain visibly excluded unless explicitly requested outside this workflow. |
