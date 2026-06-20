# 富江 GitHub Sync Notes

Recommended repository:

- `a974046927/fujie-codex-pet`

Do not place this pet package inside unrelated repositories such as `v2rayN`
unless explicitly requested.

## Repository Layout

Use this layout when uploading to GitHub under `fujie-codex-pet/`:

```text
fujie-codex-pet/README.md
fujie-codex-pet/MAC_SYNC.md
fujie-codex-pet/GITHUB_SYNC.md
fujie-codex-pet/LOOP_ENGINEERING.md
fujie-codex-pet/MANIFEST.sha256
fujie-codex-pet/design/FUJIE_DESIGN_SPEC.md
fujie-codex-pet/codex-pet-fujie/pet.json
fujie-codex-pet/source/yoruame_pet/*.py
fujie-codex-pet/tests/*.py
fujie-codex-pet/qa/runtime-check.md
fujie-codex-pet/qa/loop-engineering-baseline.md
```

## Codex Pet Metadata

```json
{
  "id": "fujie",
  "displayName": "富江",
  "description": "富江",
  "spritesheetPath": "spritesheet.webp"
}
```

## Current Local Evidence

- Local Codex pet folder: `C:\Users\lenovo\.codex\pets\fujie`
- Transfer ZIP: `E:\Codex 项目\杂谈\fujie-codex-pet-transfer.zip`
- Desktop shell: `E:\Codex 项目\杂谈\yoruame-desktop-pet`
- Tests: `38` passing via `python -m unittest discover -s tests -v`
- Loop engineering baseline: `15/15` passing via
  `python -m yoruame_pet.loop_benchmark`
- Latest local commit: updated after each feature/fix sync

## Current GitHub Status

The connected GitHub account is `a974046927`. The only writable repository
visible during the last sync check was:

- `a974046927/v2rayN`

The user requested a GitHub document rather than a new repository. The document
has been created and verified:

- Repository: `a974046927/v2rayN`
- Path: `fujie-codex-pet.md`
- URL: `https://github.com/a974046927/v2rayN/blob/master/fujie-codex-pet.md`
- Commit: `ad9370d40491dd71e26f6f46567b7a460669767a`
- Blob SHA: `e97e9bde75d75191db4f89e2b15823e62e4baea4`

New features and fixes are now synchronized into the `fujie-codex-pet/` folder
inside `a974046927/v2rayN`, matching the user's requested location. A dedicated
repository such as `a974046927/fujie-codex-pet` is still preferable if full
binary assets should be hosted on GitHub later.

## Latest Feature Sync Scope

The latest implemented feature batch includes:

- click-region interaction behavior
- affection, attention, persona, mood, and mood-intensity state
- random scare and lower-frequency idle talk
- double-click form switching
- generated dialogue system
- hard girl-persona addressing rule: only `夜雨哥哥`, `哥哥`, or `凌凌哥哥`
- rest, movement, and late-night reminders
- weather location/source tracking
- interactive typed question mode
- local document search
- AI-provider adapter with offline fallback
- optional voice-recognition adapter with safe unavailable fallback
