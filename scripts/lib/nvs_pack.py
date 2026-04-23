"""Pack key-value entries into the simulator's NVS binary format.

Format — see `simulator/platform/esp_idf_stubs/nvs_sim.c:113-161`:

    [key_len:1B][key:key_len bytes][type:1B][value_len_lo:1B][value_len_hi:1B][value:value_len bytes]

Types:
    0x01 = u8 (1 byte value)
    0x02 = u16 (2 byte value, little-endian)
    0x03 = blob (value_len bytes)

Each NVS namespace is stored as `<namespace>.nvs` in `sim_data/nvs/`.
"""

from __future__ import annotations

import struct
from pathlib import Path
from typing import Iterable

NVS_TYPE_U8 = 0x01
NVS_TYPE_U16 = 0x02
NVS_TYPE_BLOB = 0x03

NVS_MAX_KEY_LEN = 15  # per ESP-IDF; nvs_sim.c doesn't enforce a tight bound but
# matches ESP-IDF's convention and the loader bails if key_len > NVS_MAX_KEY_LEN.


def _pack_entry(key: str, type_code: int, value: bytes) -> bytes:
    if not key:
        raise ValueError("NVS key cannot be empty")
    if len(key) > NVS_MAX_KEY_LEN:
        raise ValueError(
            f"NVS key {key!r} too long ({len(key)} > {NVS_MAX_KEY_LEN})"
        )
    if len(value) > 0xFFFF:
        raise ValueError(f"NVS value for {key!r} too large: {len(value)} > 65535")
    out = bytearray()
    out.append(len(key))
    out += key.encode("ascii")
    out.append(type_code)
    out += struct.pack("<H", len(value))
    out += value
    return bytes(out)


class Namespace:
    """Builder for a single NVS namespace."""

    def __init__(self, name: str):
        self.name = name
        self._entries: list[tuple[str, int, bytes]] = []

    def set_u8(self, key: str, value: int) -> "Namespace":
        if not 0 <= value <= 0xFF:
            raise ValueError(f"u8 out of range: {value}")
        self._entries.append((key, NVS_TYPE_U8, bytes([value])))
        return self

    def set_u16(self, key: str, value: int) -> "Namespace":
        if not 0 <= value <= 0xFFFF:
            raise ValueError(f"u16 out of range: {value}")
        self._entries.append((key, NVS_TYPE_U16, struct.pack("<H", value)))
        return self

    def set_blob(self, key: str, value: bytes) -> "Namespace":
        self._entries.append((key, NVS_TYPE_BLOB, bytes(value)))
        return self

    def to_bytes(self) -> bytes:
        return b"".join(_pack_entry(k, t, v) for k, t, v in self._entries)


def write_namespace(out_dir: Path, ns: Namespace) -> Path:
    """Write a namespace to `<out_dir>/<ns.name>.nvs` and return the path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{ns.name}.nvs"
    path.write_bytes(ns.to_bytes())
    return path


def write_all(out_dir: Path, namespaces: Iterable[Namespace]) -> list[Path]:
    return [write_namespace(out_dir, ns) for ns in namespaces]


# ---------------------------------------------------------------------------
# Round-trip (used by --selfcheck in the main tool)
# ---------------------------------------------------------------------------


def parse(blob: bytes) -> list[tuple[str, int, bytes]]:
    """Inverse of `Namespace.to_bytes`. Returns `[(key, type, value), ...]`."""
    out = []
    i = 0
    n = len(blob)
    while i < n:
        key_len = blob[i]
        i += 1
        if key_len == 0 or key_len > NVS_MAX_KEY_LEN:
            break  # matches nvs_sim.c:121 early-break behavior
        if i + key_len > n:
            raise ValueError("truncated NVS blob (key)")
        key = blob[i : i + key_len].decode("ascii")
        i += key_len
        if i + 3 > n:
            raise ValueError("truncated NVS blob (type/len)")
        type_code = blob[i]
        value_len = blob[i + 1] | (blob[i + 2] << 8)
        i += 3
        if i + value_len > n:
            raise ValueError("truncated NVS blob (value)")
        value = blob[i : i + value_len]
        i += value_len
        out.append((key, type_code, value))
    return out
