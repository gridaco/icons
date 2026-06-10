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

import enrich as enrich_mod
import llm


ROOT = Path(__file__).parent.parent
DIST_DIR = ROOT / "dist"
CACHE_DIR = DIST_DIR / ".cache"
ENRICH_DIR = ROOT / "pipeline" / "enrichment"


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


def _copy_svgs(src: Path, dst: Path):
    """
    Copy only .svg files from src to dst, preserving directory structure.
    """
    if dst.exists():
        shutil.rmtree(dst)
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for path in src.rglob("*"):
        if path.is_file() and path.suffix.lower() == ".svg":
            rel = path.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


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

    # Copy licenses
    _copy_license(ROOT / "vendor" / "radix-ui-icons", DIST_DIR / "radix-ui-icons")
    _copy_license(ROOT / "vendor" / "heroicons", DIST_DIR / "heroicons")
    _copy_license(ROOT / "vendor" / "lucide-icons", DIST_DIR / "lucide-icons")
    _copy_license(ROOT / "vendor" / "phosphor-icons", DIST_DIR / "phosphor-icons")
    _copy_license(ROOT / "vendor" / "octicons", DIST_DIR / "octicons")
    _copy_license(ROOT / "vendor" / "svgl", DIST_DIR / "svgl")

    # Copy SVG assets per vendor
    # Unified layout: assets under dist/<vendor>/src/
    _copy_svgs(
        ROOT / "vendor" / "radix-ui-icons" / "packages" / "radix-icons" / "icons",
        DIST_DIR / "radix-ui-icons" / "src",
    )
    _copy_svgs(
        ROOT / "vendor" / "heroicons" / "src",
        DIST_DIR / "heroicons" / "src",
    )
    _copy_svgs(
        ROOT / "vendor" / "lucide-icons" / "icons",
        DIST_DIR / "lucide-icons" / "src",
    )
    _copy_svgs(
        ROOT / "vendor" / "phosphor-icons" / "assets",
        DIST_DIR / "phosphor-icons" / "src",
    )
    _copy_svgs(
        ROOT / "vendor" / "octicons" / "icons",
        DIST_DIR / "octicons" / "src",
    )
    _copy_svgs(
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
        """Map dist-relative path -> {properties, name} from a vendor cache."""
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
                    by_path[dist_path] = {
                        "properties": rec.get("properties", {}),
                        "name": rec.get("name"),
                    }
        return by_path

    def _load_enrichment(vendor: str) -> dict[str, dict]:
        path = ENRICH_DIR / f"{vendor}.json"
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text())
        except Exception:
            return {}

    # Attach flat file list (relative paths under dist/<vendor>)
    for vendor, pkg in vendor_packages.items():
        template_path = templates_dir / f"{vendor}.spec.json"
        if template_path.exists():
            try:
                pkg.update(json.loads(template_path.read_text()))
            except Exception:
                pass
        by_path = _load_meta_map(vendor_meta.get(vendor, Path("")))
        enrichment = _load_enrichment(vendor)
        src_root = DIST_DIR / vendor / "src"
        file_entries = []
        n_enriched = 0
        if src_root.exists():
            for p in sorted(src_root.rglob("*")):
                if p.is_file():
                    rel_path = str(p.relative_to(DIST_DIR / vendor))
                    meta = by_path.get(rel_path, {})
                    # logical name drives enrichment lookup; file stem is the
                    # per-variant name shown in the entry.
                    logical = meta.get("name") or p.stem
                    entry = {
                        "name": p.stem,
                        "file": rel_path,
                        "properties": meta.get("properties", {}),
                    }
                    record = enrichment.get(logical)
                    if record:
                        if record.get("description"):
                            entry["description"] = record["description"]
                        if record.get("tags"):
                            entry["tags"] = record["tags"]
                        n_enriched += 1
                    file_entries.append(entry)
        pkg["files"] = file_entries
        out_pkg = DIST_DIR / vendor / "data.json"
        out_pkg.parent.mkdir(parents=True, exist_ok=True)
        out_pkg.write_text(json.dumps(pkg, indent=2))
        if enrichment:
            click.echo(
                f"  {vendor}: enriched {n_enriched}/{len(file_entries)} file entries"
            )

    # Merge licenses into dist/LICENSE
    _write_merged_license()

    # Build-time count snapshot (dist/stats.json) — consumed by README badges.
    _write_stats()

    click.echo(f"Dist build complete at {DIST_DIR}")


