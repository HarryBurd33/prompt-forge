# Migrating to Prompt Forge

## v0.2.0 to v0.3.0

Select the existing discovery root; do not create a second installation:

```sh
python3 scripts/install.py --root ~/.codex/skills --upgrade
```

Only the exact five-file canonical v0.2.0 manifest is recognized. An extra file, edited byte or symlink refuses the upgrade; preserve customizations for a manual merge. The helper stages and verifies the full new package before moving the old folder to `ROOT_PARENT/.prompt-forge-backups/prompt-forge-v0.2.0-N/`. A sibling `.json` record binds old/new hashes to that root. Both stay outside discovery. The helper recognizes aliases only in the selected root; inspect other host/project roots separately to avoid competing installations. It does not claim cross-root discovery inventory.

Use the exact backup path printed by the upgrade to restore:

```sh
python3 scripts/install.py --root ~/.codex/skills --rollback ~/.codex/.prompt-forge-backups/prompt-forge-v0.2.0-1
```

Rollback verifies both trees and ownership, refuses changes made after upgrade, and moves the displaced v0.3.0 outside discovery before restoring v0.2.0. Repeated install/upgrade of the unchanged current version is a no-op. Keep the backup/record together. Ordinary rename failures restore moved directories where possible; interruption or power loss is not a transactional filesystem guarantee. Inspect an uncertain outcome before retrying.

## Optional global recommendation rule

```sh
python3 scripts/recommendation_rule.py install --codex-home ~/.codex --skill-path ~/.codex/skills/prompt-forge
python3 scripts/recommendation_rule.py remove --codex-home ~/.codex
```

`--codex-home` defaults to `CODEX_HOME` or `~/.codex`. The explicit `--skill-path` is the actual installed folder. The template `skills/prompt-forge/resources/recommendation-rule.md` has exactly one render variable, `{{SKILL_PATH}}`; the helper replaces it with the absolute installed `SKILL.md` path. The helper uses Codex's nonempty global `AGENTS.override.md` in preference to `AGENTS.md`; it does not modify project rules, configuration, or provider permissions. If precedence changes after installation, it refuses and asks for manual reconciliation rather than editing an ineffective file.

A private `.prompt-forge-recommendation-state.json` in Codex home stores original bytes, pre/post hashes, target and exact rendered block. Preserve this record. Zero blocks permits insertion; repeating the same owned block is idempotent; a changed owned block, duplicate/malformed markers or an unowned existing block refuses without touching the instructions. Unrelated bytes, including existing companion blocks, remain unchanged. Removal deletes only the unchanged owned block and its still-adjacent owned separator, preserving later unrelated edits; it never restores the entire stale global file. A missing ownership record requires manual reconciliation. Symbolic instruction/state files are refused. A pending receipt is saved before instruction mutation, then finalized afterward. On retry, exact before/after hashes permit bounded recovery; unknown concurrent changes refuse and preserve the pending receipt for inspection. Multiwriter races still require inspection; this helper is not a background service or lock manager.

Fresh-chat recommendation behavior and installed invocation require actual host verification separately from successful copying. Host-wide recommendations depend on the loaded rule, instruction precedence, user intent and available skill discovery; metadata alone is insufficient.

## Legacy Adaptive Prompt Builder migration

Prompt Forge v0.2.0 replaces Adaptive Prompt Builder. Use one installed name to avoid duplicate skill discovery. The repository's `skills/prompt-forge/` directory is canonical. `skills/adaptive-prompt-builder/` is a generated, standalone compatibility copy with the same behavior, references, template, and license. It works independently when installed by itself. Its legacy name, title, and explanatory alias note are the only differences.

From the repository root, use Python 3.9 or newer:

```sh
python3 scripts/install.py --root ~/.agents/skills
```

The helper installs only `prompt-forge`. To migrate an existing legacy installation:

```sh
python3 scripts/install.py --root ~/.agents/skills --migrate
```

`--root` means the directory containing installed skill directories. The default personal location is `~/.agents/skills`; use `--root .agents/skills` for a project installation. For a legacy host that discovers `~/.codex/skills`, pass that path explicitly. The helper migrates within the selected root, so select the root where the old skill is actually installed. You can use any disposable directory to try the helper first. The helper has no runtime dependencies and does not edit application settings. Reload skills or restart the host if needed after installation.

Migration recognizes exact file hashes from the original v0.1.0 release, the generated v0.2.0 alias and the current generated alias. It prepares and verifies the canonical copy, moves the unchanged legacy directory into `ROOT_PARENT/.prompt-forge-backups/adaptive-prompt-builder-N/`, then installs Prompt Forge. For `~/.agents/skills`, backups live under `~/.agents/.prompt-forge-backups/`, outside the skills discovery directory. If the current canonical version is already installed unchanged, it is reused. Repeating an installation or migration leaves the installed bytes unchanged and creates no additional backup after the legacy directory has been migrated.

The helper refuses to overwrite customized, unrecognized, or extra files in either relevant skill directory. It also refuses symlink installations. On refusal, existing skill files stay unchanged. For a custom installation, make a manual merge into a separate copy of Prompt Forge, preserving your edits. Review the result, move the old custom installation outside the discovery directory, and install your reviewed copy yourself. There is no force or overwrite switch. Keep backups until you are satisfied with the migration.

If a host requires the old name, copy only `skills/adaptive-prompt-builder/` to that host's skills directory. Do not install both names. To roll back a helper migration, move the canonical installation outside discovery, then restore the desired backup to `adaptive-prompt-builder/` under the skills root.

## Existing repository clones

The GitHub repository is now [HarryBurd33/prompt-forge](https://github.com/HarryBurd33/prompt-forge). Update the remote in an existing clone:

```sh
git remote set-url origin https://github.com/HarryBurd33/prompt-forge.git
git remote -v
```

The old GitHub repository URL redirects to the renamed repository. Updating the remote makes the current destination explicit. Existing clone contents and local changes do not need to be replaced.

## Distribution maintenance

Edit the canonical skill and run:

```sh
python3 scripts/package.py
python3 scripts/package.py --check
python3 -m unittest discover -s tests -v
```

The builder synchronizes the full alias, generates both portable prompts, and produces `dist/prompt-forge-v0.3.0.zip` plus `dist/SHA256SUMS`. Version metadata must agree with the packaging version. Checks reject broken or escaping source links, generated drift, changed frozen v0.1.0 archive bytes, and unsafe ZIP paths. The new ZIP contains only a complete `prompt-forge/` directory. Alias behavior is generated from the canonical source rather than maintained separately.

Historical `dist/adaptive-prompt-builder-v0.1.0.zip` and `dist/prompt-forge-v0.2.0.zip` remain unchanged and listed in checksums. The checksum for `portable/adaptive-prompt-builder.md` tracks its current generated compatibility content. Frozen v0.1.0 evaluations are historical evidence, not evaluation results for v0.2.0.
