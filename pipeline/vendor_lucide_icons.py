import json
import sys
from pathlib import Path

import click

from utils.svg_utils import parse_svg_basic


def _load_icon_metadata(json_path: Path) -> dict:
    if not json_path.exists():
        return {}
    try:
        return json.loads(json_path.read_text())
    except Exception:
        return {}


@click.command()
@click.option(
    "--out",
    type=click.Path(path_type=Path),
    default=Path(".cache/lucide-icons"),
    help="Output directory for vendor-native metadata.",
)
def process(out: Path):
    """
    Process Lucide Icons and emit vendor-native metadata.
    """
    click.echo("Processing Lucide Icons...")

    base_dir = Path(__file__).parent.parent / "vendor" / "lucide-icons"
    target_dir = base_dir / "icons"

    if not target_dir.exists():
        click.echo(
            f"PANIC: Required directory {target_dir} does not exist. Vendor structure may have changed.",
            err=True,
        )
        sys.exit(1)

    out.mkdir(parents=True, exist_ok=True)

    svg_files = list(target_dir.glob("*.svg"))
    click.echo(f"Found {len(svg_files)} SVG files in {target_dir}")

    records = []
    for svg_file in svg_files:
        stem = svg_file.stem
        meta_json_path = target_dir / f"{stem}.json"
        icon_meta = _load_icon_metadata(meta_json_path)
        svg_meta = parse_svg_basic(svg_file)
        record = {
            "name": stem,
            "path": str(svg_file.relative_to(base_dir)),
            "dist_path": str(Path("src") / svg_file.name),
            "svg": svg_meta,
            "meta": icon_meta,
            "properties": {},
        }
        records.append(record)

    out_file = out / "metadata.json"
    out_file.write_text(json.dumps(records, indent=2))
    click.echo(f"Wrote {len(records)} records to {out_file}")
