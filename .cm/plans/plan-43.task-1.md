# P43 — descriptor_validator: add WARN dialog via purpose_script_binding_check_soft

**Task ID:** `phase-43.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 7 — WARN dialog on purpose mismatch**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/descriptor_validator.c`

## Scope (single commit)

- Between the xpub verification stage and `info_confirm_proceed`, call `purpose_script_binding_check_soft(desc)`.
- If result == `PSB_WARN`: show a danger-confirm dialog with text like 'This descriptor uses a purpose-86 origin under a wsh script. This is unusual. Register anyway?' (phrasing should reflect the actual outer/purpose combination). Only proceed to info-confirm if the user confirms.
- If `PSB_OK` or `PSB_NA`: skip the dialog and continue.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: descriptor_validator: add WARN dialog via purpose_script_binding_check_soft` (or a tighter phrasing of it).
