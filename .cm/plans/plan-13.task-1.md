# P13 — registry accessors: count / get / find_by_id

**Task ID:** `phase-13.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 2 — Accessors**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 02**

## Files touched

**Modified:**
- `main/core/registry.h`
- `main/core/registry.c`

## Scope (single commit)

- Declare `size_t registry_count(void)`. Returns `registry_len`.
- Declare `registry_entry_t *registry_get(size_t i)`. Bounds-checked; returns NULL if `i >= registry_len`.
- Declare `registry_entry_t *registry_find_by_id(const char *id)`. Linear scan over `registry_entries` with `strncmp` up to `REGISTRY_ID_MAX_LEN`.

## Notes

No test needed — these are trivial accessors exercised by P18/P20 tests.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: registry accessors: count / get / find_by_id` (or a tighter phrasing of it).
