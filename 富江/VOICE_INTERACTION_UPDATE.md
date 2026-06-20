# Voice Interaction Update

Date: 2026-06-20

## What Changed

The pet now has a voice interaction path in the desktop shell.

- Click `语音` in the question panel to start listening.
- Press `V` while the pet window has focus to start the same flow.
- The pet says `我在听，哥哥你说。` before listening.
- Speech recognition runs in a background thread so the pet animation does not freeze.
- Recognized Chinese text is sent to the existing interactive question mode.
- The pet-styled answer is shown in the manga bubble and sent to Windows speech synthesis when voice reply is enabled.
- If microphone recognition or speech output fails, the pet falls back to typed input and the speech bubble.

## Files Added Or Updated Locally

- `src/yoruame_pet/voice.py`
- `src/yoruame_pet/app.py`
- `src/yoruame_pet/config.py`
- `src/yoruame_pet/loop_benchmark.py`
- `config/settings.json`
- `tests/test_voice_interaction.py`
- `tests/test_atlas_and_app.py`
- `tests/test_loop_benchmark.py`
- `qa/runtime-check.md`
- `qa/loop-engineering-baseline.md`

## Verification

- `python -m unittest discover -s tests -v`: 41 tests passing.
- `python -m yoruame_pet.loop_benchmark`: 16/16 checks passing.
- `git diff --check`: no whitespace errors; Git only reported line-ending warnings.
- A short Windows TTS self-test returned `VoiceSpeakResult(available=True, message='我说给你听了。')`.

## Local Runtime

The desktop pet was restarted locally after the update. The latest observed process was `pythonw.exe -m yoruame_pet`.