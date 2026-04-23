"""Half-block ASCII QR renderer.

Renders a QR code as a string using Unicode half-block characters
(`█ ▀ ▄ ` + space) so two vertical QR modules map to one text row.
The result fits in a markdown fenced code block and — viewed in a
monospace font with tight line height — is scannable by a camera
pointed at the screen.
"""

from __future__ import annotations

import io

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M


class QrTooLargeError(ValueError):
    """Raised when a payload exceeds QR version 40 capacity."""


def render(
    payload: bytes | str,
    *,
    error_correction: int = ERROR_CORRECT_M,
    border: int = 2,
) -> str:
    """Return the QR rendered as half-block ASCII text (no trailing newline).

    `payload` may be bytes or str. `qrcode` selects the version automatically;
    if the payload exceeds version 40 capacity the library raises
    `qrcode.exceptions.DataOverflowError`, which we wrap in `QrTooLargeError`
    with a size hint.
    """
    q = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=1,
        border=border,
    )
    if isinstance(payload, bytes):
        # Force 8-bit binary mode.
        q.add_data(payload, optimize=0)
    else:
        q.add_data(payload)
    try:
        q.make(fit=True)
    except qrcode.exceptions.DataOverflowError as exc:
        raise QrTooLargeError(
            f"payload is {len(payload)} bytes — exceeds QR version 40 at "
            f"EC level {error_correction}. Try BBQr multi-frame."
        ) from exc

    buf = io.StringIO()
    # Non-inverted rendering: dark QR modules map to `█` (both halves filled)
    # and light modules to `\xa0` (blank). On a light-theme editor the text
    # foreground is black, so `█` renders as dark and `\xa0` (space) renders
    # as light — i.e. the QR appears in its standard orientation.
    #
    # On a dark-theme editor the polarity is reversed. Most webcam QR
    # scanners (zbar, zxing) handle both polarities, so either works in
    # practice — but light theme is the safer default. The test plan's
    # section 0 tells the tester which.
    q.print_ascii(out=buf, tty=False, invert=False)
    # Swap non-breaking spaces for regular ones so text editors render
    # them as plain whitespace (no special glyph, no line-break quirks).
    text = buf.getvalue().replace("\xa0", " ")
    # Trim any trailing newline for predictable embedding.
    return text.rstrip("\n")


def module_size(text: str) -> tuple[int, int]:
    """Return `(cols, rows_of_text)` of the rendered QR string."""
    lines = text.splitlines() or [""]
    cols = max(len(line) for line in lines)
    return cols, len(lines)


def try_render_with_fallback(payload: bytes | str) -> tuple[str, int]:
    """Render with EC_M; if over 100 cols, retry with EC_L (smaller QR)."""
    text = render(payload, error_correction=ERROR_CORRECT_M)
    cols, _ = module_size(text)
    if cols > 100:
        text = render(payload, error_correction=ERROR_CORRECT_L)
    return text, module_size(text)[0]
