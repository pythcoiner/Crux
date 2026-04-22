# Descriptor rework — implementation roadmap

Detailed checklist for executing the rework described in `PLAN.md`. Each item
is intentionally fine-grained so progress can be tracked commit-by-commit.
Phases are ordered so that each phase leaves the tree buildable.

Legend:
- `[ ]` pending
- `[x]` done

---

## Phase 0 — scaffolding & CMake wiring

- [ ] Create `main/core/ss_whitelist.h` (empty skeleton with guard + include
      of `<stdbool.h>` / `<stddef.h>` / `<stdint.h>`).
- [ ] Create `main/core/ss_whitelist.c` (empty skeleton with
      `#include "ss_whitelist.h"`).
- [ ] Create `main/core/registry.h` (skeleton, include `storage.h` and
      `<wally_descriptor.h>`).
- [ ] Create `main/core/registry.c` (skeleton).
- [ ] Add all four new files to `main/CMakeLists.txt` `SRCS` list so they're
      compiled (keep the alphabetical order that file uses).
- [ ] Confirm clean build after scaffolding: `just build wave_4b` succeeds.

---

## Phase 1 — singlesig whitelist module (`ss_whitelist`)

### Types & constants

- [ ] Define `ss_script_type_t` enum (`P2PKH`, `P2SH_P2WPKH`, `P2WPKH`,
      `P2TR`).
- [ ] Define `ss_keypath_t` struct with `script`, `purpose`, `coin`,
      `account`, `chain`, `index`.
- [ ] Define constants: `SS_MAX_ACCOUNT = 100`, `SS_MAX_ADDR_INDEX = 100`,
      `MAX_KEYPATH_ORIGIN_DEPTH = 6`, `MAX_KEYPATH_TAIL_DEPTH = 2`,
      `MAX_KEYPATH_TOTAL_DEPTH = 8`.
- [ ] Add small inline helpers: `ss_is_hardened(u32)`, `ss_unharden(u32)`,
      `ss_u32_le(const unsigned char *)`.

### Parsing / whitelist check

- [ ] Implement `ss_keypath_parse(keypath_after_fp, keypath_len, out)`:
      validates length == 20 bytes (= 5 components), reads 5 `u32_le`,
      checks hardened pattern (first 3 hardened, last 2 not), fills
      `purpose / coin / account / chain / index` with unhardened values
      where applicable, sets `script` from purpose lookup.
- [ ] Implement `ss_keypath_is_whitelisted(kp, is_testnet)`: enforces
      purpose ∈ {44,49,84,86} (already done by parse), coin matches
      `is_testnet`, `account < SS_MAX_ACCOUNT`, `index < SS_MAX_ADDR_INDEX`,
      `chain ∈ {0,1}`.
- [ ] Implement `ss_keypath_format(kp, buf, buf_size)`: produces
      `m/<purpose>'/<coin>'/<account>'/<chain>/<index>` (uses `'` not `h`
      to match `key_get_derived_key` parser in `main/core/key.c:110-190`).

### Script regeneration / address derivation

- [ ] Implement `ss_scriptpubkey(script, account, chain, index, is_testnet,
      out, out_len)` dispatching per script type:
  - [ ] P2PKH: derive pubkey via `key_get_derived_key`, `hash160`,
        hand-build `OP_DUP OP_HASH160 <20> pkh OP_EQUALVERIFY OP_CHECKSIG`
        (25 bytes).
  - [ ] P2WPKH: `wally_witness_program_from_bytes(pubkey, 33,
        WALLY_SCRIPT_HASH160, …)` → 22-byte `OP_0 <20> pkh`.
  - [ ] P2SH_P2WPKH: build inner wpkh (22 bytes), compute hash160 of it,
        hand-build `OP_HASH160 <20> sh OP_EQUAL` (23 bytes).
  - [ ] P2TR: take compressed pubkey `[1..33]`, compute BIP341 tweak
        (no script tree) via `wally_ec_public_key_bip341_tweak` (or
        `wally_bip341_*`), hand-build `OP_1 <32> tweaked_xonly` (34 bytes).
