# P51 — wallet_settings.c: update update_apply_button_state

**Task ID:** `phase-51.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 9 — update_apply_button_state**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/settings/wallet_settings.c`

## Scope (single commit)

- Adjust `update_apply_button_state` so it only tracks network / brightness / permissive changes (policy and account are gone).
- Remove references to the removed state.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet_settings.c: update update_apply_button_state` (or a tighter phrasing of it).
