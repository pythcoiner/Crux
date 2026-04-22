# P74 — Device: Addresses page per-source vs Sparrow references

**Task ID:** `phase-74.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 15 — device verification (Addresses)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

## Scope (single commit)

- Open Addresses page. Switch through each source:
- Native SegWit account 0 → addresses match Sparrow at `m/84'/0'/0'/0/0..7`.
- Taproot account 0 → addresses match Sparrow at `m/86'/0'/0'/0/0..7`.
- wsh multisig source → addresses match the expected 2-of-2 derivation.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Device: Addresses page per-source vs Sparrow references` (or a tighter phrasing of it).