- [ ] Implement `ss_address(script, account, chain, index, is_testnet,
      address_out)` using `ss_scriptpubkey` + the appropriate encoder:
  - [ ] P2WPKH / P2TR: `wally_addr_segwit_from_bytes` (hrp `bc`/`tb`).
  - [ ] P2PKH / P2SH_P2WPKH: `wally_scriptpubkey_to_address` with the
        right `WALLY_NETWORK_*` constant.
- [ ] Helper: for sh(wpkh), also return the 22-byte redeem script via
      a variant `ss_scriptpubkey_with_redeem(...)` so `claim_regenerate`
      can verify it against the PSBT's redeem-script field.

### Purpose / script binding helpers

- [ ] `purpose_script_binding_check_strict(purpose, outer_script_type)`
      → bool. Used by whitelist (implicit: parse already returns the
      script from the purpose map, so this is trivially true there; expose
      as a helper anyway for explicit gating by call sites).
- [ ] `purpose_script_binding_check_soft(descriptor)` →
      `{OK, WARN, NA}` enum:
  - Walks descriptor outer tokens via libwally to determine outer type.
  - Looks at our key's origin purpose (from `wally_descriptor_get_key_origin_path_str`).
  - Applies the rules from `PLAN.md` Purpose/script-type conventions table.
  - Returns `NA` when purpose ∉ {44,48,49,84,86}.

### Unit tests under `main/core/test/`

- [ ] `test_ss_whitelist_parse.c`:
  - [ ] Round-trips all four whitelisted purposes at account 0, index 0.
  - [ ] Rejects length != 20 bytes.
  - [ ] Rejects unhardened purpose / coin / account.
  - [ ] Rejects hardened chain / index.
  - [ ] Rejects unknown purpose (44 + 1 = 45, etc.).
- [ ] `test_ss_whitelist_is_whitelisted.c`:
  - [ ] Account 0..99 accepted; account 100 rejected.
  - [ ] Index 0..99 accepted; index 100 rejected.
  - [ ] Coin = 0 accepted on mainnet / rejected on testnet, and vice versa.
- [ ] `test_ss_whitelist_regen.c`:
  - [ ] For a fixed test mnemonic (defined in the test), regenerate each
        of the four script types at (account 0, chain 0, index 0) and
        compare to known-good scripts/addresses from Sparrow or
        `bitcoin-cli getdescriptorinfo` + `deriveaddresses`.

---

## Phase 2 — descriptor registry module (`registry`)

### Types

- [ ] Define `registry_entry_t` (id, loc, desc, my_key_index, num_paths,
      origin_path[6], origin_path_len).
- [ ] Choose static capacity for the in-memory registry (e.g. `#define
      REGISTRY_MAX_ENTRIES 16`). Array of `registry_entry_t *` in registry.c.

### Init / teardown

- [ ] `registry_init(is_testnet)`:
  - [ ] Enumerate `.txt` descriptors on `STORAGE_FLASH` via
        `storage_list_descriptors` → `item_list` with `.txt` ext filter.
  - [ ] Enumerate `.txt` descriptors on `STORAGE_SD`.
  - [ ] For each filename, `storage_load_descriptor` → `descriptor_str`.
  - [ ] Parse via `wally_descriptor_parse` with the correct network flag.
  - [ ] Find our-fingerprint key index via
        `wally_descriptor_get_key_origin_fingerprint` loop (reuse logic from
        `descriptor_validator.c:55-78`).
  - [ ] Extract our key's origin path as `uint32_t[]` via
        `wally_descriptor_get_key_origin_path_str` + `parse_derivation_path`
        (reuse helper in `key.c:110-190`).
  - [ ] Read `num_paths` via `wally_descriptor_get_num_paths`.
  - [ ] Append a `registry_entry_t` with cached fields.
  - [ ] Log count at INFO level: `ESP_LOGI(TAG, "Registry: %zu entries", …)`.
- [ ] `registry_clear()`: free each `desc` via `wally_descriptor_free`,
      zero the array, reset count.

### Accessors

- [ ] `registry_count()` — returns live count.
- [ ] `registry_get(i)` — bounds-checked pointer or NULL.
- [ ] `registry_find_by_id(id)` — linear scan.

### Matching

