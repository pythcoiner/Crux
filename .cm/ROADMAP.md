# descriptor-rework - Roadmap

This document tracks implementation progress. Check off items as they are completed.

## Phase 0: Scaffolding

Status: **Complete** (1/1)

- [x] P01: Scaffolding: empty ss_whitelist/registry skeletons + CMake wiring

---

## Phase A: ss_whitelist module (additive)

Status: **Complete** (10/10)

- [x] P02: ss_whitelist: types, constants, inline helpers
- [x] P03: ss_keypath_parse + test_ss_whitelist_parse.c
- [x] P04: ss_keypath_format + round-trip test
- [x] P05: ss_keypath_is_whitelisted + test_ss_whitelist_is_whitelisted.c
- [x] P06: ss_scriptpubkey dispatcher + P2WPKH branch
- [x] P07: ss_scriptpubkey P2PKH branch
- [x] P08: ss_scriptpubkey P2SH_P2WPKH branch + ss_scriptpubkey_with_redeem variant
- [x] P09: ss_scriptpubkey P2TR branch (BIP341 tweak)
- [x] P10: ss_address dispatcher + test_ss_whitelist_regen.c integration tests
- [x] P11: purpose_script_binding_check_strict + _soft + test_purpose_binding.c

---

## Phase B: registry module (additive)

Status: **Complete** (9/9)

- [x] P12: registry: types, REGISTRY_MAX_ENTRIES, static storage
- [x] P13: registry accessors: count / get / find_by_id
- [x] P14: registry_clear (free each desc + zero array)
- [x] P15: registry_add_from_string in-memory path (persist=false)
- [x] P16: registry_add_from_string persist path via storage_save_descriptor
- [x] P17: registry_remove (free + shift + storage_delete_descriptor)
- [x] P18: registry_match_keypath + test_registry_match.c
- [x] P19: registry_init: scan flash + SD, parse all, populate, log count
- [x] P20: test_registry_parse.c (wpkh / wsh(sortedmulti) / tr / miniscript)

---

## Phase C: Settings (additive)

Status: **Complete** (1/1)

- [x] P21: Add settings_get/set_permissive_signing + KEY_PERMISSIVE_SIGNING (additive)

---

## Phase D: PSBT classifier (additive)

Status: **Complete** (7/7)

- [x] P22: psbt.h: claim_t, expected_scripts_t, input/output_ownership_t + fn decls
- [x] P23: psbt_input_utxo_script helper (witness-utxo first, fallback utxo+prevout)
- [x] P24: try_match_whitelist + try_match_registry wrappers (with cursor pagination)
- [x] P25: claim_regenerate whitelist branch + test
- [x] P26: claim_regenerate registry branch (wsh / sh(wsh) / sh(multi)) + test
- [x] P27: psbt_classify_input + fixtures A/D/E of test_psbt_classify.c
- [x] P28: psbt_classify_output + fixtures B/C of test_psbt_classify.c

---

## Phase E: Boot wiring

Status: **Complete** (1/1)

- [x] P29: Boot wiring: registry_init called after wallet_init in key_confirmation.c

---

## Phase F: PSBT signing migration

Status: **Complete** (4/4)

- [x] P30: Rewrite psbt_sign body to use classifier + claim_regenerate
- [x] P31: Delete psbt_get_output_derivation; migrate callers to psbt_classify_output
- [x] P32: Delete psbt_verify_output_with_descriptor; migrate callers
- [x] P33: Delete/replace psbt_is_multisig (callers switch to claim.kind==CLAIM_REGISTRY)

---

## Phase G: UI migration

Status: **Complete** (8/8)

- [x] P34: addresses.c: source-picker scaffold replacing type_dropdown
- [x] P35: addresses.c: refresh_address_list dispatches to ss_address / wally_descriptor_to_address
- [x] P36: addresses.c: account input + remove 'descriptor required' empty state + rename Load->Register
- [x] P37: address_checker.c: source picker
- [x] P38: address_checker.c: sweep within selected source
- [x] P39: store_descriptor.c: auto-register via registry_add_from_string(persist=false) after save
- [x] P40: load_descriptor_storage.c: register after .kef decrypt (success_from_kef_decrypt)
- [x] P41: load_descriptor_storage.c: register after plaintext load (paranoia)

---

## Phase H: descriptor_validator cleanup

Status: **Complete** (5/5)

