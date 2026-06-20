# 富江 GitHub Sync Notes

## Target

- Repository: `a974046927/v2rayN`
- Folder: `fujie-codex-pet/`
- Sync method: GitHub connector, not local `git push`, because local git login was unavailable.

## Latest Local Evidence

- Local app path: `E:\Codex 项目\杂谈\yoruame-desktop-pet`
- Transfer ZIP: `E:\Codex 项目\杂谈\fujie-codex-pet-transfer.zip`
- Latest local commit: `9516457 Use Codex thread for pet dialogue`
- Tests: `40` passing via `python -m unittest discover -s tests -v`
- Loop engineering baseline: `16/16` passing via `python -m yoruame_pet.loop_benchmark`
- Active runtime restarted as `pythonw.exe -m yoruame_pet`.

## Dialogue Thread

The Codex thread `添加宠物对话` is configured as the dedicated user/pet dialogue thread.

- Thread id: `019ee5c4-f0b8-7951-87a0-2600aaabe3cd`
- The thread was initialized with Fujie's pet persona and addressing rules.
- Future conversation with the pet should happen directly in that Codex thread.
- The desktop pet still keeps its local question panel and voice path; it does not create a second local chat log.

## Latest Feature Sync Scope

- no external API required for desktop fallback replies
- local document search remains first priority
- unmatched desktop questions use local pet-style reply instead of mentioning missing external AI
- Codex thread `添加宠物对话` is the direct display surface for user/pet dialogue
- voice interaction remains available on the desktop pet

## Girl Persona Addressing Rule

少女模式只能称呼用户为：

- `夜雨哥哥`
- `哥哥`
- `凌凌哥哥`

Bare `夜雨` must not appear as a girl-persona address.