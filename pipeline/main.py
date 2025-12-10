import json
import shutil
from pathlib import Path

import click

from vendor_radix_ui_icons import process as process_radix
from vendor_heroicons import process as process_heroicons
from vendor_lucide_icons import process as process_lucide
from vendor_phosphor_icons import process as process_phosphor
from vendor_octicons import process as process_octicons
from vendor_svgl import process as process_svgl


ROOT = Path(__file__).parent.parent
DIST_DIR = ROOT / "dist"
CACHE_DIR = DIST_DIR / ".cache"


@click.group()
def cli():
    """Root CLI."""
    pass


@click.group()
def cache():
    """
    Cache vendor-native metadata and SVG info.
    """
    pass


# Register individual vendor commands under cache
cache.add_command(process_radix, name="radix-ui-icons")
cache.add_command(process_heroicons, name="heroicons")
cache.add_command(process_lucide, name="lucide-icons")
cache.add_command(process_phosphor, name="phosphor-icons")
cache.add_command(process_octicons, name="octicons")
cache.add_command(process_svgl, name="svgl")


@cache.command(name="all")
@click.pass_context
def cache_all(ctx):
    """
    Run all vendor processors.
    """
    click.echo("Running all processors...")
    ctx.invoke(process_radix, out=CACHE_DIR / "radix-ui-icons")
    click.echo("-" * 20)
    ctx.invoke(process_heroicons, out=CACHE_DIR / "heroicons")
    click.echo("-" * 20)
    ctx.invoke(process_lucide, out=CACHE_DIR / "lucide-icons")
    click.echo("-" * 20)
    ctx.invoke(process_phosphor, out=CACHE_DIR / "phosphor-icons")
    click.echo("-" * 20)
    ctx.invoke(process_octicons, out=CACHE_DIR / "octicons")
    click.echo("-" * 20)
    ctx.invoke(process_svgl, out=CACHE_DIR / "svgl")
    click.echo("All processors finished.")


@cache.command(name="clean")
def cache_clean():
    """
    Remove the .cache directory.
    """
    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)
        click.echo(f"Removed cache directory: {CACHE_DIR}")
    else:
        click.echo("Cache directory not found; nothing to clean.")


