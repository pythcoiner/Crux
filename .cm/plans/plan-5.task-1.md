# P05 — ss_keypath_is_whitelisted + test_ss_whitelist_is_whitelisted.c

**Task ID:** `phase-5.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Parsing / whitelist check (ss_keypath_is_whitelisted)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 01**

## Files touched

**New:**
- `main/core/test/test_ss_whitelist_is_whitelisted.c`

**Modified:**
- `main/core/ss_whitelist.h`
- `main/core/ss_whitelist.c`
- `main/core/test/CMakeLists.txt`

## Scope (single commit)

- Declare `bool ss_keypath_is_whitelisted(const ss_keypath_t *kp, bool is_testnet)` in the header.
- Implement: purpose ∈ {44,49,84,86} (already enforced by parse, double-check), coin matches `is_testnet` (0 for mainnet, 1 for testnet), `account < SS_MAX_ACCOUNT`, `index < SS_MAX_ADDR_INDEX`, `chain ∈ {0,1}`.
- Add `test_ss_whitelist_is_whitelisted.c`: account 0/99 accepted, account 100 rejected; index 0/99 accepted, index 100 rejected; coin=0 accepted on mainnet / rejected on testnet; coin=1 accepted on testnet / rejected on mainnet.
- Register new test in `main/core/test/CMakeLists.txt`.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: ss_keypath_is_whitelisted + test_ss_whitelist_is_whitelisted.c` (or a tighter phrasing of it).
