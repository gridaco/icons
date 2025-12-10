import json
import re
import sys
from pathlib import Path
from typing import Dict, List

import click

from utils.svg_utils import parse_svg_basic


def _parse_icons_ts(ts_path: Path) -> Dict[str, Dict]:
    """
    Lightweight parser for phosphor src/icons.ts.
    Extracts name, categories (enum names), tags, codepoint, alias, published_in, updated_in.
    """
    if not ts_path.exists():
        return {}
    text = ts_path.read_text()
    # Narrow to the icons array
    start = text.find("export const icons =")
    if start == -1:
        return {}
    segment = text[start:]
    entries: Dict[str, Dict] = {}
    # Regex to capture blocks { ... }
    pattern = re.compile(r"\{\s*name:\s*\"(?P<name>[^\"]+)\".*?\}", re.DOTALL)
    for match in pattern.finditer(segment):
        block = match.group(0)
        name = match.group("name")
        record: Dict[str, any] = {"name": name}
        # tags
        tags_match = re.search(r"tags:\s*\[([^\]]*)\]", block, re.DOTALL)
        if tags_match:
            tags_raw = tags_match.group(1)
            tags = [
                t.strip().strip('"')
                for t in tags_raw.split(",")
                if t.strip().strip('"')
            ]
            record["tags"] = tags
        # categories
        cat_match = re.search(r"categories:\s*\[([^\]]*)\]", block, re.DOTALL)
        if cat_match:
            cats_raw = cat_match.group(1)
            cats = []
            for c in cats_raw.split(","):
                c = c.strip()
                if c.startswith("IconCategory."):
                    cats.append(c.replace("IconCategory.", "").lower())
            record["categories"] = cats
        # alias
        alias_match = re.search(r"alias:\s*\{\s*name:\s*\"([^\"]+)\"", block)
        if alias_match:
            record["alias"] = alias_match.group(1)
        # codepoint
        code_match = re.search(r"codepoint:\s*([0-9]+)", block)
        if code_match:
            record["codepoint"] = int(code_match.group(1))
        # published_in
        pub_match = re.search(r"published_in:\s*([0-9.]+)", block)
        if pub_match:
            record["published_in"] = float(pub_match.group(1))
        # updated_in
        upd_match = re.search(r"updated_in:\s*([0-9.]+)", block)
        if upd_match:
            record["updated_in"] = float(upd_match.group(1))
        entries[name] = record
    return entries


@click.command()
@click.option(
    "--out",
    type=click.Path(path_type=Path),
    default=Path(".cache/phosphor-icons"),
    help="Output directory for vendor-native metadata.",
)
def process(out: Path):
    """
    Process Phosphor Icons and emit vendor-native metadata.
    """
    click.echo("Processing Phosphor Icons...")

    base_dir = Path(__file__).parent.parent / "vendor" / "phosphor-icons"
    assets_dir = base_dir / "assets"
    icons_ts = base_dir / "src" / "icons.ts"

    if not assets_dir.exists():
        click.echo(
            f"PANIC: Required directory {assets_dir} does not exist. Vendor structure may have changed.",
            err=True,
        )
        sys.exit(1)

    out.mkdir(parents=True, exist_ok=True)

    meta_map = _parse_icons_ts(icons_ts)
    weights = ["bold", "duotone", "fill", "light", "regular", "thin"]

    total_found = 0
    records: List[Dict] = []

    for weight in weights:
        target_dir = assets_dir / weight
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

        for svg_file in svg_files:
            stem = svg_file.stem  # includes weight suffix for non-regular
            base_name = stem if weight == "regular" else stem.removesuffix(f"-{weight}")
            meta = meta_map.get(base_name, {})
            svg_meta = parse_svg_basic(svg_file)
            records.append(
                {
                    "name": base_name,
                    "weight": weight,
                    "path": str(svg_file.relative_to(base_dir)),
                    "svg": svg_meta,
                    "meta": meta,
                }
            )

    out_file = out / "metadata.json"
    out_file.write_text(json.dumps(records, indent=2))
    click.echo(f"Total Phosphor Icons found: {total_found}")
    click.echo(f"Wrote {len(records)} records to {out_file}")
