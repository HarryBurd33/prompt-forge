# Prompt Forge

Turn an idea into a standalone prompt another assistant can use in a fresh chat. Prompt Forge asks focused questions, challenges weak assumptions, makes drafts concrete, and follows up on consequential gaps until the brief is clear. It works across writing, research, planning, spreadsheets, software, GitHub work, and skill design.

**Prompt first; execution only when asked.** v0.3.0 adds selective recommendations, a concrete “deeper, not bigger” diagnosis, outcome routing to Skill Forge or Agent Forge, and optional Task Checkpoint / Model Switcher awareness. A copyable reusable prompt stays an ordinary prompt; companion skills remain optional.

## Research and real files

For research, ask:

> Use $prompt-forge to refine a research brief for [question]. Set the source scope, date range, evidence standards, exclusions, and final format. Produce a standalone prompt for my chosen research-capable assistant; do not research yet.

Copy the prompt into a host with verified research tools, then explicitly ask that host to execute it. If a Deep Research skill or product mode is available there, select it using that host's supported control; Prompt Forge does not install or activate an unavailable mode. Return findings for targeted refinement when useful. A no-browsing host must identify missing source access.

For real files, specify the file rather than just the application: “an .xlsx workbook with named sheets and formulas” or “a one-page .docx memo.” Prompt Forge prepares the prompt; the receiving host supplies authoring, recalculation and rendering tools. See the actually generated [workbook](examples/workbook-prompt.md), [document](examples/document-prompt.md) and [research](examples/research-prompt.md) prompts.

The [capability audit and fresh-receiver tests](docs/CAPABILITY-AUDIT-2026-11-08.md) verify these bounded workflows. The v0.3.0 runtime is unchanged; the supplement does not replace historical evaluation results.

## Install

Ask Codex:

```text
Use $skill-installer to install skills/prompt-forge from
https://github.com/HarryBurd33/prompt-forge.
```

Or extract [the complete skill ZIP](dist/prompt-forge-v0.3.0.zip) into `~/.agents/skills/`. The resulting path should be `~/.agents/skills/prompt-forge/SKILL.md`, with its references and template alongside it. For a project installation, use the project's `.agents/skills/` directory. These paths follow the [official OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills). If the skill does not appear, restart the host.

From a cloned repository, the safe install helper is:

```sh
python3 scripts/install.py --root ~/.agents/skills
```

Upgrading an unchanged Prompt Forge v0.2.0 in its existing root? Run `python3 scripts/install.py --root ~/.codex/skills --upgrade` (adjust the root to the actual installation). The helper verifies exact known hashes, backs up outside discovery, and refuses customizations.

Upgrading Adaptive Prompt Builder? Use `--migrate` and read [migration and rollback](docs/MIGRATION.md). Customized copies are preserved for a manual merge. The repository was renamed in place, preserving history and public visibility. `prompt-forge` is the canonical package, directory, and invocation name; the old name remains a generated standalone compatibility alias. Install one name, not both.

## Optional Codex recommendation rule

Skill metadata does not prove universal activation. To add a small recommendation rule to Codex's effective global instructions, after installing the skill:

```sh
python3 scripts/recommendation_rule.py install --codex-home ~/.codex --skill-path ~/.codex/skills/prompt-forge
python3 scripts/recommendation_rule.py remove --codex-home ~/.codex
```

The helper selects nonempty `AGENTS.override.md` before `AGENTS.md`, preserves unrelated bytes, records private ownership and refuses duplicate, malformed or customized blocks. It renders `{{SKILL_PATH}}` in the bundled template to the installed `SKILL.md`. The rule recommends refinement once for material uncertainty, honors declines and explicit execution, and skips settled work. It does not launch an interview automatically. Inspect the host's effective instructions and test a fresh chat; project instructions and user requests can still govern. See [migration and rollback](docs/MIGRATION.md) for removal and limits.

## Use it

```text
Use $prompt-forge to refine this idea into a reusable prompt:
[your rough idea]. Ask focused questions, challenge weak assumptions,
and clarify the intended outcome, artifact format, and destination.
```

For example:

