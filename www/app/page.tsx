"use client";

import { Suspense, useDeferredValue, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { parseAsString, useQueryState } from "nuqs";
import { Search } from "lucide-react";
import type MiniSearch from "minisearch";
import { GridaLogo } from "@/components/grida-logo";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
} from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";
import { InputGroup, InputGroupAddon, InputGroupInput } from "@/components/ui/input-group";
import { Skeleton } from "@/components/ui/skeleton";
import { useVirtualizer } from "@tanstack/react-virtual";
import {
  createIndex,
  type IconDoc,
  type IconVariant,
  previewSrc,
  runSearch,
  type SearchIndexFile,
  type VendorMeta,
} from "./(api)/search-core";

type Catalog = { index: MiniSearch<IconDoc>; docs: IconDoc[]; vendors: VendorMeta[] };

// Stable empty fallbacks so derived values keep a constant reference before load.
const EMPTY_DOCS: IconDoc[] = [];
const EMPTY_VENDORS: VendorMeta[] = [];

/**
 * Resolve which variant to preview for a logical icon given the active variant
 * filters. Returns null when filters are active but no variant matches (so the
 * icon is excluded), mirroring the old per-file filter behavior.
 */
function resolveVariant(
  icon: IconDoc,
  variantFilters: Record<string, string | undefined>,
): IconVariant | null {
  const active = Object.entries(variantFilters).filter(([, v]) => Boolean(v));
  if (!active.length) {
    return icon.variants.find((v) => v.file === icon.file) ?? icon.variants[0] ?? null;
  }
  return (
    icon.variants.find((v) =>
      active.every(([key, value]) => String(v.properties?.[key]) === String(value)),
    ) ?? null
  );
}

/** svgl "dark" logos are light-colored and need a dark tile to be visible. */
function isDarkLogo(vendor: string, variant: IconVariant): boolean {
  return vendor === "svgl" && variant.properties?.theme === "dark";
}

