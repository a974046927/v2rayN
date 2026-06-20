# 富江 GitHub Sync Notes

Recommended repository:

- `a974046927/fujie-codex-pet`

Do not place this pet package inside unrelated repositories such as `v2rayN`
unless explicitly requested.

## Repository Layout

Use this layout when uploading to GitHub under `富江/`:

```text
富江/README.md
富江/MAC_SYNC.md
富江/GITHUB_SYNC.md
富江/LOOP_ENGINEERING.md
富江/MANIFEST.sha256
富江/design/FUJIE_DESIGN_SPEC.md
富江/codex-pet-fujie/pet.json
富江/config/settings.json
富江/source/yoruame_pet/*.py
富江/tests/*.py
富江/qa/runtime-check.md
富江/qa/loop-engineering-baseline.md
富江/qa/codex-avatar-size.md
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
- Tests: `45` passing via `python -m unittest discover -s tests -v`
- Loop engineering baseline: `18/18` passing via
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

New features and fixes are now synchronized into the `富江/` folder
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
- Codex thread `添加宠物对话` configured as the dedicated user/pet dialogue
  thread
- background voice question mode
- Windows voice reply speaker
- local document search
- local pet-style fallback reply with no external API required
- desktop Codex task-status bridge that reads local Codex session events
- speech-recognition and PyAudio microphone dependencies installed
- voice-recognition adapter with safe unavailable fallback
- large desktop shell kept as canonical display; small Codex custom avatar
  selection disabled after rolling back the transparent-atlas workaround
