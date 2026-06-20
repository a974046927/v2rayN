# Runtime Check

## Current Status

- Local app path: `E:\Codex 项目\杂谈\yoruame-desktop-pet`
- Launcher: `E:\Codex 项目\杂谈\yoruame-desktop-pet\run_pet.ps1`
- Active runtime: one `pythonw.exe -m yoruame_pet` process was restarted after the voice update.
- The large desktop shell is the canonical pet display.

## Verified

- Unit tests pass with `python -m unittest discover -s tests -v`: `41` tests.
- Loop engineering baseline passes: `16/16` checks.
- Speech recognition dependencies are installed in the bundled Python runtime: `SpeechRecognition 3.17.0` and `PyAudio 0.2.14`.
- Audio device discovery works; 44 input/output devices were detected, including `麦克风阵列 (Realtek(R) Audio)`.
- Voice interaction runs as a background flow: she says she is listening, records speech without freezing animation, sends recognized Chinese text into question mode, then sends the pet-styled reply to Windows speech synthesis when enabled.
- Voice input and voice output both have safe fallbacks.
- Girl persona names are limited to `夜雨哥哥`, `哥哥`, and `凌凌哥哥`.
- Idle animation and spontaneous actions have been slowed down.
- Dialogue bubbles use manga-style colors, outline, symbols, and mood-specific UI.

## Manual Items To Confirm

- Click `语音` in the question panel and speak after `我在听，哥哥你说。`.
- Press `V` while the pet window has focus to start the same voice interaction.
- Confirm the spoken reply volume and voice are acceptable on this Windows machine.
