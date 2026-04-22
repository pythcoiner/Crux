# P11 — purpose_script_binding_check_strict + _soft + test_purpose_binding.c

**Task ID:** `phase-11.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Purpose / script binding helpers**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 05**

## Files touched

**New:**
- `main/core/test/test_purpose_binding.c`

**Modified:**
- `main/core/ss_whitelist.h`
- `main/core/ss_whitelist.c`
- `main/core/test/CMakeLists.txt`

## Scope (single commit)

- Define `typedef enum { PSB_OK, PSB_WARN, PSB_NA } psb_result_t;` in the header (or `psb_check_result_t`).
- Declare `bool purpose_script_binding_check_strict(uint32_t purpose, ss_script_type_t outer_script)`. Implement the fixed table (44↔P2PKH, 49↔P2SH_P2WPKH, 84↔P2WPKH, 86↔P2TR); false otherwise.
- Declare `psb_result_t purpose_script_binding_check_soft(const struct wally_descriptor *desc)`. Walk the descriptor's outer token via libwally, read our key's origin purpose via `wally_descriptor_get_key_origin_path_str`, and apply the rules in PLAN.md §Purpose/script-type conventions. Return `PSB_NA` when purpose ∉ {44,48,49,84,86}; `PSB_OK` when the combination matches the convention; `PSB_WARN` otherwise.
- Add `test_purpose_binding.c`: WARN for `wsh(sortedmulti(2,[fp/86'/0'/0']xpub...))` and `tr([fp/84'/0'/0']xpub)`; OK for `wpkh([fp/84'/0'/0']xpub)`; NA for `wpkh([fp/99'/0'/0']xpub)`.
- Register test in `main/core/test/CMakeLists.txt`.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: purpose_script_binding_check_strict + _soft + test_purpose_binding.c` (or a tighter phrasing of it).
