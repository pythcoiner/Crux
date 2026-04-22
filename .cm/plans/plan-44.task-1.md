# P44 — descriptor_validator: delete apply_changes_and_verify (lines 350-386)

**Task ID:** `phase-44.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 7 — delete apply_changes_and_verify**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/descriptor_validator.c`
- `main/core/descriptor_validator.h`

## Scope (single commit)

- Delete `apply_changes_and_verify` function (lines 350-386).
- Delete its declaration from the header if present.
- Grep for callers — there should be none after P42.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: descriptor_validator: delete apply_changes_and_verify (lines 350-386)` (or a tighter phrasing of it).
