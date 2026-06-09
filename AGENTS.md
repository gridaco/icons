# AGENTS.md

Guidance for coding agents working in this repository. (v1 — minimal)

## What this is

Grida Icons — an aggregated, enriched catalog of open-source icons with a free
public search API and a Next.js web app.

## Layout

- `vendor/` — upstream icon sources (git submodules).
- `pipeline/` — Python tooling that builds `dist/` and enriches per-icon metadata (keywords + descriptions).
- `dist/<vendor>/data.json` — built catalog; per-icon `{ name, file, properties, description, tags }`.
- `www/` — Next.js web app: search UI, public API (`app/(api)/`), docs at `/docs`.

## Web app (`www/`)

Stack: Next.js 16 (App Router, Turbopack), React 19, Tailwind v4, pnpm, Node 24.
Lint/format via oxlint + oxfmt (no ESLint/Prettier); a lefthook pre-commit runs them.

```
pnpm --dir www dev        # run locally
pnpm --dir www build      # production build
pnpm --dir www typecheck  # tsc --noEmit
pnpm --dir www lint       # oxlint
```

- The client/server search both use the prebuilt index from
  `www/scripts/build-search-index.mjs` (runs in `predev`/`prebuild`). Its output
  `www/public/search-index.json` is generated and git-ignored.
- The public API contract is documented at `/docs` and `/llms.txt`.

## Conventions

- Match the surrounding code style; let oxfmt/oxlint format.
- Do not commit generated artifacts (`www/public/dist`, `www/public/search-index.json`).
- Commit only when asked; branch off `main` for changes.
