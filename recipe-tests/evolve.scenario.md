# Evolve default acceptance scenarios

The shared cases in `verify-default-recipes.py` run against `evolve.yaml` as well
as build. They assert `.c2j` as the Codex target, enabled Shai sandboxing, default
artifact paths, recipe scope clarification and specialization locations, and
fresh review sessions with continued implementation sessions.

Real git fixtures cover retained implementation edits, discarded consultation
experiments, verification mutations, and squash integration.
Run `./recipe-tests/run-defaults.sh`; see TS-107–TS-120 for the outcome contracts.
