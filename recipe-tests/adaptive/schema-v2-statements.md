# Schema v2 migration acceptance statements

Defined before implementation. Recipe migration fits this cell; schema parsing,
validation, and checkpoint persistence remain owned by c2j.

| ID | Priority | Level / dependencies | Statement | Files |
| --- | --- | --- | --- | --- |
| V2-01 | Critical | Integration / c2j v2 | Public build, creation, and consultation inputs accept native annotations, including their artifact references, without JSON strings or transport sidecars. | build.yaml, create.yaml, recipes/adaptive/consultation.yaml |
| V2-02 | Critical | Integration / c2j v2 | Sessions use checkpoint declarations and retain their identities across resumed turns, includes, and child jobs. | build.yaml, create.yaml, recipes/adaptive/consultation.yaml |
| V2-03 | High | Integration / c2j v2 | Adaptive fixtures accept native lists and objects, preserving defaults, empty collections, and negative diagnostic cases. | recipe-tests/adaptive/*.yaml |
| V2-04 | Critical | Integration / c2j v2 | Child jobs receive annotations as typed inputs and preserve document descriptions, references, and source relationships when returning results. | recipes/adaptive/coordinate.yaml |
| V2-05 | Critical | Integration / c2j v2 | Schema migration preserves model response schemas, verification gates, human acceptance, and existing artifact delivery. | recipes/adaptive/*.yaml, recipes/create/*.yaml |
| V2-06 | High | Integration / c2j v2 | A v2 entrypoint can call existing v1 helpers without reinterpreting their checkpoint or artifact contracts. | create.yaml, recipes/kernel/*.yaml |
| V2-07 | High | Integration / c2j v2 | Public inputs reject serialized annotations, invalid document identities, and invalid artifact references before scheduling work, with errors identifying the offending fields. | build.yaml |

Validate native structured boundaries and the existing adaptive and creation
suites. Retain this document as a native fixture artifact. Replace assertions
about JSON sidecar transport with assertions about direct annotation delivery;
retain their document identity and descriptor expectations.
