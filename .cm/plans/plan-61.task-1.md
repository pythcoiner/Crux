# P61 — wallet.h: delete format_derivation_path / format_derivation_compact / get_derivation

**Task ID:** `phase-61.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — delete derivation-path formatters**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.h`
- `main/core/wallet.c`

## Scope (single commit)

- Delete declarations and bodies of `wallet_format_derivation_path`, `wallet_format_derivation_compact`, `wallet_get_derivation`.
- Grep to confirm no callers.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.h: delete format_derivation_path / format_derivation_compact / get_derivation` (or a tighter phrasing of it).
