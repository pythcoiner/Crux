# descriptor-rework — Roadmap

Implementation progress tracker. Each item is a single-commit phase; all 78 items map 1:1 to tasks in `tasks.json`.

Legend: `[ ]` pending / `[x]` complete

Authoritative spec: `.cm/spec/PLAN.md` + `SNIP.md` + `ROADMAP.md`.

---

## Group 0: Scaffolding

Status: [ ] Not Started

- [ ] **P01: Scaffolding: empty ss_whitelist/registry skeletons + CMake wiring** → `phase-1.task-1`

---

## Group A: ss_whitelist module (additive)

Status: [ ] Not Started

- [ ] **P02: ss_whitelist: types, constants, inline helpers** → `phase-2.task-1`
- [ ] **P03: ss_keypath_parse + test_ss_whitelist_parse.c** → `phase-3.task-1`
- [ ] **P04: ss_keypath_format + round-trip test** → `phase-4.task-1`
- [ ] **P05: ss_keypath_is_whitelisted + test_ss_whitelist_is_whitelisted.c** → `phase-5.task-1`
- [ ] **P06: ss_scriptpubkey dispatcher + P2WPKH branch** → `phase-6.task-1`
- [ ] **P07: ss_scriptpubkey P2PKH branch** → `phase-7.task-1`
- [ ] **P08: ss_scriptpubkey P2SH_P2WPKH branch + ss_scriptpubkey_with_redeem variant** → `phase-8.task-1`
- [ ] **P09: ss_scriptpubkey P2TR branch (BIP341 tweak)** → `phase-9.task-1`
- [ ] **P10: ss_address dispatcher + test_ss_whitelist_regen.c integration tests** → `phase-10.task-1`
- [ ] **P11: purpose_script_binding_check_strict + _soft + test_purpose_binding.c** → `phase-11.task-1`

---

## Group B: registry module (additive)

Status: [ ] Not Started

- [ ] **P12: registry: types, REGISTRY_MAX_ENTRIES, static storage** → `phase-12.task-1`
- [ ] **P13: registry accessors: count / get / find_by_id** → `phase-13.task-1`
- [ ] **P14: registry_clear (free each desc + zero array)** → `phase-14.task-1`
- [ ] **P15: registry_add_from_string in-memory path (persist=false)** → `phase-15.task-1`
- [ ] **P16: registry_add_from_string persist path via storage_save_descriptor** → `phase-16.task-1`
- [ ] **P17: registry_remove (free + shift + storage_delete_descriptor)** → `phase-17.task-1`
- [ ] **P18: registry_match_keypath + test_registry_match.c** → `phase-18.task-1`
- [ ] **P19: registry_init: scan flash + SD, parse all, populate, log count** → `phase-19.task-1`
- [ ] **P20: test_registry_parse.c (wpkh / wsh(sortedmulti) / tr / miniscript)** → `phase-20.task-1`

---

## Group C: Settings (additive)

Status: [ ] Not Started

- [ ] **P21: Add settings_get/set_permissive_signing + KEY_PERMISSIVE_SIGNING (additive)** → `phase-21.task-1`

---

## Group D: PSBT classifier (additive)

Status: [ ] Not Started

- [ ] **P22: psbt.h: claim_t, expected_scripts_t, input/output_ownership_t + fn decls** → `phase-22.task-1`
- [ ] **P23: psbt_input_utxo_script helper (witness-utxo first, fallback utxo+prevout)** → `phase-23.task-1`
- [ ] **P24: try_match_whitelist + try_match_registry wrappers (with cursor pagination)** → `phase-24.task-1`
- [ ] **P25: claim_regenerate whitelist branch + test** → `phase-25.task-1`
- [ ] **P26: claim_regenerate registry branch (wsh / sh(wsh) / sh(multi)) + test** → `phase-26.task-1`
- [ ] **P27: psbt_classify_input + fixtures A/D/E of test_psbt_classify.c** → `phase-27.task-1`
- [ ] **P28: psbt_classify_output + fixtures B/C of test_psbt_classify.c** → `phase-28.task-1`

---

## Group E: Boot wiring

Status: [ ] Not Started

- [ ] **P29: Boot wiring: registry_init called after wallet_init in key_confirmation.c** → `phase-29.task-1`

---

## Group F: PSBT signing migration

Status: [ ] Not Started

- [ ] **P30: Rewrite psbt_sign body to use classifier + claim_regenerate** → `phase-30.task-1`
- [ ] **P31: Delete psbt_get_output_derivation; migrate callers to psbt_classify_output** → `phase-31.task-1`
- [ ] **P32: Delete psbt_verify_output_with_descriptor; migrate callers** → `phase-32.task-1`
- [ ] **P33: Delete/replace psbt_is_multisig (callers switch to claim.kind==CLAIM_REGISTRY)** → `phase-33.task-1`

---

## Group G: UI migration

Status: [ ] Not Started

- [ ] **P34: addresses.c: source-picker scaffold replacing type_dropdown** → `phase-34.task-1`
- [ ] **P35: addresses.c: refresh_address_list dispatches to ss_address / wally_descriptor_to_address** → `phase-35.task-1`
- [ ] **P36: addresses.c: account input + remove 'descriptor required' empty state + rename Load->Register** → `phase-36.task-1`
- [ ] **P37: address_checker.c: source picker** → `phase-37.task-1`
- [ ] **P38: address_checker.c: sweep within selected source** → `phase-38.task-1`
- [ ] **P39: store_descriptor.c: auto-register via registry_add_from_string(persist=false) after save** → `phase-39.task-1`
- [ ] **P40: load_descriptor_storage.c: register after .kef decrypt (success_from_kef_decrypt)** → `phase-40.task-1`
- [ ] **P41: load_descriptor_storage.c: register after plaintext load (paranoia)** → `phase-41.task-1`

