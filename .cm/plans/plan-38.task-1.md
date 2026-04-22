# P38 — address_checker.c: sweep within selected source

**Task ID:** `phase-38.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 11 — sweep within source**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/shared/address_checker.c`

## Scope (single commit)

- Rewrite `address_checker_check` (lines 102-147) so that the 50-per-page sweep iterates within the selected source only:
- SS source: iterate `chain ∈ {0,1}` × `index ∈ [start, start+49]` at the user-selected account. Call `ss_address` for each.
- Registered descriptor source: iterate `multi_index ∈ {0,1}` × `child_num ∈ [start, start+49]`. Call `wally_descriptor_to_address` (or `registry_entry_address` helper).
- 'Page' button advances `start` by 50.
- Document the decision (in a comment): for SS sources we stick to the selected account and do NOT iterate accounts — the user knows which account they want to check.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: address_checker.c: sweep within selected source` (or a tighter phrasing of it).
