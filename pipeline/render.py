"""
SVG -> PNG rendering for LLM vision enrichment.

Renders an icon SVG to a black-on-white PNG using `rsvg-convert` (librsvg),
which is documented as a system prerequisite in the pipeline README. Output is
cached under ``pipeline/.cache/png/<vendor>/<name>.png`` (gitignored) so repeat
runs skip work.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

PIPELINE_DIR = Path(__file__).parent
PNG_CACHE_DIR = PIPELINE_DIR / ".cache" / "png"

_RSVG = shutil.which("rsvg-convert")


class RenderError(RuntimeError):
    """Raised when an SVG could not be rasterized."""


def _ensure_renderer() -> str:
    if _RSVG is None:
        raise RenderError(
            "rsvg-convert not found. Install librsvg (e.g. `brew install librsvg`). "
            "See pipeline/README.md."
        )
    return _RSVG


def render_png(svg_path: Path, out_path: Path, size: int = 384) -> Path:
    """
    Rasterize ``svg_path`` to ``out_path`` as a ``size`` x ``size`` PNG on a
    solid white background. Most vendor icons use ``currentColor`` / black
    strokes, so a white background yields a legible black-on-white glyph.

    Returns the output path. Raises ``RenderError`` on failure.
    """
    rsvg = _ensure_renderer()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        rsvg,
        "-w",
        str(size),
        "-h",
        str(size),
        "--keep-aspect-ratio",
        "-b",
        "white",
        "-o",
        str(out_path),
        str(svg_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not out_path.exists():
        raise RenderError(
            f"rsvg-convert failed for {svg_path}: {proc.stderr.strip() or 'no output'}"
        )
    return out_path


def render_for(
    vendor: str,
    name: str,
    svg_path: Path,
    size: int = 384,
    force: bool = False,
) -> Path:
    """
    Render the icon to its cached location and return the PNG path. Skips
    rendering when a cached PNG already exists unless ``force`` is set.
    """
    out_path = PNG_CACHE_DIR / vendor / f"{name}.png"
    if out_path.exists() and not force:
        return out_path
    return render_png(svg_path, out_path, size=size)
