import json
import re
import sys
from pathlib import Path

import click
import json5

from utils.svg_utils import parse_svg_basic


def _parse_svgs_ts(ts_path: Path) -> list:
    """
    Parse svgl src/data/svgs.ts into Python objects using json5.
    Keeps vendor-native fields: title, category, route, wordmark, url, brandUrl, shadcnCommand.
    """
    if not ts_path.exists():
        return []
    text = ts_path.read_text()
    # Drop import lines
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("import ")]
    cleaned = "\n".join(lines)
    anchor = cleaned.find("export const svgs")
    if anchor == -1:
        return []
    eq = cleaned.find("=", anchor)
    start = cleaned.find("[", eq if eq != -1 else anchor)
    end = cleaned.rfind("]")
    if start == -1 or end == -1:
        return []
    array_text = cleaned[start : end + 1]
    try:
        return json5.loads(array_text)
    except Exception:
        return []


def _infer_theme_kind(stem: str) -> tuple[str | None, str]:
    """
    Infer theme (light/dark/None) and kind (wordmark/symbol) from filename stem.
    Splits on ., -, _ and checks tokens.
    """
    tokens = re.split(r"[._-]+", stem.lower())
    theme = "light"  # default
    if "dark" in tokens:
        theme = "dark"
    elif "light" in tokens:
        theme = "light"
    kind = "wordmark" if "wordmark" in tokens else "symbol"
    return theme, kind


def _build_asset_maps(
    data_records: list,
) -> tuple[dict[str, dict], dict[str, dict[str, str]]]:
    """
    Build lookup maps from parsed svgs.ts records.

    Source of truth:
    - theme comes from the JSON key (route.light/route.dark, wordmark.light/wordmark.dark)
    - kind comes from whether the asset is referenced by route (symbol) or wordmark (wordmark)
    """

    def _norm_asset_path(v: object) -> str | None:
        if not isinstance(v, str):
            return None
        s = v.strip()
        if not s:
            return None
        return s.lstrip("/")

    record_by_asset_path: dict[str, dict] = {}
    properties_by_asset_path: dict[str, dict[str, str]] = {}

    def _register(asset_path: str | None, rec: dict, theme: str, kind: str):
        if not asset_path:
            return
        # keep first record/properties if duplicates exist
        record_by_asset_path.setdefault(asset_path, rec)
        properties_by_asset_path.setdefault(asset_path, {"theme": theme, "kind": kind})

    for rec in data_records:
        if not isinstance(rec, dict):
            continue

        route_val = rec.get("route")
        if isinstance(route_val, str):
            _register(_norm_asset_path(route_val), rec, theme="light", kind="symbol")
        elif isinstance(route_val, dict):
            for k, v in route_val.items():
                theme = str(k) if str(k) in ("light", "dark") else "light"
                _register(_norm_asset_path(v), rec, theme=theme, kind="symbol")

        wordmark_val = rec.get("wordmark")
        if isinstance(wordmark_val, str):
            _register(
                _norm_asset_path(wordmark_val), rec, theme="light", kind="wordmark"
            )
        elif isinstance(wordmark_val, dict):
            for k, v in wordmark_val.items():
                theme = str(k) if str(k) in ("light", "dark") else "light"
                _register(_norm_asset_path(v), rec, theme=theme, kind="wordmark")

    return record_by_asset_path, properties_by_asset_path


@click.command()
@click.option(
    "--out",
    type=click.Path(path_type=Path),
    default=Path(".cache/svgl"),
    help="Output directory for vendor-native metadata.",
)
def process(out: Path):
    """
    Process SVGL and emit vendor-native metadata.
    """
    click.echo("Processing SVGL...")

    base_dir = Path(__file__).parent.parent / "vendor" / "svgl"
    target_dir = base_dir / "static" / "library"
    data_ts = base_dir / "src" / "data" / "svgs.ts"

    if not target_dir.exists():
        click.echo(
            f"PANIC: Required directory {target_dir} does not exist. Vendor structure may have changed.",
            err=True,
        )
        sys.exit(1)

    out.mkdir(parents=True, exist_ok=True)

    data_records = _parse_svgs_ts(data_ts)
    record_by_asset_path, properties_by_asset_path = _build_asset_maps(data_records)

    svg_files = list(target_dir.glob("*.svg"))

    click.echo(f"Found {len(svg_files)} SVG files in {target_dir}")

    records = []
    for svg_file in svg_files:
        # svgs.ts uses "/library/<file>.svg" while files live at "static/library/<file>.svg"
        asset_key = f"library/{svg_file.name}"
        matched = record_by_asset_path.get(asset_key)
        svg_meta = parse_svg_basic(svg_file)
        props = properties_by_asset_path.get(asset_key)
        if not props:
            theme, kind = _infer_theme_kind(svg_file.stem)
            props = {"theme": theme, "kind": kind}
        else:
            theme = props.get("theme", "light")
            kind = props.get("kind", "symbol")
        dist_rel = Path("src") / svg_file.name
        records.append(
            {
                "file": svg_file.name,
                "path": str(svg_file.relative_to(base_dir)),
                "dist_path": str(dist_rel),
                "theme": theme,
                "kind": kind,
                "properties": props,
                "svg": svg_meta,
                "meta": matched,
            }
        )

    # Write detailed records keyed by file
    out_file = out / "metadata.json"
    out_file.write_text(json.dumps(records, indent=2))

    # Also write the raw parsed data array (vendor-native)
    data_file = out / "data.json"
    data_file.write_text(json.dumps(data_records, indent=2))

    click.echo(f"Wrote {len(records)} records to {out_file}")
    click.echo(f"Wrote parsed svgs.ts data to {data_file}")
