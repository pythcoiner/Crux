# P27 — psbt_classify_input + fixtures A/D/E of test_psbt_classify.c

**Task ID:** `phase-27.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 5 — psbt_classify_input**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 09**

## Files touched

**Modified:**
- `main/core/psbt.c`
- `main/core/test/test_psbt_classify.c`

## Scope (single commit)

- Implement `psbt_classify_input`:
- 1. Extract UTXO script via `psbt_input_utxo_script`; if absent → return `owned=false`.
- 2. Loop over keypaths in this input matching our fingerprint (via `wally_psbt_get_input_keypath_*`).
- 3. For each keypath, enumerate candidate claims: `try_match_whitelist` first, then `try_match_registry` with cursor pagination.
- 4. For each claim, `claim_regenerate`; compare `expected.spk` to UTXO script. If sh-family: also `wally_psbt_get_input_redeem_script` byte-compare. If wsh-family: `wally_psbt_get_input_witness_script` byte-compare.
- 5. On verified match: return `owned=true, verified=true, claim=<claim>`.
- 6. If no verified claim but fp was seen and `settings_get_permissive_signing()`: return `owned=true, verified=false, requires_ack=true`, copy raw keypaths for UI prompt.
- 7. Else: `owned=false`.
- Add fixtures A, D, E to `test_psbt_classify.c`. Fixture A: BIP84 receive (PSBT hex fixture) → verified-owned. Fixture D: attacker PSBT with correct keypath but swapped UTXO script → owned=false. Fixture E: fp-only match with unknown path, permissive=off → owned=false.

## Notes

PSBT hex fixtures are best generated offline with Sparrow or `bitcoin-cli walletprocesspsbt`; commit as hex constants in the test.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: psbt_classify_input + fixtures A/D/E of test_psbt_classify.c` (or a tighter phrasing of it).
