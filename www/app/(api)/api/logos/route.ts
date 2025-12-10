import { NextResponse } from "next/server";
import { buildSvglItems, filterItems } from "../../lib";

export const revalidate = 3600;

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const q = searchParams.get("q") ?? searchParams.get("name") ?? undefined;

  const { items, total, missing } = await buildSvglItems();
  if (missing) {
    return NextResponse.json(
      {
        error: "SVGL data not found. Ensure public/dist/svgl/data.json exists.",
      },
      { status: 500 },
    );
  }

  const filtered = filterItems(items, { q });
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
    },
  );
}
