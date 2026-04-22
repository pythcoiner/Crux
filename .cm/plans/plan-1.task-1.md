# P01 — Scaffolding: empty ss_whitelist/registry skeletons + CMake wiring

**Task ID:** `phase-1.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 0 — scaffolding & CMake wiring**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**New:**
- `main/core/ss_whitelist.h`
- `main/core/ss_whitelist.c`
- `main/core/registry.h`
- `main/core/registry.c`

**Modified:**
- `main/CMakeLists.txt`

## Scope (single commit)

- Create `main/core/ss_whitelist.h` with include-guard + `<stdbool.h>` / `<stddef.h>` / `<stdint.h>` includes. No content beyond the guard.
- Create `main/core/ss_whitelist.c` with only `#include "ss_whitelist.h"`.
- Create `main/core/registry.h` with include-guard + includes for `<stddef.h>` and `<wally_descriptor.h>` and `"storage.h"`.
- Create `main/core/registry.c` with only `#include "registry.h"`.
- Add all four filenames to `main/CMakeLists.txt` `SRCS` list in alphabetical order.
- Confirm clean build: `just build wave_4b`.

## Notes

No other files touched. No function declarations yet — those arrive in P02/P12.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Scaffolding: empty ss_whitelist/registry skeletons + CMake wiring` (or a tighter phrasing of it).
