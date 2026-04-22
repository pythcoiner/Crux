# P75 — Device: PSBT behavioural spec (every row of PLAN.md §Behavioural spec)

**Task ID:** `phase-75.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 15 — device verification (PSBT)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

## Scope (single commit)

- Craft PSBTs offline (Sparrow or `bitcoin-cli`) exercising each row of `.cm/spec/PLAN.md` §'Signing' + §'Output classification':
- `m/84'/0'/3'/0/12` → sign (account 3, not 0).
- `m/86'/0'/0'/1/4` → sign (taproot).
- `m/44'/0'/100'/0/0` → refuse (account ≥ 100).
- `m/84'/0'/0'/0/100` → refuse (index ≥ 100).
- Registered `wsh(sortedmulti(2,...))` → sign using that descriptor.
- Non-standard `m/9999'/0'/0'/0/0`, permissive=off → skip (0 signatures added).
- Same, permissive=on → ACK prompt; sign after confirm.
- Attacker PSBT with correct keypath but swapped UTXO script → refuse silently.
- Verify review-screen output classification matches the table (owned outputs show derivation path; not-ours outputs treated as external; no fingerprint-only fallback).

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Device: PSBT behavioural spec (every row of PLAN.md §Behavioural spec)` (or a tighter phrasing of it).
