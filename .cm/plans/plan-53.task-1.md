# P53 — Drop settings_get_default_policy() + wallet_set_policy() from key_confirmation.c

**Task ID:** `phase-53.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 8 — drop policy load**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 12**

## Files touched

**Modified:**
- `main/pages/shared/key_confirmation.c`

## Scope (single commit)

- In the post-mnemonic handler (lines 25-46, with P29's registry_init added), delete the `settings_get_default_policy()` call and the subsequent `wallet_set_policy(...)` call.
- After this commit, no code reads the `def_pol` NVS key or calls `wallet_set_policy`.
- Verify: `rg 'settings_get_default_policy\|wallet_set_policy\|wallet_get_policy' main/` — expect zero hits.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Drop settings_get_default_policy() + wallet_set_policy() from key_confirmation.c` (or a tighter phrasing of it).
