# 富江 GitHub Sync Notes

## Target

- Repository: `a974046927/v2rayN`
- Folder: `fujie-codex-pet/`
- Sync method: GitHub connector, not local `git push`, because local git login was unavailable.

A dedicated repository such as `a974046927/fujie-codex-pet` would still be cleaner later, but the user requested this GitHub project folder for now.

## Latest Local Evidence

- Local app path: `E:\Codex 项目\杂谈\yoruame-desktop-pet`
- Transfer ZIP: `E:\Codex 项目\杂谈\fujie-codex-pet-transfer.zip`
- Latest local commit: `2fe8579 Add voice interaction flow`
- Tests: `41` passing via `python -m unittest discover -s tests -v`
- Loop engineering baseline: `16/16` passing via `python -m yoruame_pet.loop_benchmark`
- Speech dependencies installed locally: `SpeechRecognition 3.17.0`, `PyAudio 0.2.14`
- Audio device discovery worked locally; 44 input/output devices were detected, including `麦克风阵列 (Realtek(R) Audio)`.

## Latest Feature Sync Scope

The latest implemented feature batch includes:

- background voice question mode
- Windows voice reply speaker
- `语音` button in the question panel
- `V` hotkey on the focused pet window
- safe fallback when microphone, recognition, or speech output is unavailable
- voice config keys: `enabled`, `reply_enabled`, `timeout_seconds`, `tts_rate`, `tts_volume`
- loop benchmark gate: `voice_interaction_flow`
- new voice interaction unit tests

## Current Runtime Behavior

1. Open the pet.
2. Middle click or Ctrl+left click to open the question panel.
3. Click `语音`, or press `V` while the pet window has focus.
4. Wait for `我在听，哥哥你说。`.
5. Speak the question.
6. The recognized Chinese text goes through the same assistant flow as typed questions.
7. The pet displays the answer in the manga bubble and sends the pet-styled line to Windows speech synthesis when enabled.

## Girl Persona Addressing Rule

少女模式只能称呼用户为：

- `夜雨哥哥`
- `哥哥`
- `凌凌哥哥`

Bare `夜雨` must not appear as a girl-persona address.