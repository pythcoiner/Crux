# P03 — ss_keypath_parse + test_ss_whitelist_parse.c

**Task ID:** `phase-3.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Parsing / whitelist check (ss_keypath_parse)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 01**

## Files touched

**New:**
- `main/core/test/test_ss_whitelist_parse.c`

**Modified:**
- `main/core/ss_whitelist.h`
- `main/core/ss_whitelist.c`
- `main/core/test/CMakeLists.txt`

## Scope (single commit)

- Declare `bool ss_keypath_parse(const uint8_t *keypath_after_fp, size_t keypath_len, ss_keypath_t *out)` in the header.
- Implement: require length == 20 bytes (5 components × 4), read 5 little-endian u32s via `ss_u32_le`, verify first 3 are hardened and last 2 are not, unharden the first 3, map `purpose → script` via the fixed table (44→P2PKH, 49→P2SH_P2WPKH, 84→P2WPKH, 86→P2TR). Reject any other purpose with `false`.
- Fill `out->{script,purpose,coin,account,chain,index}` from the parsed values.
- Add `test_ss_whitelist_parse.c`: round-trip all four whitelisted purposes at account 0 index 0; reject length ≠ 20; reject unhardened purpose/coin/account; reject hardened chain/index; reject unknown purpose (e.g. 45).
- Register the new test in `main/core/test/CMakeLists.txt` SRCS list.

## Notes

Test cross-checks against a hand-constructed byte sequence, not derived from libwally — the whole point is we validate the raw bytes.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: ss_keypath_parse + test_ss_whitelist_parse.c` (or a tighter phrasing of it).
