"use client";

import Link from "next/link";
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
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";
import { Search } from "lucide-react";

// Icon sets data - this will be replaced with actual data later
const iconSets = [
  { name: "Radix UI", id: "radix-ui", count: 320 },
  { name: "Material Design", id: "material", count: 2000 },
  { name: "Unicons", id: "unicons", count: 1200 },
  { name: "Ant Design", id: "antd", count: 800 },
];

function AppSidebar() {
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
              {iconSets.map((set) => (
                <SidebarMenuItem key={set.id}>
                  <SidebarMenuButton asChild>
                    <Link href="/">
                      <span>{set.name}</span>
                      <span className="ml-auto text-xs text-muted-foreground">
                        {set.count}
                      </span>
                    </Link>
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

export default function ApiPage() {
  return (
    <SidebarProvider>
      <div className="flex h-screen w-full">
        <AppSidebar />
        <main className="flex flex-1 flex-col overflow-hidden">
          {/* Search Bar */}
          <div className="border-b px-6 py-4">
            <div className="max-w-md">
              <InputGroup>
                <InputGroupInput type="search" placeholder="Search icons..." />
                <InputGroupAddon align="inline-end">
                  <Search />
                </InputGroupAddon>
              </InputGroup>
            </div>
          </div>

          {/* API Content */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="mx-auto max-w-3xl">
              <h1 className="mb-6 text-3xl font-bold">API</h1>
              <p className="text-muted-foreground">
                API documentation coming soon.
              </p>
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}
