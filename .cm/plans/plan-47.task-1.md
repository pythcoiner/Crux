# P47 — wallet_settings.c: remove policy_dropdown UI element + handlers

**Task ID:** `phase-47.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 9 — remove policy_dropdown**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/settings/wallet_settings.c`

## Scope (single commit)

- Delete the `policy_dropdown` UI element declaration (line 26) and its event handlers (lines 246-256).
- Remove any `wallet_set_policy` or `settings_set_default_policy` call inside those handlers (they become orphaned; removed with the handlers themselves).

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet_settings.c: remove policy_dropdown UI element + handlers` (or a tighter phrasing of it).
