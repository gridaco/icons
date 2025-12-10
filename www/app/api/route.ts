import { NextResponse } from "next/server";
import path from "node:path";
import fs from "node:fs/promises";

type FileEntry = {
  name: string;
  file: string;
  properties?: Record<string, unknown>;
};

type VendorData = {
  vendor?: string;
  name?: string;
  version?: string;
  files?: FileEntry[];
};

// Read built data from public/dist so it is available at runtime without FS writes.
const DIST_ROOT = path.resolve(process.cwd(), "public", "dist");
const HOST = "https://icons.grida.co";
const BASE = `${HOST}/dist`;

function buildDownloadUrl(vendorId: string, file: string): string {
  return `${BASE}/${vendorId}/${file}`;
}

async function readJson<T = unknown>(filePath: string): Promise<T | null> {
  try {
    const raw = await fs.readFile(filePath, "utf8");
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

async function loadVendors(): Promise<Array<{ id: string; data: VendorData }>> {
  const entries = await fs.readdir(DIST_ROOT, { withFileTypes: true });
  const vendors: Array<{ id: string; data: VendorData }> = [];
  for (const ent of entries) {
    if (!ent.isDirectory()) continue;
    if (ent.name.startsWith(".")) continue;
    const dataPath = path.join(DIST_ROOT, ent.name, "data.json");
    const data = await readJson<VendorData>(dataPath);
    if (data) {
      vendors.push({ id: ent.name, data });
    }
  }
  return vendors;
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const filterVendor = searchParams.get("vendor") || undefined;
  const q = searchParams.get("q") ?? searchParams.get("name") ?? "";
  const qLower = q.trim().toLowerCase();

  const vendors = await loadVendors();
  const items = vendors.flatMap(({ id, data }) =>
    (data.files ?? []).map((f) => ({
      vendor: data.vendor ?? id,
      version: data.version,
      name: f.name,
      download: buildDownloadUrl(id, f.file),
      properties: f.properties ?? {},
    }))
  );

  const total = items.length;
  let filtered = items;
  if (filterVendor) {
    filtered = filtered.filter((i) => i.vendor === filterVendor);
  }
  if (qLower) {
    filtered = filtered.filter((i) => i.name.toLowerCase().includes(qLower));
  }

  return NextResponse.json({
    total,
    count: filtered.length,
    items: filtered,
  });
}
