# P02 — ss_whitelist: types, constants, inline helpers

**Task ID:** `phase-2.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Types & constants**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 01**

## Files touched

**Modified:**
- `main/core/ss_whitelist.h`

## Scope (single commit)

- Define `ss_script_type_t` enum with `SS_SCRIPT_P2PKH`, `SS_SCRIPT_P2SH_P2WPKH`, `SS_SCRIPT_P2WPKH`, `SS_SCRIPT_P2TR`.
- Define `ss_keypath_t` struct with fields `script` (ss_script_type_t), `purpose`, `coin`, `account`, `chain`, `index` (all `uint32_t`, unhardened values).
- Define constants: `SS_MAX_ACCOUNT = 100`, `SS_MAX_ADDR_INDEX = 100`, `MAX_KEYPATH_ORIGIN_DEPTH = 6`, `MAX_KEYPATH_TAIL_DEPTH = 2`, `MAX_KEYPATH_TOTAL_DEPTH = 8`.
- Add inline helpers: `static inline bool ss_is_hardened(uint32_t)`, `static inline uint32_t ss_unharden(uint32_t)`, `static inline uint32_t ss_u32_le(const unsigned char *)`.

## Notes

Header-only change. Matches SNIP 01 signatures exactly.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: ss_whitelist: types, constants, inline helpers` (or a tighter phrasing of it).
