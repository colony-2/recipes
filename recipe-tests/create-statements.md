# Cell creation test statements

| Priority | Kind / dependencies | Files | Expected outcome |
| --- | --- | --- | --- |
| Critical | Integration / c2j, c2ops | `recipes/create/review.yaml` | Root creation resumes the consultant checkpoint and reviews project fit, existing alternatives, technology choices, repository destinations, and initial purposes together. |
| Critical | Integration / c2j reviews | `recipes/create/review.yaml` | Creation requires explicit approval; cancellation, redirection, incomplete documents, and annotations accompanying approval never authorize a push. |
| High | Integration / c2j artifacts | `recipes/create/review.yaml` | Requested changes and attachments resume the same planning session and require a revised consolidated review. |
| Critical | Integration / Git, gitvend | `create.yaml` | Approved initialization pushes PURPOSE.md through ordinary Git; gitvend creates an allowed missing repository without a separate provisioning request. |
| Critical | Integration / c2j, Git | `create.yaml` | Only successfully initialized cells are registered and reported as created; creation does not implement product features. |
| Critical | Integration / c2j, Git | `recipes/create/publish.yaml` | Each approved purpose is published as independent root history; the enclosing root repository retains its original history. |
| Critical | Integration / c2j, Git | `create.yaml`, `recipes/create/publish.yaml` | An existing destination branch fails publication without overwriting history or proceeding to root registration. |
| High | Integration / c2j, Git | `recipes/create/publish.yaml` | Initial publication honors the configured Git identity; c2j supplies the bot fallback when identity is absent. |
| High | Integration / c2j | `create.yaml` | Root registration resumes the approved session and receives only successful publication records and approved documents. |
| Critical | Integration / c2j, Git | `recipes/create/publish.yaml` | An empty purpose or failed copy prevents publication and returns no successfully created cell. |
| High | Integration / c2j reviews | `recipes/kernel/review.yaml`, `recipes/create/review.yaml` | Text questions accept answers without choice options; feedback resumes the same session before creation approval. |
| Critical | Integration / c2j, Git | `recipes/create/review.yaml`, `recipes/create/publish.yaml` | New cells always publish on main; the model's proposal schema contains no branch-selection field. |
