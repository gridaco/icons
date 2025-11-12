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

export default function AboutPage() {
  return (
    <SidebarProvider>
      <div className="flex h-screen w-full">
        <AppSidebar />
        <main className="flex flex-1 flex-col overflow-hidden">
          {/* Search Bar */}
          <div className="border-b px-6 py-4">
            <div className="max-w-md">
              <InputGroup>
                <InputGroupInput
                  type="search"
                  placeholder="Search icons..."
                />
                <InputGroupAddon align="inline-end">
                  <Search />
                </InputGroupAddon>
              </InputGroup>
            </div>
          </div>

          {/* About Content */}
          <div className="flex-1 overflow-y-auto p-6">
            <div className="mx-auto max-w-3xl">
              <h1 className="mb-6 text-3xl font-bold">About Grida Icons</h1>
              
              <div className="space-y-6">
                <section>
                  <h2 className="mb-3 text-xl font-semibold">Overview</h2>
                  <p className="text-muted-foreground leading-relaxed">
                    <strong>Grida Icons</strong> is a comprehensive icon library with rich metadata for easy search, preview, and import. Built for developers and AI agents.
                  </p>
                </section>

                <section>
                  <h2 className="mb-3 text-xl font-semibold">Features</h2>
                  <div className="space-y-4">
                    <div>
                      <h3 className="mb-2 font-medium">🎯 Rich Metadata</h3>
                      <p className="text-muted-foreground text-sm leading-relaxed">
                        Every icon comes with comprehensive metadata including keywords for better searchability, visual descriptions of icon appearance and meaning, and categorization for easy browsing.
                      </p>
                    </div>
                    <div>
                      <h3 className="mb-2 font-medium">🔍 Enhanced Search & Discovery</h3>
                      <p className="text-muted-foreground text-sm leading-relaxed">
                        Powerful search capabilities powered by metadata, visual preview of icons, and easy import and integration.
                      </p>
                    </div>
                    <div>
                      <h3 className="mb-2 font-medium">🤖 AI Agent Library</h3>
                      <p className="text-muted-foreground text-sm leading-relaxed">
                        Designed with AI agents in mind, Grida Icons provides structured metadata that AI systems can understand, semantic descriptions for intelligent icon selection, and machine-readable formats for automated workflows.
                      </p>
                    </div>
                  </div>
                </section>

                <section>
                  <h2 className="mb-3 text-xl font-semibold">Icon Sets</h2>
                  <p className="text-muted-foreground mb-4 text-sm leading-relaxed">
                    Grida Icons combines:
                  </p>
                  <ul className="text-muted-foreground ml-6 list-disc space-y-2 text-sm">
                    <li><strong>Grida-made icons</strong> - Original icon designs created by Grida</li>
                    <li><strong>Popular icon sets</strong> - Mirrored and enhanced versions of famous icon libraries including Material Icons, Lucide (Feather), Radix UI, and more</li>
                  </ul>
                </section>

                <section>
                  <h2 className="mb-3 text-xl font-semibold">Purpose</h2>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    Grida Icons serves as both a <strong>developer tool</strong> and an <strong>AI agent library</strong>, making it easier than ever to search and discover the perfect icon, preview icons before importing, import icons into your projects, and enable AI systems to intelligently select and use icons based on context.
                  </p>
                </section>

                <section>
                  <h2 className="mb-3 text-xl font-semibold">Contributing</h2>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    We welcome contributions! Whether you're adding new icons, improving metadata, or enhancing search capabilities, your help makes Grida Icons better for everyone.
                  </p>
                </section>
              </div>
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}