- [ ] `registry_match_keypath(keypath, keypath_len)`:
  - [ ] Validate `(keypath_len - 4) % 4 == 0` and total depth ≤ 8.
  - [ ] For each entry, byte-compare `origin_path_len * 4` bytes after the
        fingerprint against `entry.origin_path`.
  - [ ] Require `total_depth - origin_path_len == 2` (enforces `/<mp>/<ix>`
        suffix).
  - [ ] Enforce `mp ≤ 1` and `mp == 0` if `num_paths == 1`.
  - [ ] Reject hardened `mp` or `ix`.
- [ ] Add optional `start_index` form (or a stateful iterator) so callers
      can page past a false-positive prefix collision.

### Add / remove

- [ ] `registry_add_from_string(id, descriptor_str, loc, persist)`:
  - [ ] Parse descriptor (both networks; remember which succeeded).
  - [ ] Fail (return false) if our fingerprint is not in any key.
  - [ ] Fill a new `registry_entry_t` and append to the array.
  - [ ] If `persist`, write via `storage_save_descriptor(loc, id, bytes,
        len, /*encrypted=*/false)`.
- [ ] `registry_remove(id)`:
  - [ ] Locate entry; free `desc`; shift-remove from the array.
  - [ ] Also delete the `.txt` file via `storage_delete_descriptor`.

### Tests

- [ ] `test_registry_parse.c` — tests origin-path extraction on
      `wpkh(...)`, `wsh(sortedmulti(...))`, `tr(...)`, and a miniscript
      sample.
- [ ] `test_registry_match.c`:
  - [ ] Seed 3 registry entries with distinct origin paths.
  - [ ] Build a fake keypath matching entry #2 → match returns entry #2.
  - [ ] Unknown origin → NULL.
  - [ ] Non-matching trailing depth (1 or 3 components after origin) → NULL.
  - [ ] Hardened trailing → NULL.

---

## Phase 3 — settings (`main/core/settings.*`)

- [ ] Remove `KEY_DEFAULT_POL` constant (`settings.c:11`).
- [ ] Remove `settings_get_default_policy` / `settings_set_default_policy`
      (`settings.h:18-19`, `settings.c:48-65`).
- [ ] Add NVS key `KEY_PERMISSIVE_SIGNING = "perm_sign"`.
- [ ] Add `bool settings_get_permissive_signing(void)`; default false.
- [ ] Add `esp_err_t settings_set_permissive_signing(bool permissive)`.
- [ ] Update any call sites of the removed policy functions (expect
      `main/pages/shared/key_confirmation.c:32-34` and
      `main/pages/settings/wallet_settings.c`).

---

## Phase 4 — refactor `wallet.*`

### Header

- [ ] Remove `wallet_policy_t`.
- [ ] Remove: `wallet_format_derivation_path`, `wallet_format_derivation_compact`,
      `wallet_get_derivation`, `wallet_get_account`, `wallet_set_account`,
      `wallet_get_receive_address`, `wallet_get_change_address`,
      `wallet_get_scriptpubkey`, `wallet_get_policy`, `wallet_set_policy`,
      `wallet_has_descriptor`, `wallet_load_descriptor`,
      `wallet_clear_descriptor`, `wallet_get_multisig_receive_address`,
      `wallet_get_multisig_change_address`.
- [ ] Keep: `wallet_init`, `wallet_is_initialized`, `wallet_get_network`,
      `wallet_cleanup`, `wallet_unload`, `wallet_get_account_xpub` (may be
      called by UI for xpub-export at a specific whitelisted path — see
      Phase 9 notes; if no caller remains, remove it too).
- [ ] Keep `wallet_get_descriptor_string` / `wallet_get_descriptor_checksum`
      only if still needed for UI display of a specific registry entry; else
      move them to `registry.h` as per-entry helpers.

### Source

- [ ] Delete statics `wallet_type`, `wallet_policy`, `wallet_account`,
      `derivation_path_buffer`, `loaded_descriptor`, `account_key`.
- [ ] Delete helpers `derive_address`, `derive_multisig_address`.
- [ ] `wallet_init(network)`: just records `wallet_network` and sets
      `wallet_initialized = true`. Registry init is triggered elsewhere
      (Phase 8).
- [ ] `wallet_cleanup`: call `registry_clear()`.
- [ ] Retain the BIP-380 checksum helper (`desc_polymod`,
      `desc_compute_checksum`, …) — still used by descriptor-save UI and
      possibly for display of registered entries. Move to a small standalone
      `descriptor_checksum.c` if `wallet.c` becomes too thin.

