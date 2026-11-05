# Named-cell migration acceptance statements

Defined before implementation. Runtime registration grants belong to c2j/JobDB;
recipes own cell routing and the approved registration/publication sequence.

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| NC-01 | Critical | Integration / c2j named cells | Shared build configuration, classification, implementation, and publication select the owning cell by name, independently of its repository locator. | build.yaml, recipes/adaptive/build.yaml, recipes/adaptive/develop.yaml |
| NC-02 | Critical | Integration / c2j named cells | Consultation and prerequisite submission retain cell names separately from repository locations and deliver work to the agreed cell. | recipes/adaptive/coordinate.yaml, recipes/adaptive/resolve-target.yaml, recipes/adaptive/route-target.yaml |
| NC-03 | High | Integration / c2j named cells | Root creation targets the named root cell without deriving its identity from a repository URL. | create.yaml, recipes/adaptive/develop.yaml |
| NC-04 | Critical | Integration / c2j creation grant | Only the explicitly authorized root registration node can create approved cell records; agents and other nodes receive no creation grant. | recipes/create/publish.yaml |
| NC-05 | Critical | Integration / c2j, Git | Cell registration supplements approved purpose publication and root dependency configuration; registration alone never reports a fully created cell. | create.yaml, recipes/create/publish.yaml, recipes/create/initialize.yaml |
| NC-06 | Critical | Integration / c2j named cells | Invalid names, denied registration, and repository identity mismatches block dependent submission rather than using repository strings as cell identities. | recipes/adaptive/resolve-target.yaml, recipes/create/publish.yaml |

The delegated creation contract is available in c2j `d6553a2`. Registration must
retain its result before publication and reuse a stable request ID on replay.
Creation does not grant permission to submit initialization jobs to the new cell.
