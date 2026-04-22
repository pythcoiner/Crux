# P22 — psbt.h: claim_t, expected_scripts_t, input/output_ownership_t + fn decls

**Task ID:** `phase-22.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 5 — Header**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 05**

## Files touched

**Modified:**
- `main/core/psbt.h`

## Scope (single commit)

- Define `typedef enum { CLAIM_WHITELIST, CLAIM_REGISTRY } claim_kind_t;`
- Define `claim_t` struct with `kind` + union { whitelist: { ss_script_type_t script, uint32_t account, uint32_t chain, uint32_t index, uint32_t purpose, uint32_t coin }; registry: { registry_entry_t *entry, uint32_t multi_index, uint32_t child_num } }; plus derived path copy (uint32_t[MAX_KEYPATH_TOTAL_DEPTH], len).
- Define `expected_scripts_t` struct: `uint8_t spk[34], size_t spk_len, uint8_t redeem[64], size_t redeem_len, uint8_t witness[256], size_t witness_len`.
- Define `input_ownership_t` struct: `bool owned, bool verified, claim_t claim, bool requires_ack, uint8_t raw_keypath[MAX_KEYPATH_TOTAL_DEPTH*4+4], size_t raw_keypath_len`.
- Define `output_ownership_t` struct: `bool owned, claim_t source`. **Do NOT include an `is_change` field.**
- Declare `input_ownership_t psbt_classify_input(const struct wally_psbt *psbt, size_t i, bool is_testnet)`, `output_ownership_t psbt_classify_output(const struct wally_psbt *psbt, size_t i, bool is_testnet)`, `bool claim_regenerate(const claim_t *claim, bool is_testnet, expected_scripts_t *out)`.
- Declare helpers: `bool psbt_input_utxo_script(...)`, `bool try_match_whitelist(...)`, `bool try_match_registry(...)`.

## Notes

Header-only change. No implementations yet.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: psbt.h: claim_t, expected_scripts_t, input/output_ownership_t + fn decls` (or a tighter phrasing of it).
