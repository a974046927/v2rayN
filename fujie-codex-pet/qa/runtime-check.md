# Runtime Check

## Current Status

- Local app path: `E:\Codex 项目\杂谈\yoruame-desktop-pet`
- Launcher: `E:\Codex 项目\杂谈\yoruame-desktop-pet\run_pet.ps1`
- Current renderer: high-resolution decoded row strips from
  `E:\Codex 项目\杂谈\pet-runs\yoruame-kagehime\decoded`
- Fallback renderer: Codex atlas
  `C:\Users\lenovo\.codex\pets\yoruame-kagehime\spritesheet.webp`
- Active runtime: one `pythonw.exe -m yoruame_pet` process confirmed.
- Codex built-in custom avatar selection has been disabled in
  `C:\Users\lenovo\.codex\config.toml` by commenting out
  `selected-avatar-id = "custom:yoruame-kagehime"`. The active small-avatar
  spritesheet is restored and remains non-transparent.

## Verified

- Unit tests pass with bundled Python and `python -m unittest discover -s tests -v`: `43` tests.
- Loop engineering baseline passes: `18/18` checks.
- Speech recognition dependencies are installed in the bundled Python runtime:
  `SpeechRecognition 3.17.0` and `PyAudio 0.2.14`.
- Audio device discovery works; 44 input/output devices were detected,
  including `麦克风阵列 (Realtek(R) Audio)`.
- Window startup works with Tkinter.
- Window no longer uses enlarged `192x208` cells for desktop display.
- Purple outline was addressed by converting alpha sprites to a hard key-color
  RGB window frame before Tkinter draws them.
- Default animation speed changed from `130ms` to `260ms` per frame; idle now
  uses a slower `520ms` state-specific frame delay.
- Idle self-talk/scare checks now wait longer and trigger less often.
- Standby ambient motion is restored: ordinary idle can now low-frequency
  rotate through waving, running, and jumping, with running/jumping slowed to
  `420ms` per frame.
- Dialogue bubble changed from a plain rectangle to a comic-style rounded
  speech bubble with a tail, thicker black outline, cute font candidates, and
  slightly cuter symbol/emoji dialogue.
- Dialogue content is now generated from persona, emotion, trigger source,
  affection, and intensity instead of fixed full-sentence templates.
- Generated dialogue now favors short spoken lines and avoids obvious AI-style
  explanatory wording.
- Girl persona names are limited to `夜雨哥哥`, `哥哥`, and `凌凌哥哥`.
- Girl persona lines also reject bare `夜雨` anywhere in the line; accidental
  bare addressing is normalized back into the approved girl-name set.
- Emotion state persists as `mood` and `mood_intensity`; bubble colors,
  decorations, and outline weight follow the current emotion.
- Click-region logic is implemented for face, hair, hand, body, and skirt/legs.
- Affection, attention time, persona, mood, and mood intensity persist in local
  state.
- Random scare and idle talk use lower-frequency idle checks.
- Double left click switches between girl and mature forms.
- Middle click or Ctrl+left click opens the interactive question panel.
- Interactive question mode checks local project and transfer documents first,
  then falls back to a local pet-style reply. No external API is required.
- Desktop Codex task-status bridge reads local Codex session events and shows
  manga-bubble status updates for task start, tool/command work, GitHub sync,
  research, and completion.
- Codex thread `添加宠物对话` is configured as the dedicated user/pet dialogue
  thread.
- Voice interaction is implemented as a background flow: the pet says she is
  listening, records speech without freezing the animation, sends recognized
  Chinese text into interactive question mode, then sends the pet-styled reply
  to Windows speech synthesis when voice replies are enabled.
- Voice input still has a safe fallback; when recognition is unavailable or
  unclear, it asks for typed input instead of crashing.
- Rest, movement, and late-night reminders are implemented.
- Weather fetch failure returns `None` and does not crash the app.
- Weather summaries now keep resolved location and source, using configured
  city first and IP lookup when no city is configured.
- Latest implemented modules include local search, local pet reply fallback,
  assistant question mode, voice recognizer, voice reply speaker, Codex task
  status bridge, and loop benchmark.
- Large desktop shell is the canonical display. The built-in Codex avatar atlas
  was already measured at `198/208px` content height, so the small visible size
  came from Codex's fixed avatar renderer rather than image padding.
- The transparent-atlas workaround was rolled back because it still leaves a
  second avatar renderer active. The final approach is to stop selecting the
  Codex built-in custom avatar and use the large desktop shell as the pet.

## Manual Items To Confirm

- Desktop pet looks clear enough at the current `360px` sprite height.
- Left click drag moves the pet.
- Left click body regions trigger different dialog.
- Right click triggers the scare/split state.
- Double left click switches form.
- Middle click or Ctrl+left click opens the question panel.
- In the question panel, click `语音` and speak after the pet says
  `我在听，哥哥你说。`
- Press `V` while the pet window has focus to start the same voice interaction.
- Long idle behavior is acceptable.
