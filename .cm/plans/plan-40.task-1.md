# P40 — load_descriptor_storage.c: register after .kef decrypt

**Task ID:** `phase-40.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 12 — load_descriptor_storage (.kef path)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/load_descriptor_storage.c`

## Scope (single commit)

- In `success_from_kef_decrypt` (the post-decrypt success callback), call `registry_add_from_string(id, decrypted_str, loc, /*persist=*/false)`.
- Update the success dialog text to clarify this entry is session-only (not persistently registered until the user re-encrypts plaintext) — e.g., 'Registered (this session)'.
- Include `"core/registry.h"`.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: load_descriptor_storage.c: register after .kef decrypt` (or a tighter phrasing of it).
