# P12 — registry: types, REGISTRY_MAX_ENTRIES, static storage

**Task ID:** `phase-12.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 2 — Types**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 02**

## Files touched

**Modified:**
- `main/core/registry.h`
- `main/core/registry.c`

## Scope (single commit)

- Define `registry_entry_t` in the header matching SNIP 02: `char id[REGISTRY_ID_MAX_LEN]`, `storage_location_t loc`, `struct wally_descriptor *desc`, `size_t my_key_index`, `size_t num_paths`, `uint32_t origin_path[MAX_KEYPATH_ORIGIN_DEPTH]`, `size_t origin_path_len`.
- Define `#define REGISTRY_MAX_ENTRIES 16` and `#define REGISTRY_ID_MAX_LEN 32` in the header.
- In `registry.c`, declare a static `registry_entry_t registry_entries[REGISTRY_MAX_ENTRIES]` array and a `static size_t registry_len = 0`.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: registry: types, REGISTRY_MAX_ENTRIES, static storage` (or a tighter phrasing of it).
