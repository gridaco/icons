# Grida Icons

> An aggregated, enriched catalog of open-source icons with a free public search
> API and a web app. Built for developers and AI agents.

**Live:** [icons.grida.co](https://icons.grida.co) · **API:** [`/llms.txt`](https://icons.grida.co/llms.txt) · [API reference](https://icons.grida.co/docs)

Grida Icons mirrors several popular open-source icon sets as git submodules,
runs them through a Python pipeline that normalizes the SVGs and attaches a
uniform text layer (a one-line `description` + searchable `tags` for every
icon), and serves the result through a Next.js web app and a zero-auth REST API.

## Icon sets

Six upstream sets, ~5,000+ logical icons (many more when you count per-style/weight variants). Sources are tracked as submodules under [`vendor/`](./vendor); the published catalog lives in [`dist/`](./dist).

| Set                | id               | Source                                                              |
| ------------------ | ---------------- | ------------------------------------------------------------------- |
| Heroicons          | `heroicons`      | [tailwindlabs/heroicons](https://github.com/tailwindlabs/heroicons) |
| Lucide             | `lucide-icons`   | [lucide-icons/lucide](https://github.com/lucide-icons/lucide)       |
| Phosphor           | `phosphor-icons` | [phosphor-icons/core](https://github.com/phosphor-icons/core)       |
| Octicons           | `octicons`       | [primer/octicons](https://github.com/primer/octicons)               |
| Radix UI           | `radix-ui-icons` | [radix-ui/icons](https://github.com/radix-ui/icons)                 |
| SVGL (brand logos) | `svgl`           | [pheralb/svgl](https://github.com/pheralb/svgl)                     |

Each set keeps its upstream license — see `dist/<set>/LICENSE` (aggregated in the root [`LICENSE`](./LICENSE)). Review the source project before redistribution.

## API

A free, public, zero-auth REST API. No API key, open CORS, edge-cached. Base URL `https://icons.grida.co`.

```bash
# keyword search (ranked over name + tags; one result per logical icon)
curl "https://icons.grida.co/api/search?q=trash&limit=2"
```

- `GET /api/search?q=&vendor=&limit=&offset=` — ranked keyword search (recommended).
- `GET /api` — every icon file (one item per variant); filter by `vendor`, `q`, `variant:<key>=<value>`.
- `GET /api/logos` — brand logos (SVGL).
- `GET /api/vendors` — per-set metadata (id, name, version, count, variant axes).
- `GET /dist/{vendor}/{file}` — the raw SVG, immutable-cached and safe to hotlink.

Full contract: [`/docs`](https://icons.grida.co/docs) and [`/llms.txt`](https://icons.grida.co/llms.txt).

## Repository layout

```
vendor/      upstream icon sources (git submodules)
pipeline/    Python (uv) tooling: builds dist/ and enriches per-icon text metadata
dist/        published catalog — dist/<set>/{data.json, src/*.svg, LICENSE}
www/         Next.js web app: search UI, public API, docs
sets/        legacy pre-pipeline data-wrangling experiments (not part of the build)
```

`dist/<set>/data.json` carries package metadata plus a `files[]` list, each entry
`{ name, file, properties, description, tags }` — `description`/`tags` are the
enriched text layer; `properties` holds per-variant axes (e.g. `style`, `weight`).

## Getting started

Clone with submodules (the vendor sources live there):

```bash
git clone --recurse-submodules https://github.com/gridaco/icons
# already cloned?
git submodule update --init --recursive
```

The repo is a pnpm root pinned to **Node 24** (`.nvmrc`) and **pnpm 11.5.1**.
Formatting and linting use the **oxc** toolchain — `oxfmt` and `oxlint`, no
ESLint/Prettier — wired into a `lefthook` pre-commit hook.

```bash
pnpm install      # installs the lefthook git hook via `prepare`
pnpm fmt          # format with oxfmt        (fmt:check to verify only)
pnpm lint         # lint with oxlint
```

### Web app (`www/`)

Next.js 16 (App Router, Turbopack), React 19, Tailwind v4, MiniSearch.

```bash
pnpm --dir www dev        # dev server on http://localhost:3000
pnpm --dir www build      # production build
pnpm --dir www typecheck  # tsc --noEmit
pnpm --dir www lint       # oxlint
```

Both the client and server search read a prebuilt index from
`www/scripts/build-search-index.mjs` (run automatically in `predev`/`prebuild`).
Its output (`www/public/search-index.json`) and the copied `www/public/dist` are
generated and git-ignored.

### Pipeline (`pipeline/`)

Python 3.12+ managed with [`uv`](https://docs.astral.sh/uv/). Builds `dist/` from
the vendor submodules and enriches the per-icon text layer. See
[`pipeline/README.md`](./pipeline/README.md) for the full reference.

```bash
cd pipeline
uv sync
uv run main.py dist        # rebuild dist/ (SVGs + per-set data.json + LICENSE)
uv run main.py validate    # gate: each data.json parses and matches its SVG count
```

Enrichment fills a uniform `description` + `tags` for every icon. Native vendor
tags (Lucide/Phosphor/Octicons) are preserved; gaps are filled by a **local**
ollama vision model fed the icon as a PNG — no API cost, no data leaving the
machine. It needs `rsvg-convert` (`brew install librsvg`) and a pulled vision
model. The full ~4,260-icon pass is already committed under
[`pipeline/enrichment/`](./pipeline/enrichment); re-run only when sets add icons
or the model/prompt changes (it's resumable).

```bash
uv run main.py enrich <set>     # e.g. enrich heroicons (resumable; --force to redo)
uv run main.py enrich-validate  # contract check + per-set coverage report
```

## Keeping data fresh

[`.github/workflows/update-icons.yml`](./.github/workflows/update-icons.yml) runs
weekly (Mondays 06:00 UTC, or on demand via _workflow_dispatch_): it bumps every
`vendor/*` submodule to latest upstream, rebuilds `dist/`, runs `validate` plus a
regression gate (fails if any set's count drops >25%), and opens a
`bot/icons-update` PR. Data changes always land via that PR so a human reviews
the diff before the site serves it. No secrets required — every source is a
submodule.

## Contributing

Contributions welcome — new sources, better metadata, search improvements. Branch
off `main`; let `oxfmt`/`oxlint` handle formatting (the pre-commit hook runs
them). Don't commit generated artifacts (`www/public/dist`,
`www/public/search-index.json`). See [`AGENTS.md`](./AGENTS.md) for agent-oriented
guidance.

## License

See [`LICENSE`](./LICENSE). Each upstream icon set retains its own license under
`dist/<set>/LICENSE`.
