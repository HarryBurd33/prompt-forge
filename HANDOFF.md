# Prompt Forge v0.3.0 release handoff

The v0.3.0 runtime passed the frozen behavioral improvement gate and independent source review. The existing canonical installation is updated, seven file hashes match, the prior version is backed up, and the managed global recommendation rule preserves all unrelated instructions. Native recommendation, direct-execution exclusion and explicit invocation checks passed. See [validation](docs/VALIDATION-v0.3.0.md) for evidence and limitations.

The release is published on the existing public `main` branch at [source commit 18d8b016a34700b821f53b5aea2a65022c8c0962](https://github.com/HarryBurd33/prompt-forge/commit/18d8b016a34700b821f53b5aea2a65022c8c0962). GitHub readback confirmed tree `9d41f6a91402c6ab840f84a2b3296e45d21bd24b`, exactly matching the validated local release tree. The local main checkout was fetched and fast-forwarded to that source commit. This documentation-only completion record does not change the installed runtime. There is no remaining merge or release gate.

All 24 published file blobs matched their local Git hashes before the non-forced, expected-head branch update. The installed `SKILL.md` SHA-256 is `527239c38ea5ce0b88585aecdea462ee1f9971f0d3b9b279c50f62217901762a`; all seven installed files match the canonical source. The v0.3.0 ZIP SHA-256 is `362217c008ab0867e10068eed39c0b017ad337bb92e4bf05896a68a0ddd09de3`. Four fresh native installation checks passed, including actual catalog discovery and file-backed version verification. Private logs, checkpoint stores and personal instruction snapshots were not published.

Rollback: remove the unchanged owned recommendation block with `python3 scripts/recommendation_rule.py remove --codex-home ~/.codex`, then use `python3 scripts/install.py --root ~/.codex/skills --rollback EXACT_PRINTED_BACKUP`. Restore only after verifying no later customizations. See [migration](docs/MIGRATION.md).

## Capability follow-up

The [2026-11-08 audit](docs/CAPABILITY-AUDIT-2026-11-08.md) adds actual fresh-receiver XLSX, DOCX and research evidence plus usage examples. All four checks, including the no-browsing control, passed. The v0.3.0 runtime and installed files remain unchanged. Skill Forge owns the separate resource-check repair; its source/installation/publication status is recorded in that repository. Native Office/cloud and complete production capture limits remain explicit.

## Follow-up sessions 1–5

See [2026-11-11 validation](docs/FOLLOWUP-VALIDATION-2026-11-11.md) for the actual cloud round trip, fresh GitHub receiver and two requested-model text controls, plus current host limits. Runtime remains 0.3.0; all seven installed files match the canonical source exactly.
