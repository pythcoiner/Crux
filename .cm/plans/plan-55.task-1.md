# P55 — Remove KEY_DEFAULT_POL constant

**Task ID:** `phase-55.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 3 — remove NVS key**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/settings.c`

## Scope (single commit)

- Delete `KEY_DEFAULT_POL` constant (`settings.c:11`).
- The NVS entry itself stays on disk for devices that have already written it — that's fine, it becomes dead data. No migration needed.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Remove KEY_DEFAULT_POL constant` (or a tighter phrasing of it).
