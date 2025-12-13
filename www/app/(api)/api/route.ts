import { NextResponse } from "next/server";
import {
  ApiItemsResponse,
  buildAllItems,
  CACHE_HEADERS,
  filterItems,
  parseItemsQuery,
} from "../lib";

export const revalidate = 3600;

export async function GET(request: Request) {
  const { vendor, q, variants } = parseItemsQuery(request);

  const { items, total } = await buildAllItems();
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
