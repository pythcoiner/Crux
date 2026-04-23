#!/usr/bin/env python3
"""Generate `.cm/spec/TESTING_PLAN.md` from template + manifest.

Reads:
    test-fixtures/manifest.yaml
    .cm/spec/TESTING_PLAN.tmpl.md
Writes:
    .cm/spec/TESTING_PLAN.md

Template substitution: every `<!-- QR:label -->` marker in the template
is replaced with the fixture block — payload preview + a fenced
code block containing the half-block ASCII QR (one or more frames for
BBQr).

Behaviour:
    Unknown marker             → hard error, listing the missing label
    Unused manifest fixture    → warning (likely stale manifest entry)
    PSBT raw file missing      → renders a stub block with a prominent
                                  "MISSING: run Sparrow/bitcoin-cli" hint.
                                  (Lets you iterate on the template
                                   before PSBTs are crafted.)
    Payload exceeds QR v40     → hard error pointing at the fixture label
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib import bbqr_encode, qr_ascii  # noqa: E402

import yaml  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "test-fixtures" / "manifest.yaml"
TEMPLATE = REPO_ROOT / ".cm" / "spec" / "TESTING_PLAN.tmpl.md"
OUTPUT = REPO_ROOT / ".cm" / "spec" / "TESTING_PLAN.md"


@dataclass
class Fixture:
    label: str
    type: str
    payload_preview: str           # human-readable summary for the markdown
    frames: list[str]              # rendered ASCII QR strings (1 = single, >1 = BBQr)
    note: str | None = None
    missing_raw_file: Path | None = None
    # Only for BBQr fixtures: the raw byte payload per frame, for selfcheck.
    bbqr_raw_frames: list[str] | None = None


# ---------------------------------------------------------------------------
# Fixture preparation
# ---------------------------------------------------------------------------


def _compact_seedqr_payload(entropy_hex: str) -> bytes:
    raw = bytes.fromhex(entropy_hex)
    if len(raw) not in (16, 32):
        raise ValueError(
            f"compact_seedqr entropy must be 16 or 32 bytes, got {len(raw)}"
        )
    return raw


def _seedqr_payload(words: list[str] | str | None, entropy_hex: str | None) -> str:
    # Standard SeedQR is decimal word indices, 4 digits each, 48 or 96 chars total
    # Accept either explicit words list or entropy_hex + derive indices.
    raise NotImplementedError(
        "SeedQR (decimal) not yet implemented — use compact_seedqr"
    )


def _truncate_for_preview(text: str, max_len: int = 200) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def prepare_fixture(entry: dict) -> Fixture:
    label = entry["label"]
    kind = entry["type"]
    note = entry.get("note")

    if kind == "plain":
        payload = entry["payload"]
        frames = [qr_ascii.render(payload)]
        return Fixture(
            label=label,
            type="plain",
            payload_preview=_truncate_for_preview(payload),
            frames=frames,
            note=note,
        )

    if kind == "compact_seedqr":
        raw = _compact_seedqr_payload(entry["entropy_hex"])
        frames = [qr_ascii.render(raw)]
        return Fixture(
            label=label,
            type="compact_seedqr",
            payload_preview=f"Compact SeedQR · {len(raw)} bytes entropy · hex={entry['entropy_hex']}",
            frames=frames,
            note=note,
        )

    if kind == "seedqr":
        _seedqr_payload(entry.get("words"), entry.get("entropy_hex"))
        raise NotImplementedError  # unreachable

    if kind == "psbt":
        raw_path = REPO_ROOT / entry["from_file"]
        encoding = entry.get("encoding", "auto")
        if not raw_path.exists():
            return Fixture(
                label=label,
                type="psbt",
                payload_preview=f"MISSING raw PSBT file — see warning below",
                frames=["(QR will appear here once the raw PSBT file is placed in test-fixtures/raw/.)"],
                note=note,
                missing_raw_file=raw_path,
            )
        raw = raw_path.read_bytes()
        strategy = encoding if encoding != "auto" else bbqr_encode.recommend_single_vs_multi(len(raw))[0]
        if strategy == "base64":
            import base64 as b64
            payload = b64.b64encode(raw).decode("ascii")
            frames = [qr_ascii.render(payload)]
            preview = f"Base64 PSBT · {len(raw)} bytes raw → {len(payload)} chars base64"
            return Fixture(label=label, type="psbt", payload_preview=preview, frames=frames, note=note)
        if strategy == "binary":
            frames = [qr_ascii.render(raw)]
            return Fixture(
                label=label, type="psbt",
                payload_preview=f"Binary PSBT · {len(raw)} bytes",
                frames=frames, note=note,
            )
        if strategy in ("bbqr", "single"):
            # For 'single' and we fell here, that means recommend said single was fine — but caller
            # specified bbqr explicitly or we're in auto with a large payload.
            bbqr_frames = bbqr_encode.encode(raw, file_type="P")
            ascii_frames = [qr_ascii.render(f) for f in bbqr_frames]
            return Fixture(
                label=label, type="psbt",
                payload_preview=f"BBQr base32 · {len(raw)} bytes raw · {len(bbqr_frames)} frames",
                frames=ascii_frames, note=note, bbqr_raw_frames=bbqr_frames,
            )
        raise ValueError(f"fixture {label!r}: unknown encoding {encoding!r}")

    raise ValueError(f"fixture {label!r}: unknown type {kind!r}")


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


MARKER_RE = re.compile(r"<!--\s*QR:([A-Za-z0-9_\-]+)\s*-->")


def render_fixture_block(f: Fixture) -> str:
    """Build the markdown block that replaces a `<!-- QR:label -->` marker."""
    parts: list[str] = []
    parts.append(f"**Payload:** `{f.payload_preview}`")
    if f.note:
        parts.append(f"> {f.note}")
    parts.append("")

    if len(f.frames) == 1:
        parts.append("```text")
        parts.append(f.frames[0])
        parts.append("```")
    else:
        # Multi-frame BBQr: one fenced block per frame, with a header.
        parts.append(f"_{len(f.frames)}-frame BBQr — scroll through all frames while the webcam is pointed at the screen._")
        parts.append("")
        for i, frame in enumerate(f.frames, start=1):
            parts.append(f"**Frame {i} / {len(f.frames)}**")
            parts.append("")
            parts.append("```text")
            parts.append(frame)
            parts.append("```")
            parts.append("")

    if f.missing_raw_file is not None:
        parts.append("")
        parts.append(
            f"> ⚠️  **Missing raw PSBT**: place the hand-built binary at `{f.missing_raw_file.relative_to(REPO_ROOT)}` then rerun `python3 scripts/gen-test-plan.py`."
        )

    return "\n".join(parts)


def expand_template(template_text: str, fixtures: dict[str, Fixture]) -> tuple[str, set[str]]:
    used: set[str] = set()
    missing: list[str] = []

    def repl(match: re.Match[str]) -> str:
        label = match.group(1)
        if label not in fixtures:
            missing.append(label)
            return f"<!-- UNRESOLVED QR:{label} -->"
        used.add(label)
        return render_fixture_block(fixtures[label])

    out = MARKER_RE.sub(repl, template_text)
    if missing:
        raise SystemExit(
            "Unresolved QR markers in template (no matching fixture): "
            + ", ".join(sorted(set(missing)))
        )
    return out, used


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--manifest", type=Path, default=MANIFEST)
    ap.add_argument("--template", type=Path, default=TEMPLATE)
    ap.add_argument("--out", type=Path, default=OUTPUT)
    ap.add_argument(
        "--stats",
        action="store_true",
        help="print per-fixture QR size stats",
    )
    args = ap.parse_args()

    with args.manifest.open() as f:
        manifest = yaml.safe_load(f)

    fixtures: dict[str, Fixture] = {}
    for entry in manifest.get("fixtures") or []:
        fix = prepare_fixture(entry)
        if fix.label in fixtures:
            raise SystemExit(f"duplicate fixture label: {fix.label}")
        fixtures[fix.label] = fix

    template_text = args.template.read_text()
    rendered, used = expand_template(template_text, fixtures)

    unused = set(fixtures) - used
    for label in sorted(unused):
        print(f"warning: fixture {label!r} defined in manifest but unused in template", file=sys.stderr)

    args.out.write_text(rendered)
    print(f"wrote {args.out.relative_to(REPO_ROOT)}  ({len(rendered)} bytes)")

    if args.stats:
        print("\nFixture sizes:")
        for label, fix in fixtures.items():
            frame_count = len(fix.frames)
            widths = [max((len(line) for line in f.splitlines()), default=0) for f in fix.frames]
            max_w = max(widths) if widths else 0
            missing = " [MISSING]" if fix.missing_raw_file else ""
            print(f"  {label:40s} frames={frame_count:3d} max_cols={max_w:3d}{missing}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
