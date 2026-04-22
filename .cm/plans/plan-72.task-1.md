# P72 — Device: clean builds on wave_4b, wave_35, wave_5

**Task ID:** `phase-72.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 15 — device verification (builds)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

## Scope (single commit)

- Run `just build wave_4b`, `just build wave_35`, `just build wave_5`. Each must succeed.
- No code changes in this phase — this is a gate, not a commit. Mark phase complete in cm only if all three builds pass.

## Notes

If any board fails, the failure is investigated and fixed under the appropriate earlier phase, not in P72.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Device: clean builds on wave_4b, wave_35, wave_5` (or a tighter phrasing of it).
