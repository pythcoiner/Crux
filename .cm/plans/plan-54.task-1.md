# P54 — Remove settings_get_default_policy / settings_set_default_policy

**Task ID:** `phase-54.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 3 — remove policy API**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/settings.c`
- `main/core/settings.h`

## Scope (single commit)

- Delete `settings_get_default_policy` / `settings_set_default_policy` bodies (`settings.c:48-65`).
- Delete their declarations (`settings.h:18-19`).
- Grep to confirm no remaining callers after P53 (`rg settings_get_default_policy\|settings_set_default_policy main/`).

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Remove settings_get_default_policy / settings_set_default_policy` (or a tighter phrasing of it).
