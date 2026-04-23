"""Minimal BBQr (Better Bitcoin QR) encoder.

BBQr protocol: https://github.com/coinkite/BBQr

Frame format (all ASCII):
    "B$" + encoding(1) + file_type(1) + total(2, base36) + index(2, base36) + payload

- encoding: 'H' hex / '2' base32 / 'Z' base32+zlib
- file_type: 'P' PSBT / 'T' Tx / 'J' JSON / 'U' Unicode
- total, index: 2 chars each, base36 (0-9A-Z), value 0..1295

This encoder is intentionally minimal: base32 only (encoding='2'), no
compression. The firmware's BBQr parser (components/bbqr/src/bbqr.c)
accepts this.
"""

from __future__ import annotations

import base64

BBQR_MAGIC = "B$"
BASE36_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
HEADER_LEN = 8
MAX_PARTS = 1296  # 36^2


def _base36_2(n: int) -> str:
    if not 0 <= n < MAX_PARTS:
        raise ValueError(f"base36_2 value out of range: {n}")
    return BASE36_ALPHABET[n // 36] + BASE36_ALPHABET[n % 36]


def _base32_encode_no_pad(data: bytes) -> str:
    """RFC4648 base32 without trailing '=' padding (BBQr strips padding)."""
    return base64.b32encode(data).decode("ascii").rstrip("=")


def encode(
    data: bytes,
    *,
    file_type: str = "P",
    chunks: int | None = None,
    max_chunk_bytes: int = 400,
) -> list[str]:
    """Split `data` into BBQr frames (base32, no compression).

    If `chunks` is given, that exact number of frames is produced (equal-sized
    except the last). Otherwise the split is driven by `max_chunk_bytes` (max
    bytes per frame *before* base32 encoding) so the resulting base32 string
    fits comfortably in a single QR.

    Returns a list of ASCII strings, one per QR frame.
    """
    if len(file_type) != 1:
        raise ValueError("file_type must be exactly 1 character")

    if chunks is None:
        chunks = max(1, (len(data) + max_chunk_bytes - 1) // max_chunk_bytes)
    if chunks > MAX_PARTS:
        raise ValueError(f"too many chunks: {chunks} > {MAX_PARTS}")

    # Pad each chunk to a base32-aligned boundary (5-byte alignment) so the
    # encoded payload has no padding chars mid-sequence. Only the last chunk
    # may be short.
    chunk_size = (len(data) + chunks - 1) // chunks
    # Round up to a multiple of 5 bytes so base32 output has no internal '='.
    chunk_size = ((chunk_size + 4) // 5) * 5
    # Re-derive chunks in case rounding changed the count
    if chunk_size > 0:
        chunks = max(1, (len(data) + chunk_size - 1) // chunk_size)

    frames = []
    for i in range(chunks):
        start = i * chunk_size
        end = min(start + chunk_size, len(data))
        chunk = data[start:end]
        payload_b32 = _base32_encode_no_pad(chunk)
        header = BBQR_MAGIC + "2" + file_type + _base36_2(chunks) + _base36_2(i)
        frames.append(header + payload_b32)
    return frames


def recommend_single_vs_multi(
    data_len: int,
    *,
    max_cols: int = 100,
) -> tuple[str, int]:
    """Suggest encoding strategy for a payload of this size.

    Returns `(strategy, n_chunks)` where strategy is 'single' (fits in one QR
    rendered within `max_cols` columns) or 'bbqr' (multi-frame).

    Heuristic: single-QR base64 works up to ~1000 bytes (QR v23 ≈ 113 cols in
    half-blocks). Beyond that, use BBQr with ~400 bytes per chunk.
    """
    base64_len = (data_len + 2) // 3 * 4
    if base64_len <= 700:  # ~QR v18 half-block width ≈ 94 cols
        return "single", 1
    # BBQr base32 encoded chunk: 8 chars header + ceil(chunk_bytes/5)*8
    target_chunk = 400
    n = max(1, (data_len + target_chunk - 1) // target_chunk)
    return "bbqr", n
