# Prompt Forge handoff

Date: 2026-10-25. Release: v0.2.0. Repository: https://github.com/HarryBurd33/prompt-forge. Branch: `main`.

## Delivered

The original public Adaptive Prompt Builder repository was renamed in place; its repository ID, visibility and Git history are preserved. `prompt-forge` is canonical throughout the current skill, package, invocation and setup guide. A generated standalone `adaptive-prompt-builder` alias preserves old installations and invocation paths. The migration helper backs up recognized legacy copies outside discovery and refuses to overwrite customizations.

The proposed runtime rewrite was tested independently and was not adopted: both versions passed all seven behavioral cases and two routing probes, so the frozen improvement gate found no demonstrated benefit. This release retains baseline runtime behavior with only name/title/version changes. Three fresh receiving executions and nine distribution tests passed. See [validation](docs/VALIDATION-v0.2.0.md), [requirements](docs/REQUIREMENTS.md), and [independent evaluation](evals/v0.2.0/REPORT.md).

## Install and use

Ask the skill installer to install `skills/prompt-forge` from this repository, or run `python3 scripts/install.py --root ~/.agents/skills` from a clone. Existing legacy users should add `--migrate` and read [migration guidance](docs/MIGRATION.md). No personal installation was performed during this release; clean install and upgrade were tested in isolated directories.

Start with: `Use $prompt-forge to refine this idea into a standalone prompt: …`. Choose quick, thorough or expert challenge as useful. Draft-now, skip, judgment, go-deeper, resume and finalize controls remain available. Prompt creation is separate from execution; Skill Forge handoff is optional.

## Maintenance and remaining limits

Edit `skills/prompt-forge`, regenerate with `python3 scripts/package.py`, then run package checks and distribution tests. Follow [AGENTS.md](AGENTS.md) for usage-saving, checkpoints, independent grading and preservation of frozen evaluations. Choose ordinary effort for routine work, escalate only with a reason, and mark unavailable usage/time measurements unknown.

Native auto-discovery, other models/hosts, Windows/Linux, older Python and live cloud/Excel integrations remain untested. No separate Checkpoint and Handoff skill or Usage Router was built here. Experimental candidate snapshots, full model transcripts and private project state remain local outside this repository by design. There is no outstanding required runtime patch accepted by the evidence gate.

## Publication checkpoint

Source and distribution milestone: [`f9ef11be4042603324653d852975377570df89e9`](https://github.com/HarryBurd33/prompt-forge/commit/f9ef11be4042603324653d852975377570df89e9). The final documentation commit is its descendant containing this handoff.

The commit containing this handoff is the release checkpoint; use the repository's `main` history or `git rev-parse HEAD` in a synchronized clone to identify it. The final delivery records the exact remotely verified commit and tree. Git CLI upload credentials were unavailable in the build environment, so publication uses the authenticated GitHub connector with an ordinary fast-forward update; public Git fetch verifies the resulting tree. No force push, history rewrite, visibility change or repository deletion is involved.
