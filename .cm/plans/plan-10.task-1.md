# P10 — ss_address dispatcher + test_ss_whitelist_regen.c integration tests

**Task ID:** `phase-10.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 1 — Script regeneration / address derivation (ss_address + integration)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 01**

## Files touched

**New:**
- `main/core/test/test_ss_whitelist_regen.c`

**Modified:**
- `main/core/ss_whitelist.h`
- `main/core/ss_whitelist.c`
- `main/core/test/CMakeLists.txt`

## Scope (single commit)

- Declare `bool ss_address(ss_script_type_t script, uint32_t account, uint32_t chain, uint32_t index, bool is_testnet, char *address_out, size_t address_out_len)` in the header.
- Implement: call `ss_scriptpubkey` to get the spk, then encode: P2WPKH / P2TR → `wally_addr_segwit_from_bytes` with hrp `bc` (mainnet) / `tb` (testnet); P2PKH / P2SH_P2WPKH → `wally_scriptpubkey_to_address` with `WALLY_NETWORK_BITCOIN_MAINNET` / `WALLY_NETWORK_BITCOIN_TESTNET`.
- Add `test_ss_whitelist_regen.c`: for a known test mnemonic (hardcoded in the test), regenerate each of the four script types at (account=0, chain=0, index=0) and compare to known-good addresses / scriptPubKeys from Sparrow or `bitcoin-cli getdescriptorinfo` + `deriveaddresses`. Commit the reference values as hex constants.
- Register test in `main/core/test/CMakeLists.txt`.

## Notes

The reference values are the core of this test — pre-compute them offline before coding.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: ss_address dispatcher + test_ss_whitelist_regen.c integration tests` (or a tighter phrasing of it).
