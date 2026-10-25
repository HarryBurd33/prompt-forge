# Prompt Forge

Turn an idea into a standalone prompt another assistant can use in a fresh chat. Prompt Forge asks focused questions, challenges weak assumptions, makes drafts concrete, and follows up on consequential gaps until the brief is clear. It works across writing, research, planning, spreadsheets, software, GitHub work, and skill design.

**Prompt first; execution only when asked.** A Skill Forge handoff is an option when building a reusable skill. Prompt Forge works independently.

## Install

Ask Codex:

```text
Use $skill-installer to install skills/prompt-forge from
https://github.com/HarryBurd33/prompt-forge.
```

Or extract [the complete skill ZIP](dist/prompt-forge-v0.2.0.zip) into `~/.agents/skills/`. The resulting path should be `~/.agents/skills/prompt-forge/SKILL.md`, with its references and template alongside it. For a project installation, use the project's `.agents/skills/` directory. These paths follow the [official OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills). If the skill does not appear, restart the host.

From a cloned repository, the safe install helper is:

```sh
python3 scripts/install.py --root ~/.agents/skills
```

Upgrading Adaptive Prompt Builder? Use `--migrate` and read [migration and rollback](docs/MIGRATION.md). Customized copies are preserved for a manual merge. The repository was renamed in place, preserving history and public visibility. `prompt-forge` is the canonical package, directory, and invocation name; the old name remains a generated standalone compatibility alias. Install one name, not both.

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

Respond to each focused question and react to the draft. When a material gap remains, Prompt Forge should initiate a concrete follow-up, revise the prompt from your answer, and check again. A complete request can finish immediately; there is no fixed question count or required approval ceremony.

| Say | Effect |
| --- | --- |
| `Quick` | Resolve blockers and draft sooner. |
| `Thorough` | Explore material branches and failure cases. |
| `Expert challenge` | Stress assumptions with examples and alternatives. |
| `Draft now` | Stop questions for this turn; give a provisional prompt with assumptions. |
| `Skip` / `Use your judgment` | Label an assumption or delegate routine choices. |
| `Go deeper` | Explore a consequential uncertainty. |
| `Actually, make the output an Excel workbook` | Update the prompt, examples, and checks; retain unaffected decisions. |
| `Save a brief` / `Resume from this brief` | Preserve or restore the latest draft, decisions, gaps, and next action. |
| `Finalize` / `Prompt only` | End the interview with remaining limitations made explicit. |
| `Now carry it out` | Execute the prompt within the available tools and authorization. |

A direct task such as “sort these names” should be performed directly. The skill should not turn it into an interview unless you request prompt refinement.

## Other hosts and limitations

Paste [the portable instructions](portable/prompt-forge.md) into another LLM, then describe your idea. The file includes the supporting guidance. Hosts supporting Agent Skills may load the complete skill folder using their own setup procedure. Prompt building has no script, paid API, or Skill Forge dependency.

Available tools determine whether a recipient can browse, create files, edit a cloud document, or publish to GitHub. A prompt cannot add those tools, guarantee automatic activation, or recover a brief that was never saved. Unknown inputs and tool limits should be explicit. Private interview state is separate from distributable skill files.

## Validation and maintenance

See the [requirements-to-evidence checklist](docs/REQUIREMENTS.md), [v0.2.0 validation](docs/VALIDATION-v0.2.0.md), [handoff](HANDOFF.md), and [foundations](docs/FOUNDATIONS.md). [v0.1.0 validation](docs/VALIDATION.md) and frozen evaluation records remain historical evidence, not claims about this release.

Maintenance uses Python 3.9+ and the standard library:

```sh
python3 scripts/package.py
python3 scripts/package.py --check
python3 -m unittest discover -s tests -v
```

The canonical instructions generate the compatibility copy, both portable files, ZIP, and checksums. [AGENTS.md](AGENTS.md) preserves the usage-saving and independent-evaluation policy. MIT licensed; the adapted Skill Forge example's notices remain in [LICENSE](LICENSE).
