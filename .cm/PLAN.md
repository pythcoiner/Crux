# descriptor-rework

> Rework Kern's descriptor & derivation-path management: replace the policy-gated singlesig/multisig model with a BIP44/49/84/86 whitelist plus an auto-loaded descriptor registry, routing every sign/verify decision through a unified "match → bind → regenerate → verify" algorithm.

## Authoritative spec

The detailed plan, snippets, and roadmap live under `.cm/spec/`:

- **`.cm/spec/PLAN.md`** — code-free overview (context, target architecture, ownership methodology, UI changes, files to modify, behavioural spec, verification plan).
- **`.cm/spec/SNIP.md`** — all struct / function signatures / pseudocode referenced as `SNIP 01..12` from the PLAN.
- **`.cm/spec/ROADMAP.md`** — the original fine-grained checklist the cm phases are derived from.

This cm project is a 78-phase execution of that spec. Each phase is sized to a single commit that leaves the tree buildable.

## Goals

- Remove forced per-session policy selection; any whitelisted BIP44/49/84/86 account signs automatically.
- Auto-register plaintext descriptors on flash + SD at boot (multisig no longer requires manual load each session).
- Unify singlesig and multisig ownership checks under `psbt_classify_input` / `psbt_classify_output` using `claim_regenerate` to defeat keypath-swap attacks.
- Eliminate `wallet_policy_t` and the hardcoded derivation paths in `wallet.c`.

## Success criteria

- [ ] Clean builds on `wave_4b`, `wave_35`, `wave_5`.
- [ ] Every row of PLAN.md §"Behavioural spec" passes on device.
- [ ] `rg 'wallet_policy_t|wallet_get_policy|wallet_set_policy|wallet_get_account|wallet_set_account|wallet_get_receive_address|wallet_get_change_address|wallet_get_scriptpubkey|wallet_has_descriptor|wallet_load_descriptor|wallet_clear_descriptor|wallet_get_multisig_|wallet_format_derivation|wallet_get_derivation|settings_get_default_policy|settings_set_default_policy'` returns zero hits.
- [ ] Unit tests under `main/core/test/` pass (ss_whitelist parse/regen, registry match/parse, purpose binding, psbt_classify fixtures A-E).
- [ ] A reboot-after-store test on wave_35 lists all stored plaintext descriptors in "Registered descriptors" without any user action.

## Architecture (summary)

Three new modules + unified classifier:

1. **`main/core/ss_whitelist.{h,c}`** (SNIP 01) — singlesig derivation whitelist: purpose ∈ {44,49,84,86}, coin matches network, account < 100, index < 100, chain ∈ {0,1}. Strict purpose↔script binding via a fixed lookup table.
2. **`main/core/registry.{h,c}`** (SNIP 02) — in-memory descriptor registry populated at boot from flash + SD `.txt` files. Replaces `static struct wally_descriptor *loaded_descriptor` in `wallet.c:24`.
3. **`main/core/psbt.c`** classifier rewrite — `psbt_classify_input` / `psbt_classify_output` drive a match → bind → regenerate → verify algorithm over every PSBT keypath, with no fingerprint-only fallback.

Ownership methodology (PLAN.md §"Ownership methodology"):
1. **Match** — a keypath is recognised only if it fits the whitelist shape or a registered descriptor's origin prefix.
2. **Purpose/script binding** — hard-enforced for whitelist; soft-warn at registration time for descriptors.
3. **Regenerate** — derive expected scriptPubKey (+ redeem/witness for sh/wsh families) from the claim.
4. **Verify** — regenerated script must byte-equal the PSBT's. Keypath alone is never enough.

There is **no "change vs receive" distinction at the signer layer** — the classifier reports owned/external only; path display is a UI concern.

## Phases

The 78 phases are grouped by theme in `ROADMAP.md`:

- **Setup** (P01): scaffolding.
- **Group A** (P02–P11): `ss_whitelist` module — types, parse, format, whitelist check, script regen (P2WPKH/P2PKH/P2SH_P2WPKH/P2TR), address dispatcher, purpose binding helpers.
- **Group B** (P12–P20): `registry` module — types, accessors, clear, add (in-memory + persist), remove, match, init scan, parse tests.
- **Group C** (P21): permissive-signing setting (additive — does not touch `def_pol`).
- **Group D** (P22–P28): PSBT classifier — types, helpers, `claim_regenerate` (whitelist + registry branches), `psbt_classify_input/output` with fixtures A–E.
- **Group E** (P29): boot wiring — `registry_init` called after `wallet_init`.
- **Group F** (P30–P33): PSBT signing migration — rewrite `psbt_sign`, delete legacy output helpers.
- **Group G** (P34–P41): UI migration — Addresses page source picker, address-checker source picker, auto-register on save/decrypt.
- **Group H** (P42–P46): descriptor validator cleanup — redirect, WARN dialog, delete attribute-check state.
- **Group I** (P47–P52): settings UI migration — remove policy dropdown / account spinner / preview label, add permissive toggle, registered-descriptors sub-page.
- **Group J** (P53–P55): policy API removal — drop call site, remove getter/setter, remove NVS key.
- **Group K** (P56–P67): wallet API removal — delete statics, helpers, and header APIs one symbol at a time.
- **Group L** (P68–P71): cleanup — grep sweep, dead tests, repo-root ROADMAP, CHANGELOG.
- **Group M** (P72–P78): device verification — clean builds on all three boards, boot auto-load, addresses page, PSBT behavioural spec, settings UI, address checker, WARN-dialog gating.

## Out of scope

- BIP-1951 descriptor encryption with mnemonic-derived key.
- Migration path `.kef` → BIP-1951 envelopes.
- HMAC-signed wallet policies (Ledger-style `register_wallet`).

## References

- `.cm/spec/PLAN.md`, `.cm/spec/SNIP.md`, `.cm/spec/ROADMAP.md`
- Ledger `app-bitcoin-new` (whitelist model reference)
- `main/core/key.c:110-190` — `parse_derivation_path` helper (reused)
- `main/core/descriptor_validator.c:55-78` — fingerprint matching loop (logic reused in `registry_init`)
