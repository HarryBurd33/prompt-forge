# Prompt Forge v0.4.0 validation

Observed 2026-11-12 UTC. This upgrade makes an optional bounded model/effort plan part of the final standalone prompt. It was compared with v0.3.0 at commit `5d5284726f93a03425b5d409c5b31a78481ba24f`.

## Frozen behavioral comparison

Nine synthetic cases and a fixed rubric were frozen before construction. Three cases (R06–R08) were withheld from the candidate author. Each arm used a separate fresh executor requested as GPT-6.1 Sol / Medium; cases shared context within an arm. Exact serving revision, tokens and monetary cost were unavailable. One candidate was evaluated; no gate was weakened.

| Case | Check | v0.3.0 | v0.4.0 |
| --- | --- | --- | --- |
| R01 | One routing offer after refinement | Fail | Pass |
| R02 | Complete accepted task plan, model/effort, checks and handoffs | Fail | Pass |
| R03 | Preserve routing decline | Pass | Pass |
| R04 | Draft now, missing sources, no appended question | Pass | Pass |
| R05 | Explicit model/effort preserved with bounded plan | Fail | Pass |
| R06 | Agent Forge, unknown catalog, provisional roles and manual handoff | Fail | Pass |
| R07 | Latest correction removes Skill Forge routing | Pass | Pass |
| R08 | Standing preference, difficult diagnosis vs routine documentation | Fail | Pass |
| R09 | Exact CSV correction, empty fields, lightweight draft | Pass | Pass |

The independent reviewer found no critical violation in either arm and accepted all nine candidate cases. The reviewer was independent of candidate construction but had authored the baseline outputs; this is a non-blind comparison, not a fully independent benchmark. Actual responses, verbatim grading evidence, fixed inputs and hashes are in [the evaluation record](../evals/v0.4.0/independent-grades.json). These are synthetic model executions, not executed downstream project builds or measured savings.

## Source and distribution

The [source review](../evals/v0.4.0/independent-source-review.md) reproduced two distribution issues and verified their repairs: a nested reference link escaped into portable prompts, and an older rollback receipt could produce a misleading displaced-folder version. Portable generation now resolves nested resource links and includes each resource once. Rollback uses a version-neutral folder label.

Final verification: 25 deterministic distribution, migration and recommendation-rule tests passed, including exact v0.3.0 upgrade/rollback, idempotence, customization refusal and both portable exports. Package drift and metadata checks passed. The v0.1.0, v0.2.0 and v0.3.0 archives remain unchanged. The full seven-file skill, alias, portable prompts, v0.4.0 ZIP and checksums are synchronized.

## Limits

This validates prompt construction and distribution. It does not demonstrate live same-chat model switching, automatic continuation, native discovery in every host, globally minimum cost, or production access tracing. The test catalog and relative costs are deliberately synthetic. The receiver must verify current model IDs, supported efforts, capabilities, permissions and any cost evidence. Unsupported transitions produce a manual handoff; missing companions do not prevent a usable prompt. Prompt generation does not itself launch tasks or grant paid API or publication authority.

Earlier release and sessions 1–5 evidence remain historical. Current host switching limitations were not repaired by this instruction update. See [foundations](FOUNDATIONS-v0.4.0.md) and [migration/rollback](MIGRATION.md).
