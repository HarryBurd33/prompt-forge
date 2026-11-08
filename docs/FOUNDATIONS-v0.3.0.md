# Prompt Forge v0.3.0 foundations

Sources inspected 2026-11-08; conceptual adaptation only, no third-party prose or code redistributed.

## 1. xixu-me/prompt-library — conceptual adaptation, no copied text

Repository: [xixu-me/prompt-library](https://github.com/xixu-me/prompt-library). Retrieved default `main` at `44c9baae80e50444448a777f35ae809771698531` (committer date 2026-10-17). Inspected actual files at that immutable ref:

- [writing/prompt-generator.md](https://github.com/xixu-me/prompt-library/blob/44c9baae80e50444448a777f35ae809771698531/writing/prompt-generator.md): objective, necessary context, constraints, output and useful examples form a concise actionable prompt. Adopt the general outcome/input/output contract; it aligns with current Prompt Forge and does not itself establish a new improvement.
- [templates/prompt-template.md](https://github.com/xixu-me/prompt-library/blob/44c9baae80e50444448a777f35ae809771698531/templates/prompt-template.md): paired example inputs and outputs help make intended behavior testable. Adapt only when an example discriminates a real failure; do not impose every template section on each user response.
- [development/code-review.md](https://github.com/xixu-me/prompt-library/blob/44c9baae80e50444448a777f35ae809771698531/development/code-review.md): source code plus context and concrete prioritized findings are useful raw-material patterns. Reject its general exhaustive review checklist and style changes as a default for a narrow bug investigation; D03 forbids that expansion.
- [LICENSE](https://github.com/xixu-me/prompt-library/blob/44c9baae80e50444448a777f35ae809771698531/LICENSE): actual root file is MIT, copyright 2025 Xi Xu, with notice retention for copies/substantial portions. Relevant Markdown files inspected showed no separate license header; recursive tree lists no NOTICE. Original implementation based on general ideas requires no copied text; if builder copies substantial text/code, retain the original copyright and full license notice.

Fit/gaps: useful community candidates, not validated prompt-science findings or ready-to-adopt routing/discovery code. No independent activation, companion or evidence-first behavior. Only actual matched runs can justify usefulness.

## 2. prompts.chat — reference and counterexample

Inspected [live homepage](https://prompts.chat/) and [Job Interviewer prompt](https://prompts.chat/prompts/cmj1zb0yc000ivl0rc9ka596e_job-interviewer) (page displayed two versions; immutable prompt revision unavailable). It illustrates one-at-a-time interaction but also rigid role-only output and waiting. Retain the general focused-question pattern already in Prompt Forge; reject obligatory persona, always waiting and hiding useful explanation. These would conflict with Draft now and ordinary execution. Community publication/popularity is not evidence of reliability.

Connected repository [f/prompts.chat](https://github.com/f/prompts.chat) default `main` at `ba34d09010de8e0f4cf1e75a87972be30497f975` (2026-11-08). Inspected:

- [LICENSE](https://github.com/f/prompts.chat/blob/ba34d09010de8e0f4cf1e75a87972be30497f975/LICENSE), [LICENSE-MIT](https://github.com/f/prompts.chat/blob/ba34d09010de8e0f4cf1e75a87972be30497f975/LICENSE-MIT), [LICENSE-CC0](https://github.com/f/prompts.chat/blob/ba34d09010de8e0f4cf1e75a87972be30497f975/LICENSE-CC0). Root mapping distinguishes MIT source/site-authored material from CC0 prompt data/user submissions, with MIT default for uncertain files. MIT notice names Fatih Kadir Akin and contributors. A website footer alone would not establish the entire codebase as CC0. No community prose is copied into the target.
- [plugins/claude/prompts.chat/skills/prompt-lookup/SKILL.md](https://github.com/f/prompts.chat/blob/ba34d09010de8e0f4cf1e75a87972be30497f975/plugins/claude/prompts.chat/skills/prompt-lookup/SKILL.md): explicit tool names and variable/default handling are useful examples of concrete capability contracts. Reject its always-search requirement and dependency on a prompts.chat MCP server; neither is necessary or verified for this target. Its metadata describes activation but cannot prove a different host's automatic discovery. Map this caution to D01/D09/D12.

Full `prompts.csv` read was attempted with the GitHub connector and failed as too large/unsupported. It was not inspected and is not a copied foundation. The live inspected prompt plus actual repository skill/license files supply the limited reference evidence stated here.

## 3. Anthropic overview and current model guidance — primary references

[Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview), retrieved live on 2026-11-08. It frames clear success criteria, empirical checks and a draft as prerequisites; it explicitly identifies the tutorial as Claude 3 material and points to living best practices when they differ. Adopt evaluation-before-iteration, not a claim that every problem is solvable by prompt changes. Immutable revision and reusable-content license were not established; reference only, no copied prose.

[Current prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), retrieved live same date. Useful general methods: explicit output/constraints, relevant varied examples, clear source/input boundaries, scope control and model-specific evaluation rather than assuming technique transfer. Reject broad feature-expansion examples for this request. Do not require XML universally or insert a mandatory research hierarchy. Map to D03/D09/D12/D13. Immutable revision and content-reuse license unavailable; living primary reference only.

[Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5), linked from current guidance and inspected live. Its current instructions remove prompts that demand reasoning reproduced in the answer and recommend effort calibration with model-specific evaluations. This confirms that the older tutorial's exposed-reasoning and assistant-prefill techniques must not be transferred blindly. Prompt Forge should ask for concise decision rationale and observable evidence, not hidden reasoning. Do not encode Claude API parameters, latest model identifiers or timing/latency assertions in this model-neutral skill. Exact immutable page revision/reuse license unverified. This check establishes guidance inspected, not a live Claude behavioral experiment.

## 4. Anthropic interactive tutorial — reference with scoped licensing

[anthropics/prompt-eng-interactive-tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial), default `master` at `0d277542e927652da25b0014c9b346723af55881` (2024-04-08). GitHub metadata reports later repository pushes but the inspected default-branch commit is the revision used; do not substitute pushed_at for file version.

Inspected [README.md](https://github.com/anthropics/prompt-eng-interactive-tutorial/blob/0d277542e927652da25b0014c9b346723af55881/README.md) and the markdown/content cells of `Anthropic 1P/04_Separating_Data_and_Instructions.ipynb` and `Anthropic 1P/07_Using_Examples_Few-Shot_Prompting.ipynb` at that ref. README targets Claude 3 Haiku. The notebooks show why substitutable data needs explicit boundaries and demonstrate example input/output pairs. Adopt those general methods, with examples only where needed. Do not copy code, API credentials/setup, notebook exercises, role costumes, forced step-by-step output or assistant prefills; current model guidance is controlling when tuning a specific model.

The recursive tree has no root license and no license under `Anthropic 1P`. [AmazonBedrock/LICENSE](https://github.com/anthropics/prompt-eng-interactive-tutorial/blob/0d277542e927652da25b0014c9b346723af55881/AmazonBedrock/LICENSE) is actual MIT No Attribution with Amazon copyright; this does not establish reuse rights for the separate `Anthropic 1P` subtree. Treat 1P text as reference only. No tutorial code/text is redistributed. Map the conceptual input-boundary/example techniques to D03/D09/D13 and independent checks.

## Adoption decision and validation

Implement original concise instructions, retaining existing Prompt Forge/Skill Forge MIT notices. Add provenance links to the public report; no new dependency, MCP server, notebook runtime, corpus download, license bundle or provider-specific prompt pack is needed. None of these resources is a ready replacement for Prompt Forge's discovery, routing, companion or correction contract.

Candidate patterns selected: concrete outcome/input/output contract; raw evidence over paraphrased claims; relevant examples for discriminating boundaries; empirically checked success; current-capability honesty. Rejected patterns: decorative personas, compulsory interviews, always-search policies, exhaustive checklists, exposed hidden reasoning, hardwired provider/model tricks and gratuitous feature growth.

Actual usefulness requires matched model/settings and independent grading of development and held-out examples. Literature consistency is not observed improvement. This report records provenance and adoption choices, not a behavioral pass. No third-party source text is required for the original implementation.
