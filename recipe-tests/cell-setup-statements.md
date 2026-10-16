# Cell setup test statements

- Existing root mandates let builds proceed without setup jobs, including builds targeting subdirectories. Files: `build.yaml`, `recipes/develop/cell-setup.yaml`; critical; integration; dependencies: c2j, Git.
- Missing mandates trigger one same-cell build to inspect responsibilities, likely purpose, and external dependencies. Files: `recipes/develop/cell-setup.yaml`; critical; integration; dependencies: c2j.
- Mandate initialization builds retain review gates and do not recursively request initialization. Files: `build.yaml`, `recipes/develop/cell-setup.yaml`; critical; integration; dependencies: c2j.
- Original builds resume with the merged mandate visible in their repository before design begins. Files: `build.yaml`, `recipes/develop/cell-setup.yaml`; critical; integration; dependencies: c2j, Git.
- Failed or unmerged initialization, refresh failures, and absent refreshed mandates prevent original build design. Files: `recipes/develop/cell-setup.yaml`; critical; integration; dependencies: c2j, Git.
- Development and consultation prompts describe whole-repository cells and responsibility-based mandates without requiring file inventories. Files: `recipes/develop/agent.yaml`, `recipes/develop/consult.yaml`; high; integration; dependencies: c2j.
- Mandates need no comprehensive dependency inventory; agents discover dependencies normally and use c2j's cell listing to assess likely influence. Files: `recipes/develop/cell-setup.yaml`, `recipes/develop/agent.yaml`, `recipes/develop/consult.yaml`; high; integration; dependencies: c2j.
- Parent builds refresh through the native Git operation; runtime failures remain visible without shell refresh fallbacks. Files: `recipes/develop/cell-setup.yaml`; critical; integration; dependencies: c2j, Git.
- Build agents retain artifact access and repository context using operation defaults. Files: `recipes/develop/agent.yaml`; high; integration; dependencies: c2j, Nix, c2ops.
