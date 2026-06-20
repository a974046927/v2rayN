# Codex Avatar Size Check

## 2026-06-20

The visible duplicate pet was caused by two different renderers:

- large desktop shell: `pythonw.exe -m yoruame_pet`
- small Codex built-in avatar selected by
  `selected-avatar-id = "custom:yoruame-kagehime"`

The desktop shell is the preferred canonical display because it renders the
high-resolution row strips at a `360px` sprite height.

The Codex built-in avatar renderer appears to use a fixed display size. The
active Codex atlas already filled the standard `192x208` cell height
(`198/208px` measured), so the small size was not caused by excessive
transparent padding.

The transparent-atlas workaround was tried and rejected because it still leaves
the small Codex avatar renderer active. That workaround has been rolled back:
the active `yoruame-kagehime` spritesheet is restored and remains non-empty.

Sprite backup kept for recovery:

```text
C:\Users\lenovo\.codex\pets\yoruame-kagehime-backup-20260620-222518
```

Config backup kept for recovery:

```text
C:\Users\lenovo\.codex\config-backup-20260620-223444.toml
```

Final local setting:

- `C:\Users\lenovo\.codex\config.toml` no longer actively selects the custom
  Codex avatar.
- The old selected-avatar line is commented out, not deleted.
- The active small-avatar package remains normal rather than transparent.

Current active small-avatar spritesheet:

```text
C:\Users\lenovo\.codex\pets\yoruame-kagehime\spritesheet.webp
```

Verification:

```text
size (1536, 1872)
bbox (33, 5, 1487, 1867)
```

The large desktop pet remained running after the change:

```text
pythonw.exe -m yoruame_pet
PID 14672
```
