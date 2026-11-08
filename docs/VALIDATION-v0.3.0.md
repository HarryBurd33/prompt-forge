# Prompt Forge v0.3.0 validation

Evaluated 2026-11-08. Baseline: committed v0.2.0 at `c0d5f80e299ccd1fad5225505ee60734313c28f8`. One runtime candidate was authored. The frozen improvement gate required every candidate observable, no critical/material regression, and at least one failing or partial new requested baseline behavior repaired under matched conditions. **The combined behavioral gate passed.** Packaging and live installation are separate checks below.

## What changed and why

The existing skill already handled focused questions, corrections, Draft now and standalone prompts well. The earlier v0.2.0 comparison tied and did not justify its proposed runtime rewrite; that historical record remains unchanged. This upgrade addresses new requested behavior: selective recommendations, a four-part evidence diagnosis, outcome routing, and optional companion awareness.

In the vague volunteer-notes case, the baseline started refining without a brief recommendation; the candidate identified audience/outcome uncertainty and offered Prompt Forge before interviewing. In the stale-dashboard case, both used raw logs and code, but the candidate added an independently derived expected count and fail-before/pass-after replay. The candidate answer grew from 240 to 331 words while preserving the smallest-fix/no-new-features boundary. In the mixed-agent case, it named Agent Forge as primary and Skill Forge for the subordinate skill, preserving one shared brief. These are observed narrow benefits, not evidence that longer prompts are always better.

## Matched real model runs

Configured executors: Codex CLI 0.166.0, `gpt-6.1-sol` / `medium`, signed-in subscription, read-only sandbox, same user inputs and tool settings for each pair. Exact serving revision was not exposed. An independent `gpt-6-astra` / `xhigh` reviewer graded actual outputs using frozen observables and critical failures. The first review used neutral X/Y labels and did not inspect candidate source or the arm map before saving grades. Supplementary review followed source inspection and was not blind.

There were 15 development cases (including a separately frozen existing-project recommendation case) and four held-out cases concealed from the constructor until runtime freeze. Cases cover vague ideas, direct execution, existing-project refinement, prompt/skill/agent/mixed routes, decline, Draft now, Quick/Skip/Resume, conflicting corrections, absent/current companions, unsupported tools and settled ongoing work. Each case started fresh; sequential cases replayed actual prior responses into fresh contexts. This tests response continuity, not native persistent-session resume.

The first 46 responses scored candidate 106/106 and baseline 90/106, but four pairs read current-host companion contracts outside the narrowly specified fixture. Their answer scores were preserved, not silently counted as clean evidence. A proposed correction using local companion files was rejected by automatic approval review; its partial baseline run was stopped and excluded. A safe correction supplied only contracts fetched from pinned public GitHub commits and forbade personal-file reads. Eight matched rerun responses resolved those four pairs without changing inputs, candidate or rubric. Independent audit verified all 26 commands stayed in staged fixtures. Agent routing D06 then tied, so its original improvement is not claimed.

**Combined clean evidence:** 15 original pairs plus four public-fixture rerun pairs; candidate **106/106, 19 full cases**, baseline **92/106, 12 full cases**. No observed critical failure or material candidate regression. Clean improvements remain in D01/D08/D15/H01 recommendations, D03/H03 diagnosis, D03 independent verification, and D07 mixed routing. Scores are rubric points, not 106 separate tests or a statistical accuracy estimate.

| Case | Baseline points | Candidate points | Evidence used |
|---|---:|---:|---|
| D01 | 2/4 | 4/4 | original matched run |
| D02 | 4/4 | 4/4 | original matched run |
| D03 | 5/8 | 8/8 | original matched run |
| D04 | 4/4 | 4/4 | original matched run |
| D05 | 6/6 | 6/6 | original matched run |
| D06 | 6/6 | 6/6 | public-fixture matched rerun |
| D07 | 5/6 | 6/6 | original matched run |
| D08 | 2/4 | 4/4 | original matched run |
| D09 | 6/6 | 6/6 | public-fixture matched rerun |
| D10 | 6/6 | 6/6 | public-fixture matched rerun |
| D11 | 4/4 | 4/4 | original matched run |
| D12 | 6/6 | 6/6 | original matched run |
| D13 | 6/6 | 6/6 | original matched run |
| D14 | 4/4 | 4/4 | original matched run |
| D15 | 2/4 | 4/4 | original matched run |
| H01 | 4/6 | 6/6 | original matched run |
| H02 | 6/6 | 6/6 | original matched run |
| H03 | 6/8 | 8/8 | original matched run |
| H04 | 8/8 | 8/8 | public-fixture matched rerun |

