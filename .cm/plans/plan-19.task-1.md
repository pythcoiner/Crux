# P19 — registry_init: scan flash + SD, parse all, populate, log count

**Task ID:** `phase-19.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 2 — Init / teardown (registry_init)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 02**

## Files touched

**Modified:**
- `main/core/registry.h`
- `main/core/registry.c`

## Scope (single commit)

- Declare `void registry_init(bool is_testnet)`.
- Call `registry_clear()` first (idempotent).
- Enumerate `.txt` descriptors on `STORAGE_FLASH` via `storage_list_descriptors` with `.txt` filter. For each filename, call `storage_load_descriptor` to get `descriptor_str`, then `registry_add_from_string(id, descriptor_str, STORAGE_FLASH, /*persist=*/false)`.
- Repeat for `STORAGE_SD`.
- Log count at INFO level: `ESP_LOGI(TAG, "Registry: %zu entries loaded", registry_len)`. Use the existing file's TAG pattern; add `static const char *TAG = "registry";` at the top of registry.c if not already present.

## Notes

Do not fail the boot if SD is not mounted; just skip the SD enumeration.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: registry_init: scan flash + SD, parse all, populate, log count` (or a tighter phrasing of it).
