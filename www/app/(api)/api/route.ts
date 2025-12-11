import { NextResponse } from "next/server";
import { buildAllItems, filterItems } from "../lib";

export const revalidate = 3600;

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const vendor = searchParams.get("vendor") || undefined;
  const q = searchParams.get("q") ?? searchParams.get("name") ?? undefined;
  const variants: Record<string, string> = {};
  searchParams.forEach((value, key) => {
    if (key.startsWith("variant:") && value) {
      variants[key.replace("variant:", "")] = value;
    }
  });

  const { items, total } = await buildAllItems();
  const filtered = filterItems(items, { vendor, q, variants });

  return NextResponse.json(
    {
      total,
      count: filtered.length,
      items: filtered,
    },
    {
      headers: {
        "cache-control":
          "public, max-age=0, s-maxage=3600, stale-while-revalidate=86400",
      },
    }
  );
}
