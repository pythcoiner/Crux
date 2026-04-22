# Rework descriptor & derivation-path management

Code-free overview. All interfaces, structs and pseudocode live in
[SNIP.md](./SNIP.md); the plan references them by anchor ("see
[SNIP 01](./SNIP.md#snip-01--ss_whitelisth-interface)" and so on).

Step-by-step execution is tracked in [ROADMAP.md](./ROADMAP.md).

---

## Context

Today's signer forces the user to pick a **policy** (singlesig or multisig)
before it will do anything. The policy is a global setting (`wallet_policy_t`
in `main/core/wallet.h:17-20`, persisted in NVS under key `"def_pol"` in
`main/core/settings.c`) and it gates:

- the derivation path used to derive the account key — hardcoded
  `m/84'/c'/a'` for singlesig and `m/48'/c'/a'/2'` for multisig
  (`wallet.c:26-45`),
- the only script types the signer recognises,
- which address-generation function the Addresses page calls
  (`pages/home/addresses.c:313-344`),
- the rules the PSBT signer applies when deciding "is this input ours?"
  (`psbt.c:295-334`) — it requires `purpose ∈ {84, 48}`, the hardcoded coin
  type, and `account == wallet_get_account()`,
- the rules for "is this output ours?" — same shape in `psbt.c:202-256`
  (singlesig) and `psbt.c:523-635` (multisig, which additionally requires a
  descriptor to have been loaded manually).

Two bad consequences:

1. A singlesig user with standard HD wallet structure (multiple accounts,
   BIP84/BIP49/BIP86, …) is locked to **one** path per session and must
   change settings to sign anything else.
2. A multisig user must manually load **one** descriptor per session; the
   device has no concept of a persistent "registered" set.

### Goal

Replace the policy-gated model with:

- **Singlesig whitelist** that mirrors the Ledger Bitcoin app
  (`app-bitcoin-new`):
  - script types `pkh` (BIP44), `sh(wpkh)` (BIP49), `wpkh` (BIP84), single-key
    `tr` (BIP86);
  - origin path **exactly** `m/purpose'/coin'/account'` (3 hardened components);
    purpose matches script type, coin ∈ {`0'` mainnet, `1'` testnet},
    account hardened in `0'..100'`;
  - script suffix `/<0;1>/*`, address index unhardened, index < 100
    (stricter than Ledger's 50 000 cap — we mirror the account bound).
  - **No** user-selected account — any account in the range is accepted.
- **Descriptor registry**: all plaintext `.txt` descriptors on flash + SD are
  auto-parsed into an in-memory registry at boot (after the mnemonic is
  unlocked). KEF-encrypted `.kef` descriptors keep today's explicit-load flow.
- **Address verification**: registered descriptors + whitelist-derivable
  singlesig paths both contribute to ownership checks and change/receive
  regeneration.
- **Unknown-path default = refuse**, with a settings toggle for a permissive
  mode that instead shows keypath info for each unexplained input/output and
  asks the user to ACK per signature.

### Phase-2 follow-up (not implemented in this rework)

- Replace `.kef` descriptor envelopes with BIP-1951 (bitcoin/bips PR 1951)
  encrypted descriptors, keyed from the mnemonic, so the boot flow can
  auto-decrypt and register them too.

---

## Target architecture

### New module: derivation whitelist — `main/core/ss_whitelist.{h,c}`

Interface, constants, and function signatures:
**[SNIP 01](./SNIP.md#snip-01--ss_whitelisth-interface)**.

Reuses `key_get_derived_key()` (`key.c:286-301`),
`wally_witness_program_from_bytes`, `wally_addr_segwit_from_bytes`,
`wally_address_to_scriptpubkey`, and for taproot
`wally_ec_public_key_from_private_key` + `wally_bip341_*` libwally helpers.

### New module: descriptor registry — `main/core/registry.{h,c}`

Replaces the single `static struct wally_descriptor *loaded_descriptor` in
`wallet.c:24`. Interface: **[SNIP 02](./SNIP.md#snip-02--registryh-interface)**.

### Refactored `wallet.h`

Removes: `wallet_policy_t`, `wallet_get_policy`, `wallet_set_policy`,
`wallet_format_derivation_path`, `wallet_format_derivation_compact`,
`wallet_get_account`, `wallet_set_account`, `wallet_get_derivation`,
`wallet_get_receive_address`, `wallet_get_change_address`,
`wallet_get_scriptpubkey`, `wallet_has_descriptor`, `wallet_load_descriptor`,
`wallet_clear_descriptor`, `wallet_get_descriptor_string`,
`wallet_get_descriptor_checksum`, `wallet_get_multisig_receive_address`,
`wallet_get_multisig_change_address`.

Keep / new: **[SNIP 03](./SNIP.md#snip-03--walleth-after-shrinking)**.

All address/scriptPubKey/derivation queries move to `ss_whitelist` or the
registry. `wallet.c` becomes a thin shell over those two, plus the BIP-380
checksum helper (kept as-is for descriptor registration UI).

### Settings — `main/core/settings.{h,c}`

Drop `settings_get_default_policy` / `settings_set_default_policy`. New API:
**[SNIP 04](./SNIP.md#snip-04--settingsh-additions)**.

---

## Ownership methodology

This is the core of the rework. Every sign/verify decision routes through
this algorithm. The four-part principle:

1. **Match** — a PSBT keypath is "recognised" only if it fits either the
   strict singlesig whitelist shape or a registered descriptor's origin
   prefix (for our fingerprint).
2. **Purpose/script binding (whitelist only, hard-enforced)** — for the
   singlesig whitelist, the BIP32 purpose in the origin is what *selects*
   the expected script type via a fixed lookup table (44→pkh, 49→sh(wpkh),
   84→wpkh, 86→tr). Mismatch is impossible by construction. For **registered
   descriptors** this is a **soft convention only**: a descriptor whose
   origin purpose doesn't match its outer script (e.g. `wsh(sortedmulti(...,
   [fp/86'/0'/0']xpub, ...))`) is still registrable, but registration shows
   a warning dialog so the user can confirm or cancel. The regenerate+verify
   step (principle #4) already guarantees correctness at sign time regardless
   of purpose convention.
3. **Regenerate** — we re-derive the expected script (scriptPubKey and, where
   applicable, redeemScript / witnessScript) from the claim.
4. **Verify** — the regenerated script must byte-equal what's in the PSBT.
   A keypath alone is never enough — this defeats any attempt to swap the
   UTXO / output script under a correct-looking keypath.

The signer classifies each input as sign-or-refuse and each output as
owned-or-external, nothing more. **There is no "change vs receive"
distinction at the signer layer** — that convention belongs to the wallet
UX (Addresses page), not to the signing or verification flow. The chain /
multi-index component of a claim is surfaced to the review UI only as raw
derivation metadata alongside the amount.

### Purpose ↔ script-type conventions

| Purpose | Conventional outer script                    | Whitelist                 | Registry         |
|--------:|----------------------------------------------|---------------------------|------------------|
|      44 | `pkh(...)`                                   | Enforced                  | Warn on mismatch |
|      48 | `wsh(sortedmulti)` or `sh(wsh(sortedmulti))` | N/A (4-component origin)  | Warn on mismatch |
|      49 | `sh(wpkh(...))`                              | Enforced                  | Warn on mismatch |
|      84 | `wpkh(...)`                                  | Enforced                  | Warn on mismatch |
|      86 | `tr(...)` single-key, no script tree         | Enforced                  | Warn on mismatch |
|   other | any (custom miniscript, etc.)                | Not a whitelist candidate | No warning       |

Note on BIP48: origin's 4th hardened component (`script_type`) is `1'` for
the `sh(wsh(...))` variant and `2'` for plain `wsh(...)`. Both forms are
permitted by the convention row above.

Codified as:

- `purpose_script_binding_check_strict(purpose, descriptor_outer_type)` —
  boolean, used by `try_match_whitelist`. Failure ⇒ no claim.
- `purpose_script_binding_check_soft(descriptor)` — returns
  `{OK, WARN, NA}`. Used by the registration UI: on `WARN`, a dialog like
  "This descriptor uses a purpose-86 origin under a `wsh` script. This is
  unusual. Register anyway?" gates whether the entry is added.

### Terminology

- **Keypath (PSBT)**: 4 fingerprint bytes + N little-endian u32 BIP32
  components (hardened bit = top bit). Libwally's
  `wally_psbt_get_input_keypath` / `wally_psbt_get_output_keypath` deliver
  the bytes; we read components at offsets 4, 8, 12, … .
- **Source**: what explains a keypath.
  - *Whitelist source* = one of the four `ss_script_type_t` + (account,
    chain, index).
  - *Registry source* = a `registry_entry_t` + (multi_index, child_num).
- **Claim**: (source, derived path, expected script type). A claim is
  candidate ownership — not yet verified.
- **Verified claim**: a claim whose regenerated script(s) match the PSBT's.

### Helpers and algorithm

- Types and function signatures: **[SNIP 05](./SNIP.md#snip-05--psbt-helpers-types-and-function-declarations)**.
- `try_match_whitelist` algorithm: **[SNIP 06](./SNIP.md#snip-06--try_match_whitelist-algorithm)**.
- `try_match_registry` algorithm: **[SNIP 07](./SNIP.md#snip-07--try_match_registry-algorithm)**.
- `claim_regenerate` per script type: **[SNIP 08](./SNIP.md#snip-08--claim_regenerate-per-script-type)**.
- Input classifier `psbt_classify_input`: **[SNIP 09](./SNIP.md#snip-09--psbt_classify_input)**.
- Signing loop replacing `psbt_sign` body: **[SNIP 10](./SNIP.md#snip-10--signing-loop-replaces-psbt_sign-body)**.
- Output classifier `psbt_classify_output`: **[SNIP 11](./SNIP.md#snip-11--psbt_classify_output)**.

### Replaces in `psbt.c`

| Old                                                     | New                                                  |
|---------------------------------------------------------|------------------------------------------------------|
| `psbt_get_output_derivation` (psbt.c:202-256)           | `psbt_classify_output` using the unified algorithm   |
| `psbt_verify_output_with_descriptor` (psbt.c:523-635)   | Folded into `psbt_classify_output`'s registry branch |
| `psbt_is_multisig` (psbt.c:489-521)                     | Optional; use `claim.kind == CLAIM_REGISTRY`         |
| `psbt_sign`'s BIP84/BIP48 inline logic (psbt.c:295-334) | Driven by `classify_input`                           |

### Why this is safe

- An attacker who crafts a PSBT with a correct-looking BIP32 keypath but a
  swapped UTXO / output script cannot fool the device: `claim_regenerate`
  + byte-equal `utxo_script` / `out_script` detects the mismatch.
- An attacker who crafts an unknown path hoping the user will ACK it
  in permissive mode sees the raw path in the review screen — no hidden
  derivation.
- Fingerprint collisions do not matter: whichever keypath/claim verifies,
  verifies for our actual key.
- For multisig/miniscript the verification covers not just the outer
  scriptPubKey but also the inner redeem-/witness-script, so a quorum
  substitution attack is rejected.
- **Purpose/script-type mismatches are impossible** in the whitelist (the
  lookup table is authoritative). For registered descriptors the convention
  is not hard-enforced — a user *can* register an unusual combination after
  acknowledging a warning — but the regenerate+verify step still catches
  any attempt to sign for a script that doesn't match the descriptor's
  derivation at the claimed indices. The warning is a UX safeguard, not a
  security boundary.

---

## UI changes

### `pages/settings/wallet_settings.c`

Remove: policy dropdown (`wallet_settings.c:26, 246-256`), account spinner
(line ~47), and the derivation-path preview logic tied to policy.

Add: a "Permissive signing" toggle wired to
`settings_{get,set}_permissive_signing`, with a clear warning label.

Add a sub-page (or entry) "Registered descriptors" that lists
`registry_get(i)->id` for each in-memory entry, with "Remove" and "View"
actions. Tapping an entry opens a read-only view similar to today's
descriptor info dialog.

### `pages/home/addresses.c` + `pages/shared/address_checker.c`

Add a **source picker** as the top selector on both pages:

- "Native SegWit" → `SS_SCRIPT_P2WPKH`, asks for account (0..99).
- "Taproot" → `SS_SCRIPT_P2TR`, asks for account.
- "Legacy" → `SS_SCRIPT_P2PKH`, asks for account.
- "Wrapped SegWit" → `SS_SCRIPT_P2SH_P2WPKH`, asks for account.
- One entry per registered descriptor (label = registry id).

Within the selected source, today's receive/change pagination is reused
**for address display only** (browsing addresses as a user). The signing
flow does not use this distinction — see the note in the ownership
methodology. Existing calls to `wallet_get_{receive,change}_address()` and
`wallet_get_multisig_{receive,change}_address()` are replaced with
`ss_address(...)` or `wally_descriptor_to_address(entry->desc, ...)`.

`address_checker_check()` (`address_checker.c:102-147`) keeps today's
50-per-page sweep logic but sweeps only inside the user-chosen source.

### Descriptor load/save flow

- `pages/store_descriptor.c`: unchanged save flow. After a successful
  plaintext save, call `registry_add_from_string(id, str, loc, false)` so the
  just-saved descriptor is immediately active (no reboot required).
- `pages/load_descriptor_storage.c`: for `.kef` files, the post-decrypt
  success callback calls `registry_add_from_string(id, str, loc, false)` —
  encrypted descriptors still need the explicit load per session, but once
  loaded they join the active registry alongside the auto-loaded plaintext
  ones.
- `pages/shared/descriptor_loader.c` / `core/descriptor_validator.c`: the
  "attribute change confirmation" dialog (mismatched policy/account/network)
  in `descriptor_validator.c:401-492` is deleted — there is no longer a
  "current policy" to mismatch against. Network mismatch (mainnet vs testnet)
  is kept and still triggers the confirm flow.

### Boot wiring

`pages/shared/key_confirmation.c:25-46` (post-mnemonic handler): drop the
policy load and call `registry_init` after `wallet_init`. Before/after
diff: **[SNIP 12](./SNIP.md#snip-12--boot-wiring-beforeafter)**.

---

## Files to modify / add

**New**
- `main/core/ss_whitelist.h`, `ss_whitelist.c`
- `main/core/registry.h`, `registry.c`
- (optional) `main/pages/settings/registered_descriptors.c` + header
- Tests under `main/core/test/` for `ss_whitelist` parse/format and
  `registry_match_keypath`.

**Modified**
- `main/core/wallet.h`, `wallet.c` — delete policy + hardcoded-path API;
  keep network/init/cleanup; keep BIP-380 checksum helper.
- `main/core/psbt.c` — rewrite `psbt_sign` signing loop (`psbt.c:258-357`),
  merge `psbt_get_output_derivation` (`psbt.c:202-256`) and
  `psbt_verify_output_with_descriptor` (`psbt.c:523-635`) into a single
  whitelist-or-registry classifier. `psbt_is_multisig` (`psbt.c:489-521`) may
  be removed — call sites should switch to querying the registry entry that
  matched.
- `main/core/settings.h`, `settings.c` — drop `def_pol`; add
  `permissive_signing`.
- `main/core/descriptor_validator.c` — delete policy-mismatch path
  (`check_attributes_and_verify`, `apply_changes_and_verify`, related state
  fields in `validation_context_t`); keep fingerprint + xpub verification;
  call `registry_add_from_string` on info-confirm.
- `main/pages/settings/wallet_settings.c` — remove policy dropdown, remove
  account spinner; add permissive-signing toggle.
- `main/pages/home/addresses.c` — replace `type_dropdown` with source picker
  covering SS script types + registry entries; adjust `refresh_address_list`
  to dispatch to `ss_address` or `wally_descriptor_to_address`.
- `main/pages/shared/address_checker.c` — same source-picker pattern; sweep
  within the chosen source only.
- `main/pages/shared/key_confirmation.c:25-46` — drop policy load, call
  `registry_init` after `wallet_init`.
- `main/pages/store_descriptor.c` and `load_descriptor_storage.c` — call
  `registry_add_from_string` after a successful save / decrypt so the new
  descriptor is immediately active this session.
- `main/core/psbt.h` — update signatures to reflect merged output classifier.

**Unchanged** (reused as-is)
- `main/core/storage.c/h` — directory layout, save/load/list APIs.
- `main/core/key.c/h` — `key_get_derived_key`, `key_get_fingerprint`.
- libwally usage (same set already cataloged: `wally_descriptor_parse`,
  `wally_descriptor_to_address`, `wally_descriptor_get_num_paths`, BIP32
  helpers, address encoders).

---

## Behavioural spec (acceptance criteria)

Written as a list because some cells are too wide for a column-aligned
table to remain readable in a plain-text editor.

### Signing

- PSBT input keypath `m/84'/0'/3'/0/12`, fingerprint matches, mainnet —
  **sign** (account 3, not 0).
- PSBT input keypath `m/86'/0'/0'/1/4`, fingerprint matches — **sign**
  (taproot).
- PSBT input keypath `m/44'/0'/100'/0/0` — **refuse** (account ≥ 100).
- PSBT input keypath `m/84'/0'/0'/0/100` — **refuse** (index ≥ 100).
- PSBT input keypath matches a registered `wsh(sortedmulti(2,...))` origin
  — **sign** using that descriptor.
- PSBT input keypath non-standard (e.g. `m/9999'/0'/0'/0/0`), fingerprint
  matches, permissive=off — **skip** (signature count stays at 0 for that
  input).
- Same, permissive=on — user is prompted to ACK with keypath info; sign
  if confirmed.

### Output classification

- Output with a whitelist-matching keypath and scriptPubKey that matches
  regeneration — marked **owned**; full derivation path shown next to
  the amount. No "change/receive" label.
- Output whose keypath matches a registered descriptor and whose script
  matches — same: owned, path displayed.
- Output whose fingerprint matches ours but neither the whitelist nor any
  registered descriptor explain it — **not** marked as owned (treated as
  external destination). The old fingerprint-only fallback is removed.

### Descriptor registration

- Register `wsh(sortedmulti(2,[fp/86'/0'/0']xpub,...))` — warning
  ("purpose 86 under wsh is unusual"); registered iff user confirms.
- Register `tr([fp/84'/0'/0']xpub)` — warning ("purpose 84 under tr is
  unusual"); registered iff user confirms.
- Register `wpkh([fp/99'/0'/0']xpub)` — no warning (custom purpose);
  registered.

### Persistence

- After wiping flash and rebooting with 3 plaintext descriptors stored:
  `registry_count() == 3` without any user action.
- A `.kef` descriptor on disk is not auto-loaded; it's still loadable via
  today's page, and once loaded this session it joins the registry until
  reboot.

### UI

- Settings page: no policy dropdown, no account spinner. "Permissive
  signing" toggle present, default off.
- Addresses page: source picker with 4 singlesig entries plus one entry
  per registered descriptor. Picking "Native SegWit" + account 2 shows
  `m/84'/coin'/2'/0/0..7`.

---

## Verification plan

1. **Build**: `just build wave_4b`, `just build wave_35`, `just build wave_5`
   all succeed.
2. **Unit tests** (add under `main/core/test/`):
   - `ss_keypath_parse` round-trips `m/{44,49,84,86}'/0'/0'/0/0` and rejects
     lengths ≠ 5, unhardened purpose/coin/account, hardened chain/index.
   - `ss_keypath_is_whitelisted` rejects account ≥ 100, index ≥ 100,
     wrong coin type vs testnet flag, unknown purpose.
   - `registry_match_keypath` returns the correct entry when multiple
     registered descriptors are present; returns NULL when none match.
   - `purpose_script_binding_check_soft` returns `WARN` for
     `wsh(sortedmulti(2,[fp/86'/0'/0']xpub...))` and `tr([fp/84'/0'/0']xpub)`,
     returns `OK` for `wpkh([fp/84'/0'/0']xpub)`, returns `NA` for
     `wpkh([fp/99'/0'/0']xpub)` (non-standard purpose).
   - `registry_add_from_string` accepts all three regardless (no
     mismatch-based rejection); UI is responsible for the WARN dialog.
3. **Simulator / device integration**:
   - Flash (`just flash`) to wave_35.
   - With a known mnemonic: store plaintext descriptors
     `wpkh([fp/84'/0'/0']xpub.../<0;1>/*)`, `tr(...)`, and
     `wsh(sortedmulti(2,[fp/48'/0'/0'/2']xpub,[fp2/…]xpub))`.
   - Reboot. Confirm "Registered descriptors" page lists all three without
     any load action.
4. **PSBT signing**:
   - Craft (offline, e.g. via Sparrow or `bitcoin-cli`) PSBTs exercising each
     row of the behavioural-spec table and scan them in.
   - Verify signature counts and the review screen's classification of
     outputs against the table.
5. **Settings**:
   - Verify the removed policy/account UI truly is gone.
   - Toggle permissive signing and rerun the non-standard-keypath PSBT;
     confirm the ACK prompt appears and gating works in both states.
6. **Addresses**:
   - Addresses page: switch among the 4 SS source entries and one registered
     descriptor; confirm addresses match those generated by a reference
     wallet at the same paths.
   - Address checker: paste both an in-registry multisig address and an
     out-of-range singlesig (account 200) address; confirm found / not-found
     respectively.

---

## Out of scope (phase 2)

- BIP-1951 descriptor encryption with mnemonic-derived key, replacing KEF
  for descriptors and enabling auto-decryption at boot.
- Migration path from `.kef` → BIP-1951 envelopes.
- Hardening beyond Ledger parity (e.g. HMAC-signed wallet policies à la
  Ledger's `register_wallet`). Our registry is file-backed; the trust
  boundary is "the device's own flash/SD", which is adequate for now.
