# P39 — store_descriptor.c: auto-register after plaintext save

**Task ID:** `phase-39.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 12 — store_descriptor auto-register**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/store_descriptor.c`

## Scope (single commit)

- After the successful `do_save_plaintext` path returns, call `registry_add_from_string(id, descriptor_text, target_location, /*persist=*/false)`.
- Persist is false because `storage_save_descriptor` was already called by the save flow.
- If `registry_add_from_string` returns false, log a warning (`ESP_LOGW`) and continue — the file is on disk and will be re-tried by `registry_init` at next boot.
- Include `"core/registry.h"`.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: store_descriptor.c: auto-register after plaintext save` (or a tighter phrasing of it).
