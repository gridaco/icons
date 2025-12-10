import json
import sys
from pathlib import Path

import click

from utils.svg_utils import parse_svg_basic


@click.command()
@click.option(
    "--out",
    type=click.Path(path_type=Path),
    default=Path(".cache/heroicons"),
    help="Output directory for vendor-native metadata.",
)
def process(out: Path):
    """
    Process Heroicons.
    """
    click.echo("Processing Heroicons...")

    base_dir = Path(__file__).parent.parent / "vendor" / "heroicons"
    src_dir = base_dir / "src"

    if not src_dir.exists():
        click.echo(
            f"PANIC: Required directory {src_dir} does not exist. Vendor structure may have changed.",
            err=True,
        )
        sys.exit(1)

    out.mkdir(parents=True, exist_ok=True)

    # Heroicons has multiple variants in src/
    variants = ["16/solid", "20/solid", "24/solid", "24/outline"]

    total_found = 0
    records = []

    for variant in variants:
        target_dir = src_dir / variant
        if not target_dir.exists():
            click.echo(
                f"PANIC: Required directory {target_dir} does not exist. Vendor structure may have changed.",
                err=True,
            )
            sys.exit(1)

        svg_files = list(target_dir.glob("*.svg"))
        count = len(svg_files)
        total_found += count
        click.echo(f"Found {count} SVG files in {target_dir}")

        size, style = variant.split("/")
        for svg_file in svg_files:
            stem = svg_file.stem
            svg_meta = parse_svg_basic(svg_file)
            records.append(
                {
                    "name": stem,
                    "size": size,
                    "style": style,
                    "path": str(svg_file.relative_to(base_dir)),
                    "svg": svg_meta,
                }
            )

    out_file = out / "metadata.json"
    out_file.write_text(json.dumps(records, indent=2))
    click.echo(f"Total Heroicons found: {total_found}")
    click.echo(f"Wrote {len(records)} records to {out_file}")
