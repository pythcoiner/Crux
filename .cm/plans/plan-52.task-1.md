# P52 — registered_descriptors.c sub-page with Remove/View (optional)

**Task ID:** `phase-52.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 9 — registered_descriptors sub-page**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**New:**
- `main/pages/settings/registered_descriptors.c`
- `main/pages/settings/registered_descriptors.h`

**Modified:**
- `main/pages/settings/wallet_settings.c`
- `main/CMakeLists.txt`

## Scope (single commit)

- Create `main/pages/settings/registered_descriptors.c` + `.h`.
- List rows: one per `registry_get(i)`. Show `id` and a short script-type badge (wpkh / tr / wsh-multi / …).
- On row tap: detail dialog showing the descriptor string via a new helper `registry_entry_to_string(entry, buf, len)` that wraps `wally_descriptor_canonicalize` + the existing BIP-380 checksum helper. Add a 'Remove' button in the detail view → `registry_remove(id)` → close sub-page.
- Add an entry on `wallet_settings.c` page that navigates into the sub-page.
- Add the new .c file to `main/CMakeLists.txt` SRCS list.

## Notes

Mark as optional in the plan — skip if out of scope for a given sprint. If skipped, leave a task plan note and move on.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: registered_descriptors.c sub-page with Remove/View (optional)` (or a tighter phrasing of it).
