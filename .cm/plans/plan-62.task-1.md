# P62 — wallet.h: delete get_account / set_account

**Task ID:** `phase-62.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — delete account API**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.h`
- `main/core/wallet.c`

## Scope (single commit)

- Delete declarations and bodies of `wallet_get_account` and `wallet_set_account`.
- Grep to confirm no callers.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.h: delete get_account / set_account` (or a tighter phrasing of it).
