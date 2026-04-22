# P24 — try_match_whitelist + try_match_registry wrappers (cursor pagination)

**Task ID:** `phase-24.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 5 — Helpers (try_match_*)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 06, SNIP 07**

## Files touched

**Modified:**
- `main/core/psbt.c`

## Scope (single commit)

- Implement `bool try_match_whitelist(const uint8_t *keypath, size_t keypath_len, bool is_testnet, claim_t *claim_out)`. Thin wrapper: `ss_keypath_parse` + `ss_keypath_is_whitelisted`; on success, fill `claim_out->kind = CLAIM_WHITELIST` and the whitelist union fields.
- Implement `bool try_match_registry(const uint8_t *keypath, size_t keypath_len, size_t *cursor, claim_t *claim_out)`. Thin wrapper over `registry_match_keypath` that passes through the cursor for pagination. On match, fill `claim_out->kind = CLAIM_REGISTRY` with the entry and the multi_index/child_num parsed from the keypath tail.
- Both write the derived full path into `claim_out->derived_path[]` with length.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: try_match_whitelist + try_match_registry wrappers (cursor pagination)` (or a tighter phrasing of it).
