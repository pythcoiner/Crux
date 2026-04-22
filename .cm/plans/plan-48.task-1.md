# P48 — wallet_settings.c: remove account spinner + save handler

**Task ID:** `phase-48.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 9 — remove account spinner**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/settings/wallet_settings.c`

## Scope (single commit)

- Delete the account spinner UI element (declared ~line 47) and its save handler.
- Remove any `wallet_set_account` calls.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet_settings.c: remove account spinner + save handler` (or a tighter phrasing of it).
