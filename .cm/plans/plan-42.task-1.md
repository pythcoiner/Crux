# P42 — descriptor_validator: redirect info_confirm_proceed to registry_add_from_string

**Task ID:** `phase-42.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 7 — info_confirm_proceed redirect**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/descriptor_validator.c`
- `main/core/descriptor_validator.h`

## Scope (single commit)

- In `info_confirm_proceed`, replace the `wallet_load_descriptor(...)` call with `registry_add_from_string(<id-from-UI>, descriptor_str, loc, /*persist=*/true)`.
- The ID prompt currently lives in `store_descriptor.c`. Move or share that UI flow so the validator can solicit an ID right after info-confirm. Options: (a) share a helper in `main/pages/shared/descriptor_id_prompt.c` (new file), or (b) temporarily inline a minimal prompt in the validator. Pick (a) if the code naturally factors; otherwise (b) and defer the refactor.
- Include `"core/registry.h"`.

## Notes

This is the highest-risk UI change in the series — be conservative. If a shared helper is out of scope, just inline the minimum prompt and leave a TODO-free comment describing the duplication.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: descriptor_validator: redirect info_confirm_proceed to registry_add_from_string` (or a tighter phrasing of it).
