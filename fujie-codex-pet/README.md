# 富江 Codex Pet Transfer Pack

This folder is the portable handoff package for moving the current pet design to
another machine, including a Mac.

## Contents

- `codex-pet-fujie/`: ready-to-copy Codex pet package.
- `assets/high-res-rows/`: high-resolution row strips used by the desktop shell.
- `assets/contact-sheet.png`: full Codex atlas contact sheet.
- `assets/resolution-preview.png`: old low-resolution display versus new
  high-resolution display comparison.
- `design/FUJIE_DESIGN_SPEC.md`: visual, interaction, dialogue, and behavior
  design notes.
- `MAC_SYNC.md`: Mac-side copy instructions.
- `GITHUB_SYNC.md`: GitHub target layout, current upload status, and sync notes.
- `LOOP_ENGINEERING.md`: local loop-engineering baseline and workflow.
- `MANIFEST.sha256`: hashes for the key portable files.

## Current Interaction Model

- Dialogue is generated from persona, emotion, trigger source, affection, and
  intensity instead of using fixed full-sentence templates.
- Girl persona addressing is hard-limited to `夜雨哥哥`, `哥哥`, and `凌凌哥哥`.
- Comic speech bubbles change color, accent marks, and outline weight by mood.
- The desktop shell prefers high-resolution row strips so the pet does not look
  blurry when displayed larger than Codex atlas size.
- The large desktop shell is the canonical display. The currently selected
  built-in Codex avatar was made transparent to avoid showing a second small pet
  when the summon button is used.
- Double click switches between girl and mature forms.
- Middle click or Ctrl+left click opens interactive question mode.
- Question mode searches local project/transfer documents first, then uses an
  AI-provider adapter when configured, otherwise degrades naturally.
- Voice input is optional and safe: when unavailable, the pet asks for typed
  input instead of crashing.
- Loop engineering baseline currently checks 15 requirement gates and is run
  alongside the 38-test suite.

## Codex Pet Metadata

The portable Codex pet is named and described as:

- id: `fujie`
- displayName: `富江`
- description: `富江`
