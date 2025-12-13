import fs from "node:fs/promises";
import path from "node:path";

export type FileEntry = {
  name: string;
  file: string;
  properties?: Record<string, unknown>;
};

export type VendorData = {
  vendor?: string;
  name?: string;
  version?: string;
  files?: FileEntry[];
};

export type ApiItem = {
  vendor: string;
  version?: string;
  name: string;
  download: string;
  properties: Record<string, unknown>;
};

export type ApiItemsResponse = {
  total: number;
  count: number;
  items: ApiItem[];
};

export type ApiErrorResponse = {
  error: string;
};

export type ApiVendorSummary = {
  id: string;
  count: number;
  vendor?: string;
  name?: string;
  version?: string;
};

export type ApiVendorsResponse = {
  total: number;
  items: ApiVendorSummary[];
};

export type ItemsQuery = {
  vendor?: string;
  q?: string;
  variants: Record<string, string>;
};

export const CACHE_CONTROL_HEADER_VALUE =
  "public, max-age=0, s-maxage=3600, stale-while-revalidate=86400";

export const CACHE_HEADERS = {
  "cache-control": CACHE_CONTROL_HEADER_VALUE,
} as const;

export function parseItemsQuery(request: Request): ItemsQuery {
  const { searchParams } = new URL(request.url);
  const vendor = searchParams.get("vendor") || undefined;
  const q = searchParams.get("q") ?? searchParams.get("name") ?? undefined;

  const variants: Record<string, string> = {};
  searchParams.forEach((value, key) => {
    if (key.startsWith("variant:") && value) {
      variants[key.slice("variant:".length)] = value;
    }
  });

  return { vendor, q, variants };
}

const HOST =
  process.env.NODE_ENV === "production"
    ? "https://icons.grida.co"
    : "http://localhost:3001";
const BASE = `${HOST}/dist`;
const DIST_ROOT = path.resolve(process.cwd(), "public", "dist");

async function readJson<T>(filePath: string): Promise<T | null> {
  try {
    const raw = await fs.readFile(filePath, "utf8");
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

function buildDownloadUrl(vendorId: string, file: string): string {
  return `${BASE}/${vendorId}/${file}`;
}

export async function loadAllVendors(): Promise<
  Array<{ id: string; data: VendorData }>
> {
  const entries = await fs.readdir(DIST_ROOT, { withFileTypes: true });
  const vendors: Array<{ id: string; data: VendorData }> = [];
  for (const ent of entries) {
    if (!ent.isDirectory() || ent.name.startsWith(".")) continue;
    const dataPath = path.join(DIST_ROOT, ent.name, "data.json");
    const data = await readJson<VendorData>(dataPath);
    if (data) {
      vendors.push({ id: ent.name, data });
    }
  }
  return vendors;
}

export async function buildAllItems() {
  const vendors = await loadAllVendors();
  const items = vendors.flatMap(({ id, data }) =>
    (data.files ?? []).map((f) => ({
      vendor: data.vendor ?? id,
      version: data.version,
      name: f.name,
      download: buildDownloadUrl(id, f.file),
      properties: f.properties ?? {},
    }))
  );
  return { items, total: items.length };
}

export async function buildSvglItems() {
  const data = await readJson<VendorData>(
    path.join(DIST_ROOT, "svgl", "data.json")
  );
  if (!data) return { items: [], total: 0, missing: true };
  const items =
    data.files?.map((f) => ({
      vendor: data.vendor ?? "svgl",
      version: data.version,
      name: f.name,
      download: buildDownloadUrl("svgl", f.file),
      properties: f.properties ?? {},
    })) ?? [];
  return { items, total: items.length, missing: false };
}

export function filterItems(
  items: ApiItem[],
  opts: { vendor?: string; q?: string; variants?: Record<string, string> }
) {
  const qLower = opts.q?.trim().toLowerCase() ?? "";
  let filtered = items;
  if (opts.vendor) {
    filtered = filtered.filter((i) => i.vendor === opts.vendor);
  }
  if (qLower) {
    filtered = filtered.filter((i) => i.name.toLowerCase().includes(qLower));
  }
  const variantEntries = Object.entries(opts.variants ?? {}).filter(([, v]) =>
    Boolean(v)
  );
  if (variantEntries.length) {
    filtered = filtered.filter((i) =>
      variantEntries.every(([key, value]) => {
        const propValue = i.properties?.[key];
        return propValue !== undefined && String(propValue) === String(value);
      })
    );
  }
  return filtered;
}
