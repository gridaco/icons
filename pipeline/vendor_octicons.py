import json
import sys
from pathlib import Path

import click

from utils.svg_utils import parse_svg_basic


def _load_keywords(base_dir: Path) -> dict:
    keywords_path = base_dir / "keywords.json"
    if not keywords_path.exists():
        return {}
    try:
        return json.loads(keywords_path.read_text())
    except Exception:
        return {}


def _base_icon_name(stem: str) -> str:
    # Remove size suffix (-16 or -24). Also handle -inset-16, etc.
    parts = stem.split("-")
    if parts and parts[-1] in {"12", "16", "24", "32", "48", "96"}:
        parts = parts[:-1]
    return "-".join(parts)


def _extract_size_and_inset(stem: str) -> tuple[str | None, bool]:
    """
    From a filename stem like `alert-16` or `accessibility-inset-24`,
    extract size and inset flag.
    """
    parts = stem.split("-")
    size = None
    inset = False
    if parts and parts[-1].isdigit():
        size = parts[-1]
        base_parts = parts[:-1]
        if base_parts and base_parts[-1] == "inset":
            inset = True
    return size, inset


@click.command()
@click.option(
    "--out",
    type=click.Path(path_type=Path),
    default=Path(".cache/octicons"),
    help="Output directory for vendor-native metadata.",
)
def process(out: Path):
    """
    Process Octicons and emit vendor-native metadata.
    """
    click.echo("Processing Octicons...")

    base_dir = Path(__file__).parent.parent / "vendor" / "octicons"
    target_dir = base_dir / "icons"

    if not target_dir.exists():
        click.echo(
            f"PANIC: Required directory {target_dir} does not exist. Vendor structure may have changed.",
            err=True,
        )
        sys.exit(1)

    out.mkdir(parents=True, exist_ok=True)

    keywords_map = _load_keywords(base_dir)
    svg_files = list(target_dir.glob("*.svg"))

    click.echo(f"Found {len(svg_files)} SVG files in {target_dir}")

    records = []
    for svg_file in svg_files:
        stem = svg_file.stem
        base_name = _base_icon_name(stem)
        size, inset = _extract_size_and_inset(stem)
        svg_meta = parse_svg_basic(svg_file)
        dist_rel = Path("src") / svg_file.name
        variables = {"size": size} if size else {}
        records.append(
            {
                "name": base_name,
                "file": stem,
                "dist_path": str(dist_rel),
                "path": str(svg_file.relative_to(base_dir)),
                "keywords": keywords_map.get(base_name, []),
                "size": size,
                "inset": inset,
                "properties": variables,
                "svg": svg_meta,
            }
        )

    out_file = out / "metadata.json"
    out_file.write_text(json.dumps(records, indent=2))
    click.echo(f"Wrote {len(records)} records to {out_file}")
