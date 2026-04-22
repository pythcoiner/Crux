# P50 — wallet_settings.c: add 'Permissive signing' toggle

**Task ID:** `phase-50.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 9 — add permissive toggle**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/settings/wallet_settings.c`

## Scope (single commit)

- Add an LVGL toggle labelled 'Permissive signing'.
- Initial value: `settings_get_permissive_signing()`.
- On change: `settings_set_permissive_signing(new_value)`.
- Caption/helper text: 'Allow signing for unknown derivation paths after on-screen confirmation. Reduces safety.'

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet_settings.c: add 'Permissive signing' toggle` (or a tighter phrasing of it).
