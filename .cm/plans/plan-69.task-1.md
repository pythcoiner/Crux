# P69 — Remove dead tests covering deleted policy paths under main/core/test/

**Task ID:** `phase-69.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Cleanup — dead tests**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/test/`

## Scope (single commit)

- List tests under `main/core/test/` that exercise the removed `wallet_*` policy/account/descriptor API.
- Delete each; update the test CMakeLists.
- Verify `just test` still passes.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Remove dead tests covering deleted policy paths under main/core/test/` (or a tighter phrasing of it).
