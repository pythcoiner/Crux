# Kern Project Structure

Kern is a Bitcoin signing device firmware built on ESP-IDF. This rework
touches the core wallet/PSBT/descriptor subsystem and its UI.

## Directory Layout

```
/
├── main/
│   ├── main.c                  - firmware entry point
│   ├── CMakeLists.txt          - top-level main component CMake (SRCS list)
│   ├── core/                   - wallet state, crypto, PSBT, descriptor handling
│   │   ├── wallet.{c,h}        - policy-gated singlesig/multisig state (being rewritten)
│   │   ├── psbt.{c,h}          - PSBT signing + output classification
│   │   ├── settings.{c,h}      - NVS-backed settings (def_pol → perm_sign)
│   │   ├── descriptor_validator.{c,h} - descriptor UI validation flow
│   │   ├── key.{c,h}           - key derivation, fingerprint, parse_derivation_path
│   │   ├── storage.{c,h}       - flash/SD descriptor file I/O
│   │   ├── crypto_utils.{c,h}  - hashes, HMAC helpers
│   │   ├── kef.{c,h}           - KEF encrypted envelope format
│   │   ├── pin.{c,h}, session.{c,h}, message_sign.{c,h}, base43.{c,h}, error.{c,h}
│   │   └── test/               - Unity-based unit tests for core modules
│   └── pages/                  - LVGL UI pages
│       ├── home/addresses.c               - Addresses page (source picker target)
│       ├── shared/address_checker.c       - address-lookup page (source picker target)
│       ├── shared/key_confirmation.c      - post-PIN handler (boot wiring)
│       ├── shared/descriptor_loader.c     - descriptor-load flow
│       ├── settings/wallet_settings.c     - settings page (policy dropdown removal)
│       ├── store_descriptor.c             - save-descriptor flow
│       └── load_descriptor_storage.c      - load-descriptor flow (.kef + plaintext)
├── components/                 - ESP-IDF components (bbqr, libwally, display, LVGL, etc.)
├── managed_components/         - idf_component_manager fetched deps
├── simulator/                  - desktop SDL simulator for UI work
├── build_{wave_4b,wave_35,wave_5}/ - per-board build outputs
├── sdkconfig.defaults          - shared ESP-IDF config
├── sdkconfig.defaults.{wave_4b,wave_35,wave_5} - per-board overrides
├── partitions.csv              - flash partition layout
├── .justfile                   - build/flash/sim task runner
├── CMakeLists.txt              - project-level CMake
└── .cm/spec/          - authoritative spec for this rework (PLAN.md, SNIP.md, ROADMAP.md)
```

## Module Organization

- **`main/core/ss_whitelist`** (new) — singlesig derivation whitelist. Types, parsing, range checks, script regeneration (P2PKH, P2SH_P2WPKH, P2WPKH, P2TR), address derivation, purpose↔script binding helpers.
- **`main/core/registry`** (new) — in-memory descriptor registry. Scans flash + SD at boot; matches PSBT keypaths against registered descriptor origins; provides add/remove/iteration APIs.
- **`main/core/psbt`** (rewritten classifier) — `claim_t`, `psbt_classify_input`, `psbt_classify_output`, `claim_regenerate`. Drives sign/verify decisions through match→bind→regenerate→verify.
- **`main/core/wallet`** (shrunk) — becomes a thin network/init/cleanup wrapper. All policy/account/derivation-path state moves to `ss_whitelist` and `registry`. Retains BIP-380 checksum helper.
- **`main/core/settings`** — drops `def_pol` (policy NVS key), adds `perm_sign` (permissive signing toggle).
- **`main/core/descriptor_validator`** — drops attribute-mismatch confirmation flow (no more "current policy" to mismatch against); keeps fingerprint + xpub verification; gains soft purpose-binding WARN dialog.
- **`main/pages/home/addresses.c`** and **`main/pages/shared/address_checker.c`** — gain a source-picker dropdown covering the 4 singlesig script types + one entry per registered descriptor.

## Data Flow

PSBT signing (post-rewrite):

1. PSBT bytes arrive via QR / USB / SD.
2. `psbt_sign` iterates inputs.
3. Per input, `psbt_classify_input` is called:
   - Extract UTXO script (witness-utxo first, fallback to utxo+prevout).
   - For each keypath matching our fingerprint, enumerate candidate claims via `try_match_whitelist` then `try_match_registry`.
   - For each claim, `claim_regenerate` produces expected spk (+ redeem/witness for sh/wsh).
   - Byte-compare regenerated script(s) vs PSBT's fields.
4. If verified → derive at the claim's full path via `key_get_derived_key` + `wally_psbt_sign`.
5. If fingerprint matched but nothing verified + permissive=on → UI ACK, sign at raw keypath; else skip.
6. Outputs are classified similarly but without the UTXO/redeem/witness cross-check.

## Configuration

- **`sdkconfig`** — ESP-IDF default + per-board overrides.
- **`main/CMakeLists.txt`** — `idf_component_register SRCS` list; new .c files must be added here in alphabetical order.
- **`main/core/test/CMakeLists.txt`** — test-harness `SRCS` list; new test files must be registered here.
- **`.justfile`** — `just build <board>`, `just flash <board>`, `just test`, `just format`.

## External Dependencies

- **libwally** (via `components/` or managed_components) — BIP32/BIP39/descriptor parsing, address encoders, BIP341 helpers. Used extensively by the rework for script regeneration and descriptor operations.
- **Unity** — test harness under `main/core/test/`.
- **LVGL** — UI framework under `main/pages/`.

## Build Artifacts

- **`build_wave_4b/`**, **`build_wave_35/`**, **`build_wave_5/`** — per-board firmware binaries and `compile_commands.json`.
- **`simulator/build/kern_simulator`** — desktop SDL simulator.

## Important Patterns

### Libwally usage for script work

Don't hand-parse BIP32 paths — use `parse_derivation_path` from `key.c:110-190`. For descriptors, use `wally_descriptor_parse`, `wally_descriptor_to_script` (vary `depth` per outer shape), `wally_descriptor_to_address`, `wally_descriptor_get_num_paths`, `wally_descriptor_get_key_origin_*`. For BIP341, use `wally_ec_public_key_bip341_tweak` / `wally_bip341_*`.

### PSBT keypath format

4 fingerprint bytes + N little-endian u32 BIP32 components (hardened bit = top bit = `0x80000000`). Reads via `wally_psbt_get_input_keypath` / `wally_psbt_get_output_keypath`; components at offsets 4, 8, 12, …

### Scope discipline

Each phase ≈ one commit. Never touch files outside the phase's "Files touched" list — if a caller needs fixing but is in a later phase, the tree must still build regardless.

## Notes for Agents

- The authoritative spec is `.cm/spec/PLAN.md` + `SNIP.md` + `ROADMAP.md`. SNIP anchors are referenced from task plans — follow them.
- Every phase must leave the tree buildable via `just build wave_4b`. If a deletion breaks callers, the migration of those callers is in an earlier phase — verify that phase was completed first.
- New `.c` files must be added to `main/CMakeLists.txt` `SRCS` list (alphabetical order).
- New test `.c` files must be added to `main/core/test/` CMakeLists.
- Tests use the Unity harness. Pattern: look at existing tests under `main/core/test/` for style.
- Writing to NVS: use `esp_err_t` return + `NVS_HANDLE_T`. Pattern: see `settings.c`.
- Never add `// TODO` / `// FIXME` markers — complete the phase or raise a blocker.
