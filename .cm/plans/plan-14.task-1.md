# P14 — registry_clear (free each desc + zero array)

**Task ID:** `phase-14.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 2 — Init / teardown (clear)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 02**

## Files touched

**Modified:**
- `main/core/registry.h`
- `main/core/registry.c`

## Scope (single commit)

- Declare `void registry_clear(void)`.
- Implement: for each `i < registry_len`, call `wally_descriptor_free(registry_entries[i].desc)` if non-NULL. Then `memset(registry_entries, 0, sizeof registry_entries)` and `registry_len = 0`.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: registry_clear (free each desc + zero array)` (or a tighter phrasing of it).
