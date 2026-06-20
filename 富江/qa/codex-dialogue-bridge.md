# Codex Dialogue Bridge

Date: 2026-06-21

## Current State

- Middle click on the pet, or Ctrl+left click, starts microphone voice interaction directly.
- `V` still starts voice interaction.
- `Q` opens the typed question window.
- Recognized speech is sent to the Codex thread named `宠物对话`.
- Active resumable thread id: `019ee617-e56c-7833-a036-4850de2ece1a`.
- The old non-resumable duplicate thread was renamed to `宠物对话-旧备份` and archived, not deleted.
- Codex replies are shown in the desktop pet manga bubble and are spoken when voice reply is enabled.
- The bridge uses local Codex CLI/app-server and does not require an external API key.

## Runtime Path

1. `YoruamePetApp.start_voice_interaction()` records microphone input in a background thread.
2. `YoruamePetApp.answer_question()` tries `CodexDialogueBridge` before local fallback.
3. `NodeCodexDialogueClient` sends UTF-8 JSON to `codex_app_bridge.mjs`.
4. `codex_app_bridge.mjs` starts `codex app-server`, resumes the configured thread, sends the recognized text with `turn/start`, collects `agentMessage` deltas, and returns the final reply.
5. The pet displays the returned text in the bubble and sends it to Windows speech synthesis.

## Verification

- `python -m unittest discover -s tests -p 'test_*.py'`: 49 tests passing.
- `python -m yoruame_pet.loop_benchmark`: 18/18 checks passing.
- Real bridge smoke test returned: `收到，哥哥，桥接初始化正常。`

## 2026-06-21 Console And Feedback Fix

- The bridge now starts `node.exe` with `CREATE_NO_WINDOW` on Windows.
- The helper starts the temporary `codex app-server` with `windowsHide: true`.
- After speech recognition, the pet immediately shows `我去宠物对话问一下，哥哥等我一下。`.
- The Codex thread request runs in a background worker, so the pet window does not appear frozen while waiting for the reply.
- Verification: 51 unit tests passing; loop baseline remains 18/18.
- Real voice-path simulation showed the waiting bubble first, then a Codex-thread reply in the pet bubble.
