# Classifier transport expectations

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| CL-01 | Critical | Integration / c2j, Python | Repository context exceeding stdout capacity is retained as an artifact and requires design without a JSON parsing failure. | recipes/adaptive/classify.yaml |
| CL-02 | Critical | Integration / c2j, Python | Missing, unreadable, oversized, malformed, or truncated context cannot authorize skipping design. | recipes/adaptive/classify.yaml |
| CL-03 | High | Integration / c2j, mocked Jev | Complete small context preserves its text and may skip design only with a valid low complexity assessment. | recipes/adaptive/classify.yaml |
| CL-04 | High | Integration / c2j, Python | JSON escaping and Unicode expansion count toward the inline transport budget. | recipes/adaptive/classify.yaml |
