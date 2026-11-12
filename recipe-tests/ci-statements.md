# Recipe CI test statements

Defined before implementing `.github/workflows/recipes.yml`. The npm installation statement remains the release-pin control; source pins add the immutable-source control below without removing npm support.

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / GitHub Actions | `.github/workflows/recipes.yml` | Pushes to main and pull requests run deterministic recipe tests on Linux. |
| Critical | Integration / npm, GitHub Releases | `.github/workflows/recipes.yml` | Each run installs the exact c2j npm release pinned in .c2j-version and records its version and source commit. |
| Critical | Integration / c2j, Nix, public Cachix cache | `.github/workflows/recipes.yml` | Repository-wide discovery executes recipe cases with their declared tools and requires no live model credentials. |
| Critical | Integration / c2j, GitHub Actions | `.github/workflows/recipes.yml` | A required recipe failure fails CI; logs and test reports remain available for diagnosis. |
| High | Integration / c2j | `.github/workflows/recipes.yml` | Live suites remain visibly excluded unless explicitly requested outside this workflow. |
| Critical | Integration / Git, Go 1.26.8 | `scripts/install-c2j.sh`, `.github/workflows/recipes.yml` | Source pins fetch the exact public commit, preserve readonly module resolution, and identify the runtime without inventing a release version. |
