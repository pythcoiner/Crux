# P60 — wallet.h: delete wallet_policy_t enum

**Task ID:** `phase-60.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — delete wallet_policy_t**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.h`

## Scope (single commit)

- Delete `wallet_policy_t` enum and typedef (lines 17-20).
- Grep to confirm no remaining references (`rg wallet_policy_t`).

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.h: delete wallet_policy_t enum` (or a tighter phrasing of it).
