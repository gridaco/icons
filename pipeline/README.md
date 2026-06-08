# Pipeline

Vendor-native metadata extraction for icon sets. The pipeline does **not** map to the universal spec; it collects each vendor's own metadata and basic SVG dimensions, then writes vendor JSON outputs under `.cache/<vendor>/metadata.json`.

## Requirements

- Python 3.12+
- uv (for env + deps)
- **rsvg-convert** (from librsvg) — required only for `enrich` (SVG→PNG). Install with `brew install librsvg`.
- **ollama** with a vision model pulled — required only for `enrich`. Default model `gemma4:e4b-mlx`; override with `--model`.

## Install

```
cd pipeline
uv sync
```

## Commands

Run from `pipeline/` (or prefix with `uv run pipeline/main.py ...` from repo root):

- `uv run main.py radix-ui-icons`
- `uv run main.py heroicons`
- `uv run main.py lucide-icons`
- `uv run main.py phosphor-icons`
- `uv run main.py octicons`
- `uv run main.py svgl`
- `uv run main.py all` (runs all vendors)

Each command writes metadata to `.cache/<vendor>/metadata.json` by default. Use `--out <dir>` on individual vendor commands to override.

### Build + validate

- `uv run main.py dist` — clean, re-cache all vendors, and build the published `dist/` (SVGs + per-vendor `data.json` + merged `LICENSE`).
- `uv run main.py validate` — sanity-check a built `dist/`: every vendor's `data.json` must parse, list >0 files, and have an entry count matching the `.svg` files in `dist/<vendor>/src`. Exits non-zero on failure. This is the gate that catches an upstream submodule moving its folders out from under a hard-coded source path in `dist` (which would otherwise ship an empty vendor silently).

### Enrichment (text metadata for search)

`enrich` adds a uniform text layer — a one-line `description` for every logical icon plus `tags` — used
for plain text search (and, later, embeddings). Gaps are filled by a local ollama vision model fed the
icon rendered as a black-on-white PNG; **native vendor tags (lucide/phosphor/octicons) are always
preserved**, and the LLM only fills missing tags while always writing the description. svgl (logos) is out
of scope this pass.

Records are committed, durable artifacts under [`enrichment/<vendor>.json`](./enrichment), keyed by logical
icon name:

```jsonc
{ "academic-cap": { "description": "...", "tags": ["education", ...],
                    "tags_source": "llm",       // "vendor" | "llm"
                    "description_source": "llm", "model": "gemma4:e4b-mlx", "rev": 1 } }
```

- `uv run main.py enrich <vendor>` — enrich one vendor (e.g. `enrich radix-ui-icons`). Resumable: re-running
  skips icons already present. Flags: `--model`, `--force`, `--limit N`, `--only-missing/--all`, `--png-size 384`.
- `uv run main.py enrich all` — all in-scope vendors (excludes svgl).
- `uv run main.py enrich render <vendor>` — only render the representative PNGs into the cache (`.cache/png/`).
- `uv run main.py enrich-validate` — assert every record conforms (non-empty description ≤ 160 chars; at least
  one tag; **LLM-generated** tags ≤ 12 and short/lowercase, while **native vendor** tags are preserved verbatim
  and only sanity-checked) and print per-vendor coverage (`enriched / unique`) with gaps. Exits non-zero on
  violations.

`dist` folds enrichment into each `data.json` file entry as **top-level** `description` + `tags` (the
per-variant `properties` stay variant-only); missing enrichment is simply omitted, never fatal.

Prompt tuning is done with the throwaway harness `experiments/tune.py` (not wired into builds):
`uv run experiments/tune.py --mode random --count 50` prints a review table for manual inspection.

#### Running the full coverage pass (operational runbook)

> **Status:** the full ~4260-icon pass is **complete** (committed 2026-06): radix-ui-icons 332,
> heroicons 324, lucide-icons 1714, phosphor-icons 1512, octicons 378. svgl (logos) remains out of
> scope. Re-run only when vendors add icons or the model/prompt changes — it's resumable, so a re-run
> just fills new gaps.

**Why this shape.** Enrichment runs against a *local* ollama vision model (no API cost, no rate limit,
no data leaving the machine) — so duration, not money, is the only budget. At **~40–70s/icon** the full
pass is **many hours** (in practice it spans days across interruptions); that's expected. The run is
**resumable** and flushes to `enrichment/<vendor>.json` every 10 icons, so a crash or `Ctrl-C` never
loses more than a few icons. Native vendor tags are preserved; the LLM only fills the gaps.

