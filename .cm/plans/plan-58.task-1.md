# P58 — wallet.c: wallet_cleanup calls registry_clear()

**Task ID:** `phase-58.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — wallet_cleanup**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.c`
- `main/core/registry.h`

## Scope (single commit)

- In `wallet_cleanup`, add a call to `registry_clear()`.
- Include `"registry.h"` in wallet.c.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.c: wallet_cleanup calls registry_clear()` (or a tighter phrasing of it).