def _copy_tree(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    if src.exists():
        shutil.copytree(src, dst)


def _copy_file(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _copy_license(src_dir: Path, dst_dir: Path):
    """
    Copy a license file from src_dir to dst_dir (if present).
    Checks common license filenames.
    """
    for fname in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
        src = src_dir / fname
        if src.exists():
            _copy_file(src, dst_dir / fname)
            return


def _ensure_dist_placeholders():
    """
    Ensure dist directory exists with placeholder files: .gitkeep, README.md.
    (LICENSE is generated from vendor licenses during dist build.)
    """
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    (DIST_DIR / ".gitkeep").write_text("")
    (DIST_DIR / ".gitignore").write_text(".cache/\n")
    templates_dir = ROOT / "pipeline" / "templates"
    readme_template = templates_dir / "README.dist.md"
    if readme_template.exists():
        (DIST_DIR / "README.md").write_text(readme_template.read_text())
    else:
        (DIST_DIR / "README.md").write_text(
            "# Distribution\n\nBuilt icon metadata and assets.\n"
        )


def _write_merged_license():
    """
    Merge vendor licenses into dist/LICENSE with separators.
    """
    vendors = [
        "radix-ui-icons",
        "heroicons",
        "lucide-icons",
        "phosphor-icons",
        "octicons",
        "svgl",
    ]
    parts = []
    for vendor in vendors:
        vdir = DIST_DIR / vendor
        found = None
        for fname in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
            candidate = vdir / fname
            if candidate.exists():
                found = candidate
                break
        if found:
            parts.append(f"===== {vendor} / {found.name} =====\n")
            parts.append(found.read_text())
            if not parts[-1].endswith("\n"):
                parts[-1] += "\n"
            parts.append("\n")
    out = DIST_DIR / "LICENSE"
    if parts:
        out.write_text("".join(parts))
    else:
        out.write_text("No vendor licenses found.\n")


@click.command()
@click.pass_context
def dist(ctx):
    """
    Build dist outputs: clean cache, cache all vendors, then copy metadata and SVGs into dist/.
    """
    # Clean dist first
    ctx.invoke(clean)
    # Clean cache first
    ctx.invoke(cache_clean)
    # Rebuild cache
    ctx.invoke(cache_all)

    _ensure_dist_placeholders()

    vendor_meta = {
        "radix-ui-icons": CACHE_DIR / "radix-ui-icons" / "metadata.json",
        "heroicons": CACHE_DIR / "heroicons" / "metadata.json",
        "lucide-icons": CACHE_DIR / "lucide-icons" / "metadata.json",
        "phosphor-icons": CACHE_DIR / "phosphor-icons" / "metadata.json",
        "octicons": CACHE_DIR / "octicons" / "metadata.json",
        "svgl": CACHE_DIR / "svgl" / "metadata.json",
    }
    # Extra data file for svgl
    svgl_data = CACHE_DIR / "svgl" / "data.json"
    if svgl_data.exists():
        _copy_file(svgl_data, DIST_DIR / "svgl" / "data.json")

    # Copy licenses
    _copy_license(ROOT / "vendor" / "radix-ui-icons", DIST_DIR / "radix-ui-icons")
    _copy_license(ROOT / "vendor" / "heroicons", DIST_DIR / "heroicons")
    _copy_license(ROOT / "vendor" / "lucide-icons", DIST_DIR / "lucide-icons")
    _copy_license(ROOT / "vendor" / "phosphor-icons", DIST_DIR / "phosphor-icons")
    _copy_license(ROOT / "vendor" / "octicons", DIST_DIR / "octicons")
    _copy_license(ROOT / "vendor" / "svgl", DIST_DIR / "svgl")

    # Copy SVG assets per vendor
    # Unified layout: assets under dist/<vendor>/src/
    _copy_tree(
        ROOT / "vendor" / "radix-ui-icons" / "packages" / "radix-icons" / "icons",
        DIST_DIR / "radix-ui-icons" / "src",
    )
    _copy_tree(
        ROOT / "vendor" / "heroicons" / "src",
        DIST_DIR / "heroicons" / "src",
    )
    _copy_tree(
        ROOT / "vendor" / "lucide-icons" / "icons",
        DIST_DIR / "lucide-icons" / "src",
    )
    _copy_tree(
        ROOT / "vendor" / "phosphor-icons" / "assets",
        DIST_DIR / "phosphor-icons" / "src",
    )
    _copy_tree(
        ROOT / "vendor" / "octicons" / "icons",
        DIST_DIR / "octicons" / "src",
    )
    _copy_tree(
        ROOT / "vendor" / "svgl" / "static" / "library",
        DIST_DIR / "svgl" / "src",
    )

    # Package metadata (SPEC package schema) -> dist/<vendor>/data.json
    vendor_packages = {
        "radix-ui-icons": {},
        "heroicons": {},
        "lucide-icons": {},
        "phosphor-icons": {},
        "octicons": {},
        "svgl": {},
    }
    templates_dir = ROOT / "pipeline" / "templates"

    def _load_meta_map(meta_path: Path) -> dict[str, dict]:
        if not meta_path.exists():
            return {}
        try:
            data = json.loads(meta_path.read_text())
        except Exception:
            return {}
        by_path: dict[str, dict] = {}
        if isinstance(data, list):
            for rec in data:
                if not isinstance(rec, dict):
                    continue
                dist_path = rec.get("dist_path")
                if dist_path:
                    by_path[dist_path] = rec.get("properties", {})
        return by_path

    # Attach flat file list (relative paths under dist/<vendor>)
    for vendor, pkg in vendor_packages.items():
        template_path = templates_dir / f"{vendor}.spec.json"
        if template_path.exists():
            try:
                pkg.update(json.loads(template_path.read_text()))
            except Exception:
                pass
        by_path = _load_meta_map(vendor_meta.get(vendor, Path("")))
        src_root = DIST_DIR / vendor / "src"
        file_entries = []
        if src_root.exists():
            for p in sorted(src_root.rglob("*")):
                if p.is_file():
                    rel_path = str(p.relative_to(DIST_DIR / vendor))
                    name = p.stem
                    properties = by_path.get(rel_path, {})
                    file_entries.append(
                        {
                            "name": name,
                            "file": rel_path,
                            "properties": properties,
                        }
                    )
        pkg["files"] = file_entries
        out_pkg = DIST_DIR / vendor / "data.json"
        out_pkg.parent.mkdir(parents=True, exist_ok=True)
        out_pkg.write_text(json.dumps(pkg, indent=2))

    # Merge licenses into dist/LICENSE
    _write_merged_license()

    click.echo(f"Dist build complete at {DIST_DIR}")


@click.command(name="clean")
def clean():
    """Remove the dist directory and recreate placeholders."""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
        click.echo(f"Removed dist directory: {DIST_DIR}")
    _ensure_dist_placeholders()
    click.echo("Dist directory reset with placeholders (.gitkeep, README.md).")


# Expose only cache and dist at the root
cli.add_command(cache, name="cache")
cli.add_command(dist, name="dist")
cli.add_command(clean, name="clean")


if __name__ == "__main__":
    cli()
