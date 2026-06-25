---
title: "Ops"
weight: 50
---

Use the smallest op that matches the job. Prefer selector-backed c2ops for LLM, Codex, GitHub Actions, and policy gate behavior.

Use child recipe ops for explicit durable child-job lifecycle control. Use `child_group` when the parent needs fan-out/fan-in aggregation.