---

## Group H: descriptor_validator cleanup

Status: [ ] Not Started

- [ ] **P42: descriptor_validator: redirect info_confirm_proceed to registry_add_from_string(persist=true)** → `phase-42.task-1`
- [ ] **P43: descriptor_validator: add WARN dialog via purpose_script_binding_check_soft** → `phase-43.task-1`
- [ ] **P44: descriptor_validator: delete apply_changes_and_verify (lines 350-386)** → `phase-44.task-1`
- [ ] **P45: descriptor_validator: delete check_attributes_and_verify + state fields** → `phase-45.task-1`
- [ ] **P46: descriptor_validator: delete parse_origin_path helper (lines 80-143)** → `phase-46.task-1`

---

## Group I: Settings UI migration

Status: [ ] Not Started

- [ ] **P47: wallet_settings.c: remove policy_dropdown UI element + handlers** → `phase-47.task-1`
- [ ] **P48: wallet_settings.c: remove account spinner + save handler** → `phase-48.task-1`
- [ ] **P49: wallet_settings.c: remove derivation-path preview label** → `phase-49.task-1`
- [ ] **P50: wallet_settings.c: add 'Permissive signing' toggle wired to new setting** → `phase-50.task-1`
- [ ] **P51: wallet_settings.c: update update_apply_button_state** → `phase-51.task-1`
- [ ] **P52: registered_descriptors.c sub-page with Remove/View (optional)** → `phase-52.task-1`

---

## Group J: Policy API removal

Status: [ ] Not Started

- [ ] **P53: Drop settings_get_default_policy() + wallet_set_policy() from key_confirmation.c** → `phase-53.task-1`
- [ ] **P54: Remove settings_get_default_policy / settings_set_default_policy** → `phase-54.task-1`
- [ ] **P55: Remove KEY_DEFAULT_POL constant** → `phase-55.task-1`

---

## Group K: Wallet API removal

Status: [ ] Not Started

- [ ] **P56: wallet.c: delete derive_address, derive_multisig_address helpers** → `phase-56.task-1`
- [ ] **P57: wallet.c: simplify wallet_init(network) to network-record only** → `phase-57.task-1`
- [ ] **P58: wallet.c: wallet_cleanup calls registry_clear()** → `phase-58.task-1`
- [ ] **P59: wallet.c: delete statics (wallet_type/policy/account/derivation_path_buffer/loaded_descriptor/account_key)** → `phase-59.task-1`
- [ ] **P60: wallet.h: delete wallet_policy_t enum** → `phase-60.task-1`
- [ ] **P61: wallet.h: delete format_derivation_path/format_derivation_compact/get_derivation** → `phase-61.task-1`
- [ ] **P62: wallet.h: delete get_account / set_account** → `phase-62.task-1`
- [ ] **P63: wallet.h: delete get_receive_address / get_change_address / get_scriptpubkey** → `phase-63.task-1`
- [ ] **P64: wallet.h: delete has_descriptor / load_descriptor / clear_descriptor** → `phase-64.task-1`
- [ ] **P65: wallet.h: delete get_multisig_receive_address / get_multisig_change_address** → `phase-65.task-1`
- [ ] **P66: wallet.h: delete get_policy / set_policy** → `phase-66.task-1`
- [ ] **P67: Move BIP-380 checksum helper to descriptor_checksum.c (optional)** → `phase-67.task-1`

---

## Group L: Cleanup

Status: [ ] Not Started

- [ ] **P68: Final rg sweep for stragglers of the removed wallet_* API; migrate or delete** → `phase-68.task-1`
- [ ] **P69: Remove dead tests covering deleted policy paths under main/core/test/** → `phase-69.task-1`
- [ ] **P70: Update repo-root ROADMAP.md to reflect new model** → `phase-70.task-1`
- [ ] **P71: CHANGELOG entry for the rework** → `phase-71.task-1`

---

## Group M: Device verification

Status: [ ] Not Started

- [ ] **P72: Device: clean builds on wave_4b, wave_35, wave_5** → `phase-72.task-1`
- [ ] **P73: Device: flash wave_35, store 3 plaintext descriptors, reboot, verify auto-load** → `phase-73.task-1`
- [ ] **P74: Device: Addresses page per-source vs Sparrow references** → `phase-74.task-1`
- [ ] **P75: Device: PSBT behavioural spec (every row of PLAN.md §Behavioural spec)** → `phase-75.task-1`
- [ ] **P76: Device: Settings UI gone/added as expected; permissive toggle works** → `phase-76.task-1`
- [ ] **P77: Device: Address checker known + random per source** → `phase-77.task-1`
- [ ] **P78: Device: WARN-dialog gating on mismatched descriptor registration** → `phase-78.task-1`

---

## Summary

| Group | Name | Items | Status |
|------:|------|------:|--------|
| 0 | Scaffolding | 1 | Not Started |
| A | ss_whitelist module (additive) | 10 | Not Started |
| B | registry module (additive) | 9 | Not Started |
| C | Settings (additive) | 1 | Not Started |
| D | PSBT classifier (additive) | 7 | Not Started |
| E | Boot wiring | 1 | Not Started |
| F | PSBT signing migration | 4 | Not Started |
| G | UI migration | 8 | Not Started |
| H | descriptor_validator cleanup | 5 | Not Started |
| I | Settings UI migration | 6 | Not Started |
| J | Policy API removal | 3 | Not Started |
| K | Wallet API removal | 12 | Not Started |
| L | Cleanup | 4 | Not Started |
| M | Device verification | 7 | Not Started |
| **Total** | | **78** | **0 / 78** |
