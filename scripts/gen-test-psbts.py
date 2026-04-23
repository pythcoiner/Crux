#!/usr/bin/env python3
"""Build the 9 raw PSBT fixtures that gen-qr.py expects.

Each PSBT is a single-input, two-output spend (one external, one
self-change for psbt_H) that exercises one row of PLAN.md §"Behavioural
spec → Signing". Inputs are synthetic — the prevout txid is hashed from
the fixture label so each PSBT round-trips through wally_psbt_from_bytes
deterministically.

Run:
    ./scripts/.venv/bin/python scripts/gen-test-psbts.py

Writes to test-fixtures/raw/psbt_*.bin (one file per fixture).
"""

from __future__ import annotations

import hashlib
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from embit import bip32, bip39, ec, networks, script
from embit.psbt import PSBT, InputScope, OutputScope, DerivationPath
from embit.transaction import Transaction, TransactionInput, TransactionOutput

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "test-fixtures" / "raw"

MNEMONIC = (
    "abandon abandon abandon abandon abandon abandon abandon abandon "
    "abandon abandon abandon about"
)
NET = networks.NETWORKS["main"]

# Sane defaults for synthetic transactions
INPUT_VALUE_SATS = 100_000
FEE_SATS = 1_000
EXTERNAL_OUTPUT_VALUE = INPUT_VALUE_SATS - FEE_SATS
# A made-up external destination (not derivable from the test mnemonic).
EXTERNAL_BECH32 = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"


def fake_prevout_txid(label: str) -> bytes:
    """Deterministic 32-byte txid for the synthetic input."""
    return hashlib.sha256(b"kern-test-fixture:" + label.encode()).digest()


def parse_path(path_str: str) -> list[int]:
    """`m/84'/0'/3'/0/12` → [0x80000054, 0x80000000, 0x80000003, 0, 12]."""
    parts = path_str.lstrip("m/").split("/")
    out = []
    for p in parts:
        if p.endswith("'") or p.endswith("h"):
            n = int(p[:-1]) | 0x80000000
        else:
            n = int(p)
        out.append(n)
    return out


def derive(root: bip32.HDKey, path: list[int]) -> bip32.HDKey:
    return root.derive(path)


def script_pubkey_for_purpose(child_pub: ec.PublicKey, purpose: int):
    """Build the standard scriptPubKey for the given BIP-purpose at this pubkey."""
    if purpose == 84:  # P2WPKH
        return script.p2wpkh(child_pub)
    if purpose == 86:  # P2TR (single-key, no script tree)
        return script.p2tr(child_pub)
    if purpose == 44:  # P2PKH
        return script.p2pkh(child_pub)
    if purpose == 49:  # P2SH-P2WPKH
        return script.p2sh(script.p2wpkh(child_pub))
    # 9999 — nonsense purpose; treat as P2WPKH on the wire (the fixture
    # tests refusal of the keypath, not the scriptPubKey shape).
    return script.p2wpkh(child_pub)


