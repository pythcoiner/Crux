# P34 — addresses.c: source-picker scaffold replacing type_dropdown

**Task ID:** `phase-34.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 10 — UI addresses page**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/home/addresses.c`

## Scope (single commit)

- Replace `type_dropdown` (declared line 27) with a `source_dropdown` LVGL element whose options are populated at page-enter time as:
- `Native SegWit` (→ SS_SCRIPT_P2WPKH)
- `Taproot` (→ SS_SCRIPT_P2TR)
- `Legacy` (→ SS_SCRIPT_P2PKH)
- `Wrapped SegWit` (→ SS_SCRIPT_P2SH_P2WPKH)
- One entry per `registry_get(i)->id` for `i < registry_count()`
- Include `"core/ss_whitelist.h"` and `"core/registry.h"`.
- Keep the existing receive/change pagination controls; they remain functional in this commit even though they still call the old `wallet_get_*_address` APIs (those get migrated in P35).

## Notes

Scaffold only — no behavior change yet beyond the dropdown shape. Build must stay green.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: addresses.c: source-picker scaffold replacing type_dropdown` (or a tighter phrasing of it).
