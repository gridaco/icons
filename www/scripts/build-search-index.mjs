// Build a compact, prebuilt search index consumed by both the client (instant,
// in-memory MiniSearch) and the /api/search route (server-side MiniSearch).
//
// Source of truth is the repo-root `dist/*/data.json` produced by the pipeline.
// Output is `www/public/search-index.json`, served as a static CDN asset.
//
// Icons are grouped into LOGICAL icons: many vendors bake the variant value into
// the file name (e.g. phosphor `acorn-bold`, octicons `accessibility-16`,
// svgl `1password-dark`), while heroicons shares one `name` across size/style.
// We collapse both shapes by stripping a trailing `-{propertyValue}` that comes
// from the file's OWN `properties` — a value-keyed strip that is safe because we
// never strip a suffix the file doesn't actually declare as a variant value.
//
// Size lever: `description` is included so cards/tooltips/detail pages can show it
// WITHOUT a second fetch. It is display-only and NOT a searchable field (search is
// name + tags). Dropping it here would shrink the payload (~2-3MB -> ~300KB gzip)
// at the cost of needing a per-icon fetch for the description.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const WWW_DIR = path.resolve(SCRIPT_DIR, "..");
const REPO_DIST = path.resolve(WWW_DIR, "..", "dist");
const PUBLIC_DIST = path.resolve(WWW_DIR, "public", "dist");
// Prefer the repo dist (always present); fall back to the copied public/dist.
const DIST_ROOT = fs.existsSync(REPO_DIST) ? REPO_DIST : PUBLIC_DIST;
const OUT_FILE = path.resolve(WWW_DIR, "public", "search-index.json");

/** Strip a trailing `-{value}` for each of the file's own variant property values. */
function toBaseName(name, properties) {
  let base = name;
  for (const value of Object.values(properties ?? {})) {
    const suffix = `-${value}`;
    if (base.endsWith(suffix) && base.length > suffix.length) {
      base = base.slice(0, -suffix.length);
    }
  }
  return base;
}

/** Pick the variant matching the vendor's defaults, else the first file. */
function pickPreview(variants, variantSpec) {
  const defaults = Object.entries(variantSpec ?? {})
    .map(([key, spec]) => [key, spec?.default])
    .filter(([, def]) => def !== undefined);
  if (defaults.length) {
    const match = variants.find((v) =>
      defaults.every(([key, def]) => String(v.properties?.[key]) === String(def)),
    );
    if (match) return match;
  }
  return variants[0];
}

function build() {
  const vendorDirs = fs
    .readdirSync(DIST_ROOT, { withFileTypes: true })
    .filter((e) => e.isDirectory() && !e.name.startsWith("."))
    .map((e) => e.name)
    .sort();

  const icons = [];
  const vendors = {};
  for (const vendorId of vendorDirs) {
    const dataPath = path.join(DIST_ROOT, vendorId, "data.json");
    if (!fs.existsSync(dataPath)) continue;
    const data = JSON.parse(fs.readFileSync(dataPath, "utf8"));
    const variantSpec = data.variants ?? {};
    vendors[vendorId] = {
      id: vendorId,
      name: data.name ?? vendorId,
      version: data.version,
      url: data.url,
      license: data.license,
      variants: variantSpec,
    };

    // Group files by (vendor, baseName).
    const groups = new Map();
    for (const f of data.files ?? []) {
      const base = toBaseName(f.name, f.properties);
      let g = groups.get(base);
      if (!g) {
        g = { base, variants: [], description: "", tags: [] };
        groups.set(base, g);
      }
      g.variants.push({ file: f.file, name: f.name, properties: f.properties ?? {} });
      // tags/description are identical across a concept's variants — take first non-empty.
      if (!g.description && f.description) g.description = f.description;
      if (!g.tags.length && Array.isArray(f.tags) && f.tags.length) g.tags = f.tags;
    }

    for (const g of groups.values()) {
      const preview = pickPreview(g.variants, variantSpec);
      icons.push({
        id: `${vendorId}/${g.base}`,
        vendor: vendorId,
        name: g.base,
        tags: g.tags,
        description: g.description,
        file: preview.file,
        variants: g.variants,
      });
    }
  }

  // Stable order: vendor, then name.
  icons.sort((a, b) => a.vendor.localeCompare(b.vendor) || a.name.localeCompare(b.name));

  const payload = { version: 1, count: icons.length, vendors, icons };
  fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
  fs.writeFileSync(OUT_FILE, JSON.stringify(payload));

  const bytes = fs.statSync(OUT_FILE).size;
  const withTags = icons.filter((i) => i.tags.length).length;
  console.log(
    `[build-search-index] ${icons.length} logical icons (${withTags} with tags) -> ` +
      `${OUT_FILE} (${(bytes / 1024 / 1024).toFixed(2)} MB) from ${DIST_ROOT}`,
  );
}

build();
