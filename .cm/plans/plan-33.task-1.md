# P33 — Delete/replace psbt_is_multisig (callers switch to claim.kind==CLAIM_REGISTRY)

**Task ID:** `phase-33.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 6 — delete/replace psbt_is_multisig**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/psbt.c`
- `main/core/psbt.h`

## Scope (single commit)

- Grep for callers of `psbt_is_multisig`.
- For each, replace with the equivalent question answered by `psbt_classify_input(...).claim.kind == CLAIM_REGISTRY` (or the corresponding output classifier).
- Delete `psbt_is_multisig` body (psbt.c:489-521) and declaration.
- Alternative: if callers prefer a convenience helper, keep a thin `bool psbt_input_matches_registry(...)` wrapper instead.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Delete/replace psbt_is_multisig (callers switch to claim.kind==CLAIM_REGISTRY)` (or a tighter phrasing of it).
