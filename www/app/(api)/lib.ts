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
  items: Array<{
    vendor: string;
    version?: string;
    name: string;
    download: string;
    properties: Record<string, unknown>;
  }>,
  opts: { vendor?: string; q?: string }
) {
  const qLower = opts.q?.trim().toLowerCase() ?? "";
  let filtered = items;
  if (opts.vendor) {
    filtered = filtered.filter((i) => i.vendor === opts.vendor);
  }
  if (qLower) {
    filtered = filtered.filter((i) => i.name.toLowerCase().includes(qLower));
  }
  return filtered;
}
