import type { MetadataRoute } from "next";
import { getCatalog } from "./(api)/catalog";
import { SITE_URL } from "./(api)/lib";

// One sitemap file covers the whole catalog (well under the 50k URL / 50MB
// per-file limit). Lists home, vendor-filtered views, and every logical icon
// so crawlers discover the on-demand (ISR) per-icon pages.
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const { icons, vendors } = await getCatalog();

  const staticRoutes: MetadataRoute.Sitemap = [
    { url: `${SITE_URL}/`, changeFrequency: "weekly", priority: 1 },
    { url: `${SITE_URL}/docs`, changeFrequency: "monthly", priority: 0.5 },
    { url: `${SITE_URL}/about`, changeFrequency: "monthly", priority: 0.3 },
  ];

  const vendorRoutes: MetadataRoute.Sitemap = Object.keys(vendors).map((id) => ({
    url: `${SITE_URL}/?vendor=${id}`,
    changeFrequency: "weekly",
    priority: 0.5,
  }));

  const iconRoutes: MetadataRoute.Sitemap = icons.map((icon) => ({
    url: `${SITE_URL}/icons/${icon.vendor}/${encodeURIComponent(icon.name)}`,
    changeFrequency: "monthly",
    priority: 0.6,
  }));

  return [...staticRoutes, ...vendorRoutes, ...iconRoutes];
}