@click.command(name="clean")
def clean():
    """Remove the dist directory and recreate placeholders."""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
        click.echo(f"Removed dist directory: {DIST_DIR}")
    _ensure_dist_placeholders()
    click.echo("Dist directory reset with placeholders (.gitkeep, README.md).")


# Vendors that must be present in a healthy dist build.
DIST_VENDORS = [
    "radix-ui-icons",
    "heroicons",
    "lucide-icons",
    "phosphor-icons",
    "octicons",
    "svgl",
]

_CACHE_COMMANDS = {
    "radix-ui-icons": process_radix,
    "heroicons": process_heroicons,
    "lucide-icons": process_lucide,
    "phosphor-icons": process_phosphor,
    "octicons": process_octicons,
    "svgl": process_svgl,
}


def _logical_name(rec: dict) -> str | None:
    """
    Grouping key for variant records in a vendor cache: icon vendors key
    variants by `name`; svgl groups a brand's symbol/wordmark/theme files
    under the vendor-native `meta.title`.
    """
    name = rec.get("name") or (rec.get("meta") or {}).get("title")
    if name:
        return str(name)
    path = rec.get("dist_path") or rec.get("file")
    return Path(path).stem if path else None


def _compute_stats() -> dict:
    """
    Per-vendor and aggregate counts: `files` is one per variant SVG (matches
    data.json entries), `unique` is logical icons (brands for svgl). Vendor
    kind comes from the spec template's category URI (icons-ui vs logos).
    """
    vendors: dict[str, dict] = {}
    totals = {"files": 0, "unique": 0}
    by_kind: dict[str, dict[str, int]] = {}
    for vendor in DIST_VENDORS:
        data_path = DIST_DIR / vendor / "data.json"
        if not data_path.exists():
            raise SystemExit(f"stats: {data_path} missing — run `dist` first")
        data = json.loads(data_path.read_text())
        records = json.loads((CACHE_DIR / vendor / "metadata.json").read_text())
        unique = {n for n in (_logical_name(r) for r in records) if n}
        kind = (
            "logos"
            if any(str(c).endswith("/logos") for c in data.get("categories") or [])
            else "icons"
        )
        n_files = len(data.get("files") or [])
        vendors[vendor] = {
            "name": data.get("name") or vendor,
            "kind": kind,
            "files": n_files,
            "unique": len(unique),
        }
        totals["files"] += n_files
        totals["unique"] += len(unique)
        agg = by_kind.setdefault(kind, {"files": 0, "unique": 0})
        agg["files"] += n_files
        agg["unique"] += len(unique)
    return {"totals": {**totals, **by_kind}, "vendors": vendors}


def _write_stats() -> dict:
    """
    Write dist/stats.json. Deliberately carries no timestamp so the file only
    diffs when counts actually change (keeps the weekly refresh PR clean).
    """
    stats = _compute_stats()
    (DIST_DIR / "stats.json").write_text(json.dumps(stats, indent=2) + "\n")
    return stats


def _echo_stats(stats: dict) -> None:
    click.echo(f"{'vendor':<18}{'kind':>6}{'files':>8}{'unique':>8}")
    for vendor, s in stats["vendors"].items():
        click.echo(f"{vendor:<18}{s['kind']:>6}{s['files']:>8}{s['unique']:>8}")
    t = stats["totals"]
    icons = t.get("icons", {"files": 0, "unique": 0})
    logos = t.get("logos", {"files": 0, "unique": 0})
    click.echo(
        f"totals: {t['unique']} unique / {t['files']} files "
        f"(icons {icons['unique']}/{icons['files']}, logos {logos['unique']}/{logos['files']})"
    )


@click.command(name="stats")
@click.pass_context
def stats_cmd(ctx):
    """
    Regenerate dist/stats.json from the built dist/ and vendor cache.

    Counts per vendor: `files` (one entry per variant SVG, same as data.json)
    and `unique` (logical icons; brands for svgl). Needs dist/<vendor>/data.json
    (run `dist` first); missing cache metadata is rebuilt per vendor, which
    requires the vendor submodules to be checked out.
    """
    for vendor in DIST_VENDORS:
        if not (CACHE_DIR / vendor / "metadata.json").exists():
            click.echo(f"  cache miss for {vendor}; building metadata...")
            ctx.invoke(_CACHE_COMMANDS[vendor], out=CACHE_DIR / vendor)
    stats = _write_stats()
    _echo_stats(stats)
    click.echo(f"Wrote {DIST_DIR / 'stats.json'}")


