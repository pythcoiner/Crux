# P18 — registry_match_keypath + test_registry_match.c

**Task ID:** `phase-18.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 2 — Matching**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 02, SNIP 07**

## Files touched

**New:**
- `main/core/test/test_registry_match.c`

**Modified:**
- `main/core/registry.h`
- `main/core/registry.c`
- `main/core/test/CMakeLists.txt`

## Scope (single commit)

- Declare `registry_entry_t *registry_match_keypath(const uint8_t *keypath, size_t keypath_len, size_t *cursor)`. Cursor enables paging past false-positive prefix collisions (see SNIP 07).
- Implement: validate `(keypath_len - 4) % 4 == 0` and total depth ≤ `MAX_KEYPATH_TOTAL_DEPTH`. For each entry starting at `*cursor`, byte-compare `origin_path_len * 4` bytes starting at `keypath + 4` against `entry.origin_path`. Require `total_depth - origin_path_len == 2` (the `/<mp>/<ix>` suffix). Enforce `mp ≤ 1`, plus `mp == 0` if `entry.num_paths == 1`. Reject hardened `mp` or `ix`.
- Advance `*cursor` past the returned entry so the caller can re-invoke for the next match.
- Add `test_registry_match.c`: seed 3 registry entries with distinct origin paths via `registry_add_from_string(..., persist=false)`; build a fake keypath matching entry #2; expect match = entry #2. Unknown origin → NULL. Non-matching trailing depth (1 or 3 components after origin) → NULL. Hardened trailing → NULL.
- Register test in `main/core/test/CMakeLists.txt`.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: registry_match_keypath + test_registry_match.c` (or a tighter phrasing of it).
