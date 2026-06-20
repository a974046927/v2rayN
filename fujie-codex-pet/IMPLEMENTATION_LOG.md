# Fujie Codex Pet Implementation Log

## 2026-06-20

### Local Commits

- `590427d Add assistant mode and loop benchmark`
- `1af844b Enforce girl persona address rules`

### Latest Verification

- Unit tests: `38` passing
- Loop engineering baseline: `15/15` passing
- Transfer ZIP: `E:\Codex 项目\杂谈\fujie-codex-pet-transfer.zip`
- Transfer ZIP SHA256: `29CE34B9453947875B3751E47F444B4F424E17DF2CF68878433CD16B3BF94585`

### Landed Features

- click-region interaction behavior
- affection, attention, persona, mood, and mood-intensity state
- random scare and lower-frequency idle talk
- double-click form switching
- generated dialogue system
- hard girl-persona addressing rule: girl form only uses `夜雨哥哥`, `哥哥`, or `凌凌哥哥`
- rest, movement, and late-night reminders
- weather location/source tracking
- interactive typed question mode
- local document search
- AI-provider adapter with offline fallback
- optional voice-recognition adapter with safe unavailable fallback
- local loop-engineering baseline

### Girl Addressing Fix

The latest fix adds a test that samples all girl-persona moods and triggers. It fails if a generated girl line starts with any unapproved address or contains bare `夜雨` after approved names are removed.

The dialogue generator now exposes `GIRL_APPROVED_NAMES = ("夜雨哥哥", "哥哥", "凌凌哥哥")` and normalizes accidental bare `夜雨` in girl-persona output back into the approved name set. Weather rain reminders were also changed from bare `夜雨` to `哥哥` so direct weather bubbles do not bypass the rule.
