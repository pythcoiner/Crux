# P41 — load_descriptor_storage.c: register after plaintext load (paranoia)

**Task ID:** `phase-41.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 12 — load_descriptor_storage (plaintext path)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/load_descriptor_storage.c`

## Scope (single commit)

- In the plaintext branch of `load_selected`, after successful load, also call `registry_add_from_string(id, str, loc, /*persist=*/false)`.
- This is paranoia — plaintext descriptors are normally already in the registry via `registry_init`. Handle the 'already present' case by treating it as a no-op (or guard via `registry_find_by_id` before the add).

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: load_descriptor_storage.c: register after plaintext load (paranoia)` (or a tighter phrasing of it).
