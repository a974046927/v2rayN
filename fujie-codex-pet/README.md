# 富江 Codex Pet Transfer Pack

This folder is the portable handoff package for the current Fujie desktop/Codex pet work.

## Current Status

- Local desktop shell: `E:\Codex 项目\杂谈\yoruame-desktop-pet`
- Local transfer ZIP: `E:\Codex 项目\杂谈\fujie-codex-pet-transfer.zip`
- Latest local commit: `2fe8579 Add voice interaction flow`
- Unit tests: `41` passing with `python -m unittest discover -s tests -v`
- Loop engineering baseline: `16/16` passing with `python -m yoruame_pet.loop_benchmark`

## Current Interaction Model

- Large desktop pet is the canonical display; the small Codex summon avatar is not kept running beside it.
- Dialogue is generated from persona, emotion, trigger source, affection, and intensity instead of fixed full-sentence templates.
- Girl persona addressing is hard-limited to `夜雨哥哥`, `哥哥`, and `凌凌哥哥`.
- Comic speech bubbles change color, accent marks, symbols, and outline weight by mood.
- Middle click or Ctrl+left click opens the interactive question panel.
- The question panel searches local pet documents first, then uses an AI-provider adapter when configured, otherwise falls back naturally.
- Voice interaction is enabled locally: click `语音` in the question panel or press `V` while the pet window has focus.
- The pet says `我在听，哥哥你说。`, listens in the background, answers the recognized question, and speaks the pet-styled reply through Windows speech synthesis when available.
- If recognition or speech output is unavailable, she falls back to the manga speech bubble instead of crashing.

## GitHub Folder Notes

This folder is being updated through the connected GitHub app because local git login was unavailable. New feature/fix notes should be kept under `fujie-codex-pet/`.