@click.command(name="validate")
def validate():
    """
    Sanity-check the built dist/ before publishing.

    For each vendor asserts that data.json exists and parses, that it lists at
    least one file, and that the number of file entries matches the number of
    .svg assets actually copied into dist/<vendor>/src. A zero count or a
    mismatch usually means an upstream submodule restructured its folders and a
    hard-coded source path in the `dist` builder now points at nothing — the
    failure mode that would otherwise ship an empty vendor silently.
    """
    errors: list[str] = []
    click.echo(f"{'vendor':<18}{'entries':>9}{'svgs':>8}  status")
    for vendor in DIST_VENDORS:
        vdir = DIST_DIR / vendor
        data_path = vdir / "data.json"
        if not data_path.exists():
            errors.append(f"{vendor}: data.json missing")
            click.echo(f"{vendor:<18}{'MISSING':>9}")
            continue
        try:
            data = json.loads(data_path.read_text())
        except Exception as e:
            errors.append(f"{vendor}: data.json invalid JSON ({e})")
            click.echo(f"{vendor:<18}{'BADJSON':>9}")
            continue

        files = data.get("files") or []
        n_entries = len(files)
        src_dir = vdir / "src"
        n_svgs = (
            sum(1 for p in src_dir.rglob("*.svg") if p.is_file())
            if src_dir.exists()
            else 0
        )

        status = "ok"
        if n_entries == 0:
            errors.append(f"{vendor}: 0 entries (upstream path drift?)")
            status = "EMPTY"
        elif n_entries != n_svgs:
            errors.append(
                f"{vendor}: data.json entries ({n_entries}) != src svgs ({n_svgs})"
            )
            status = "MISMATCH"
        click.echo(f"{vendor:<18}{n_entries:>9}{n_svgs:>8}  {status}")

    if errors:
        click.echo("\nVALIDATION FAILED:")
        for e in errors:
            click.echo(f"  - {e}")
        raise SystemExit(1)
    click.echo("\nAll vendors valid.")


@click.group()
def enrich():
    """
    Per-icon text metadata (description + tags) via local LLM vision.

    Writes committed records to pipeline/enrichment/<vendor>.json keyed by
    logical icon name. Resumable: re-running skips already-enriched icons.
    """
    pass


_MODEL_OPT = click.option(
    "--model", default=llm.DEFAULT_MODEL, show_default=True, help="ollama vision model."
)
_FORCE_OPT = click.option(
    "--force", is_flag=True, help="Re-render and re-generate even if cached/existing."
)
_LIMIT_OPT = click.option("--limit", type=int, default=None, help="Cap icons processed.")
_ONLY_MISSING_OPT = click.option(
    "--only-missing/--all",
    default=True,
    show_default=True,
    help="Skip icons already in the enrichment file (default) or redo all.",
)
_PNG_SIZE_OPT = click.option(
    "--png-size", type=int, default=384, show_default=True, help="Render size (px)."
)


def _enrich_one(vendor, model, only_missing, force, limit, png_size):
    records = enrich_mod.enrich_vendor(
        vendor,
        model=model,
        only_missing=only_missing,
        force=force,
        limit=limit,
        png_size=png_size,
    )
    enriched, unique, _ = enrich_mod.coverage(vendor)
    click.echo(f"{vendor}: {enriched}/{unique} enriched ({len(records)} records).")


@enrich.command(name="vendor")
@click.argument("vendor", type=click.Choice(enrich_mod.VENDORS))
@_MODEL_OPT
@_FORCE_OPT
@_LIMIT_OPT
@_ONLY_MISSING_OPT
@_PNG_SIZE_OPT
def enrich_vendor_cmd(vendor, model, force, limit, only_missing, png_size):
    """Enrich a single VENDOR."""
    _enrich_one(vendor, model, only_missing, force, limit, png_size)


@enrich.command(name="all")
@_MODEL_OPT
@_FORCE_OPT
@_LIMIT_OPT
@_ONLY_MISSING_OPT
@_PNG_SIZE_OPT
def enrich_all_cmd(model, force, limit, only_missing, png_size):
    """Enrich all in-scope vendors (excludes svgl)."""
    for vendor in enrich_mod.VENDORS:
        click.echo("-" * 20)
        _enrich_one(vendor, model, only_missing, force, limit, png_size)


