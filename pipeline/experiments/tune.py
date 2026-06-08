"""
Throwaway prompt-tuning / review harness for issue #10 (NOT wired into builds).

Renders a sample of icons, runs the frozen prompt in ``pipeline/llm.py`` through
the local vision model, and prints a review table:

    vendor · name · tags_source · latency · description · tags

Two modes:
  * --mode diverse  (default) — a hand-picked set of ambiguous shapes and
    near-duplicates that must stay distinguishable.
  * --mode random --count 50 --seed 0 — a random sample across the 5 in-scope
    vendors, for the manual review/iteration loop.

Run from pipeline/:  uv run experiments/tune.py --mode random --count 50
"""

from __future__ import annotations

import random
import sys
import time
from pathlib import Path

import click

# Make sibling pipeline modules importable when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import enrich as enrich_mod  # noqa: E402
import llm  # noqa: E402
from render import render_for  # noqa: E402

# Deliberately diverse: ambiguous shapes + near-duplicates that must differ.
DIVERSE: list[tuple[str, str]] = [
    ("radix-ui-icons", "dot"),
    ("radix-ui-icons", "circle"),
    ("radix-ui-icons", "square"),
    ("heroicons", "arrow-up"),
    ("heroicons", "arrow-up-circle"),
    ("heroicons", "chevron-up"),
    ("heroicons", "trash"),
    ("lucide-icons", "trash-2"),
    ("lucide-icons", "accessibility"),
    ("lucide-icons", "graduation-cap"),
    ("octicons", "git-merge"),
    ("octicons", "git-branch"),
    ("phosphor-icons", "shopping-cart"),
    ("phosphor-icons", "shopping-bag"),
    ("phosphor-icons", "heart"),
]


# Known-hard cases (modifier marks, logos, fine detail) + a few that were
# already good, to catch regressions when tuning the prompt.
HARD: list[tuple[str, str]] = [
    # slash / modifier (disabled, remove, error)
    ("lucide-icons", "search-slash"),
    ("phosphor-icons", "lightning-slash"),
    ("lucide-icons", "shield-x"),
    ("lucide-icons", "ticket-x"),
    ("heroicons", "shield-exclamation"),
    # circle/square wrappers + inner element
    ("phosphor-icons", "stop-circle"),
    ("heroicons", "play-circle"),
    ("heroicons", "arrow-up-circle"),
    # fine interior detail
    ("lucide-icons", "calculator"),
    ("lucide-icons", "copyleft"),
    # embedded brand logos (describe geometry, no brand guess)
    ("phosphor-icons", "sketch-logo"),
    ("phosphor-icons", "spotify-logo"),
    # regression guards (were good)
    ("phosphor-icons", "barbell"),
    ("phosphor-icons", "syringe"),
    ("octicons", "git-merge"),
    ("radix-ui-icons", "dot"),
]


def _index(vendor: str) -> dict:
    return {ic.name: ic for ic in enrich_mod.load_logical_icons(vendor)}


def _collect_named(pairs: list) -> list:
    picks = []
    caches: dict[str, dict] = {}
    for vendor, name in pairs:
        idx = caches.setdefault(vendor, _index(vendor))
        ic = idx.get(name)
        if ic is None:
            click.echo(f"  (skip {vendor}/{name}: not found)", err=True)
            continue
        picks.append((vendor, ic))
    return picks


def _collect_random(count: int, seed: int) -> list:  # noqa: D401
    rng = random.Random(seed)
    pool = []
    for vendor in enrich_mod.VENDORS:
        for ic in enrich_mod.load_logical_icons(vendor):
            pool.append((vendor, ic))
    rng.shuffle(pool)
    return pool[:count]


@click.command()
@click.option(
    "--mode", type=click.Choice(["diverse", "hard", "random"]), default="diverse"
)
@click.option("--count", type=int, default=50, help="random mode: sample size.")
@click.option("--seed", type=int, default=0, help="random mode: RNG seed.")
@click.option("--model", default=llm.DEFAULT_MODEL, show_default=True)
@click.option("--png-size", type=int, default=384, show_default=True)
@click.option(
    "--no-name-hint", is_flag=True, help="A/B: drop the filename hint from the prompt."
)
def main(mode, count, seed, model, png_size, no_name_hint):
    if mode == "diverse":
        picks = _collect_named(DIVERSE)
    elif mode == "hard":
        picks = _collect_named(HARD)
    else:
        picks = _collect_random(count, seed)
    click.echo(f"model={model}  mode={mode}  n={len(picks)}  name_hint={not no_name_hint}\n")

    rows = []
    for vendor, ic in picks:
        need_tags = not ic.native_tags
        src = "vendor" if ic.native_tags else "llm"
        try:
            png = render_for(vendor, ic.name, ic.svg_path, size=png_size)
            t0 = time.perf_counter()
            out = llm.generate(
                png, ic.name, vendor, need_tags=need_tags, model=model,
                use_name_hint=not no_name_hint,
                hint_tags=ic.native_tags or None,
            )
            dt = time.perf_counter() - t0
        except Exception as e:
            click.echo(f"SKIP {vendor}/{ic.name}: {e}", err=True)
            continue
        tags = out["tags"] if need_tags else ic.native_tags
        rows.append((vendor, ic.name, src, dt, out["description"], tags))

    # Print a readable review table.
    click.echo("=" * 100)
    for vendor, name, src, dt, desc, tags in rows:
        click.echo(f"{vendor}/{name}  [{src}, {dt:.1f}s]")
        click.echo(f"    desc: {desc}")
        click.echo(f"    tags: {', '.join(tags)}")
    click.echo("=" * 100)
    if rows:
        avg = sum(r[3] for r in rows) / len(rows)
        click.echo(f"{len(rows)} icons, avg {avg:.1f}s/icon")


if __name__ == "__main__":
    main()