def build_psbt(
    label: str,
    *,
    in_path: str,
    out_path: str | None = None,
    fp_only_out_path: str | None = None,
    swap_utxo_script: bool = False,
    extra_change_path: str | None = None,
) -> bytes:
    """Build a single-input PSBT with our keypath, optionally with a second
    'self' output for classification tests.

    `in_path`:               BIP32 path of the input we'd sign for.
    `out_path`:              if given, second output is this owned path
                             (psbt_H — owned-output classification).
    `fp_only_out_path`:      if given, second output keypath has our
                             fingerprint but the path is non-whitelisted
                             (psbt_I — fp-only must NOT be marked owned).
    `swap_utxo_script`:      replace the witness-utxo scriptPubKey with
                             a different valid scriptPubKey (psbt_G —
                             attacker swap).
    `extra_change_path`:     unused; reserved for future tests.
    """
    seed = bip39.mnemonic_to_seed(MNEMONIC)
    root = bip32.HDKey.from_seed(seed, version=NET["xprv"])
    fp = root.child(0).fingerprint  # actually just root.my_fingerprint?
    fp = root.my_fingerprint

    # --- input pubkey/script
    in_path_ints = parse_path(in_path)
    in_purpose = (in_path_ints[0] & 0x7FFFFFFF) if in_path_ints[0] & 0x80000000 else in_path_ints[0]
    in_child = derive(root, in_path_ints)
    in_pub = in_child.key.get_public_key()
    in_spk = script_pubkey_for_purpose(in_pub, in_purpose)

    if swap_utxo_script:
        # Replace with a different valid P2WPKH at a fixed dummy pubkey.
        # The keypath in the PSBT still points at our key, but the UTXO
        # script doesn't match — the regenerate+verify step must reject.
        dummy_pub = derive(root, parse_path("m/84'/0'/0'/1/77")).key.get_public_key()
        in_spk_in_psbt = script.p2wpkh(dummy_pub)
    else:
        in_spk_in_psbt = in_spk

    # --- unsigned tx skeleton
    txin = TransactionInput(
        txid=fake_prevout_txid(label),
        vout=0,
        sequence=0xFFFFFFFD,  # RBF
    )
    outputs = [
        TransactionOutput(
            value=EXTERNAL_OUTPUT_VALUE,
            script_pubkey=script.address_to_scriptpubkey(EXTERNAL_BECH32),
        ),
    ]

    # Optional second self-output (psbt_H) — owned output at out_path
    self_out_pub = None
    self_out_path_ints = None
    if out_path is not None:
        self_out_path_ints = parse_path(out_path)
        self_out_pub = derive(root, self_out_path_ints).key.get_public_key()
        outputs.append(
            TransactionOutput(
                value=10_000,  # tiny self-output
                script_pubkey=script.p2wpkh(self_out_pub),
            )
        )
        # Re-balance external output to keep fee = FEE_SATS
        outputs[0].value = INPUT_VALUE_SATS - 10_000 - FEE_SATS

    # Optional fp-only output (psbt_I) — different external scriptPubKey
    # but the keypath in PSBT_OUT_BIP32_DERIVATION points at our fp on
    # a non-standard path. Keep the scriptPubKey as a vanilla external
    # P2WPKH at the wrong-path child to make it look "non-ours" via the
    # regenerate check.
    fp_only_out_pub = None
    fp_only_path_ints = None
    if fp_only_out_path is not None:
        fp_only_path_ints = parse_path(fp_only_out_path)
        fp_only_out_pub = derive(root, fp_only_path_ints).key.get_public_key()
        outputs.append(
            TransactionOutput(
                value=5_000,
                script_pubkey=script.p2wpkh(fp_only_out_pub),
            )
        )
        outputs[0].value = INPUT_VALUE_SATS - 5_000 - FEE_SATS

    tx = Transaction(version=2, vin=[txin], vout=outputs, locktime=0)

    # --- PSBT scaffold
    psbt_obj = PSBT(tx)

    # --- input scope
    iscope = psbt_obj.inputs[0]
    fake_witness_utxo = TransactionOutput(
        value=INPUT_VALUE_SATS,
        script_pubkey=in_spk_in_psbt,
    )
    iscope.witness_utxo = fake_witness_utxo
    iscope.bip32_derivations[in_pub] = DerivationPath(fp, in_path_ints)

    # --- output scopes (BIP32 derivations for the self/fp-only outputs)
    if self_out_pub is not None:
        oscope: OutputScope = psbt_obj.outputs[1]
        oscope.bip32_derivations[self_out_pub] = DerivationPath(fp, self_out_path_ints)
    if fp_only_out_pub is not None:
        # Place at the trailing index regardless of whether self-out was
        # also present.
        idx = len(outputs) - 1
        oscope = psbt_obj.outputs[idx]
        oscope.bip32_derivations[fp_only_out_pub] = DerivationPath(fp, fp_only_path_ints)

    return psbt_obj.serialize()


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fixtures = [
        ("psbt_A_bip84_acct3",          dict(in_path="m/84'/0'/3'/0/12")),
        ("psbt_B_bip86",                dict(in_path="m/86'/0'/0'/1/4")),
        ("psbt_C_bip44_acct100",        dict(in_path="m/44'/0'/100'/0/0")),
        ("psbt_D_bip84_idx100",         dict(in_path="m/84'/0'/0'/0/100")),
        ("psbt_F_nonstandard_purpose",  dict(in_path="m/9999'/0'/0'/0/0")),
        ("psbt_G_attacker_swapped_utxo", dict(in_path="m/84'/0'/0'/0/0", swap_utxo_script=True)),
        ("psbt_H_output_classification", dict(in_path="m/84'/0'/0'/0/0", out_path="m/84'/0'/0'/1/3")),
        ("psbt_I_fp_only",              dict(in_path="m/84'/0'/0'/0/0", fp_only_out_path="m/1234'/0'/0'/0/0")),
    ]
    # psbt_E (wsh multisig) needs a real descriptor; skip for now
    # (placeholder PSBT also doesn't help — the firmware expects
    # the input to match the registered desc_wsh_2of2 byte-exactly).

    for label, kwargs in fixtures:
        data = build_psbt(label, **kwargs)
        path = OUT_DIR / f"{label}.bin"
        path.write_bytes(data)
        print(f"  wrote {path.relative_to(REPO_ROOT)}  ({len(data)} bytes)")

    print(
        f"\nNote: psbt_E_wsh_multisig still needs a hand-crafted PSBT against "
        f"the desc_wsh_2of2 descriptor (cosigner xpub must be real). Generate "
        f"it offline once the descriptor is finalized."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
