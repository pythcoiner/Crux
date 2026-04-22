# P68 — Final rg sweep for stragglers of the removed wallet_* API

**Task ID:** `phase-68.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 13 — remove old single-descriptor in-memory state**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

## Scope (single commit)

- Run:
```
- rg -n 'wallet_has_descriptor|wallet_load_descriptor|wallet_clear_descriptor|wallet_get_multisig_|wallet_get_receive_address|wallet_get_change_address|wallet_get_scriptpubkey|wallet_get_policy|wallet_set_policy|wallet_get_account|wallet_set_account|wallet_format_derivation|wallet_get_derivation'
```
- For each hit: migrate to the new API (registry / ss_whitelist) or delete if the surrounding feature is dead.
- Ensure the code still compiles cleanly with `-Wunused-function` and `-Wunused-variable`.

## Notes

If the grep returns zero hits, this commit can be empty (skip creating a commit, mark phase complete).

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Final rg sweep for stragglers of the removed wallet_* API` (or a tighter phrasing of it).
