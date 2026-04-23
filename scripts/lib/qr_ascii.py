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
    dark_theme: bool = False,
) -> str:
    """Return the QR rendered as half-block ASCII text (no trailing newline).

    `payload` may be bytes or str. `qrcode` selects the version automatically;
    if the payload exceeds version 40 capacity the library raises
    `qrcode.exceptions.DataOverflowError`, which we wrap in `QrTooLargeError`
    with a size hint.

    Polarity:
    - `dark_theme=False` (default, for light-theme editors): dark QR modules
      map to `█` so they render as dark pixels on a white background —
      standard QR orientation for the camera.
    - `dark_theme=True` (for dark-theme editors): polarity inverted so `█`
      renders as light pixels on a dark background, and the blanks become
      the dark "modules" the QR expects around its finder patterns. Still a
      valid standard-orientation QR from the camera's point of view.

    Without this flag set correctly, the quiet zone around the QR ends up
    the wrong polarity and zbar/zxing often fail to lock on.
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
    # `invert` in qrcode's print_ascii swaps which of (\xa0, ▀, ▄, █) is used
    # for (light/light, dark/light, light/dark, dark/dark). For a dark-theme
    # editor we want the "dark half" to be the BACKGROUND (i.e. rendered as
    # the editor's light foreground char), which corresponds to invert=True.
    q.print_ascii(out=buf, tty=False, invert=dark_theme)
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
