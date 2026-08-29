"""Light-theme acceptance tests for style.css (lighttheme lane).

Verifies:
1. A single @media (prefers-color-scheme: light) block exists at the end
   of style.css, overriding EVERY token defined in :root.
2. The light palette passes WCAG contrast thresholds:
   - text-primary  on bg-primary >= 7:1   (body text)
   - text-secondary on bg-primary >= 4.5:1
   - gold          on bg-primary >= 3:1   (large text / UI)
   - nav link color (text-secondary) >= 4.5:1
3. Zero existing lines were modified: the original dark rules are still
   present verbatim and the pre-append file content is an exact prefix.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import os

_REPO_DEFAULT = "/Volumes/external_drive/Git/projects/ongoing/DAF/docxology"
REPO = Path(os.environ.get("DOCXOLOGY_ROOT", _REPO_DEFAULT))
STYLE = REPO / "style.css"

# sha256 of style.css exactly as it was before the light block was
# appended (1463 lines, base commit 94bd3699).
DARK_PREFIX_SHA256 = "4f0c2e92af3e3ce8a3061423949c6a617f5a44f1f4c707e4643fd5547aa14f98"
DARK_PREFIX_LINES = 1463

# Verbatim dark :root tokens that must be untouched.
DARK_TOKENS = [
    "--bg-primary:    #0a0908;",
    "--text-primary:  #f4f1ea;",
    "--gold:          #e8e2d4;",
    "--paper-line:    rgba(244,241,234,0.2);",
]

# Expected light values (must match the appended block).
LIGHT_EXPECTED = {
    "--bg-primary": "#faf8f4",
    "--bg-secondary": "#f1ede4",
    "--bg-card": "rgba(255,255,255,0.97)",
    "--bg-glass": "rgba(20,18,16,0.03)",
    "--text-primary": "#1a1713",
    "--text-secondary": "#4a4338",
    "--text-muted": "#6b6459",
    "--red": "#c0392b",
    "--red-bright": "#a93226",
    "--red-pure": "#b3392b",
    "--red-glow": "rgba(192,57,43,0.12)",
    "--gold": "#7a5c10",
    "--gold-bright": "#5f4700",
    "--gold-glow": "rgba(122,92,16,0.12)",
    "--gold-03": "rgba(122,92,16,0.03)",
    "--gold-04": "rgba(122,92,16,0.04)",
    "--gold-05": "rgba(122,92,16,0.05)",
    "--gold-07": "rgba(122,92,16,0.07)",
    "--gold-08": "rgba(122,92,16,0.08)",
    "--gold-10": "rgba(122,92,16,0.1)",
    "--gold-12": "rgba(122,92,16,0.12)",
    "--gold-15": "rgba(122,92,16,0.15)",
    "--gold-18": "rgba(122,92,16,0.18)",
    "--gold-20": "rgba(122,92,16,0.2)",
    "--gold-30": "rgba(122,92,16,0.3)",
    "--gold-35": "rgba(122,92,16,0.35)",
    "--gold-40": "rgba(122,92,16,0.4)",
    "--gold-60": "rgba(122,92,16,0.6)",
    "--silver": "#5c574d",
    "--silver-bright": "#1a1713",
    "--border": "rgba(26,23,19,0.2)",
    "--border-hover": "rgba(192,57,43,0.6)",
    "--radius": "3px",
    "--paper-line": "rgba(26,23,19,0.25)",
    "--paper-soft": "rgba(26,23,19,0.05)",
    "--art-a": 'url("assets/hero-art/ant-head.webp")',
    "--art-b": 'url("assets/hero-art/decentral-antelligence-agency.webp")',
    "--art-c": 'url("assets/hero-art/mesh-network.webp")',
    "--art-d": 'url("assets/hero-art/an-ant-is-a-colony.webp")',
    "--art-e": 'url("assets/hero-art/army-ants.webp")',
}


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _contrast(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    l1, l2 = sorted((_relative_luminance(fg), _relative_luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    return tuple(int(v[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _light_block(text: str) -> str:
    """Return the appended light-theme block (from its marker comment)."""
    marker = "/* ── LIGHT THEME (prefers-color-scheme: light) ──"
    idx = text.index(marker)
    return text[idx:]


def test_dark_rules_untouched_prefix_hash() -> None:
    """The original file content is an exact, unmodified prefix."""
    text = STYLE.read_text(encoding="utf-8")
    prefix = "\n".join(text.split("\n")[:DARK_PREFIX_LINES]) + "\n"
    assert (
        hashlib.sha256(prefix.encode("utf-8")).hexdigest() == DARK_PREFIX_SHA256
    ), "pre-existing style.css content was modified"


def test_dark_tokens_verbatim() -> None:
    text = STYLE.read_text(encoding="utf-8")
    for token in DARK_TOKENS:
        assert token in text, f"dark token missing or altered: {token}"


def test_single_light_media_block_appended() -> None:
    text = STYLE.read_text(encoding="utf-8")
    assert text.count("@media (prefers-color-scheme: light)") == 1
    block = _light_block(text)
    # The block must live after the original file (append-only).
    idx = text.index(block)
    assert idx > DARK_PREFIX_LINES, "light block must be appended at end"
    # Forced-colors and print blocks still present.
    assert "@media (forced-colors: active)" in text
    assert "@media print" in text


def test_all_root_tokens_overridden() -> None:
    text = STYLE.read_text(encoding="utf-8")
    root = re.search(r":root\s*\{(.*?)\n\s*\}", text, re.DOTALL)
    assert root, "dark :root block not found"
    dark_tokens = set(re.findall(r"--[\w-]+(?=\s*:)", root.group(1)))
    block = _light_block(text)
    light_tokens = set(re.findall(r"--[\w-]+(?=\s*:)", block))
    missing = dark_tokens - light_tokens
    assert not missing, f"light block does not override: {sorted(missing)}"
    for token, expected in LIGHT_EXPECTED.items():
        m = re.search(re.escape(token) + r":\s*(.+?);", block)
        assert m and m.group(1).strip() == expected, (
            f"unexpected light value for {token}: {m.group(1).strip() if m else None}"
        )


def test_light_palette_contrast_wcag() -> None:
    bg = _hex_to_rgb(LIGHT_EXPECTED["--bg-primary"])
    text_primary = _hex_to_rgb(LIGHT_EXPECTED["--text-primary"])
    text_secondary = _hex_to_rgb(LIGHT_EXPECTED["--text-secondary"])
    gold = _hex_to_rgb(LIGHT_EXPECTED["--gold"])
    red = _hex_to_rgb(LIGHT_EXPECTED["--red-pure"])

    c_body = _contrast(text_primary, bg)
    c_secondary = _contrast(text_secondary, bg)
    c_gold = _contrast(gold, bg)
    c_nav = c_secondary  # nav links use --text-secondary
    c_red = _contrast(red, bg)

    assert c_body >= 7.0, f"text-primary on bg-primary {c_body:.2f}:1 < 7:1"
    assert c_secondary >= 4.5, f"text-secondary on bg-primary {c_secondary:.2f}:1 < 4.5:1"
    assert c_gold >= 3.0, f"gold on bg-primary {c_gold:.2f}:1 < 3:1"
    assert c_nav >= 4.5
    # Link color (a{color:var(--red-pure)}) should also clear 4.5:1.
    assert c_red >= 4.5, f"link red on bg-primary {c_red:.2f}:1 < 4.5:1"
