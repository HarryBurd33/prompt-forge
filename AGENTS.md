# Maintaining Prompt Forge

`skills/prompt-forge` is the canonical skill. Edit it first, then regenerate the legacy alias, portable files, and package with `python3 scripts/package.py`. Preserve license notices and user customizations. Do not manually maintain divergent copies.

Use an appropriate model for each bounded task. Use ordinary effort for routine implementation; escalate for consequential ambiguity, failed checks, or important independent review. Prefer reliable local/free models when checks support their use. Do not claim a model or effort change that the host cannot perform. Higher reasoning and additional agents must justify their cost.

Freeze acceptance rules and evaluation settings before behavioral comparisons. Keep held-out inputs separate from the candidate author until the candidate is frozen. Use independent grading of actual outputs; retain prior frozen evidence unchanged. Record useful completion, retries, elapsed time, and observed usage, marking unavailable values unknown. Do not infer per-task token use or cost from shared account quota.

Checkpoint at meaningful boundaries. Keep private interview state, credentials, raw private conversations, live queue databases, and local evaluation workspaces outside the repository. Publish only sanitized cases, results, and handoffs. Commit meaningful milestones; use ordinary fast-forward pushes to the established repository, preserving its visibility and branch rules. Never force-push or delete the repository.

Before release, run package drift checks, distribution/migration tests, and relevant behavioral regressions. Document actual platform coverage and any blocked work in `HANDOFF.md`. Do not claim that a filesystem install proves native automatic discovery or cross-model behavior.
