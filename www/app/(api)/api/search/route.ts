import { NextResponse } from "next/server";
import type MiniSearch from "minisearch";
import { getCatalog } from "../../catalog";
import { buildDownloadUrl, CACHE_HEADERS } from "../../lib";
import { createIndex, type IconDoc, runSearch } from "../../search-core";

export const revalidate = 3600;

const MAX_LIMIT = 500;
const DEFAULT_LIMIT = 100;

type LoadedIndex = { mini: MiniSearch<IconDoc>; docs: IconDoc[] };

// Built once per server instance (module scope), not per request — avoids
// re-indexing the catalog on every call.
let indexPromise: Promise<LoadedIndex> | null = null;

function loadIndex(): Promise<LoadedIndex> {
  if (!indexPromise) {
    indexPromise = (async () => {
      const { icons } = await getCatalog();
      return { mini: createIndex(icons), docs: icons };
    })();
  }
  return indexPromise;
}

function parseIntParam(value: string | null, fallback: number, max: number): number {
  const n = Number.parseInt(value ?? "", 10);
  if (!Number.isFinite(n) || n < 0) return fallback;
  return Math.min(n, max);
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const q = searchParams.get("q") ?? searchParams.get("name") ?? undefined;
  const vendor = searchParams.get("vendor") || undefined;
  const limit = parseIntParam(searchParams.get("limit"), DEFAULT_LIMIT, MAX_LIMIT);
  const offset = parseIntParam(searchParams.get("offset"), 0, Number.MAX_SAFE_INTEGER);

  const { mini, docs } = await loadIndex();
  const { total, items } = runSearch(mini, docs, { q, vendor, limit, offset });

  return NextResponse.json(
    {
      total,
      count: items.length,
      limit,
      offset,
      items: items.map((doc) => ({
        id: doc.id,
        vendor: doc.vendor,
        name: doc.name,
        description: doc.description,
        tags: doc.tags,
        download: buildDownloadUrl(doc.vendor, doc.file),
        url: `/icons/${doc.vendor}/${doc.name}`,
        variants: doc.variants.map((v) => ({
          name: v.name,
          properties: v.properties,
          download: buildDownloadUrl(doc.vendor, v.file),
        })),
      })),
    },
    { headers: { ...CACHE_HEADERS } },
  );
}
