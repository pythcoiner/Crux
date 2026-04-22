# P35 — addresses.c: refresh_address_list dispatches to ss_address / wally_descriptor_to_address

**Task ID:** `phase-35.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 10 — refresh_address_list rewrite**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/home/addresses.c`

## Scope (single commit)

- Rewrite `refresh_address_list` (lines 313-344) to dispatch based on current source:
- Singlesig source: call `ss_address(script, account, chain, index, is_testnet, buf, sizeof buf)` for each displayed row.
- Registered descriptor source: call `wally_descriptor_to_address(entry->desc, mp, child_num, 0, &addr)` (or a thin `registry_entry_address(entry, mp, ix, buf, len)` helper in registry.c).
- Remove all calls to `wallet_get_receive_address`, `wallet_get_change_address`, `wallet_get_multisig_receive_address`, `wallet_get_multisig_change_address` from this file.

## Notes

After this commit, addresses.c no longer depends on the old wallet_*_address API.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: addresses.c: refresh_address_list dispatches to ss_address / wally_descriptor_to_address` (or a tighter phrasing of it).