---

## Phase 5 — PSBT classifier

New logic goes in `main/core/psbt.c`; header `psbt.h` grows new types.

### Header

- [ ] Define `claim_t` (CLAIM_WHITELIST | CLAIM_REGISTRY with union).
- [ ] Define `expected_scripts_t`.
- [ ] Define `input_ownership_t` (`owned`, `verified`, `claim`,
      `requires_ack`, raw keypath copy for permissive prompt).
- [ ] Define `output_ownership_t` (`owned`, `source` (claim)). **Do not**
      include an `is_change` field — the signer has no notion of
      change vs receive. UI code that needs to display the derivation
      reads it from `source` as raw coordinates.
- [ ] Declare: `psbt_classify_input`, `psbt_classify_output`,
      `claim_regenerate`, and their helpers `try_match_whitelist`,
      `try_match_registry`, `psbt_input_utxo_script`.

### Helpers

- [ ] `psbt_input_utxo_script(psbt, i, out, out_cap, out_len)`:
  - [ ] Try `wally_psbt_get_input_witness_utxo_alloc` first.
  - [ ] Fallback to `wally_psbt_get_input_utxo_alloc` + index into prevout.
  - [ ] Return false if neither present.
- [ ] `try_match_whitelist(keypath, keypath_len, is_testnet, claim_out)`
      — thin wrapper over `ss_keypath_parse` + `ss_keypath_is_whitelisted`.
- [ ] `try_match_registry(keypath, keypath_len, claim_out)` — thin
      wrapper over `registry_match_keypath` that paginates through
      duplicates (takes a `size_t *cursor`).

### `claim_regenerate`

- [ ] Whitelist branch: calls `ss_scriptpubkey_with_redeem` and fills
      `expected_scripts_t`. P2TR: spk only; P2SH_P2WPKH: spk + redeem;
      others: spk only.
- [ ] Registry branch:
  - [ ] `wally_descriptor_to_script` at depth 0 → `spk`.
  - [ ] If outer is `wsh(...)`: depth 1 → `witness` script.
  - [ ] If outer is `sh(wsh(...))`: depth 1 → `redeem` (the p2wsh wrapper
        itself = `OP_0 <32> sha256(witness)`), depth 2 → `witness`.
  - [ ] If outer is `sh(multi(...))` or `sh(sortedmulti(...))` (non-nested):
        depth 1 → `redeem` (the bare multisig witness-less script).
  - [ ] Otherwise: spk only.
- [ ] Unit-test `claim_regenerate` against each of these shapes using a
      known mnemonic + descriptor + known scripts.

### `psbt_classify_input`

- [ ] Extract UTXO script first; if absent, return NOT_OURS.
- [ ] For each keypath matching our fingerprint, enumerate candidate claims
      (whitelist → registry, with pagination).
- [ ] For each claim, regenerate and compare to UTXO script.
- [ ] If sh(...) family: also byte-compare redeem vs
      `wally_psbt_get_input_redeem_script`.
- [ ] If wsh(...) family: also byte-compare witness vs
      `wally_psbt_get_input_witness_script`.
- [ ] If no verified claim but fp was seen: if permissive setting is on,
      return `verified=false, requires_ack=true` with raw keypaths copied
      into the result for the UI; else NOT_OURS.

### `psbt_classify_output`

- [ ] Output script comes from `wally_psbt_get_global_tx_alloc` →
      `tx->outputs[i].script` (same as today in `psbt.c:598-599`).
- [ ] Same enumerate-claims-and-verify loop as input, but no UTXO extraction
      and no extra redeem/witness check (outputs in a PSBT don't carry
      those; verification against the spk is sufficient to decide
      ownership).
- [ ] On a verified match, return `owned=true` with the claim. The
      review UI can render the derivation path from the claim for display,
      but the classifier itself does not tag the output as "change" or
      "receive".

### Tests

