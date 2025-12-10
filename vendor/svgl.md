# SVGL Specification

This directory contains the [SVGL](https://github.com/pheralb/svgl) repository as a git submodule.

**License**: MIT License - See `vendor/svgl/LICENSE` for details.

**Last Updated**: 2025-12-10

> **Note**: This submodule is maintained externally. Update this date when the submodule is updated to track changes in the upstream repository.

## Overview

SVGL is a library of optimized SVG logos for brands and companies. It provides a structured data format for logo metadata and an API endpoint for accessing logos programmatically.

## Statistics

- **Total Logos**: ~550+ entries in `svgs.ts` (4,337 lines)
- **SVG Files**: 919 SVG files in `static/library/`
- **Categories**: 38 different categories
- **API Rate Limit**: 5 requests per 5 seconds (sliding window)

## File Structure

### Data Source

- **Logo Metadata**: `src/data/svgs.ts` - Main data file with all logo entries
- **Data Export**: `src/data/index.ts` - Exports `svgsData` with auto-generated IDs
- **Types**: `src/types/svg.ts` - TypeScript interfaces

### SVG Files

- **Location**: `static/library/` - Contains all 919 SVG logo files
- **Naming Patterns**:
  - Simple: `react.svg`
  - Light/Dark variants: `react-light.svg`, `react-dark.svg`
  - Wordmarks: `react-wordmark.svg`, `react-wordmark-light.svg`
  - Special formats: `github_light.svg`, `github_dark.svg`
- **Filename inference (theme/kind)**:
  - Tokens are split on `.`, `-`, `_`
  - `light` → theme: light
  - `dark` → theme: dark
  - `wordmark` → kind: wordmark
  - Otherwise, kind defaults to symbol

### API Implementation

- **API Routes**: `api-routes/src/index.ts` - Hono-based API server
- **Utils**: `api-routes/src/utils.ts` - URL transformation utilities

## Data Structure

### Type Definition

Location: `src/types/svg.ts`

```typescript
export interface iSVG {
  id?: number; // Auto-generated index
  title: string; // Logo name (e.g., "React")
  category: Category | Category[]; // Single or multiple categories
  route: string | ThemeOptions; // Path to SVG file(s)
  wordmark?: string | ThemeOptions; // Optional wordmark variant
  brandUrl?: string; // Link to brand guidelines
  shadcnCommand?: string; // Optional shadcn CLI command
  url: string; // Company/product website
}

export type ThemeOptions = {
  dark: string; // Path to dark mode SVG
  light: string; // Path to light mode SVG
};
```

### Data Examples

**Simple Logo (single file):**

```typescript
{
  title: "React",
  category: "Library",
  route: "/library/react.svg",
  url: "https://react.dev/"
}
```

**Logo with Light/Dark Variants:**

```typescript
{
  title: "React",
  category: "Library",
  route: {
    light: "/library/react_light.svg",
    dark: "/library/react_dark.svg"
  },
  url: "https://react.dev/"
}
```

**Logo with Wordmark:**

```typescript
{
  title: "PayPal",
  category: "Payment",
  route: "/library/paypal.svg",
  wordmark: "/library/paypal-wordmark.svg",
  url: "https://paypal.com"
}
```

**Full Example (all properties):**

```typescript
{
  title: "NVIDIA",
  category: ["AI", "Hardware", "Platform"],
  route: {
    light: "/library/nvidia-icon-light.svg",
    dark: "/library/nvidia-icon-dark.svg"
  },
  wordmark: {
    light: "/library/nvidia-wordmark-light.svg",
    dark: "/library/nvidia-wordmark-dark.svg"
  },
  url: "https://www.nvidia.com",
  brandUrl: "https://www.nvidia.com/en-us/about-nvidia/legal-info/logo-brand-usage"
}
```

## Categories

All categories are defined in `src/types/categories.ts`:

```typescript
"AI" |
  "Software" |
  "Hardware" |
  "Library" |
  "Hosting" |
  "Framework" |
  "Devtool" |
  "Monorepo" |
  "CMS" |
  "Database" |
  "Compiler" |
  "Crypto" |
  "Cybersecurity" |
  "Social" |
  "Entertainment" |
  "Browser" |
  "Language" |
  "Education" |
  "Design" |
  "Community" |
  "Marketplace" |
  "Music" |
  "Vercel" |
  "Google" |
  "Payment" |
  "VoidZero" |
  "Authentication" |
  "IoT" |
  "Config" |
  "Secrets" |
  "IaC" |
  "Analytics" |
  "Sync Engine" |
  "Platform" |
  "Automation" |
  "Nuxt" |
  "Microsoft";
```

## Path Resolution

The API uses `addFullUrl()` utility function to convert relative paths to full URLs:

- Input: `"/library/react.svg"`
- Output: `"https://svgl.app/library/react.svg"`

## API Endpoints

SVGL provides the following API endpoints:

### GET /

Returns all logos.

**Query Parameters:**

- `limit`: Number of results (integer)
- `search`: Filter by title (case-insensitive string)

**Response:** Array of `iSVG` objects with full URLs

### GET /categories

Returns category list with counts.

**Response:** `[{ category: string, total: number }]`

### GET /category/:category

Returns logos in a specific category.

**Parameters:**

- `category`: Category name (case-insensitive, capitalized automatically)

**Response:** Array of `iSVG` objects

### GET /svg/:filename

Returns SVG file content.

**Parameters:**

- `filename`: SVG filename

**Query Parameters:**

- `no-optimize`: Return unoptimized SVG (boolean)

**Response:** SVG XML content (optimized by default)

## Technical Specifications

- **License**: MIT License
- **SVG Optimization**: Uses `optimizeSvg()` utility (located in `src/utils/optimizeSvg.ts`)
- **Size Limit**: Each SVG is limited to 21kb (as per SVGL guidelines)
- **ViewBox Requirement**: All SVGs must have a `viewBox` attribute (not removed during optimization)
- **Rate Limiting**: Public API uses Upstash Redis with sliding window algorithm (5 requests per 5 seconds)
- **CORS**: API has CORS enabled (`access-control-allow-origin: *`)

## Related Files

- `src/utils/optimizeSvg.ts` - SVG optimization logic
- `src/utils/parseSvgFilename.ts` - Filename parsing utilities
- `api-routes/wrangler.toml` - Cloudflare Workers configuration
- `package.json` - Dependencies (Hono, Upstash, etc.)

## References

- [SVGL GitHub Repository](https://github.com/pheralb/svgl)
- [SVGL Website](https://svgl.app)
- [SVGL API Documentation](https://svgl.app/docs/api)
