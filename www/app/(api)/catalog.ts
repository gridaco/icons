import fs from "node:fs/promises";
import path from "node:path";
import type { IconDoc, SearchIndexFile, VendorMeta } from "./search-core";

// Server-side loader for the prebuilt search index (public/search-index.json).
// Cached at module scope so the catalog is parsed once per server instance and
// reused by the /api/search route, the per-icon pages, and the sitemap.

const INDEX_PATH = path.resolve(process.cwd(), "public", "search-index.json");

export type Catalog = {
  icons: IconDoc[];
  vendors: Record<string, VendorMeta>;
  byId: Map<string, IconDoc>;
};

let catalogPromise: Promise<Catalog> | null = null;

export function getCatalog(): Promise<Catalog> {
  if (!catalogPromise) {
    catalogPromise = (async () => {
      const raw = await fs.readFile(INDEX_PATH, "utf8");
      const { icons, vendors } = JSON.parse(raw) as SearchIndexFile;
      const byId = new Map(icons.map((icon) => [icon.id, icon]));
      return { icons, vendors, byId };
    })();
  }
  return catalogPromise;
}

export async function getIcon(vendor: string, name: string): Promise<IconDoc | undefined> {
  const { byId } = await getCatalog();
  return byId.get(`${vendor}/${name}`);
}