```text
Use $prompt-forge to refine a prompt for turning messy meeting notes into
an action tracker. Help me decide whether I need a document, an Excel
workbook, or GitHub issues. Produce the prompt first.
```

For Skill Forge:

```text
Use $prompt-forge to refine my checkpoint-skill idea into a standalone
prompt for Skill Forge. Clarify which usage signal is observable,
what can trigger saving, what must be preserved, and how resumption
will be verified. Do not build the checkpoint skill yet.
```

For an executable agent:

```text
Use $prompt-forge to refine a build prompt for Agent Forge: a manually
invoked inventory-reconciliation agent with a playbook, toolbox, bounded
retries and recovery. Produce the prompt first; do not build it yet.
```

For a focused improvement:

```text
Use $prompt-forge. Deeper, not bigger: investigate stale dashboard counts
using raw logs and code. Preserve the existing scope. Draft now.
```

Respond to each focused question and react to the draft. When a material gap remains, Prompt Forge should initiate a concrete follow-up, revise the prompt from your answer, and check again. A complete request can finish immediately; there is no fixed question count or required approval ceremony.

| Say | Effect |
| --- | --- |
| `Quick` | Resolve blockers and draft sooner. |
| `Thorough` | Explore material branches and failure cases. |
| `Expert challenge` | Stress assumptions with examples and alternatives. |
| `Draft now` | Stop questions for this turn; give a provisional prompt with assumptions. |
| `Skip` / `Use your judgment` | Label an assumption or delegate routine choices. |
| `Go deeper` / `Deeper, not bigger` | Name the omitted practitioner action, raw material, method/tool and independent evidence; turn useful findings into prompt actions without expanding scope. |
| `Actually, make the output an Excel workbook` | Update the prompt, examples, and checks; retain unaffected decisions. |
| `Save a brief` / `Resume from this brief` | Preserve or restore the latest draft, decisions, gaps, and next action. |
| `Finalize` / `Prompt only` | End the interview with remaining limitations made explicit. |
| `Now carry it out` | Execute the prompt within the available tools and authorization. |

A direct task such as “sort these names” should be performed directly. The skill should not turn it into an interview unless you request prompt refinement.

## Other hosts and limitations

Paste [the portable instructions](portable/prompt-forge.md) into another LLM, then describe your idea. The file includes the supporting guidance. Hosts supporting Agent Skills may load the complete skill folder using their own setup procedure. Prompt building has no script, paid API, or Skill Forge dependency.

Available tools determine whether a recipient can browse, create files, edit a cloud document, or publish to GitHub. A prompt cannot add those tools, guarantee automatic activation, or recover a brief that was never saved. Unknown inputs and tool limits should be explicit. Private interview state is separate from distributable skill files.

## Validation and maintenance

v0.3.0 passed 19 matched behavioral cases (including four corrected fixture pairs), independent review, 22 filesystem tests and fresh native installation checks. See [v0.3.0 validation and limits](docs/VALIDATION-v0.3.0.md) and [foundations](docs/FOUNDATIONS-v0.3.0.md). Earlier reports below remain historical.

See the [requirements-to-evidence checklist](docs/REQUIREMENTS.md), [v0.2.0 validation](docs/VALIDATION-v0.2.0.md), [handoff](HANDOFF.md), and [foundations](docs/FOUNDATIONS.md). [v0.1.0 validation](docs/VALIDATION.md) and frozen evaluation records remain historical evidence, not claims about this release.

Maintenance uses Python 3.9+ and the standard library:

```sh
python3 scripts/package.py
python3 scripts/package.py --check
python3 -m unittest discover -s tests -v
```

The canonical instructions generate the compatibility copy, both portable files, ZIP, and checksums. [AGENTS.md](AGENTS.md) preserves the usage-saving and independent-evaluation policy. MIT licensed; the adapted Skill Forge example's notices remain in [LICENSE](LICENSE).

Recent evidence: [sessions 1–5 follow-up](docs/FOLLOWUP-VALIDATION-2026-11-11.md), including private cloud recalculation, a fresh GitHub receiver and bounded portability controls.
