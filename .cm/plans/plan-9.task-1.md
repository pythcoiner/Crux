# P09 — ss_scriptpubkey P2TR branch (BIP341 tweak)

**Task ID:** `phase-9.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Script regeneration (P2TR)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 01**

## Files touched

**Modified:**
- `main/core/ss_whitelist.c`

## Scope (single commit)

- Add P2TR branch in `ss_scriptpubkey`: derive compressed pubkey via `key_get_derived_key` at `m/86'/coin'/account'/chain/index`, drop the prefix byte (take `pubkey[1..33]`) to get x-only pubkey input, apply BIP341 key-path tweak (no script tree) to get the output 32-byte x-only pubkey.
- Use `wally_ec_public_key_bip341_tweak(pubkey33, 33, NULL, 0, flags, tweaked32, 32)` or the closest libwally equivalent available in this tree. If the single-call helper is absent, fall back to `wally_bip341_*` primitives as per SNIP 01.
- Hand-build 34-byte output: `OP_1 <32> tweaked_xonly`. `out[0] = 0x51; out[1] = 0x20; memcpy(out+2, tweaked32, 32); *out_len = 34;`

## Notes

If the single-shot bip341 tweak helper is not exported by the libwally version in `components/`, document the fallback in the commit message.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: ss_scriptpubkey P2TR branch (BIP341 tweak)` (or a tighter phrasing of it).
