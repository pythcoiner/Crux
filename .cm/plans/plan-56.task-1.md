# P56 — wallet.c: delete derive_address, derive_multisig_address helpers

**Task ID:** `phase-56.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — delete derive_* helpers**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.c`

## Scope (single commit)

- Grep to confirm no callers of `derive_address` or `derive_multisig_address` remain (should be true after P35).
- Delete both helpers.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.c: delete derive_address, derive_multisig_address helpers` (or a tighter phrasing of it).
