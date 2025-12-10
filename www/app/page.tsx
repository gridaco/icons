"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { Search } from "lucide-react";
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
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";
import { useVirtualizer } from "@tanstack/react-virtual";

type IconItem = {
  vendor: string;
  version?: string;
  name: string;
  download: string;
  properties: Record<string, unknown>;
};

type ApiResponse = {
  total: number;
  count: number;
  items: IconItem[];
};

type VendorItem = {
  id: string;
  name?: string;
  version?: string;
};

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
              {vendors.map((set) => (
                <SidebarMenuItem key={set.id}>
                  <SidebarMenuButton
                    isActive={active === set.id}
                    onClick={() => onSelect?.(set.id)}
                  >
                    <span>{set.name ?? set.id}</span>
                    <span className="ml-auto text-xs text-muted-foreground">
                      {set.count}
                    </span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
              <SidebarMenuItem>
                <SidebarMenuButton
                  isActive={!active}
                  onClick={() => onSelect?.(undefined)}
                >
                  <span>All</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Other Resources</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a
                    href="https://fonts.grida.co"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <span>Fonts</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a
                    href="https://grida.co/library"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
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
              <Link href="/api">
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

export default function Home() {
  const [icons, setIcons] = useState<IconItem[]>([]);
  const [vendors, setVendors] = useState<VendorItem[]>([]);
  const [search, setSearch] = useState("");
  const [vendorFilter, setVendorFilter] = useState<string | undefined>(
    undefined
  );
  const [loading, setLoading] = useState(false);
  const listParentRef = useRef<HTMLDivElement | null>(null);
  const [columns, setColumns] = useState(2);

  useEffect(() => {
    const controller = new AbortController();
    const loadVendors = async () => {
      try {
        const res = await fetch("/api/vendors", { signal: controller.signal });
        if (!res.ok) return;
        const data: { items: VendorItem[] } = await res.json();
        setVendors(data.items);
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") return;
        console.error(err);
      }
    };
    loadVendors();
    return () => controller.abort();
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    const load = async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (search.trim()) params.set("q", search.trim());
        if (vendorFilter) params.set("vendor", vendorFilter);
        const res = await fetch(`/api?${params.toString()}`, {
          signal: controller.signal,
        });
        if (!res.ok) return;
        const data: ApiResponse = await res.json();
        setIcons(data.items);
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") return;
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    load();
    return () => controller.abort();
  }, [search, vendorFilter]);

  const vendorsWithCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    for (const icon of icons) {
      counts[icon.vendor] = (counts[icon.vendor] ?? 0) + 1;
    }
    const mergedIds = new Set<string>([
      ...Object.keys(counts),
      ...vendors.map((v) => v.id),
    ]);
    return Array.from(mergedIds).map((id) => {
      const meta = vendors.find((v) => v.id === id);
      return { id, name: meta?.name, count: counts[id] ?? 0 };
    });
  }, [icons, vendors]);

  // Keep a simple breakpoint-based column count to align with the grid classes
  useEffect(() => {
    if (typeof window === "undefined") return;
    const node = listParentRef.current;
    if (!node) return;

    const calcColumns = (width: number) => {
      if (width >= 1280) return 6; // xl
      if (width >= 1024) return 5; // lg
      if (width >= 768) return 4; // md
      if (width >= 640) return 3; // sm
      return 2;
    };

    const resizeObserver = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (!entry) return;
      const next = calcColumns(entry.contentRect.width);
      setColumns((prev) => (prev === next ? prev : next));
    });

    resizeObserver.observe(node);
    setColumns(calcColumns(node.getBoundingClientRect().width));

    return () => resizeObserver.disconnect();
  }, []);

  const rowCount = Math.ceil(icons.length / Math.max(columns, 1));

  const virtual = useVirtualizer({
    count: rowCount,
    getScrollElement: () => listParentRef.current,
    estimateSize: () => 220, // card height incl. gap/padding
    overscan: 8,
  });

  return (
    <SidebarProvider>
      <div className="flex h-screen w-full bg-background">
        <AppSidebar
          vendors={vendorsWithCounts}
          active={vendorFilter}
          onSelect={setVendorFilter}
        />
        <main className="flex flex-1 flex-col overflow-hidden">
          <div className="border-b bg-card/40 px-6 py-4 backdrop-blur">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-muted-foreground">
                  {loading
                    ? "Loading icons..."
                    : `Showing ${icons.length} icons`}
                </p>
                {vendorFilter && (
                  <p className="text-xs text-muted-foreground">
                    Filtered by {vendorFilter}
                  </p>
                )}
              </div>
              <div className="w-full max-w-md">
                <InputGroup>
                  <InputGroupInput
                    type="search"
                    placeholder="Search icons..."
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

          <div className="flex-1 overflow-y-auto p-6" ref={listParentRef}>
            <div
              className="relative w-full"
              style={{ height: virtual.getTotalSize() }}
            >
              {virtual.getVirtualItems().map((row) => {
                const start = row.index * Math.max(columns, 1);
                const slice = icons.slice(start, start + Math.max(columns, 1));
                return (
                  <div
                    key={row.key}
                    className="absolute left-0 right-0"
                    style={{ transform: `translateY(${row.start}px)` }}
                  >
                    <div
                      className="grid gap-4"
                      style={{
                        gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))`,
                      }}
                    >
                      {slice.map((icon) => (
                        <div key={icon.download} className="h-full">
                          <Button
                            variant="ghost"
                            className="group flex h-full w-full flex-col items-center justify-between gap-3 rounded-xl border bg-card/60 p-4 text-center shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                            asChild
                          >
                            <a
                              href={icon.download}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              <div className="flex h-14 w-14 items-center justify-center rounded-lg border bg-muted/70">
                                <Image
                                  src={icon.download}
                                  alt={icon.name}
                                  width={32}
                                  height={32}
                                  className="h-8 w-8 object-contain"
                                />
                              </div>
                              <div className="flex flex-col items-center gap-1">
                                <span className="line-clamp-1 text-xs font-medium">
                                  {icon.name}
                                </span>
                                <span className="rounded-full bg-muted px-2 py-0.5 text-[11px] text-muted-foreground group-hover:text-foreground">
                                  {icon.vendor}
                                </span>
                              </div>
                            </a>
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
            {icons.length === 0 && !loading && (
              <div className="mt-6 text-sm text-muted-foreground">
                No icons found. Try a different search or set.
              </div>
            )}
            {loading && (
              <div className="mt-6 text-sm text-muted-foreground">
                Loading...
              </div>
            )}
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}
