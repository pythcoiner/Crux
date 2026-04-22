# P64 — wallet.h: delete has_descriptor / load_descriptor / clear_descriptor

**Task ID:** `phase-64.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — delete descriptor API**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.h`
- `main/core/wallet.c`

## Scope (single commit)

- Delete `wallet_has_descriptor`, `wallet_load_descriptor`, `wallet_clear_descriptor`.
- Grep to confirm no callers.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.h: delete has_descriptor / load_descriptor / clear_descriptor` (or a tighter phrasing of it).
