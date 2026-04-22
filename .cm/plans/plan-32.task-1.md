# P32 — Delete psbt_verify_output_with_descriptor; migrate callers

**Task ID:** `phase-32.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 6 — delete psbt_verify_output_with_descriptor**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/psbt.c`
- `main/core/psbt.h`

## Scope (single commit)

- Grep for callers of `psbt_verify_output_with_descriptor`.
- Replace each with `psbt_classify_output` (which now folds in the descriptor-based verification via its registry branch).
- Delete the function body (psbt.c:523-635) and declaration.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Delete psbt_verify_output_with_descriptor; migrate callers` (or a tighter phrasing of it).
