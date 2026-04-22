# P06 — ss_scriptpubkey dispatcher + P2WPKH branch

**Task ID:** `phase-6.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Script regeneration / address derivation (P2WPKH)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 01**

## Files touched

**Modified:**
- `main/core/ss_whitelist.h`
- `main/core/ss_whitelist.c`

## Scope (single commit)

- Declare `bool ss_scriptpubkey(ss_script_type_t script, uint32_t account, uint32_t chain, uint32_t index, bool is_testnet, uint8_t *out, size_t *out_len)` in the header.
- Add a dispatch `switch` over `script`. Other branches can return false / unimplemented for now; only P2WPKH is implemented in this commit.
- P2WPKH branch: derive the compressed pubkey via `key_get_derived_key` at `m/84'/coin'/account'/chain/index`, then `wally_witness_program_from_bytes(pubkey, 33, WALLY_SCRIPT_HASH160, out, 22, out_len)`. Result is a 22-byte `OP_0 <20> pkh`.

## Notes

Keep `key_get_derived_key` usage consistent with existing call sites. No test added here — see P10 for integration tests.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: ss_scriptpubkey dispatcher + P2WPKH branch` (or a tighter phrasing of it).
