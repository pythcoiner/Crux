# P37 — address_checker.c: source picker

**Task ID:** `phase-37.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 11 — address_checker source picker**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/shared/address_checker.c`

## Scope (single commit)

- Add a source-picker dropdown at the top of the page, identical to the one in `addresses.c` (4 SS types + one entry per registered descriptor).
- For SS sources, also show an account input (0..99).
- Store the selected source in page-scoped state.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: address_checker.c: source picker` (or a tighter phrasing of it).