- [ ] Given a constructed PSBT fixture (hex blob + expected classification
      per input/output), run the classifiers and compare.
  - [ ] Fixture A: BIP84 receive + BIP84 change.
  - [ ] Fixture B: BIP86 taproot receive + non-ours external.
  - [ ] Fixture C: wsh-multisig registered descriptor, 2-of-3.
  - [ ] Fixture D: attacker PSBT with correct keypath but swapped UTXO
        script — must NOT be marked as ours.
  - [ ] Fixture E: fp-only match with unknown path, permissive=off → NOT_OURS.

---

## Phase 6 — PSBT signing loop rewrite

In `psbt.c`:

- [ ] Replace the body of `psbt_sign` (`psbt.c:258-357`) with a loop over
      inputs that calls `psbt_classify_input` and signs when `owned`.
- [ ] When `verified=true`: derive key at the claim's full path
      (`ss_keypath_format` or registry path formatter) and call
      `wally_psbt_sign` with `EC_FLAG_GRIND_R`.
- [ ] When `verified=false, requires_ack=true`: invoke a UI callback
      (function pointer passed to `psbt_sign` or a context struct) that
      blocks for user ACK; if confirmed, derive at the raw keypath and
      sign. Otherwise skip.
- [ ] Self-cosign edge case: keep a list of verified claims per input and
      call `wally_psbt_sign` once per claim's derived key.
- [ ] Delete the inline BIP84/BIP48 branches (`psbt.c:295-334`).
- [ ] Delete `psbt_get_output_derivation` (`psbt.c:202-256`) once all
      call sites are migrated.
- [ ] Delete `psbt_verify_output_with_descriptor` (`psbt.c:523-635`) once
      all call sites are migrated.
- [ ] Consider deleting `psbt_is_multisig` (`psbt.c:489-521`): either keep
      as a convenience, or replace call sites with
      `psbt_classify_input(...).claim.kind == CLAIM_REGISTRY`.

---

## Phase 7 — descriptor validator cleanup

In `main/core/descriptor_validator.{h,c}`:

- [ ] Delete `apply_changes_and_verify` (lines 350-386).
- [ ] Delete `check_attributes_and_verify` (lines 400-492) — everything
      after the fingerprint check.
- [ ] Delete fields `target_network`, `target_policy`, `target_account`,
      `needs_*_change` from `validation_context_t` (lines 21-26).
- [ ] Delete `parse_origin_path` helper (lines 80-143) — no longer needed.
- [ ] Keep `find_matching_key_index`, `extract_xpub_from_key`,
      `parse_multisig_threshold`, `extract_descriptor_info`,
      `verify_xpub_and_show_info`, `info_confirm_proceed`.
- [ ] In `descriptor_validate_and_load`: after the fingerprint stage, go
      straight to `verify_xpub_and_show_info` (skip attribute check).
- [ ] In `info_confirm_proceed`: replace `wallet_load_descriptor(…)` with
      `registry_add_from_string(<id-chosen-via-UI>, descriptor_str, loc,
      /*persist=*/true)`.
  - [ ] The ID prompt is currently in `store_descriptor.c`; move or share
        that flow so the validator can ask for an ID right after
        info-confirm.
- [ ] Add `purpose_script_binding_check_soft` call between xpub verify and
      info-confirm; if `WARN`, pop a `dialog_show_danger_confirm` with the
      "unusual combination" message; user's response gates whether we
      reach `info_confirm_proceed`.

---

## Phase 8 — boot wiring

In `main/pages/shared/key_confirmation.c` (lines 25-46):

- [ ] Delete the `settings_get_default_policy()` call and
      `wallet_set_policy(...)`.
- [ ] After `wallet_init(net)`, call `registry_init(is_testnet)`.
- [ ] Log a line naming the registry count so that device logs confirm the
      auto-load worked.

In `main/main.c` (if it has any policy-related init): no change expected,
but audit.

---

## Phase 9 — UI: wallet settings page

In `main/pages/settings/wallet_settings.c`:

- [ ] Remove `policy_dropdown` UI element (declared line 26, used lines
      246-256) and all handlers.
- [ ] Remove the account spinner (see line ~47 + save handler).
- [ ] Remove the derivation-path preview label that tracks policy/account.
- [ ] Add a "Permissive signing" toggle, wired to
      `settings_get_permissive_signing` (initial value) and
      `settings_set_permissive_signing` (on change).
- [ ] Label it with a short warning: "Allow signing for unknown derivation
      paths after on-screen confirmation. Reduces safety."
