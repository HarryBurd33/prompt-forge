# Independent source review

I wrote the baseline behavioral responses before receiving this review assignment. I reviewed the frozen rubric and cases, the candidate skill and its supporting instructions, and the distribution repository's installer, package generator, and tests. I assessed source behavior separately from the frozen output comparison.

## Result

The candidate source contract meets the routing requirements in the frozen rubric. The portable-link and rollback backup-name defects were reproduced, corrected, and rechecked. I found no remaining source-contract blocker in the reviewed scope.

- `candidate/prompt-forge/SKILL.md:35,59–63` requires an optional offer after material refinement, preserves settled choices and immediate drafting, embeds the entire accepted project plan inside the copyable prompt, and keeps execution scoped to existing authorization.
- `candidate/prompt-forge/references/routing-and-companions.md:15–27` requires complete dependency order, bounded input and output scope, a qualified model and reasoning effort or provisional tier, cost evidence and handoff overhead, acceptance checks, consequential review, bounded escalation, milestone and transition checkpoints, and verified transitions or an inline manual fallback. The instructions preserve explicit choices and user authority. `candidate/prompt-forge/references/skill-forge-handoff.md:7` carries the contract into Skill Forge and Agent Forge builds.
- `scripts/install.py:32–39,80–93,117–137,154–180` recognizes exact v0.3 canonical and alias manifests and backs up recognized installs outside discovery. I compared both manifest dictionaries with the frozen v0.3 ZIP contents and checked the ZIP digest. Disposable local tests passed a v0.3 → v0.4 → v0.3 round trip and a v0.3 alias migration using the frozen candidate as the install source. Repository tests at `tests/test_upgrade_rule.py:64–97` cover v0.3 upgrade, rollback, idempotence, and customization refusal.

## Findings

1. **Fixed — Nested resource link escaped both portable prompts.** The candidate reference at `candidate/prompt-forge/references/skill-forge-handoff.md:7` adds a relative link to the routing contract. Before the packaging fix, the canonical and alias portable variants contained `](routing-and-companions.md#bounded-cost-aware-routing)` at generated lines 128 and 131 respectively, with no target beside the portable files. The revised generator at `scripts/package.py:92–117` resolves nested links relative to their source, includes each file once, and flattens labels. I ran the revised generator on the frozen candidate in memory and verified that both portable variants contain one bounded-routing section and zero remaining local-file links. `tests/test_distribution.py:129–135` adds coverage for both variants.
2. **Fixed — An older rollback mislabeled the displaced backup.** The original `scripts/install.py:171` named the displaced directory after the running installer's `package.VERSION`. A disposable v0.2 → v0.3 install rolled back by the v0.4 tool restored the correct v0.2 bytes and stored the displaced v0.3 bytes in `prompt-forge-v0.4.0-rollback-1`. The installer now uses a version-neutral displaced-directory prefix at line 171. I repeated the older rollback and verified the name `prompt-forge-rollback-1`, the displaced v0.3 manifest, and the restored v0.2 manifest.

The repository canonical source remained v0.3 during my initial check, so running the v0.4 package check there returned a version mismatch. My packaging and install checks used the frozen v0.4 candidate directly.
