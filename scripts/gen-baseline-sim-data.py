#!/usr/bin/env python3
"""Generate the `sim_data/` baseline tarball for TESTING_PLAN.md §1.

Reads `test-fixtures/manifest.yaml` → `bootstrap:` section.
Writes:
    test-fixtures/baseline-sim-data/nvs/pin.nvs
    test-fixtures/baseline-sim-data/nvs/settings.nvs
    test-fixtures/baseline-sim-data/sdcard/kern/descriptors/<id>.txt

The NVS pin namespace is populated with `pin_hash` (32-byte blob derived
via PBKDF2-HMAC-SHA256 with 100000 iterations, salt =
SHA256("C-Krux-fallback-salt-v1")) — matching `main/core/pin.c:42-62` +
220-236. This is the fallback salt used when the eFuse HMAC peripheral
is unavailable (always the case in the simulator).

Usage:
    python3 scripts/gen-baseline-sim-data.py

After generation, on the simulator host:
    rm -rf simulator/sim_data
    cp -r test-fixtures/baseline-sim-data/ simulator/sim_data/
    just sim-webcam wave_35
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.nvs_pack import Namespace, write_namespace  # noqa: E402

import yaml  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "test-fixtures" / "baseline-sim-data"
MANIFEST = REPO_ROOT / "test-fixtures" / "manifest.yaml"

PIN_FALLBACK_SALT_TAG = b"C-Krux-fallback-salt-v1"
PIN_PBKDF2_ITERATIONS = 100000
PIN_HASH_SIZE = 32


def compute_pin_hash(pin: str) -> bytes:
    """Match `compute_device_salt` + `pin_setup` paths in main/core/pin.c."""
    salt = hashlib.sha256(PIN_FALLBACK_SALT_TAG).digest()
    return hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        salt,
        PIN_PBKDF2_ITERATIONS,
        dklen=PIN_HASH_SIZE,
    )


def build(manifest_path: Path, out_dir: Path, clean: bool) -> None:
    with manifest_path.open() as f:
        manifest = yaml.safe_load(f)
    bootstrap = manifest.get("bootstrap") or {}

    if clean and out_dir.exists():
        shutil.rmtree(out_dir)

    # --- NVS: pin namespace ---
    pin = bootstrap.get("pin")
    if pin is None:
        raise SystemExit("manifest.yaml: bootstrap.pin is required")
    split_pos = int(bootstrap.get("split_pos", 2))
    if not 1 <= split_pos < len(pin):
        raise SystemExit(
            f"manifest.yaml: split_pos {split_pos} invalid for PIN length {len(pin)}"
        )

    pin_ns = (
        Namespace("pin")
        .set_blob("pin_hash", compute_pin_hash(pin))
        .set_u8("split_pos", split_pos)
        .set_u8("has_efuse", 0)
    )

    # --- NVS: settings namespace ---
    settings = bootstrap.get("settings") or {}
    settings_ns = Namespace("settings")
    for key, value in settings.items():
        if key in ("def_net", "bright", "ae_tgt", "perm_sign"):
            settings_ns.set_u8(key, int(value))
        elif key == "focus":
            settings_ns.set_u16(key, int(value))
        else:
            raise SystemExit(f"manifest.yaml: unknown settings key {key!r}")

    # --- SD card: plaintext descriptors ---
    descriptors = bootstrap.get("baseline_descriptors") or []
    sd_dir = out_dir / "sdcard" / "kern" / "descriptors"
    sd_dir.mkdir(parents=True, exist_ok=True)
    for entry in descriptors:
        path = sd_dir / f"{entry['id']}.txt"
        path.write_text(entry["str"] + "\n", encoding="utf-8")
        print(f"  wrote {path.relative_to(REPO_ROOT)}")

    # --- Also create empty mnemonics dir (firmware expects it to exist) ---
    (out_dir / "sdcard" / "kern" / "mnemonics").mkdir(parents=True, exist_ok=True)

    # --- Write NVS files ---
    nvs_dir = out_dir / "nvs"
    for ns in (pin_ns, settings_ns):
        p = write_namespace(nvs_dir, ns)
        print(f"  wrote {p.relative_to(REPO_ROOT)}  ({p.stat().st_size} bytes)")

    print(f"\nBaseline sim_data written to {out_dir.relative_to(REPO_ROOT)}/")
    print("Copy it onto machine B before §1:")
    print(f"  rsync -a {out_dir.relative_to(REPO_ROOT)}/ simulator/sim_data/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--manifest", type=Path, default=MANIFEST)
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument(
        "--no-clean",
        action="store_true",
        help="don't wipe the output dir before regenerating",
    )
    args = ap.parse_args()
    build(args.manifest, args.out, clean=not args.no_clean)
    return 0


if __name__ == "__main__":
    sys.exit(main())
