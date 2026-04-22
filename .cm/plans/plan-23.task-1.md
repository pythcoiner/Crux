# P23 — psbt_input_utxo_script helper (witness-utxo first, fallback utxo+prevout)

**Task ID:** `phase-23.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 5 — Helpers (psbt_input_utxo_script)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 05**

## Files touched

**Modified:**
- `main/core/psbt.c`

## Scope (single commit)

- Implement `bool psbt_input_utxo_script(const struct wally_psbt *psbt, size_t i, uint8_t *out, size_t out_cap, size_t *out_len)`.
- Try `wally_psbt_get_input_witness_utxo_alloc` first. On success, copy `tx_output->script` into `out` (respecting `out_cap`), set `*out_len`, free the tx_output, return true.
- Fallback: `wally_psbt_get_input_utxo_alloc`; index into `tx->outputs[prevout_index]` via `wally_psbt_get_input_previous_txid` or the existing utxo+vout lookup helper; copy script. Clean up allocated tx.
- Return false if neither path produced a script.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: psbt_input_utxo_script helper (witness-utxo first, fallback utxo+prevout)` (or a tighter phrasing of it).
