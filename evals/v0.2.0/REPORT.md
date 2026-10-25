# Independent Prompt Forge upgrade evaluation

Evaluation date: 2026-10-25. Baseline commit: `1c438b4d4436c079f61ecddd4304997b945c7e11`. Candidate 1 skill SHA-256: `e24fdd9e855da02abc2dd6c77c6c0df0f5f50bcf7a18844dc1fec336006c18b1`.

**Verdict: all tested behavioral and routing cases pass for both versions; behavioral improvement is not demonstrated. Candidate 1 does not meet the frozen improvement gate and must not be activated as a proven behavioral upgrade.** This is a tied result, not a regression or a broad equivalence claim. Canonical rename, packaging and migration may proceed using preserved baseline runtime behavior and separate deterministic evidence. That release choice is distinct from adopting Candidate 1's new runtime instructions.

## Actual observed results

Scores: 0 fails, 1 partial, 2 meets frozen observables. No critical failures. Independent grader reviewed actual executor artifacts; executors did not grade their own work.

| Case | Coverage | Baseline | Candidate 1 | Questions baseline / candidate | Qualifying improvement |
|---|---|---:|---:|---|---|
| L1 | Rough draft → focused policy/design probe → revision → audience/duration correction → closure | 2 | 2 | 1,1,1,0 / 1,1,1,0 | No |
| D1 | Initial adaptive question, draft-now, artifact/audience correction, example and closure | 2 | 2 | 1,0,0,0 / 1,0,0,0 | No |
| D2 | Conflicting length, supplied hostile style example, immediate prompt vs future email draft | 2 | 2 | 1,0 / 1,0 | No |
| D3 | Missing browser/tools, future pasted sources, dates/unknowns, independent use | 2 | 2 | 0 / 0 | No |
| D4 | Quick, draft-now, delegated judgment, explicit assumptions | 2 | 2 | 0 / 0 | No |
| D5 | Resume from compact brief, corrected destination, final prompt | 2 | 2 | 0 / 0 | No |
| H1 | Held-out portable prompt generation and actual execution in unrelated fresh context | 2 | 2 | 0 / 0 | No |
| R1 | Explicit prompt request yields reusable prompt | 2 | 2 | 0 / 0 | No |
| R2 | Direct execution yields sorted list directly | 2 | 2 | 0 / 0 | No |

Both H1 fresh recipients actually produced ordered priorities `P2, P1, P3, P1, P2`, correct columns and evidence-grounded reasons. This demonstrates narrow text-only fresh-context execution. It does not demonstrate external artifact creation, tool integrations or platform-wide portability.

Candidate 1 prioritized the missing real policy first in L1; baseline first asked about participation/facilitation while visibly retaining the policy blocker. Both then initiated useful focused probes, revised drafts, propagated corrections and closed. The frozen observables passed for both; wording and question-order differences do not establish a repaired failing observable.

## Protocol and effort

Model requested for every bounded executor: `gpt-6.1-sol`, medium ordinary effort; exact model revision unknown. Host: Codex desktop collaboration execution. Both conditions used identical frozen user inputs, text-only task capabilities and effort settings. No network, publication, future task mutation or invented tool verification occurred in these runs.

L1 started in a fresh executor per condition. D1 and D2 followed in that same condition context, with each user turn supplied only after the prior response; future scripted turns were withheld. D3/D4/D5/R1/R2 were grouped independent requests sharing each condition's executor context. This saves usage but permits context effects. H1 generation used a separate fresh context per condition; execution used another unrelated fresh context receiving only the generated prompt. The user was synthetic; the model responses and receiving executions were real, not authored demonstration transcripts.

The independent evaluator froze criteria and the held-out input before candidate review; the candidate author received development inputs only until candidate freeze. Grading was independent but not blind to condition labels. One candidate, seven executor contexts, 35 actual case responses including the three fresh receiving executions; retries: 0. Baseline/candidate generation responses: 16 each, plus three receiving responses. Unnecessary interview questions observed: 0. Captured artifact interval: 693.6 seconds, measured from first response-file creation to final response-file modification; full orchestration wall time and per-case latency were not instrumented. Token usage, cost, local/free-model availability and precise model revision: unknown. The time budget was extended operationally from 30 to 60 minutes to complete actual sequential runs; acceptance criteria, model, effort and candidate limit were unchanged.

## Scope and limits

These are seven small synthetic behavioral cases and two routing probes, one run per condition, plus one fresh receiving execution per condition. The matrix does not establish native skill auto-discovery, all host/platform support, model superiority, statistical reliability, current web-fact retrieval, actual cloud document/email saving, all mode/control combinations, or private-state filesystem enforcement. Routing probes exercise response behavior under supplied skill instructions; they do not test a native platform selector. Clean install/migration/packaging and policy/source checks are separate static or deterministic evidence and cannot substitute for observed benefit.

The original version 0.1 frozen evaluation configuration is preserved. Full transcripts and snapshots remain private outside the repository. This public directory contains sanitized synthetic case definitions, frozen acceptance rules, independent grades, configuration and evidence hashes. H1 is now public synthetic regression material; future reuse must not be labeled held out.

## Supplemental email execution

After the tied matrix, root requested one bounded fresh execution of the baseline D2 generated prompt to cover a second artifact workflow. Its acceptance rules were frozen before the additional call; the original improvement gate and matrix scores were unchanged. One unrelated fresh text-only recipient actually produced the email, and an independent deterministic count found **120 whitespace-separated body words**. the fictional recipient, the fixture order, two-day delay and the fixture refund amount refund were preserved; subject was separate; there was no legal admission, invented refund-processing assertion or recipient address. The recipient reported that no draft was saved because email tools were unavailable. No email was sent. Correctness checks pass; the prose is somewhat stilted around uncertainty. This single-condition coverage addition cannot establish candidate improvement. See `d2-execution-grade.json` and `d2-execution-acceptance.md`; the full execution artifact remains private.

## Release decision

The chosen release uses the preserved baseline runtime instructions with canonical `prompt-forge` metadata, `Prompt Forge` title and version `0.2.0`. Independent source comparison confirmed all five runtime files equal the frozen baseline after only those three metadata/name substitutions; release skill SHA-256: `567dea1703a23a650327930106ab2e5aec4e65d684da9fe85998fc14bf44d006`. Candidate 1's additional runtime instructions were **not adopted**. The passing baseline behavioral evidence supports preserving that behavior, while rename, package and migration validation are separate deterministic checks. This source-preserving release decision does not claim candidate behavioral benefit, native discovery or new platform coverage. See `release-decision.json` for the release record. The matrix consists of seven behavioral cases and two routing probes; the supplemental email receiving execution adds a second artifact workflow without changing the improvement gate.

## Public evidence sanitization

The full email execution artifact is omitted from publication. Fictional recipient/order/refund identifiers are generalized in the public D2 case, acceptance presentation and grades; exact frozen originals and execution hashes remain private. This publication-only sanitization does not change the evaluated inputs, model settings, acceptance gate or results.