- [ ] Adjust `update_apply_button_state` now that only network / brightness
      / permissive can change.

Registered descriptors sub-page (optional but recommended):

- [ ] Create `main/pages/settings/registered_descriptors.c` + header.
- [ ] List rows: one per `registry_get(i)`. Show `id` and a short script-
      type badge (wpkh / tr / wsh-multi / …).
- [ ] On row tap: show detail dialog with the descriptor string (via a new
      `registry_entry_to_string` that wraps `wally_descriptor_canonicalize`
      + the existing BIP-380 checksum helper).
- [ ] "Remove" button in detail view → `registry_remove(id)`; close page.
- [ ] Add an entry on wallet_settings page linking into this sub-page.

---

## Phase 10 — UI: addresses page source picker

In `main/pages/home/addresses.c`:

- [ ] Replace `type_dropdown` (declared line 27) with a **source** dropdown
      listing `[Native SegWit, Taproot, Legacy, Wrapped SegWit, …registry
      entries…]`. Populate registry entries from `registry_count()` /
      `registry_get(i)->id`.
- [ ] When source is a singlesig type: show an inline account input
      (0..99). Default 0, remembered within the session only.
- [ ] When source is a registered descriptor: account input is hidden;
      receive/change pagination works via `wally_descriptor_to_address`
      (or a helper `registry_entry_address(entry, mp, ix, &addr)`).
- [ ] Replace calls to `wallet_get_receive_address` / `wallet_get_change_address`
      in `refresh_address_list` (lines 313-344) with the dispatcher above.
- [ ] Remove the "descriptor required" empty state at lines 316-324 — now
      every source has something to show; if the registry is empty, the
      dropdown just doesn't list those entries.
- [ ] Keep the "Load descriptor" button but rename it "Register
      descriptor" and have it feed back into `descriptor_loader` → the
      registration flow from Phase 7.

---

## Phase 11 — UI: address checker

In `main/pages/shared/address_checker.c`:

- [ ] Add the same source picker at the top of the page.
- [ ] In `address_checker_check` (lines 102-147), once the user enters an
      address, sweep within the selected source only. Reuse the 50-per-page
      scheme; page button adds 50 more.
- [ ] For singlesig source: also iterate over `account` 0..SS_MAX_ACCOUNT-1?
      — **decision**: stick to the current account selected in the picker,
      as the user knows which account they want to check. Document that.
- [ ] For registered descriptor source: iterate `multi_index ∈ {0, 1}` ×
      `child_num ∈ [start, start+49]`.

---

## Phase 12 — UI: descriptor load / save glue

`main/pages/store_descriptor.c`:

- [ ] After a successful plaintext save (both the `do_save_plaintext`
      path and the `.kef` save path on the plaintext branch), call
      `registry_add_from_string(id, descriptor_text, target_location,
      /*persist=*/false)`. Persist is already done by the save itself.
- [ ] If `registry_add_from_string` returns false, log but continue (the
      file is saved even if in-memory registry didn't accept it — next
      boot will re-try via `registry_init`).

`main/pages/load_descriptor_storage.c`:

- [ ] After a successful `.kef` decrypt (`success_from_kef_decrypt`), call
      `registry_add_from_string` so the decrypted descriptor becomes
      active this session.
- [ ] After a successful plaintext load (`load_selected`'s plaintext
      branch), also add to the registry (paranoia; normally it's already
      there from `registry_init`).
- [ ] On successful add, the "success" dialog can read "Registered (this
      session)" for `.kef` entries so the user understands it's not
      persistent as registered-plaintext.

`main/pages/shared/descriptor_loader.c`: no functional change, but check
that the flow still makes sense after Phase 7's validator changes.

---

## Phase 13 — remove old single-descriptor in-memory state

- [ ] Grep the codebase for remaining callers of the old wallet-descriptor
      API that were missed:
  ```
  rg -n 'wallet_has_descriptor|wallet_load_descriptor|wallet_clear_descriptor|wallet_get_multisig_|wallet_get_receive_address|wallet_get_change_address|wallet_get_scriptpubkey|wallet_get_policy|wallet_set_policy|wallet_get_account|wallet_set_account|wallet_format_derivation|wallet_get_derivation'
  ```
