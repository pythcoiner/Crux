# P63 — wallet.h: delete get_receive_address / get_change_address / get_scriptpubkey

**Task ID:** `phase-63.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — delete address/scriptpubkey APIs**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.h`
- `main/core/wallet.c`

## Scope (single commit)

- Delete declarations and bodies of `wallet_get_receive_address`, `wallet_get_change_address`, `wallet_get_scriptpubkey`.
- Grep to confirm no callers.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.h: delete get_receive_address / get_change_address / get_scriptpubkey` (or a tighter phrasing of it).
