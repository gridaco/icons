import MiniSearch, { type SearchResult } from "minisearch";

// Shape of one logical icon in public/search-index.json (built by
// scripts/build-search-index.mjs). Shared by the /api/search route (server) and
// the web app (client) so both search identically off one index.

export type IconVariant = {
  file: string;
  name: string;
  properties: Record<string, string>;
};

export type IconDoc = {
  id: string; // `${vendor}/${name}`
  vendor: string;
  name: string;
  tags: string[];
  description: string;
  file: string; // preview/default variant file
  variants: IconVariant[];
};

export type VendorMeta = {
  id: string;
  name: string;
  version?: string;
  url?: string;
  license?: string;
  variants?: Record<string, { title?: string; default?: string; enum?: string[] }>;
};

export type SearchIndexFile = {
  version: number;
  count: number;
  vendors: Record<string, VendorMeta>;
  icons: IconDoc[];
};

export type SearchParams = {
  q?: string;
  vendor?: string;
  /** Page size. Omit for no pagination (return all matches after `offset`). */
  limit?: number;
  offset?: number;
};

/** Same-origin static asset path for an icon SVG (served from /dist). */
export function previewSrc(vendor: string, file: string): string {
  return `/dist/${vendor}/${file}`;
}

export type SearchOutcome = {
  total: number;
  items: IconDoc[];
};

// Searchable fields. `keywords` is a synthetic field — the tags array joined
// into text so each tag is tokenized; it is never stored. `description` is
// intentionally NOT searchable (display-only until embeddings land). `name` is
// boosted over keywords. storeFields keep the ORIGINAL shapes (tags as array).
const SEARCHABLE_FIELDS = ["name", "keywords"] as const;
const STORE_FIELDS = ["vendor", "name", "description", "file", "variants", "tags"] as const;

export function createIndex(docs: IconDoc[]): MiniSearch<IconDoc> {
  const mini = new MiniSearch<IconDoc>({
    idField: "id",
    fields: [...SEARCHABLE_FIELDS],
    storeFields: [...STORE_FIELDS],
    extractField: (doc, field) => {
      if (field === "keywords") return (doc.tags ?? []).join(" ");
      // Stored fields (e.g. tags array, variants) are returned as-is.
      return doc[field as keyof IconDoc] as unknown as string;
    },
    searchOptions: {
      boost: { name: 2 },
      prefix: true,
      fuzzy: 0.2,
    },
  });
  mini.addAll(docs);
  return mini;
}

function resultToDoc(r: SearchResult): IconDoc {
  return {
    id: r.id as string,
    vendor: r.vendor,
    name: r.name,
    tags: r.tags ?? [],
    description: r.description ?? "",
    file: r.file,
    variants: r.variants ?? [],
  };
}

/**
 * Run a query against the prebuilt index. Empty query returns all docs (so the
 * web app and API share one "browse all + filter" path). Vendor filter and
 * pagination apply to both branches.
 */
export function runSearch(
  mini: MiniSearch<IconDoc>,
  docs: IconDoc[],
  { q, vendor, limit, offset = 0 }: SearchParams,
): SearchOutcome {
  const query = q?.trim();
  let results: IconDoc[] = query ? mini.search(query).map(resultToDoc) : docs;

  if (vendor) {
    results = results.filter((d) => d.vendor === vendor);
  }

  const total = results.length;
  const items = limit === undefined ? results.slice(offset) : results.slice(offset, offset + limit);
  return { total, items };
}
