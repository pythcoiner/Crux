# P07 — ss_scriptpubkey P2PKH branch

**Task ID:** `phase-7.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Script regeneration (P2PKH)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 01**

## Files touched

**Modified:**
- `main/core/ss_whitelist.c`

## Scope (single commit)

- Add P2PKH branch in `ss_scriptpubkey`: derive pubkey via `key_get_derived_key` at `m/44'/coin'/account'/chain/index`, hash160 the pubkey (33 bytes → 20 bytes) via `wally_hash160`, then hand-build the 25-byte script: `OP_DUP OP_HASH160 <20> pkh OP_EQUALVERIFY OP_CHECKSIG`.
- `out[0] = 0x76; out[1] = 0xa9; out[2] = 0x14; memcpy(out+3, pkh20, 20); out[23] = 0x88; out[24] = 0xac; *out_len = 25;`

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: ss_scriptpubkey P2PKH branch` (or a tighter phrasing of it).
