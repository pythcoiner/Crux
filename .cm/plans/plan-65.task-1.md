# P65 — wallet.h: delete get_multisig_receive_address / get_multisig_change_address

**Task ID:** `phase-65.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — delete multisig address APIs**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.h`
- `main/core/wallet.c`

## Scope (single commit)

- Delete `wallet_get_multisig_receive_address`, `wallet_get_multisig_change_address`.
- Grep to confirm no callers.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.h: delete get_multisig_receive_address / get_multisig_change_address` (or a tighter phrasing of it).
