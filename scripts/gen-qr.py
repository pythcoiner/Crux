#!/usr/bin/env python3
"""Print the ASCII-half-block QR for a test fixture to stdout.

Reads test-fixtures/manifest.yaml and renders the requested fixture's
QR. Output goes to stdout only — this tool never modifies
.cm/spec/TESTING_PLAN.md (which is hand-edited).

Examples:

    # Print one fixture's QR + payload
    python3 scripts/gen-qr.py mnemonic_boot

    # Same, inverted polarity for dark-theme editors
    python3 scripts/gen-qr.py mnemonic_boot --dark-theme

    # List every label defined in the manifest
    python3 scripts/gen-qr.py --list

    # Dump every fixture (separated by `--- label ---` headers)
    python3 scripts/gen-qr.py --all
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib import bbqr_encode, qr_ascii  # noqa: E402

import yaml  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "test-fixtures" / "manifest.yaml"


# ---------------------------------------------------------------------------
# Per-fixture rendering
# ---------------------------------------------------------------------------


def _compact_seedqr_payload(entropy_hex: str) -> bytes:
    raw = bytes.fromhex(entropy_hex)
    if len(raw) not in (16, 32):
        raise ValueError(
            f"compact_seedqr entropy must be 16 or 32 bytes, got {len(raw)}"
        )
    return raw


def render_fixture(entry: dict, *, dark_theme: bool) -> tuple[str, list[str]]:
    """Return (preview_line, [ascii_qr_frames])."""

    def _qr(payload):
        return qr_ascii.render(payload, dark_theme=dark_theme)

    label = entry["label"]
    kind = entry["type"]

    if kind == "plain":
        payload = entry["payload"]
        preview = payload if len(payload) <= 200 else payload[:199] + "…"
        return preview, [_qr(payload)]

    if kind == "compact_seedqr":
        raw = _compact_seedqr_payload(entry["entropy_hex"])
        preview = (
            f"Compact SeedQR · {len(raw)} bytes entropy · hex={entry['entropy_hex']}"
        )
        return preview, [_qr(raw)]

    if kind == "psbt":
        raw_path = REPO_ROOT / entry["from_file"]
        if not raw_path.exists():
            raise SystemExit(
                f"fixture {label!r}: missing raw PSBT at "
                f"{raw_path.relative_to(REPO_ROOT)}"
            )
        raw = raw_path.read_bytes()
        encoding = entry.get("encoding", "auto")
        if encoding == "auto":
            encoding = bbqr_encode.recommend_single_vs_multi(len(raw))[0]

        if encoding == "base64":
            import base64 as b64

            payload = b64.b64encode(raw).decode("ascii")
            preview = (
                f"Base64 PSBT · {len(raw)} bytes raw → {len(payload)} chars base64"
            )
            return preview, [_qr(payload)]
        if encoding == "binary":
            return f"Binary PSBT · {len(raw)} bytes", [_qr(raw)]
        if encoding in ("bbqr", "single"):
            frames = bbqr_encode.encode(raw, file_type="P")
            preview = (
                f"BBQr base32 · {len(raw)} bytes raw · {len(frames)} frames"
            )
            return preview, [_qr(f) for f in frames]
        raise ValueError(f"fixture {label!r}: unknown encoding {encoding!r}")

    raise ValueError(f"fixture {label!r}: unknown type {kind!r}")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def emit(label: str, preview: str, frames: list[str]) -> None:
    print(f"# {label}")
    print(f"payload: {preview}")
    print()
    if len(frames) == 1:
        print("```text")
        print(frames[0])
        print("```")
    else:
        print(f"({len(frames)}-frame BBQr — scroll through every frame)")
        for i, f in enumerate(frames, start=1):
            print()
            print(f"## frame {i}/{len(frames)}")
            print()
            print("```text")
            print(f)
            print("```")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("label", nargs="?", help="fixture label to render")
    ap.add_argument(
        "--all", action="store_true", help="dump every fixture (sequential)"
    )
    ap.add_argument(
        "--list",
        action="store_true",
        help="print every fixture label defined in the manifest, one per line",
    )
    ap.add_argument(
        "--dark-theme",
        action="store_true",
        help="invert QR polarity for dark-theme editors",
    )
    ap.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST,
        help=f"manifest path (default: {MANIFEST.relative_to(REPO_ROOT)})",
    )
    args = ap.parse_args()

    with args.manifest.open() as f:
        manifest = yaml.safe_load(f)
    fixtures = {entry["label"]: entry for entry in (manifest.get("fixtures") or [])}

    if args.list:
        for lbl in fixtures:
            print(lbl)
        return 0

    if args.all:
        for i, (lbl, entry) in enumerate(fixtures.items()):
            if i:
                print()
                print("---")
                print()
            preview, frames = render_fixture(entry, dark_theme=args.dark_theme)
            emit(lbl, preview, frames)
        return 0

    if not args.label:
        ap.error("supply a fixture label, --all, or --list")

    if args.label not in fixtures:
        sys.exit(
            f"unknown fixture {args.label!r}. "
            f"Try `--list` or one of: {', '.join(fixtures)}"
        )

    preview, frames = render_fixture(fixtures[args.label], dark_theme=args.dark_theme)
    emit(args.label, preview, frames)
    return 0


if __name__ == "__main__":
    sys.exit(main())
