"""
Per-icon text-metadata enrichment.

Reads the vendor-native metadata cache (``dist/.cache/<vendor>/metadata.json``),
dedupes variants down to one **logical icon** per name, renders a representative
variant to PNG, asks the local vision model for a description (+ tags where the
vendor ships none), and writes a committed record per logical name to
``pipeline/enrichment/<vendor>.json``.

Native vendor tags are always preserved; the LLM only fills missing tags and
always supplies the description.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Iterable

import click

import llm
from render import render_for

# Vendor processors (used to (re)build the metadata cache on demand).
from vendor_radix_ui_icons import process as _p_radix
from vendor_heroicons import process as _p_heroicons
from vendor_lucide_icons import process as _p_lucide
from vendor_phosphor_icons import process as _p_phosphor
from vendor_octicons import process as _p_octicons

PIPELINE_DIR = Path(__file__).parent
ROOT = PIPELINE_DIR.parent
CACHE_DIR = ROOT / "dist" / ".cache"
VENDOR_DIR = ROOT / "vendor"
ENRICH_DIR = PIPELINE_DIR / "enrichment"

REV = 1

# In-scope vendors (svgl logos are intentionally out of scope this pass).
VENDORS = [
    "radix-ui-icons",
    "heroicons",
    "lucide-icons",
    "phosphor-icons",
    "octicons",
]

_PROCESSORS = {
    "radix-ui-icons": _p_radix,
    "heroicons": _p_heroicons,
    "lucide-icons": _p_lucide,
    "phosphor-icons": _p_phosphor,
    "octicons": _p_octicons,
}


# --- native-tag extraction ---------------------------------------------------
def _native_tags(vendor: str, rec: dict) -> list[str]:
    if vendor == "lucide-icons":
        meta = rec.get("meta") or {}
        return list(meta.get("tags") or []) + list(meta.get("categories") or [])
    if vendor == "phosphor-icons":
        meta = rec.get("meta") or {}
        return list(meta.get("tags") or [])
    if vendor == "octicons":
        return list(rec.get("keywords") or [])
    return []  # radix-ui-icons, heroicons


# --- representative-variant selection ----------------------------------------
def _pref_rank(vendor: str, rec: dict) -> int:
    """Lower is more preferred when areas tie (cleanest canonical variant)."""
    props = rec.get("properties") or {}
    if vendor == "heroicons":
        return 0 if rec.get("style") == "outline" else 1
    if vendor == "phosphor-icons":
        return 0 if props.get("weight") == "regular" else 1
    return 0


def _area(rec: dict) -> float:
    svg = rec.get("svg") or {}
    return (svg.get("width") or 0) * (svg.get("height") or 0)


def _representative(vendor: str, recs: list[dict]) -> dict:
    # Largest viewBox area first, then vendor preference, then stable by path.
    return sorted(
        recs,
        key=lambda r: (-_area(r), _pref_rank(vendor, r), r.get("path", "")),
    )[0]


# --- metadata loading --------------------------------------------------------
def ensure_metadata(vendor: str) -> Path:
    """Return the vendor metadata.json path, building the cache if absent."""
    meta_path = CACHE_DIR / vendor / "metadata.json"
    if not meta_path.exists():
        click.echo(f"  cache miss for {vendor}; building metadata...")
        _PROCESSORS[vendor].callback(out=CACHE_DIR / vendor)
    return meta_path


class LogicalIcon:
    __slots__ = ("name", "svg_path", "native_tags")

    def __init__(self, name: str, svg_path: Path, native_tags: list[str]):
        self.name = name
        self.svg_path = svg_path
        self.native_tags = native_tags


def load_logical_icons(vendor: str) -> list[LogicalIcon]:
    """Dedupe vendor metadata to one LogicalIcon per name (sorted by name)."""
    meta_path = ensure_metadata(vendor)
    records = json.loads(meta_path.read_text())
    by_name: dict[str, list[dict]] = {}
    for rec in records:
        name = rec.get("name")
        if name:
            by_name.setdefault(name, []).append(rec)

    icons: list[LogicalIcon] = []
    for name in sorted(by_name):
        recs = by_name[name]
        rep = _representative(vendor, recs)
        svg_path = VENDOR_DIR / vendor / rep["path"]
        # Native tags merged across all variants of this logical icon.
        tags: list[str] = []
        for r in recs:
            tags.extend(_native_tags(vendor, r))
        icons.append(LogicalIcon(name, svg_path, llm.normalize_tags(tags)))
    return icons


# --- persistence -------------------------------------------------------------
def load_records(vendor: str) -> dict[str, dict]:
    path = ENRICH_DIR / f"{vendor}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return {}
    return {}


def save_records(vendor: str, records: dict[str, dict]) -> None:
    ENRICH_DIR.mkdir(parents=True, exist_ok=True)
    path = ENRICH_DIR / f"{vendor}.json"
    ordered = {k: records[k] for k in sorted(records)}
    path.write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n")


# --- core --------------------------------------------------------------------
def enrich_vendor(
    vendor: str,
    model: str = llm.DEFAULT_MODEL,
    only_missing: bool = True,
    force: bool = False,
    limit: int | None = None,
    png_size: int = 384,
    on_render: Callable[[str], None] | None = None,
) -> dict[str, dict]:
    """
    Enrich one vendor. Resumable: existing keys are skipped unless ``force``.
    Flushes to disk every few icons so a long run can be interrupted safely.
    Returns the full records map for the vendor.
    """
    icons = load_logical_icons(vendor)
    records = {} if force else load_records(vendor)

    todo = [
        ic
        for ic in icons
        if force or not (only_missing and ic.name in records)
    ]
    if limit is not None:
        todo = todo[:limit]

    flush_every = 10
    done = 0
    with click.progressbar(todo, label=f"enrich {vendor}", show_pos=True) as bar:
        for ic in bar:
            try:
                png = render_for(
                    vendor, ic.name, ic.svg_path, size=png_size, force=force
                )
                if on_render:
                    on_render(str(png))
                need_tags = not ic.native_tags
                out = llm.generate(
                    png,
                    ic.name,
                    vendor,
                    need_tags=need_tags,
                    model=model,
                    # Ground the description with native tags when we have them.
                    hint_tags=ic.native_tags or None,
                )
            except (llm.LLMError, Exception) as e:  # keep going, log the gap
                click.echo(f"\n  SKIP {vendor}/{ic.name}: {e}", err=True)
                continue

            if ic.native_tags:
                tags = ic.native_tags
                tags_source = "vendor"
            else:
                tags = out["tags"]
                tags_source = "llm"

            records[ic.name] = {
                "description": out["description"],
                "tags": tags,
                "tags_source": tags_source,
                "description_source": "llm",
                "model": model,
                "rev": REV,
            }
            done += 1
            if done % flush_every == 0:
                save_records(vendor, records)

    save_records(vendor, records)
    return records


def coverage(vendor: str) -> tuple[int, int, list[str]]:
    """Return (enriched, unique, missing_names) for a vendor."""
    icons = load_logical_icons(vendor)
    names = [ic.name for ic in icons]
    records = load_records(vendor)
    missing = [n for n in names if n not in records]
    return len(names) - len(missing), len(names), missing
