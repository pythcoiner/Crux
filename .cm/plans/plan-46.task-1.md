# P46 — descriptor_validator: delete parse_origin_path helper (lines 80-143)

**Task ID:** `phase-46.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 7 — delete parse_origin_path**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/descriptor_validator.c`

## Scope (single commit)

- Delete the `parse_origin_path` helper (lines 80-143). It's no longer called after the `check_attributes_and_verify` deletion.
- Confirm no remaining references via `rg parse_origin_path main/`.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: descriptor_validator: delete parse_origin_path helper (lines 80-143)` (or a tighter phrasing of it).
