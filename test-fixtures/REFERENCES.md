# Test reference values

The test mnemonic is the well-known BIP39 test vector:

```
abandon abandon abandon abandon abandon abandon abandon abandon
abandon abandon abandon about
```

Master fingerprint (mainnet): `73c5da0a`

Fill in the values below using Sparrow or `bitcoin-cli
getdescriptorinfo` + `deriveaddresses`, then:

1. Paste the real xpubs + checksums into `test-fixtures/manifest.yaml`.
2. Paste the addresses into the `addr_*` fixtures.
3. Run `python3 scripts/gen-test-plan.py` to regenerate
   `.cm/spec/TESTING_PLAN.md` with the real data in the embedded ASCII
   QRs.

---

## Account xpubs

| Derivation                 | xpub (fill in)     |
|----------------------------|--------------------|
| `m/84'/0'/0'`              | zpub6… or xpub6…   |
| `m/84'/0'/2'`              |                    |
| `m/84'/0'/3'`              |                    |
| `m/86'/0'/0'`              |                    |
| `m/44'/0'/0'`              |                    |
| `m/49'/0'/0'`              |                    |
| `m/48'/0'/0'/2'` (wsh ms)  |                    |

For the wsh 2-of-2 baseline descriptor, also pick a second dummy xpub
(e.g. derived from another test mnemonic) and record its fingerprint
here.

## Reference addresses at index 0 / chain 0

| Descriptor                                    | Address (fill in)  |
|-----------------------------------------------|--------------------|
| `wpkh([73c5da0a/84'/0'/0']xpub.../<0;1>/*)`  | `bc1q...`          |
| `tr([73c5da0a/86'/0'/0']xpub.../<0;1>/*)`    | `bc1p...`          |
| `wpkh([73c5da0a/49'/0'/0']xpub.../<0;1>/*)`  | `3...`             |
| `wpkh([73c5da0a/44'/0'/0']xpub.../<0;1>/*)`  | `1...`             |
| wsh 2-of-2 multisig at `0/0`                  | `bc1q...`          |

## PSBT fixtures

Hand-craft offline (Sparrow: "Create Transaction" → "Save as PSBT", or
`bitcoin-cli walletcreatefundedpsbt` + `walletprocesspsbt`). Save under
`test-fixtures/raw/` with these exact filenames — the manifest refers
to them. Then re-run `python3 scripts/gen-test-plan.py`.

| Filename                                         | Input keypath(s)                  | Output(s)                                    |
|--------------------------------------------------|-----------------------------------|----------------------------------------------|
| `psbt_A_bip84_acct3.bin`                         | `m/84'/0'/3'/0/12`                | any                                          |
| `psbt_B_bip86.bin`                               | `m/86'/0'/0'/1/4`                 | any                                          |
| `psbt_C_bip44_acct100.bin`                       | `m/44'/0'/100'/0/0`               | any                                          |
| `psbt_D_bip84_idx100.bin`                        | `m/84'/0'/0'/0/100`               | any                                          |
| `psbt_E_wsh_multisig.bin`                        | wsh-multisig registered           | any                                          |
| `psbt_F_nonstandard_purpose.bin`                 | `m/9999'/0'/0'/0/0`               | any                                          |
| `psbt_G_attacker_swapped_utxo.bin`               | `m/84'/0'/0'/0/0` + swapped UTXO  | any                                          |
| `psbt_H_output_classification.bin`               | `m/84'/0'/0'/0/0`                 | owned at `m/84'/0'/0'/1/3` + external `bc1q` |
| `psbt_I_fp_only.bin`                             | `m/84'/0'/0'/0/0`                 | fp-matching but non-matching output keypath  |
