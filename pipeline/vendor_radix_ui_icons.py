import json
import sys
from pathlib import Path

import click

from utils.svg_utils import parse_svg_basic


@click.command()
@click.option(
    "--out",
    type=click.Path(path_type=Path),
    default=Path(".cache/radix-ui-icons"),
    help="Output directory for vendor-native metadata.",
)
def process(out: Path):
    """
    Process Radix UI Icons.
    """
    click.echo("Processing Radix UI Icons...")

    base_dir = Path(__file__).parent.parent / "vendor" / "radix-ui-icons"
    target_dir = base_dir / "packages" / "radix-icons" / "icons"
    manifest_path = base_dir / "packages" / "radix-icons" / "manifest.json"

    if not target_dir.exists():
        click.echo(
            f"PANIC: Required directory {target_dir} does not exist. Vendor structure may have changed.",
            err=True,
        )
        sys.exit(1)

    out.mkdir(parents=True, exist_ok=True)

    manifest = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
        except Exception:
            manifest = {}

    svg_files = list(target_dir.glob("*.svg"))

    click.echo(f"Found {len(svg_files)} SVG files in {target_dir}")

    records = []
    for svg_file in svg_files:
        stem = svg_file.stem
        svg_meta = parse_svg_basic(svg_file)
        records.append(
            {
                "name": stem,
                "path": str(svg_file.relative_to(base_dir)),
                "svg": svg_meta,
                "manifest_path": manifest.get("icons", {}).get(":15", {}).get(stem),
            }
        )

    out_file = out / "metadata.json"
    out_file.write_text(json.dumps(records, indent=2))
    click.echo(f"Wrote {len(records)} records to {out_file}")
