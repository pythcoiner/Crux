# P08 — ss_scriptpubkey P2SH_P2WPKH branch + ss_scriptpubkey_with_redeem variant

**Task ID:** `phase-8.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Script regeneration (P2SH_P2WPKH + redeem variant)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 01**

## Files touched

**Modified:**
- `main/core/ss_whitelist.h`
- `main/core/ss_whitelist.c`

## Scope (single commit)

- Add P2SH_P2WPKH branch in `ss_scriptpubkey`: build inner 22-byte `wpkh` (same as P2WPKH branch), compute hash160 of those 22 bytes → 20-byte sh, hand-build 23-byte `OP_HASH160 <20> sh OP_EQUAL`.
- `out[0] = 0xa9; out[1] = 0x14; memcpy(out+2, sh20, 20); out[22] = 0x87; *out_len = 23;`
- Declare and implement `bool ss_scriptpubkey_with_redeem(ss_script_type_t script, uint32_t account, uint32_t chain, uint32_t index, bool is_testnet, uint8_t *spk_out, size_t *spk_len, uint8_t *redeem_out, size_t *redeem_len)`: same as `ss_scriptpubkey` plus, for P2SH_P2WPKH, also returns the 22-byte inner wpkh as the redeem script. For other script types, `*redeem_len = 0`.
- `claim_regenerate` (P25) will rely on the redeem variant to verify PSBT `redeem_script` fields on sh-nested inputs.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: ss_scriptpubkey P2SH_P2WPKH branch + ss_scriptpubkey_with_redeem variant` (or a tighter phrasing of it).
