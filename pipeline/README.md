# Pipeline

Vendor-native metadata extraction for icon sets. The pipeline does **not** map to the universal spec; it collects each vendor's own metadata and basic SVG dimensions, then writes vendor JSON outputs under `.cache/<vendor>/metadata.json`.

## Requirements

- Python 3.12+
- uv (for env + deps)

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