@enrich.command(name="render")
@click.argument("vendor", type=click.Choice(enrich_mod.VENDORS))
@_FORCE_OPT
@_LIMIT_OPT
@_PNG_SIZE_OPT
def enrich_render_cmd(vendor, force, limit, png_size):
    """Render (only) a VENDOR's representative PNGs into the cache."""
    icons = enrich_mod.load_logical_icons(vendor)
    if limit is not None:
        icons = icons[:limit]
    from render import render_for

    with click.progressbar(icons, label=f"render {vendor}", show_pos=True) as bar:
        for ic in bar:
            try:
                render_for(vendor, ic.name, ic.svg_path, size=png_size, force=force)
            except Exception as e:
                click.echo(f"\n  SKIP {vendor}/{ic.name}: {e}", err=True)


# Register the in-scope vendors as direct subcommands too: `enrich radix-ui-icons`
for _v in enrich_mod.VENDORS:
    def _make(vendor):
        @_MODEL_OPT
        @_FORCE_OPT
        @_LIMIT_OPT
        @_ONLY_MISSING_OPT
        @_PNG_SIZE_OPT
        def _cmd(model, force, limit, only_missing, png_size):
            _enrich_one(vendor, model, only_missing, force, limit, png_size)

        _cmd.__doc__ = f"Enrich {vendor}."
        return _cmd

    enrich.command(name=_v)(_make(_v))


@click.command(name="enrich-validate")
def enrich_validate():
    """
    Validate enrichment records against the contract and report coverage.

    Each record must have a non-empty description (<= bound) and 1-12 lowercase
    non-empty tags with no stray punctuation. Prints per-vendor coverage
    (enriched / unique) and lists gaps. Exits non-zero on contract violations.
    """
    errors: list[str] = []
    click.echo(f"{'vendor':<18}{'enriched':>9}{'unique':>8}  status")
    for vendor in enrich_mod.VENDORS:
        records = enrich_mod.load_records(vendor)
        for name, rec in records.items():
            desc = rec.get("description") or ""
            tags = rec.get("tags") or []
            if not desc:
                errors.append(f"{vendor}/{name}: empty description")
            elif len(desc) > llm.DESC_MAX:
                errors.append(f"{vendor}/{name}: description > {llm.DESC_MAX} chars")
            # LLM-generated tags must meet the strict contract; native vendor
            # tags are preserved verbatim and only sanity-checked (they can be
            # numerous and multi-word, e.g. lucide's "heart rate monitor").
            src = rec.get("tags_source")
            if not tags:
                errors.append(f"{vendor}/{name}: no tags")
            elif src == "llm":
                if len(tags) > llm.TAGS_MAX:
                    errors.append(
                        f"{vendor}/{name}: {len(tags)} llm tags (max {llm.TAGS_MAX})"
                    )
                for t in tags:
                    if not isinstance(t, str) or not t or not llm._TAG_OK.match(t):
                        errors.append(f"{vendor}/{name}: bad llm tag {t!r}")
                        break
            else:  # vendor / preserved
                for t in tags:
                    if not isinstance(t, str) or not t.strip():
                        errors.append(f"{vendor}/{name}: empty vendor tag")
                        break
        enriched, unique, missing = enrich_mod.coverage(vendor)
        status = "ok" if enriched == unique else f"{len(missing)} gaps"
        click.echo(f"{vendor:<18}{enriched:>9}{unique:>8}  {status}")
        if missing:
            preview = ", ".join(missing[:10])
            more = f" (+{len(missing) - 10} more)" if len(missing) > 10 else ""
            click.echo(f"  gaps: {preview}{more}")

    if errors:
        click.echo("\nENRICH VALIDATION FAILED:")
        for e in errors[:50]:
            click.echo(f"  - {e}")
        if len(errors) > 50:
            click.echo(f"  ... (+{len(errors) - 50} more)")
        raise SystemExit(1)
    click.echo("\nAll enrichment records conform to the contract.")


# Expose only cache and dist at the root
cli.add_command(cache, name="cache")
cli.add_command(dist, name="dist")
cli.add_command(clean, name="clean")
cli.add_command(validate, name="validate")
cli.add_command(stats_cmd, name="stats")
cli.add_command(enrich, name="enrich")
cli.add_command(enrich_validate, name="enrich-validate")


if __name__ == "__main__":
    cli()
