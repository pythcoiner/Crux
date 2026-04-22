# P45 — descriptor_validator: delete check_attributes_and_verify + state fields

**Task ID:** `phase-45.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 7 — delete check_attributes_and_verify + state**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/descriptor_validator.c`
- `main/core/descriptor_validator.h`

## Scope (single commit)

- Delete `check_attributes_and_verify` (lines 400-492 — everything after the fingerprint check).
- Delete fields from `validation_context_t` (lines 21-26): `target_network`, `target_policy`, `target_account`, `needs_*_change` (and any related state used only by the deleted function).
- Update `descriptor_validate_and_load`: after the fingerprint stage, jump straight to `verify_xpub_and_show_info` (skip attribute check).
- Keep `find_matching_key_index`, `extract_xpub_from_key`, `parse_multisig_threshold`, `extract_descriptor_info`, `verify_xpub_and_show_info`, `info_confirm_proceed`.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: descriptor_validator: delete check_attributes_and_verify + state fields` (or a tighter phrasing of it).
