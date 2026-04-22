# P17 — registry_remove (free + shift + storage_delete_descriptor)

**Task ID:** `phase-17.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 2 — Add / remove (registry_remove)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 02**

## Files touched

**Modified:**
- `main/core/registry.h`
- `main/core/registry.c`

## Scope (single commit)

- Declare `bool registry_remove(const char *id)`.
- Implement: `registry_find_by_id(id)` to locate entry index; if not found, return false; `wally_descriptor_free` its `desc`; shift-remove (memmove) subsequent entries down; decrement `registry_len`; call `storage_delete_descriptor(entry.loc, id)` to remove the `.txt` file from storage.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: registry_remove (free + shift + storage_delete_descriptor)` (or a tighter phrasing of it).
