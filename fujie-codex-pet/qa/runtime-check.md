# Runtime Check

## Current Status

- Local app path: `E:\Codex 项目\杂谈\yoruame-desktop-pet`
- Launcher: `E:\Codex 项目\杂谈\yoruame-desktop-pet\run_pet.ps1`
- Current renderer: high-resolution decoded row strips from
  `E:\Codex 项目\杂谈\pet-runs\yoruame-kagehime\decoded`
- Fallback renderer: Codex atlas
  `C:\Users\lenovo\.codex\pets\yoruame-kagehime\spritesheet.webp`
- Active runtime: one `pythonw.exe -m yoruame_pet` process confirmed.

## Verified

- Unit tests pass with `python -m unittest discover -s tests -v`: `38` tests.
- Loop engineering baseline passes: `15/15` checks.
- Window startup works with Tkinter.
- Window no longer uses enlarged `192x208` cells for desktop display.
- Purple outline was addressed by converting alpha sprites to a hard key-color
  RGB window frame before Tkinter draws them.
- Default animation speed changed from `130ms` to `260ms` per frame; idle now
  uses a slower `520ms` state-specific frame delay.
- Idle self-talk/scare checks now wait longer and trigger less often.
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
  then uses an AI-provider adapter, then falls back naturally when no AI is
  configured.
- Voice input has a safe optional recognizer; when unavailable, it asks for
  typed input instead of crashing.
- Rest, movement, and late-night reminders are implemented.
- Weather fetch failure returns `None` and does not crash the app.
- Weather summaries now keep resolved location and source, using configured
  city first and IP lookup when no city is configured.
- Latest implemented modules include local search, AI-provider fallback,
  assistant question mode, voice fallback, and loop benchmark.

## Manual Items To Confirm

- Desktop pet looks clear enough at the current `360px` sprite height.
- Left click drag moves the pet.
- Left click body regions trigger different dialog.
- Right click triggers the scare/split state.
- Double left click switches form.
- Middle click or Ctrl+left click opens the question panel.
- Long idle behavior is acceptable.
