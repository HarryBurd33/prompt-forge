# Prompt Forge v0.2.0 validation

Validated on 2026-10-25. This release completes the canonical rename, compatibility distribution, safe migration, documentation, and requirement audit. It preserves the prior runtime instructions after an experimental rewrite failed to demonstrate a behavioral advantage under the frozen improvement gate.

## Release decision

The earlier audit identified optional post-draft wording as a possible weakness. Actual sequential tests now show that the previous skill can initiate focused post-draft questions, revise, propagate corrections, and stop at material closure. Both it and the proposed stronger wording passed the same checks. That small tie does not prove equivalence or greater reliability. The experimental rewrite remains private and is not the released or installed runtime.

The release's five runtime files match the baseline exactly after changing only the skill name, version, and title. An independent evaluator verified that comparison. The canonical skill SHA-256 is `567dea1703a23a650327930106ab2e5aec4e65d684da9fe85998fc14bf44d006`. See [release decision](../evals/v0.2.0/release-decision.json) and [independent report](../evals/v0.2.0/REPORT.md).

## Executed evidence

- **Behavior:** seven synthetic cases passed for both baseline and candidate, including actual sequential draft/refinement/correction/closure, contradictory requirements, supplied examples, missing tools, draft-now and resume.
- **Routing:** two response-behavior probes passed for both conditions. These are not native automatic-discovery tests.
- **Fresh chat:** three actual executions passed across structured classification and writing; the writing example's body was independently counted at exactly 120 words. No external email was saved or sent.
- **Distribution:** nine isolated tests passed, covering clean/repeat installation, original/current legacy migration, preservation of customized files, symlink refusal, standalone alias parity, link/drift rejection, and safe deterministic ZIP contents/checksums.
- **Format:** the official skill-creator validator passed the canonical skill, compatibility skill and extracted release ZIP.
- **Preservation:** all 16 prior frozen evaluation files and the original v0.1.0 ZIP remain unchanged. The original Git history and public repository identity are retained.

Behavior runs used `gpt-6.1-sol` at medium effort, with exact revision unknown. There were seven executor contexts, 35 actual responses, and no behavioral retries. The captured-artifact interval was 693.6 seconds; total orchestration time, per-case latency, token consumption and cost were not instrumented. Some cases shared a condition context; held-out generation and receiving executions used fresh contexts. Grading was independent but not blinded. Detailed protocol limits and the unchanged evaluation settings are in the report. No verified reliable local/free evaluator was configured; none is claimed to have run.

## Platform and installation limits

Deterministic checks ran on macOS arm64 with Python 3.15; the helpers target Python 3.9+ using the standard library, but older Python, Windows and Linux were not executed. The temporary validator dependency is not part of the runtime package. Prompt building itself has no Python dependency.

No existing installed Prompt Forge or Adaptive Prompt Builder copy was found in the standard personal/project skill directories, plugin cache, admin location, or matching local skill configuration. Tests installed into disposable directories only. Publishing does not install the skill in a personal directory. Custom installations outside the searched locations remain possible.

Native skill selection, other LLMs/hosts, live web research, cloud document saving, actual Excel creation, and end-to-end execution of every artifact route remain untested. Static instructions and historical tests are identified separately in the [requirements checklist](REQUIREMENTS.md). The release supports an interview workflow; it cannot guarantee unstated intent, tools, automatic triggers or unlimited persistence.

## Reproduce and roll back

Run `python3 scripts/package.py --check` and `python3 -m unittest discover -s tests -v` from the repository. Synthetic cases, independent rules, grades and evidence hashes are in `evals/v0.2.0`; they are now regression inputs, not future held-out cases. Private snapshots and full response logs are excluded.

Use [migration and rollback](MIGRATION.md) for installation changes. The original archive remains available, and original source is preserved at commit `1c438b4d4436c079f61ecddd4304997b945c7e11`. Do not force-reset customized working copies.
