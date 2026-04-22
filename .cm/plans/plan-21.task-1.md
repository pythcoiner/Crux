# P21 — Add settings_get/set_permissive_signing + KEY_PERMISSIVE_SIGNING (additive)

**Task ID:** `phase-21.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 3 — settings**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 04**

## Files touched

**Modified:**
- `main/core/settings.h`
- `main/core/settings.c`

## Scope (single commit)

- Add NVS key `#define KEY_PERMISSIVE_SIGNING "perm_sign"` in settings.c alongside other KEY_* constants.
- Declare `bool settings_get_permissive_signing(void)` in settings.h. Implement in settings.c: open NVS, read `KEY_PERMISSIVE_SIGNING` as u8, default to 0 (false) if absent.
- Declare `esp_err_t settings_set_permissive_signing(bool permissive)`. Implement: open NVS R/W, write u8, commit, close.
- Do NOT touch `KEY_DEFAULT_POL` or `settings_get/set_default_policy` — that removal happens in P53-P55.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Add settings_get/set_permissive_signing + KEY_PERMISSIVE_SIGNING (additive)` (or a tighter phrasing of it).
