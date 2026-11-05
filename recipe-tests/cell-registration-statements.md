# Cell registration expectations

Defined before implementing the registration node.

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| CR-01 | Critical | Integration / c2j | Approved cell registration runs in root with an explicit creation grant before initialization, without granting creation to other tasks. | recipes/create/register-cell.yaml, recipes/create/publish.yaml |
| CR-02 | Critical | Integration / c2j | Retrying the same approved registration returns the same registry identity; conflicting names or changed repository mappings fail without publication. | recipes/create/register-cell.yaml |
| CR-03 | Critical | Integration / c2j | Missing creation authority or non-root ownership prevents registration, even when the task selects the root workspace. | recipes/create/register-cell.yaml |
| CR-04 | High | Integration / c2j artifacts | A successful registration remains recorded if initialization subsequently fails. | recipes/create/register-cell.yaml, recipes/create/publish.yaml |
| CR-05 | Critical | Integration / c2j, Git | Registry creation supplements purpose publication and root dependency integration; registration alone never reports a cell as ready. | create.yaml, recipes/create/publish.yaml |
