# P15 — registry_add_from_string in-memory path (persist=false)

**Task ID:** `phase-15.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 2 — Add / remove (registry_add_from_string, in-memory path)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 02**

## Files touched

**Modified:**
- `main/core/registry.h`
- `main/core/registry.c`

## Scope (single commit)

- Declare `bool registry_add_from_string(const char *id, const char *descriptor_str, storage_location_t loc, bool persist)`.
- Implement persist=false path only. Persist=true path is a no-op `goto done` for now — populated in P16.
- Steps: check `registry_len < REGISTRY_MAX_ENTRIES`; call `wally_descriptor_parse` with the correct network flag (mainnet first, fall back to testnet if first fails); find our-fingerprint key index via the `wally_descriptor_get_key_origin_fingerprint` loop (pattern from `descriptor_validator.c:55-78`); if no key matches our fingerprint, `wally_descriptor_free` and return false.
- Extract our key's origin path via `wally_descriptor_get_key_origin_path_str` then convert to `uint32_t[]` using the `parse_derivation_path` helper in `key.c:110-190`.
- Read `num_paths` via `wally_descriptor_get_num_paths`.
- Fill a new `registry_entry_t` in `registry_entries[registry_len]` with `id` (strncpy into `id[]`), `loc`, `desc`, `my_key_index`, `num_paths`, `origin_path[]`, `origin_path_len`. Increment `registry_len`.
- Return true.

## Notes

Reuse the fingerprint-matching loop from descriptor_validator.c:55-78 — factor it into a static helper if cleaner.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: registry_add_from_string in-memory path (persist=false)` (or a tighter phrasing of it).
