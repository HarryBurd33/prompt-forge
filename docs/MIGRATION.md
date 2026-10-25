# Migrating to Prompt Forge

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

Migration recognizes exact file hashes from the original v0.1.0 release and the current generated alias. It prepares and verifies the canonical copy, moves the unchanged legacy directory into `ROOT_PARENT/.prompt-forge-backups/adaptive-prompt-builder-N/`, then installs Prompt Forge. For `~/.agents/skills`, backups live under `~/.agents/.prompt-forge-backups/`, outside the skills discovery directory. If the current canonical version is already installed unchanged, it is reused. Repeating an installation or migration leaves the installed bytes unchanged and creates no additional backup after the legacy directory has been migrated.

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

The builder synchronizes the full alias, generates both portable prompts, and produces `dist/prompt-forge-v0.2.0.zip` plus `dist/SHA256SUMS`. Version metadata must agree with the packaging version. Checks reject broken or escaping source links, generated drift, changed frozen v0.1.0 archive bytes, and unsafe ZIP paths. The new ZIP contains only a complete `prompt-forge/` directory. Alias behavior is generated from the canonical source rather than maintained separately.

The original `dist/adaptive-prompt-builder-v0.1.0.zip` and its checksum remain available unchanged. The checksum for `portable/adaptive-prompt-builder.md` tracks its current generated compatibility content. Frozen v0.1.0 evaluations are historical evidence, not evaluation results for v0.2.0.
