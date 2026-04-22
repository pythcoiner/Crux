# P77 — Device: Address checker known + random per source

**Task ID:** `phase-77.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 15 — device verification (address checker)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

## Scope (single commit)

- Paste a Sparrow-generated address at `m/84'/0'/2'/0/5` with account 2 selected → result shows 'Receive #5'.
- Paste a random mainnet address → result shows 'Not found'.
- Paste a registered-multisig address → result found on the multisig source.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Device: Address checker known + random per source` (or a tighter phrasing of it).