**Prerequisites**

1. `brew install librsvg uv` (provides `rsvg-convert` + `uv`; both live in `/opt/homebrew/bin`, which
   isn't always on a non-login shell's `PATH` — export it for detached/cron runs).
2. ollama running on `:11434` with the vision model pulled: `ollama pull gemma4:e4b-mlx`.
   This model **ignores ollama's `format=<schema>` constraint** (ollama/ollama#15260); `llm.py` already
   handles that by parsing JSON defensively and bumping temperature on retry — no action needed, just
   don't be surprised by occasional `SKIP` lines in the log.
3. `cd pipeline && uv sync`.

**Launch (durable, multi-hour).** Run vendor-by-vendor rather than `enrich all` so an interruption in
one vendor still leaves the others flushed and resumable. `caffeinate` keeps the Mac awake; `nohup`
detaches it from the terminal; `tee` keeps a timestamped log:

```bash
cd pipeline
LOG="enrich-run-$(date +%Y%m%d-%H%M%S).log"
caffeinate -i nohup bash -c '
  export PATH="/opt/homebrew/bin:$PATH"
  for v in radix-ui-icons heroicons lucide-icons phosphor-icons octicons; do
    uv run main.py enrich "$v" --model gemma4:e4b-mlx --png-size 384
  done
' >> "$LOG" 2>&1 &
echo "logging to pipeline/$LOG"
```

Add `--force` to any `enrich` call (or set it in the loop) to regenerate from scratch instead of
filling gaps.

**Monitor (read-only, separate terminal).** Nothing here touches the run:

```bash
cd pipeline
# per-vendor coverage so far
for v in radix-ui-icons heroicons lucide-icons phosphor-icons octicons; do
  printf "%-16s %s\n" "$v" "$(python3 -c "import json;print(len(json.load(open(f'enrichment/$v.json'))))")"
done
ollama ps                                   # model loaded / GPU in use
tail -f "$(ls -t enrich-run-*.log | head -1)"   # one line per icon, with live ETA
```

**Finalize.** When all vendors are done, fold the text layer into the published data and gate it:

```bash
uv run main.py dist            # writes top-level description+tags into dist/*/data.json
uv run main.py validate        # entry/svg-count gate
uv run main.py enrich-validate # contract + per-vendor coverage report
```

Then review and commit deliberately — keep the **pipeline code**, the **`enrichment/*.json`** data, and
the **`dist/*/data.json`** rebuild as separate commits. The `*.log` files and `.cache/` are gitignored;
the run is otherwise the only thing that writes `enrichment/*.json`.

## Auto-update

[`.github/workflows/update-icons.yml`](../.github/workflows/update-icons.yml) runs weekly (and on demand via *workflow_dispatch*): it bumps every `vendor/*` submodule to latest upstream, runs `dist`, runs `validate` plus a regression gate (fails if any vendor's count drops >25%), and opens a PR (`bot/icons-update`). The data change always lands via that PR. No secrets are needed.

> The `version` field in each `data.json` comes from `templates/<vendor>.spec.json` and is **not** auto-derived from the submodule — bump it by hand when an upstream cuts a release worth labelling.

## Outputs (per vendor)

- All commands write to `.cache/<vendor>/metadata.json` by default (override with `--out <dir>` on the specific vendor command).
- **Radix UI Icons**: name, path, SVG viewBox/width/height, manifest path (if present)
- **Heroicons**: name, size, style, path, SVG viewBox/width/height
- **Lucide Icons**: name, path, SVG viewBox/width/height, vendor JSON metadata (tags, categories, contributors, aliases, deprecated)
- **Phosphor Icons**: name, weight, path, SVG viewBox/width/height, catalog fields (tags, categories, codepoint, alias, published/updated)
- **Octicons**: name, file, path, SVG viewBox/width/height, keywords from `keywords.json`
- **SVGL**: file, path, SVG viewBox/width/height, matched entry from `src/data/svgs.ts`; also writes parsed `svgs.ts` to `.cache/svgl/data.json`

## Notes

- Extraction is vendor-native; no field renaming to the universal spec.
- SVG parsing is basic: viewBox/width/height are pulled from the `<svg>` element, falling back to viewBox values when width/height are absent or non-numeric.
