# Distribution

This directory contains prebuilt icon assets and metadata for each vendor.

At the root:

- `stats.json` — build-generated counts: per-vendor and aggregate `files`
  (one per variant SVG) and `unique` (logical icons / brands), grouped into
  `icons` vs `logos`.
- `LICENSE` — all vendor licenses, aggregated.

Per vendor:

- `data.json` — package-level metadata.
- `metadata.json` — vendor-native icon metadata.
- `src/` — SVG assets (layout normalized with `src` as the common parent).
- `LICENSE` — vendor license (also aggregated in the root `LICENSE`).

To rebuild, run your project’s build pipeline.
