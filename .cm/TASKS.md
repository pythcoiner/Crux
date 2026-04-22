# descriptor-rework — Tasks

78 phases × 1 task = 78 tasks. Each phase is one commit.

Status legend: pending / in_progress / completed / deferred

| Phase | Task ID | Title | Type | Status | Depends on |
|------:|---------|-------|------|--------|-----------|
| P01 | `phase-1.task-1` | Scaffolding: empty ss_whitelist/registry skeletons + CMake wiring | implement | pending | `—` |
| P02 | `phase-2.task-1` | ss_whitelist: types, constants, inline helpers | implement | pending | `phase-1.task-1` |
| P03 | `phase-3.task-1` | ss_keypath_parse + test_ss_whitelist_parse.c | implement | pending | `phase-2.task-1` |
| P04 | `phase-4.task-1` | ss_keypath_format + round-trip test | implement | pending | `phase-3.task-1` |
| P05 | `phase-5.task-1` | ss_keypath_is_whitelisted + test_ss_whitelist_is_whitelisted.c | implement | pending | `phase-4.task-1` |
| P06 | `phase-6.task-1` | ss_scriptpubkey dispatcher + P2WPKH branch | implement | pending | `phase-5.task-1` |
| P07 | `phase-7.task-1` | ss_scriptpubkey P2PKH branch | implement | pending | `phase-6.task-1` |
| P08 | `phase-8.task-1` | ss_scriptpubkey P2SH_P2WPKH branch + ss_scriptpubkey_with_redeem variant | implement | pending | `phase-7.task-1` |
| P09 | `phase-9.task-1` | ss_scriptpubkey P2TR branch (BIP341 tweak) | implement | pending | `phase-8.task-1` |
| P10 | `phase-10.task-1` | ss_address dispatcher + test_ss_whitelist_regen.c integration tests | implement | pending | `phase-9.task-1` |
| P11 | `phase-11.task-1` | purpose_script_binding_check_strict + _soft + test_purpose_binding.c | implement | pending | `phase-10.task-1` |
| P12 | `phase-12.task-1` | registry: types, REGISTRY_MAX_ENTRIES, static storage | implement | pending | `phase-11.task-1` |
| P13 | `phase-13.task-1` | registry accessors: count / get / find_by_id | implement | pending | `phase-12.task-1` |
| P14 | `phase-14.task-1` | registry_clear (free each desc + zero array) | implement | pending | `phase-13.task-1` |
| P15 | `phase-15.task-1` | registry_add_from_string in-memory path (persist=false) | implement | pending | `phase-14.task-1` |
| P16 | `phase-16.task-1` | registry_add_from_string persist path via storage_save_descriptor | implement | pending | `phase-15.task-1` |
| P17 | `phase-17.task-1` | registry_remove (free + shift + storage_delete_descriptor) | implement | pending | `phase-16.task-1` |
| P18 | `phase-18.task-1` | registry_match_keypath + test_registry_match.c | implement | pending | `phase-17.task-1` |
| P19 | `phase-19.task-1` | registry_init: scan flash + SD, parse all, populate, log count | implement | pending | `phase-18.task-1` |
| P20 | `phase-20.task-1` | test_registry_parse.c (wpkh / wsh(sortedmulti) / tr / miniscript) | implement | pending | `phase-19.task-1` |
| P21 | `phase-21.task-1` | Add settings_get/set_permissive_signing + KEY_PERMISSIVE_SIGNING (additive) | implement | pending | `phase-20.task-1` |
| P22 | `phase-22.task-1` | psbt.h: claim_t, expected_scripts_t, input/output_ownership_t + fn decls | implement | pending | `phase-21.task-1` |
| P23 | `phase-23.task-1` | psbt_input_utxo_script helper (witness-utxo first, fallback utxo+prevout) | implement | pending | `phase-22.task-1` |
| P24 | `phase-24.task-1` | try_match_whitelist + try_match_registry wrappers (with cursor pagination) | implement | pending | `phase-23.task-1` |
| P25 | `phase-25.task-1` | claim_regenerate whitelist branch + test | implement | pending | `phase-24.task-1` |
| P26 | `phase-26.task-1` | claim_regenerate registry branch (wsh / sh(wsh) / sh(multi)) + test | implement | pending | `phase-25.task-1` |
| P27 | `phase-27.task-1` | psbt_classify_input + fixtures A/D/E of test_psbt_classify.c | implement | pending | `phase-26.task-1` |
| P28 | `phase-28.task-1` | psbt_classify_output + fixtures B/C of test_psbt_classify.c | implement | pending | `phase-27.task-1` |
| P29 | `phase-29.task-1` | Boot wiring: registry_init called after wallet_init in key_confirmation.c | implement | pending | `phase-28.task-1` |
| P30 | `phase-30.task-1` | Rewrite psbt_sign body to use classifier + claim_regenerate | implement | pending | `phase-29.task-1` |
| P31 | `phase-31.task-1` | Delete psbt_get_output_derivation; migrate callers to psbt_classify_output | implement | pending | `phase-30.task-1` |
| P32 | `phase-32.task-1` | Delete psbt_verify_output_with_descriptor; migrate callers | implement | pending | `phase-31.task-1` |
| P33 | `phase-33.task-1` | Delete/replace psbt_is_multisig (callers switch to claim.kind==CLAIM_REGISTRY) | implement | pending | `phase-32.task-1` |
| P34 | `phase-34.task-1` | addresses.c: source-picker scaffold replacing type_dropdown | implement | pending | `phase-33.task-1` |
| P35 | `phase-35.task-1` | addresses.c: refresh_address_list dispatches to ss_address / wally_descriptor_to_address | implement | pending | `phase-34.task-1` |
| P36 | `phase-36.task-1` | addresses.c: account input + remove 'descriptor required' empty state + rename Load->Register | implement | pending | `phase-35.task-1` |
| P37 | `phase-37.task-1` | address_checker.c: source picker | implement | pending | `phase-36.task-1` |
| P38 | `phase-38.task-1` | address_checker.c: sweep within selected source | implement | pending | `phase-37.task-1` |
| P39 | `phase-39.task-1` | store_descriptor.c: auto-register via registry_add_from_string(persist=false) after save | implement | pending | `phase-38.task-1` |
| P40 | `phase-40.task-1` | load_descriptor_storage.c: register after .kef decrypt (success_from_kef_decrypt) | implement | pending | `phase-39.task-1` |
| P41 | `phase-41.task-1` | load_descriptor_storage.c: register after plaintext load (paranoia) | implement | pending | `phase-40.task-1` |
| P42 | `phase-42.task-1` | descriptor_validator: redirect info_confirm_proceed to registry_add_from_string(persist=true) | implement | pending | `phase-41.task-1` |
| P43 | `phase-43.task-1` | descriptor_validator: add WARN dialog via purpose_script_binding_check_soft | implement | pending | `phase-42.task-1` |
| P44 | `phase-44.task-1` | descriptor_validator: delete apply_changes_and_verify (lines 350-386) | implement | pending | `phase-43.task-1` |
| P45 | `phase-45.task-1` | descriptor_validator: delete check_attributes_and_verify + state fields | implement | pending | `phase-44.task-1` |
| P46 | `phase-46.task-1` | descriptor_validator: delete parse_origin_path helper (lines 80-143) | implement | pending | `phase-45.task-1` |
| P47 | `phase-47.task-1` | wallet_settings.c: remove policy_dropdown UI element + handlers | implement | pending | `phase-46.task-1` |
| P48 | `phase-48.task-1` | wallet_settings.c: remove account spinner + save handler | implement | pending | `phase-47.task-1` |
| P49 | `phase-49.task-1` | wallet_settings.c: remove derivation-path preview label | implement | pending | `phase-48.task-1` |
| P50 | `phase-50.task-1` | wallet_settings.c: add 'Permissive signing' toggle wired to new setting | implement | pending | `phase-49.task-1` |
| P51 | `phase-51.task-1` | wallet_settings.c: update update_apply_button_state | implement | pending | `phase-50.task-1` |
| P52 | `phase-52.task-1` | registered_descriptors.c sub-page with Remove/View (optional) | implement | pending | `phase-51.task-1` |
| P53 | `phase-53.task-1` | Drop settings_get_default_policy() + wallet_set_policy() from key_confirmation.c | implement | pending | `phase-52.task-1` |
| P54 | `phase-54.task-1` | Remove settings_get_default_policy / settings_set_default_policy | implement | pending | `phase-53.task-1` |
| P55 | `phase-55.task-1` | Remove KEY_DEFAULT_POL constant | implement | pending | `phase-54.task-1` |
| P56 | `phase-56.task-1` | wallet.c: delete derive_address, derive_multisig_address helpers | implement | pending | `phase-55.task-1` |
| P57 | `phase-57.task-1` | wallet.c: simplify wallet_init(network) to network-record only | implement | pending | `phase-56.task-1` |
| P58 | `phase-58.task-1` | wallet.c: wallet_cleanup calls registry_clear() | implement | pending | `phase-57.task-1` |
| P59 | `phase-59.task-1` | wallet.c: delete statics (wallet_type/policy/account/derivation_path_buffer/loaded_descriptor/account_key) | implement | pending | `phase-58.task-1` |
| P60 | `phase-60.task-1` | wallet.h: delete wallet_policy_t enum | implement | pending | `phase-59.task-1` |
| P61 | `phase-61.task-1` | wallet.h: delete format_derivation_path/format_derivation_compact/get_derivation | implement | pending | `phase-60.task-1` |
| P62 | `phase-62.task-1` | wallet.h: delete get_account / set_account | implement | pending | `phase-61.task-1` |
| P63 | `phase-63.task-1` | wallet.h: delete get_receive_address / get_change_address / get_scriptpubkey | implement | pending | `phase-62.task-1` |
| P64 | `phase-64.task-1` | wallet.h: delete has_descriptor / load_descriptor / clear_descriptor | implement | pending | `phase-63.task-1` |
| P65 | `phase-65.task-1` | wallet.h: delete get_multisig_receive_address / get_multisig_change_address | implement | pending | `phase-64.task-1` |
| P66 | `phase-66.task-1` | wallet.h: delete get_policy / set_policy | implement | pending | `phase-65.task-1` |
| P67 | `phase-67.task-1` | Move BIP-380 checksum helper to descriptor_checksum.c (optional) | implement | pending | `phase-66.task-1` |
| P68 | `phase-68.task-1` | Final rg sweep for stragglers of the removed wallet_* API; migrate or delete | implement | pending | `phase-67.task-1` |
| P69 | `phase-69.task-1` | Remove dead tests covering deleted policy paths under main/core/test/ | implement | pending | `phase-68.task-1` |
| P70 | `phase-70.task-1` | Update repo-root ROADMAP.md to reflect new model | implement | pending | `phase-69.task-1` |
| P71 | `phase-71.task-1` | CHANGELOG entry for the rework | implement | pending | `phase-70.task-1` |
| P72 | `phase-72.task-1` | Device: clean builds on wave_4b, wave_35, wave_5 | implement | pending | `phase-71.task-1` |
| P73 | `phase-73.task-1` | Device: flash wave_35, store 3 plaintext descriptors, reboot, verify auto-load | implement | pending | `phase-72.task-1` |
| P74 | `phase-74.task-1` | Device: Addresses page per-source vs Sparrow references | implement | pending | `phase-73.task-1` |
| P75 | `phase-75.task-1` | Device: PSBT behavioural spec (every row of PLAN.md §Behavioural spec) | implement | pending | `phase-74.task-1` |
| P76 | `phase-76.task-1` | Device: Settings UI gone/added as expected; permissive toggle works | implement | pending | `phase-75.task-1` |
| P77 | `phase-77.task-1` | Device: Address checker known + random per source | implement | pending | `phase-76.task-1` |
| P78 | `phase-78.task-1` | Device: WARN-dialog gating on mismatched descriptor registration | implement | pending | `phase-77.task-1` |