Public fixtures used Agent Forge at `5b62de4bbf0c968e39a134eb2dd04d0f3c45798d` (v0.1.0), Task Checkpoint at `8678db12c936b7d99998fd227d9127efb2a222d9` (v0.8.3), and Model Switcher at `7d06f4a882923d6eed5c01a42be8cae7dc446ad3` (v0.5.4). Task Checkpoint and Model Switcher main contracts matched the installed bytes. The local Agent Forge v0.2.0 differs from public v0.1.0 in optional freshness-binding guidance; these reruns do not certify that unpublished version or execute companion runtimes.

## Deterministic and static checks

All **22 disposable filesystem tests passed**, independently rerun by the parent and reviewer. Coverage includes existing distribution behavior, exact v0.2.0 upgrade, unchanged legacy v0.1/v0.2/current aliases, backup/rollback, custom/extra/symlink refusal, global override precedence, idempotent block installation, duplicate/malformed/customized block refusal, surgical removal preserving later edits, interrupted receipt recovery and injected directory/receipt failures. Unknown concurrent changes are preserved for reconciliation. This is not a power-loss or multiwriter transaction guarantee.

Package drift checks passed after integration into the canonical checkout. Both skill names passed metadata/relative-link validation (seven files, four relative links each); the validator is not a full YAML parser. Historical archives remain unchanged; the new ZIP and portable files are generated by the existing packaging workflow. Tests ran on macOS with Python 3.15; the helpers target Python 3.9+, but other Python/platform combinations were not run here.

## Native installation checks

The existing canonical installation was upgraded in place to v0.3.0 after the behavioral gate passed. All seven installed file hashes equal the frozen candidate. The exact prior v0.2.0 tree and hash-bound rollback receipt are outside skill discovery. No competing personal canonical/alias copy was found. The owned recommendation block was added to the effective global instructions; every preceding byte was preserved, and the host refreshed its loaded instructions with the new block.

Four fresh native CLI checks, using the actual installation and global rule rather than staged substitutes, passed: vague idea -> brief recommendation, clear CSV request -> exact sorted rows without an interview, explicit invocation -> usable standalone CSV prompt; catalog inspection -> one Prompt Forge entry at the actual installed path, with v0.3.0 verified through file-reading tools. Native CLI evidence is bounded; metadata and file copying alone do not establish universal desktop activation.

## Limits, provenance and privacy

Small synthetic samples, single runs, unknown exact model revision and unblinded supplemental grading limit generalization. No live cloud document/spreadsheet output, actual companion quota-triggered save/model transition, scheduled agent operation, other model or non-Codex host was tested. Prompt preparation does not authorize constructing its described artifact. External publication/readback is recorded separately in the release handoff.

The original 46-response matrix reported 2,906,374 input tokens (including 2,299,008 cached input tokens) and 21,295 output tokens; summed response elapsed time was 942.769 seconds across parallel runs. These are CLI-reported evaluation metrics, not total project tokens, cost or wall time. Supplementary runs, workers, review, setup and publication add overhead. Monetary cost is unknown; no paid API fallback was used. Shared account allowance is not attributable task cost.

Raw conversations, installed personal instructions, private task/checkpoint state, full evaluation records and grading packets remain outside the repository. This public report and [summary](../evals/v0.3.0/summary.json) contain sanitized outcomes and evidence hashes. [Foundations](FOUNDATIONS-v0.3.0.md) records inspected revisions, rights, adopted techniques and rejected patterns. No third-party prompt corpus/code or new runtime dependency is bundled. Rollback instructions are in [MIGRATION.md](MIGRATION.md).
