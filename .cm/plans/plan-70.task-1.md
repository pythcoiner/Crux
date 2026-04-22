# P70 — Update repo-root ROADMAP.md to reflect new model

**Task ID:** `phase-70.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Cleanup — repo-root ROADMAP.md**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `ROADMAP.md`

## Scope (single commit)

- Read `/home/pyth/Kern/ROADMAP.md` and replace any 'policy'/'singlesig vs multisig' wording with the new registry + whitelist model described in `.cm/spec/PLAN.md`.
- Keep this file terse — it's a high-level product roadmap, not a task list.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Update repo-root ROADMAP.md to reflect new model` (or a tighter phrasing of it).