- [x] P42: descriptor_validator: redirect info_confirm_proceed to registry_add_from_string(persist=true)
- [x] P43: descriptor_validator: add WARN dialog via purpose_script_binding_check_soft
- [x] P44: descriptor_validator: delete apply_changes_and_verify (lines 350-386)
- [x] P45: descriptor_validator: delete check_attributes_and_verify + state fields
- [x] P46: descriptor_validator: delete parse_origin_path helper (lines 80-143)

---

## Phase I: Settings UI migration

Status: **Complete** (6/6)

- [x] P47: wallet_settings.c: remove policy_dropdown UI element + handlers
- [x] P48: wallet_settings.c: remove account spinner + save handler
- [x] P49: wallet_settings.c: remove derivation-path preview label
- [x] P50: wallet_settings.c: add 'Permissive signing' toggle wired to new setting
- [x] P51: wallet_settings.c: update update_apply_button_state
- [x] P52: registered_descriptors.c sub-page with Remove/View (optional)

---

## Phase J: Policy API removal

Status: **Complete** (3/3)

- [x] P53: Drop settings_get_default_policy() + wallet_set_policy() from key_confirmation.c
- [x] P54: Remove settings_get_default_policy / settings_set_default_policy
- [x] P55: Remove KEY_DEFAULT_POL constant

---

## Phase K: Wallet API removal

Status: **Complete** (12/12)

- [x] P56: wallet.c: delete derive_address, derive_multisig_address helpers
- [x] P57: wallet.c: simplify wallet_init(network) to network-record only
- [x] P58: wallet.c: wallet_cleanup calls registry_clear()
- [x] P59: wallet.c: delete statics (wallet_type/policy/account/derivation_path_buffer/loaded_descriptor/account_key)
- [x] P60: wallet.h: delete wallet_policy_t enum
- [x] P61: wallet.h: delete format_derivation_path/format_derivation_compact/get_derivation
- [x] P62: wallet.h: delete get_account / set_account
- [x] P63: wallet.h: delete get_receive_address / get_change_address / get_scriptpubkey
- [x] P64: wallet.h: delete has_descriptor / load_descriptor / clear_descriptor
- [x] P65: wallet.h: delete get_multisig_receive_address / get_multisig_change_address
- [x] P66: wallet.h: delete get_policy / set_policy
- [x] P67: Move BIP-380 checksum helper to descriptor_checksum.c (optional)

---

## Phase L: Cleanup

Status: **Complete** (4/4)

- [x] P68: Final rg sweep for stragglers of the removed wallet_* API; migrate or delete
- [x] P69: Remove dead tests covering deleted policy paths under main/core/test/
- [x] P70: Update repo-root ROADMAP.md to reflect new model
- [x] P71: CHANGELOG entry for the rework

---

## Phase M: Device verification

Status: **In Progress** (1/7)

- [x] P72: Device: clean builds on wave_4b, wave_35, wave_5
- [ ] P73: Device: flash wave_35, store 3 plaintext descriptors, reboot, verify auto-load
- [ ] P74: Device: Addresses page per-source vs Sparrow references
- [ ] P75: Device: PSBT behavioural spec (every row of PLAN.md §Behavioural spec)
- [ ] P76: Device: Settings UI gone/added as expected; permissive toggle works
- [ ] P77: Device: Address checker known + random per source
- [ ] P78: Device: WARN-dialog gating on mismatched descriptor registration

---

## Summary

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 0: Scaffolding | Complete | 1/1 |
| Phase A: ss_whitelist module (additive) | Complete | 10/10 |
| Phase B: registry module (additive) | Complete | 9/9 |
| Phase C: Settings (additive) | Complete | 1/1 |
| Phase D: PSBT classifier (additive) | Complete | 7/7 |
| Phase E: Boot wiring | Complete | 1/1 |
| Phase F: PSBT signing migration | Complete | 4/4 |
| Phase G: UI migration | Complete | 8/8 |
| Phase H: descriptor_validator cleanup | Complete | 5/5 |
| Phase I: Settings UI migration | Complete | 6/6 |
| Phase J: Policy API removal | Complete | 3/3 |
| Phase K: Wallet API removal | Complete | 12/12 |
| Phase L: Cleanup | Complete | 4/4 |
| Phase M: Device verification | In Progress | 1/7 |
| **Total** | | **72/78** |
