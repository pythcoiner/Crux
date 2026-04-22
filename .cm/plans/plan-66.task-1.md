# P66 — wallet.h: delete get_policy / set_policy

**Task ID:** `phase-66.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — delete policy get/set**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.h`
- `main/core/wallet.c`

## Scope (single commit)

- Delete `wallet_get_policy`, `wallet_set_policy`.
- Grep to confirm no callers.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.h: delete get_policy / set_policy` (or a tighter phrasing of it).
