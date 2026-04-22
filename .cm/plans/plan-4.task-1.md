# P04 — ss_keypath_format + round-trip test

**Task ID:** `phase-4.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Parsing / whitelist check (ss_keypath_format)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 01**

## Files touched

**Modified:**
- `main/core/ss_whitelist.h`
- `main/core/ss_whitelist.c`
- `main/core/test/test_ss_whitelist_parse.c`

## Scope (single commit)

- Declare `bool ss_keypath_format(const ss_keypath_t *kp, char *buf, size_t buf_size)` in the header.
- Implement: produce `m/<purpose>'/<coin>'/<account>'/<chain>/<index>`. Use `'` not `h` to match the parser in `main/core/key.c:110-190`.
- Return false on buffer overflow; true with null-terminated string otherwise.
- Extend `test_ss_whitelist_parse.c` with a round-trip test: format → parse (requires a raw-bytes round trip via a helper in the test, OR simply assert the expected string for each of the four whitelisted paths at account 0/index 0).

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: ss_keypath_format + round-trip test` (or a tighter phrasing of it).
