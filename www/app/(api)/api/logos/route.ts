import { NextResponse } from "next/server";
import {
  ApiErrorResponse,
  ApiItemsResponse,
  buildSvglItems,
  CACHE_HEADERS,
  filterItems,
  parseItemsQuery,
} from "../../lib";

export const revalidate = 3600;

export async function GET(request: Request) {
  const { vendor, q, variants } = parseItemsQuery(request);

  const { items, total, missing } = await buildSvglItems();
  if (missing) {
    return NextResponse.json<ApiErrorResponse>(
      {
        error: "SVGL data not found. Ensure public/dist/svgl/data.json exists.",
      },
      { status: 500 }
    );
  }

  const filtered = filterItems(items, { vendor, q, variants });
  return NextResponse.json<ApiItemsResponse>(
    {
      total,
      count: filtered.length,
      items: filtered,
    },
    {
      headers: {
        ...CACHE_HEADERS,
      },
    }
  );
}