- [ ] Migrate each hit to the new API (registry / ss_whitelist), or delete
      if the surrounding feature is dead.
- [ ] Ensure the code compiles cleanly with `-Wunused-function` and
      `-Wunused-variable` in `main/CMakeLists.txt` (ESP-IDF default).

---

## Phase 14 — tests under `main/core/test/`

All unit-test files go under `main/core/test/` and are registered via the
existing test CMake wiring (add each new `.c` to the `SRCS` in that
sub-CMakeLists).

- [ ] `test_ss_whitelist_parse.c` (Phase 1).
- [ ] `test_ss_whitelist_is_whitelisted.c` (Phase 1).
- [ ] `test_ss_whitelist_regen.c` (Phase 1).
- [ ] `test_registry_parse.c` (Phase 2).
- [ ] `test_registry_match.c` (Phase 2).
- [ ] `test_purpose_binding.c` (Phase 1 helper): `OK` / `WARN` / `NA`
      coverage per the table.
- [ ] `test_psbt_classify.c` (Phase 5): the five fixtures above.

Reference-generate expected bytes via `bitcoin-cli getdescriptorinfo` and
`bitcoin-cli deriveaddresses` on a throwaway mnemonic, commit the expected
values as hex constants in each test.

---

## Phase 15 — device verification

Run on all three targets: `wave_4b`, `wave_35`, `wave_5`.

- [ ] `just build wave_4b` (and `wave_35`, `wave_5`) — clean builds.
- [ ] `just flash wave_35` and boot with a test mnemonic.
- [ ] Store 3 plaintext descriptors:
  - [ ] `wpkh([fp/84'/0'/0']xpub.../<0;1>/*)#cksum`
  - [ ] `tr([fp/86'/0'/0']xpub.../<0;1>/*)#cksum`
  - [ ] `wsh(sortedmulti(2,[fp/48'/0'/0'/2']xpub.../<0;1>/*,[fp2/48'/0'/0'/2']xpub.../<0;1>/*))#cksum`
- [ ] Reboot; open "Registered descriptors" — all three present without
      any load action.
- [ ] Open the Addresses page; switch through each source:
  - [ ] Native SegWit account 0 shows the same address as Sparrow at
        `m/84'/0'/0'/0/0`.
  - [ ] Taproot account 0 shows the same address as Sparrow at
        `m/86'/0'/0'/0/0`.
  - [ ] The wsh multisig registered source shows the expected 2-of-2
        address.
- [ ] Scan PSBTs built offline:
  - [ ] BIP84 account 3 → signs.
  - [ ] BIP86 taproot → signs.
  - [ ] BIP44 account 100 → refused (account out of range).
  - [ ] BIP84 index 100 → refused (index out of range).
  - [ ] Registered wsh multisig → signs.
  - [ ] Attacker PSBT with mismatched UTXO script → refused silently (no
        signature added, user sees "0 signatures added" on the review
        screen).
  - [ ] Unknown path + permissive=off → refused.
  - [ ] Unknown path + permissive=on → ACK prompt; sign after confirm.
- [ ] Settings page: verify no policy / account spinner, permissive toggle
      present and default off.
- [ ] Address checker: paste a known Sparrow-generated address at
      `m/84'/0'/2'/0/5` (account 2 source) — "Receive #5" found. Paste
      a random mainnet address — "Not found".
- [ ] Try to register a mismatched descriptor (e.g. `tr([fp/84'/0'/0']xpub...)`)
      and confirm the WARN dialog appears. Registering anyway should add
      it to the registry; it should sign PSBTs that reference it.

---

## Cleanup & housekeeping

- [ ] Remove/rename old tests under `main/core/test/` that cover the dead
      code (policy-based derivation paths, the old `wallet_get_*` API).
- [ ] Update `ROADMAP.md` in the repo root (`/ROADMAP.md`), if present, to
      reflect the new model.
- [ ] Update `docs/` screenshots if any show the old policy dropdown or
      account spinner.
- [ ] Cut a CHANGELOG entry describing the rework (user-facing: "no more
      policy selection; any whitelisted BIP44/49/84/86 account is accepted;
      registered descriptors auto-load at boot").
- [ ] Optional: add a migration note for users who had a non-zero account
      in settings (their PSBTs still work — account is now inferred from
      the PSBT).
