# Optional build title expectations

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| TITLE-01 | High | Integration / c2j, mocked agents | A build accepts an optional string title and supplies it with the original request to classification and development. | build.yaml, recipes/adaptive/build.yaml |
| TITLE-02 | High | Integration / c2j | Omitting title preserves the existing request and behavior. | build.yaml |
