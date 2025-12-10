import { NextResponse } from "next/server";
import { loadAllVendors } from "../../lib";

export const revalidate = 3600;

export async function GET() {
  const vendors = await loadAllVendors();
  const items = vendors.map(({ id, data }) => {
    // Exclude files to keep payload small
    const { files, ...rest } = data;
    void files;
    return {
      id,
      ...rest,
    };
  });

  return NextResponse.json(
    {
      total: items.length,
      items,
    },
    {
      headers: {
        "cache-control":
          "public, max-age=0, s-maxage=3600, stale-while-revalidate=86400",
      },
    }
  );
}