function AppSidebar({
  vendors,
  active,
  onSelect,
}: {
  vendors: { id: string; name?: string; count: number }[];
  active?: string;
  onSelect?: (id: string | undefined) => void;
}) {
  return (
    <Sidebar>
      <SidebarHeader>
        <div className="px-2 py-1">
          <Link href="/" className="flex items-center gap-2">
            <GridaLogo className="h-5 w-5" />
            <span className="text-lg font-bold">Icons</span>
          </Link>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Icon Sets</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton isActive={!active} onClick={() => onSelect?.(undefined)}>
                  <span>All</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              {vendors.map((set) => (
                <SidebarMenuItem key={set.id}>
                  <SidebarMenuButton
                    isActive={active === set.id}
                    onClick={() => onSelect?.(set.id)}
                  >
                    <span>{set.name ?? set.id}</span>
                    <span className="ml-auto text-xs text-muted-foreground">{set.count}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Other Resources</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="https://fonts.grida.co" target="_blank" rel="noopener noreferrer">
                    <span>Fonts</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="https://grida.co/library" target="_blank" rel="noopener noreferrer">
                    <span>Photos</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild>
              <Link href="/docs">
                <span>API</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton asChild>
              <Link href="/about">
                <span>About</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}

// URL is the source of truth for `q` and `vendor` (via nuqs) so views are
// shareable and browser back/forward navigates between them. Typing updates `q`
// optimistically while the URL write is throttled (replace = no history spam);
// selecting a set pushes a history entry.
function IconsExplorer() {
  const [search, setSearch] = useQueryState(
    "q",
    parseAsString.withDefault("").withOptions({ throttleMs: 250, clearOnDefault: true }),
  );
  const [vendorFilter, setVendorFilter] = useQueryState(
    "vendor",
    parseAsString.withOptions({ history: "push", clearOnDefault: true }),
  );

  // Keep typing fluid: the input tracks `search`, but the heavy filter reads a
  // deferred value so the 5k-item recompute never blocks keystrokes.
  const deferredSearch = useDeferredValue(search);
  const isStale = deferredSearch !== search;

  const [catalog, setCatalog] = useState<Catalog | null>(null);
  // Explicit per-axis variant picks. Absent = use the vendor's default; "" = show
  // all (no filter on that axis). Stale keys from another vendor are harmless
  // because the effective filter only reads the active vendor's axes.
  const [variantSelections, setVariantSelections] = useState<Record<string, string>>({});
  const listParentRef = useRef<HTMLDivElement | null>(null);
  const [gridWidth, setGridWidth] = useState(0);

  const loading = catalog === null;
  const index = catalog?.index ?? null;
  const docs = catalog?.docs ?? EMPTY_DOCS;
  const vendors = catalog?.vendors ?? EMPTY_VENDORS;

  // Load the prebuilt search index once and build MiniSearch in-memory. It
  // carries both the icons and vendor metadata, so no other fetch is needed and
  // all subsequent searches are local — no network per keystroke.
  useEffect(() => {
    const controller = new AbortController();
    (async () => {
      try {
        const res = await fetch("/search-index.json", { signal: controller.signal });
        if (!res.ok) return;
        const data: SearchIndexFile = await res.json();
        setCatalog({
          index: createIndex(data.icons),
          docs: data.icons,
          vendors: Object.values(data.vendors),
        });
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") return;
        console.error(err);
      }
    })();
    return () => controller.abort();
  }, []);

  // Logical-icon counts per vendor, derived from the index.
  const countsByVendor = useMemo(() => {
    const map = new Map<string, number>();
    for (const d of docs) map.set(d.vendor, (map.get(d.vendor) ?? 0) + 1);
    return map;
  }, [docs]);

  const vendorsWithCounts = useMemo(
    () =>
      vendors.map((v) => ({
        id: v.id,
        name: v.name,
        count: countsByVendor.get(v.id) ?? 0,
      })),
    [vendors, countsByVendor],
  );

  const activeVendor = useMemo(
    () => vendors.find((v) => v.id === vendorFilter),
    [vendors, vendorFilter],
  );

  // Effective filters, derived during render (no effect): each axis falls back to
  // the vendor default; "" means "All" (no filter on that axis).
  const variantFilters = useMemo(() => {
    const spec = activeVendor?.variants;
    if (!spec) return {} as Record<string, string>;
    const out: Record<string, string> = {};
    for (const [key, s] of Object.entries(spec)) {
      const value = variantSelections[key] ?? s.default;
      if (value) out[key] = value;
    }
    return out;
  }, [activeVendor, variantSelections]);

  // In-memory search + vendor filter, then variant-aware preview resolution.
  const icons = useMemo(() => {
    if (!index) return [] as { icon: IconDoc; src: string; dark: boolean }[];
    const { items } = runSearch(index, docs, {
      q: deferredSearch,
      vendor: vendorFilter ?? undefined,
    });
    const out: { icon: IconDoc; src: string; dark: boolean }[] = [];
    for (const icon of items) {
      const variant = resolveVariant(icon, variantFilters);
      if (variant) {
        out.push({
          icon,
          src: previewSrc(icon.vendor, variant.file),
          dark: isDarkLogo(icon.vendor, variant),
        });
      }
    }
    return out;
  }, [index, docs, deferredSearch, vendorFilter, variantFilters]);

  // Density-based columns: aim for ~TARGET-wide cells (auto-fill), so cells stay
  // compact and square at any width instead of ballooning at low column counts.
  const TARGET_CELL = 148;
  useEffect(() => {
    if (typeof window === "undefined") return;
    const node = listParentRef.current;
    if (!node) return;

    const measure = (width: number) => {
      if (width > 0) setGridWidth(width);
    };

    const resizeObserver = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (entry) measure(entry.contentRect.width);
    });

    resizeObserver.observe(node);
    return () => resizeObserver.disconnect();
  }, []);

  // Square cells sized to the measured width, so the bordered grid tiles exactly.
  const columns = gridWidth > 0 ? Math.max(2, Math.round(gridWidth / TARGET_CELL)) : 6;
  const cellSize = gridWidth > 0 ? Math.floor(gridWidth / columns) : TARGET_CELL;
  const rowCount = Math.ceil(icons.length / Math.max(columns, 1));

  const virtual = useVirtualizer({
    count: rowCount,
    getScrollElement: () => listParentRef.current,
    estimateSize: () => cellSize,
    overscan: 6,
  });

  // Re-measure rows when the cell size changes (column/width breakpoint).
  useEffect(() => {
    virtual.measure();
  }, [cellSize, virtual]);

  return (
    <SidebarProvider>
      <div className="flex h-screen w-full bg-background">
        <AppSidebar
          vendors={vendorsWithCounts}
          active={vendorFilter ?? undefined}
          onSelect={(id) => setVendorFilter(id ?? null)}
        />
        <main className="flex flex-1 flex-col overflow-hidden">
          <div className="border-b bg-card/40 px-6 py-4 backdrop-blur">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-muted-foreground">
                  {loading ? "Loading icons..." : `Showing ${icons.length} icons`}
                </p>
                {vendorFilter && (
                  <p className="text-xs text-muted-foreground">
                    Filtered by {activeVendor?.name ?? vendorFilter}
                  </p>
                )}
              </div>
              <div className="w-full max-w-md">
                <InputGroup>
                  <InputGroupInput
                    type="search"
                    placeholder="Search icons by name or keyword..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                  />
                  <InputGroupAddon align="inline-end">
                    <Search />
                  </InputGroupAddon>
                </InputGroup>
              </div>
            </div>
          </div>

          {activeVendor?.variants && Object.keys(activeVendor.variants).length > 0 && (
            <div className="border-b bg-card/30 px-6 py-3">
              <div className="flex flex-wrap gap-4">
                {Object.entries(activeVendor.variants).map(([key, spec]) => {
                  const current = variantSelections[key] ?? spec.default;
                  return (
                    <div key={key} className="flex flex-col gap-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-semibold text-muted-foreground">
                          {spec.title ?? key}
                        </span>
                        <div className="flex items-center gap-1">
                          <Button
                            size="sm"
                            variant={variantSelections[key] === "" ? "secondary" : "ghost"}
                            onClick={() => setVariantSelections((prev) => ({ ...prev, [key]: "" }))}
                          >
                            All
                          </Button>
                          {(spec.enum ?? []).map((option) => (
                            <Button
                              key={option}
                              size="sm"
                              variant={current === option ? "secondary" : "ghost"}
                              onClick={() =>
                                setVariantSelections((prev) => ({ ...prev, [key]: option }))
                              }
                            >
                              {option}
                            </Button>
                          ))}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          <div className="flex-1 overflow-y-auto" ref={listParentRef}>
            {loading ? (
              <GridSkeleton />
            ) : (
              <div className="bg-card">
                <div
                  className="relative w-full transition-opacity duration-150"
                  style={{ height: virtual.getTotalSize(), opacity: isStale ? 0.6 : 1 }}
                >
                  {virtual.getVirtualItems().map((row) => {
                    const start = row.index * Math.max(columns, 1);
                    const slice = icons.slice(start, start + Math.max(columns, 1));
                    return (
                      <div
                        key={row.key}
                        className="absolute inset-x-0 grid"
                        style={{
                          transform: `translateY(${row.start}px)`,
                          height: row.size,
                          gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))`,
                        }}
                      >
                        {slice.map(({ icon, src, dark }) => (
                          <Link
                            key={icon.id}
                            href={`/icons/${icon.vendor}/${encodeURIComponent(icon.name)}`}
                            title={icon.description || icon.name}
                            className="group flex flex-col items-center justify-center gap-2.5 border-r border-b p-3 text-center transition-colors hover:bg-accent"
                          >
                            <div
                              className={
                                dark
                                  ? "flex h-12 w-12 items-center justify-center rounded-lg bg-neutral-900"
                                  : "flex h-12 w-12 items-center justify-center"
                              }
                            >
                              <img
                                src={src}
                                alt={icon.name}
                                width={28}
                                height={28}
                                loading="lazy"
                                className={
                                  icon.vendor === "svgl"
                                    ? "h-7 w-7 object-contain"
                                    : "h-7 w-7 object-contain dark:invert"
                                }
                              />
                            </div>
                            <div className="flex w-full flex-col items-center">
                              <span className="line-clamp-1 max-w-full text-xs font-medium">
                                {icon.name}
                              </span>
                              <span className="text-[10px] text-muted-foreground/70">
                                {icon.vendor}
                              </span>
                            </div>
                          </Link>
                        ))}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
            {!loading && icons.length === 0 && (
              <div className="p-6 text-sm text-muted-foreground">
                No icons found. Try a different search or set.
              </div>
            )}
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}

function GridSkeleton() {
  return (
    <div className="bg-card">
      <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-7 xl:grid-cols-8">
        {Array.from({ length: 30 }, (_, i) => (
          <div
            key={i}
            className="flex aspect-square flex-col items-center justify-center gap-2.5 border-r border-b p-3"
          >
            <Skeleton className="h-12 w-12 rounded-lg" />
            <Skeleton className="h-2.5 w-2/3" />
          </div>
        ))}
      </div>
    </div>
  );
}

export default function Home() {
  // nuqs/useQueryState reads useSearchParams(), which needs a Suspense boundary.
  return (
    <Suspense fallback={<GridSkeleton />}>
      <IconsExplorer />
    </Suspense>
  );
}
