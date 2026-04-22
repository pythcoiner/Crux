# P31 — Delete psbt_get_output_derivation; migrate callers to psbt_classify_output

**Task ID:** `phase-31.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 6 — delete psbt_get_output_derivation**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/psbt.c`
- `main/core/psbt.h`

## Scope (single commit)

- Grep for callers of `psbt_get_output_derivation` (likely in the review UI).
- For each caller, replace with a call to `psbt_classify_output` and read `source.derived_path` from the returned claim.
- Delete the function body (psbt.c:202-256) and its declaration from psbt.h.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Delete psbt_get_output_derivation; migrate callers to psbt_classify_output` (or a tighter phrasing of it).
