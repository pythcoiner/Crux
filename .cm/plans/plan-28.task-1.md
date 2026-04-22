# P28 — psbt_classify_output + fixtures B/C of test_psbt_classify.c

**Task ID:** `phase-28.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 5 — psbt_classify_output**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 11**

## Files touched

**Modified:**
- `main/core/psbt.c`
- `main/core/test/test_psbt_classify.c`

## Scope (single commit)

- Implement `psbt_classify_output`:
- 1. Get output script from `wally_psbt_get_global_tx_alloc` → `tx->outputs[i].script` (same pattern as `psbt.c:598-599`).
- 2. Loop over output keypaths matching our fingerprint.
- 3. Same enumerate-claims-and-verify loop as `psbt_classify_input`, but no UTXO extraction and no redeem/witness cross-check — comparing spk is sufficient for output ownership.
- 4. On verified match → `owned=true, source=<claim>`. **Do NOT tag the output as change or receive** — the signer has no such concept.
- Add fixtures B, C. Fixture B: BIP86 taproot receive + non-ours external output → owned=true and owned=false respectively. Fixture C: wsh-multisig registered descriptor, 2-of-3 → owned=true.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: psbt_classify_output + fixtures B/C of test_psbt_classify.c` (or a tighter phrasing of it).
