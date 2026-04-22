# P16 — registry_add_from_string persist path via storage_save_descriptor

**Task ID:** `phase-16.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 2 — Add / remove (registry_add_from_string, persist path)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 02**

## Files touched

**Modified:**
- `main/core/registry.c`

## Scope (single commit)

- After the in-memory append succeeds, if `persist == true`: call `storage_save_descriptor(loc, id, (const uint8_t *)descriptor_str, strlen(descriptor_str), /*encrypted=*/false)`.
- On save failure: rollback the in-memory add (free the desc, decrement registry_len) and return false.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: registry_add_from_string persist path via storage_save_descriptor` (or a tighter phrasing of it).
