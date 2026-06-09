import type { Metadata } from "next";
import Link from "next/link";
import { SITE_URL } from "../(api)/lib";

export const metadata: Metadata = {
  title: "API Reference | Grida Icons",
  description:
    "Free, public, zero-auth REST API for searching 5,000+ icons across Heroicons, Lucide, Phosphor, Octicons, Radix, and SVGL — with keywords, descriptions, and downloadable SVGs.",
  alternates: { canonical: "/docs" },
};

type Param = { name: string; type: string; required?: boolean; desc: string };

function ParamTable({ params }: { params: Param[] }) {
  return (
    <div className="mt-4 overflow-hidden rounded-lg border">
      <table className="w-full text-sm">
        <thead className="bg-muted/50 text-left text-xs text-muted-foreground">
          <tr>
            <th className="px-4 py-2 font-medium">Parameter</th>
            <th className="px-4 py-2 font-medium">Type</th>
            <th className="px-4 py-2 font-medium">Description</th>
          </tr>
        </thead>
        <tbody>
          {params.map((p) => (
            <tr key={p.name} className="border-t">
              <td className="px-4 py-2 align-top font-mono text-xs">
                {p.name}
                {p.required && <span className="ml-1 text-[10px] text-amber-600">required</span>}
              </td>
              <td className="px-4 py-2 align-top font-mono text-xs text-muted-foreground">
                {p.type}
              </td>
              <td className="px-4 py-2 align-top text-muted-foreground">{p.desc}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Code({ children }: { children: string }) {
  return (
    <pre className="mt-4 overflow-x-auto rounded-lg border bg-muted/40 p-4 text-xs leading-relaxed">
      <code>{children}</code>
    </pre>
  );
}

function Method({ path }: { path: string }) {
  return (
    <div className="flex items-center gap-2 font-mono text-sm">
      <span className="rounded bg-emerald-600/10 px-2 py-0.5 text-xs font-semibold text-emerald-700">
        GET
      </span>
      <span>{path}</span>
    </div>
  );
}

export default function DocsPage() {
  const base = SITE_URL;

  return (
    <main className="mx-auto max-w-3xl px-6 py-12">
      <nav className="mb-8 text-sm text-muted-foreground">
        <Link href="/" className="hover:text-foreground">
          ← Back to Icons
        </Link>
      </nav>

      <h1 className="text-3xl font-bold">API Reference</h1>
      <p className="mt-3 text-base text-muted-foreground">
        A free, public, zero-auth REST API over the Grida Icons catalog — 5,000+ icons from
        Heroicons, Lucide, Phosphor, Octicons, Radix UI, and SVGL, enriched with keywords and
        descriptions. No API key, CORS open to all origins, responses cached at the edge.
      </p>

      <section className="mt-8">
        <h2 className="text-sm font-semibold text-muted-foreground">Base URL</h2>
        <Code>{base}</Code>
      </section>

      {/* ---------------- Search ---------------- */}
      <section className="mt-12 border-t pt-8">
        <h2 className="text-xl font-semibold">Search icons</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Ranked keyword search over icon names and tags (prefix + fuzzy matching). Returns one
          result per logical icon, with its variants grouped. This is the recommended endpoint for
          building search UIs.
        </p>
        <div className="mt-4">
          <Method path="/api/search" />
        </div>
        <ParamTable
          params={[
            { name: "q", type: "string", desc: "Search query (matches name + tags). Alias: name." },
            { name: "vendor", type: "string", desc: "Restrict to one set, e.g. lucide-icons." },
            { name: "limit", type: "number", desc: "Page size. Default 100, max 500." },
            { name: "offset", type: "number", desc: "Pagination offset. Default 0." },
          ]}
        />
        <Code>{`curl "${base}/api/search?q=trash&limit=2"`}</Code>
        <Code>{`{
  "total": 16,
  "count": 2,
  "limit": 2,
  "offset": 0,
  "items": [
    {
      "id": "heroicons/trash",
      "vendor": "heroicons",
      "name": "trash",
      "description": "Wastebasket symbol indicating the action of deleting data.",
      "tags": ["trash", "delete", "remove", "bin"],
      "download": "${base}/dist/heroicons/src/24/outline/trash.svg",
      "url": "/icons/heroicons/trash",
      "variants": [
        {
          "name": "trash",
          "properties": { "size": "24", "style": "solid" },
          "download": "${base}/dist/heroicons/src/24/solid/trash.svg"
        }
      ]
    }
  ]
}`}</Code>
      </section>

      {/* ---------------- List ---------------- */}
      <section className="mt-12 border-t pt-8">
        <h2 className="text-xl font-semibold">List icons</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Lists every icon file (each variant is a separate item). Filtering is exact substring on
          name. Use <span className="font-mono text-xs">/api/search</span> for ranked search.
        </p>
        <div className="mt-4">
          <Method path="/api" />
        </div>
        <ParamTable
          params={[
            { name: "vendor", type: "string", desc: "Restrict to one set." },
            { name: "q", type: "string", desc: "Case-insensitive substring on the icon name." },
            {
              name: "variant:<key>",
              type: "string",
              desc: "Filter by a variant property, e.g. variant:style=solid or variant:weight=bold.",
            },
          ]}
        />
        <Code>{`curl "${base}/api?vendor=phosphor-icons&variant:weight=bold"`}</Code>
      </section>

      {/* ---------------- Logos ---------------- */}
      <section className="mt-12 border-t pt-8">
        <h2 className="text-xl font-semibold">Brand logos (SVGL)</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Same shape as <span className="font-mono text-xs">/api</span>, scoped to the SVGL brand
          logo set (light/dark themes, symbol/wordmark kinds).
        </p>
        <div className="mt-4">
          <Method path="/api/logos" />
        </div>
        <Code>{`curl "${base}/api/logos?variant:theme=dark"`}</Code>
      </section>

      {/* ---------------- Vendors ---------------- */}
      <section className="mt-12 border-t pt-8">
        <h2 className="text-xl font-semibold">List sets</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Metadata for every icon set, including its variant axes and counts.
        </p>
        <div className="mt-4">
          <Method path="/api/vendors" />
        </div>
        <Code>{`{
  "total": 6,
  "items": [
    {
      "id": "heroicons",
      "name": "Heroicons",
      "version": "2.2.0",
      "count": 1288,
      "variants": {
        "size": { "title": "Size", "default": "24", "enum": ["16", "20", "24"] },
        "style": { "title": "Style", "default": "outline", "enum": ["solid", "outline"] }
      }
    }
  ]
}`}</Code>
      </section>

      {/* ---------------- Assets ---------------- */}
      <section className="mt-12 border-t pt-8">
        <h2 className="text-xl font-semibold">Raw SVG assets</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Every <span className="font-mono text-xs">download</span> URL points at the raw SVG,
          served with <span className="font-mono text-xs">Access-Control-Allow-Origin: *</span> and
          an immutable one-year cache — safe to hotlink or embed directly.
        </p>
        <div className="mt-4">
          <Method path="/dist/{vendor}/{file}" />
        </div>
        <Code>{`<img src="${base}/dist/lucide-icons/src/arrow-up.svg" width="24" height="24" />`}</Code>
      </section>

      {/* ---------------- Notes ---------------- */}
      <section className="mt-12 border-t pt-8">
        <h2 className="text-xl font-semibold">Notes</h2>
        <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-muted-foreground">
          <li>No authentication. All endpoints accept GET and respond with JSON.</li>
          <li>
            CORS is open to every origin; responses set{" "}
            <span className="font-mono text-xs">s-maxage=3600, stale-while-revalidate=86400</span>.
          </li>
          <li>
            Each icon set keeps its upstream license — review the source project before
            redistribution.
          </li>
        </ul>
      </section>
    </main>
  );
}
