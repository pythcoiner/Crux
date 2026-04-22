# P49 — wallet_settings.c: remove derivation-path preview label

**Task ID:** `phase-49.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 9 — remove derivation-preview label**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/settings/wallet_settings.c`

## Scope (single commit)

- Delete the derivation-path preview label that updated on policy/account change.
- Delete the helper that formatted the preview (if local to this file).

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet_settings.c: remove derivation-path preview label` (or a tighter phrasing of it).
