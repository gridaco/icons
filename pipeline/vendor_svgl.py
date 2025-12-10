import json
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
    # map by route strings (strip leading slash)
    by_route = {}
    for rec in data_records:
        route_val = rec.get("route")
        if isinstance(route_val, str):
            by_route[route_val.lstrip("/")] = rec
        elif isinstance(route_val, dict):
            for v in route_val.values():
                by_route[str(v).lstrip("/")] = rec

    svg_files = list(target_dir.glob("*.svg"))

    click.echo(f"Found {len(svg_files)} SVG files in {target_dir}")

    records = []
    for svg_file in svg_files:
        rel = svg_file.relative_to(target_dir)
        key = str(rel)
        matched = by_route.get(key)
        svg_meta = parse_svg_basic(svg_file)
        records.append(
            {
                "file": svg_file.name,
                "path": str(svg_file.relative_to(base_dir)),
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
