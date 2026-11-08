# Prompt Forge v0.3.0 release handoff

The v0.3.0 runtime passed the frozen behavioral improvement gate and independent source review. The existing canonical installation is updated, seven file hashes match, the prior version is backed up, and the managed global recommendation rule preserves all unrelated instructions. Native recommendation, direct-execution exclusion and explicit invocation checks passed. See [validation](docs/VALIDATION-v0.3.0.md) for evidence and limitations.

Publication/readback is the remaining release step at this local checkpoint. Publish only this repository's sanitized changes by fast-forward to its existing public main branch, then record the verified source commit and final local synchronization here. Do not publish private logs, checkpoint stores or personal instruction snapshots.

Rollback: remove the unchanged owned recommendation block with `python3 scripts/recommendation_rule.py remove --codex-home ~/.codex`, then use `python3 scripts/install.py --root ~/.codex/skills --rollback EXACT_PRINTED_BACKUP`. Restore only after verifying no later customizations. See [migration](docs/MIGRATION.md).
