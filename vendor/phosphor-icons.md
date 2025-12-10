# Phosphor Icons Specification

This directory contains the [Phosphor Icons Core](https://github.com/phosphor-icons/core) repository as a git submodule.

**License**: MIT License - See `vendor/phosphor-icons/LICENSE` for details.

**Last Updated**: 2025-05-21

> **Note**: This submodule is maintained externally. Update this date when the submodule is updated to track changes in the upstream repository.

## Overview

Phosphor Icons is a flexible icon family for interfaces, systems, and products. The core repository contains raw SVG assets and catalog data including tags, categories, and release versions. Icons are available in six weights (regular, thin, light, bold, fill, duotone) with consistent design language across all variants.

## Statistics

- **Total Unique Icons**: 1,512 icons
- **Total SVG Files**: 18,144 files (1,512 icons × 6 weights × 2 directories)
- **Icon Weights**: 6 variants (regular, thin, light, bold, fill, duotone)
- **ViewBox**: 256×256 pixels (all icons)
- **Package Version**: 2.1.1

## File Structure

### SVG Assets

- **Location**: `assets/<weight>/` - Contains optimized SVG files
- **Alternative Location**: `raw/<weight>/` - Contains raw source SVG files
- **Weights**: `bold`, `duotone`, `fill`, `light`, `regular`, `thin`
- **Naming Convention**: Kebab-case with weight suffix (e.g., `acorn-regular.svg`, `address-book-bold.svg`)
- **Note**: Files in `assets/` directory omit the weight suffix (e.g., `acorn.svg`)

### Catalog Data

- **Location**: `src/icons.ts` - Main catalog file (20,593 lines)
- **Type Definitions**: `src/types.ts` - TypeScript interfaces and enums
- **Index**: `src/index.ts` - Exports catalog and types

## Data Structure

### IconEntry Interface

```typescript
export interface IconEntry {
  name: string;                    // Kebab-case name (e.g., "cloud-lightning")
  pascal_name: string;             // PascalCase name (e.g., "CloudLightning")
  alias?: {                        // Optional deprecated name for backwards compatibility
    name: string;
    pascal_name: string;
  };
  codepoint: number;               // Unicode code point for font implementations
  categories: readonly IconCategory[]; // Array of categories
  figma_category: FigmaCategory;   // Figma-specific category
  tags: readonly string[];         // Searchable tags (e.g., ["*new*", "meteorology", "cloudy"])
  published_in: number;            // Version when icon was first published
  updated_in: number;              // Version when icon was last updated
}
```

### Icon Weights (IconStyle Enum)

```typescript
export enum IconStyle {
  REGULAR = "regular",   // Default weight
  THIN = "thin",         // Thinnest stroke
  LIGHT = "light",       // Light stroke
  BOLD = "bold",         // Bold stroke
  FILL = "fill",         // Filled variant
  DUOTONE = "duotone",   // Two-tone variant (uses 2 codepoints)
}
```

### Icon Categories (IconCategory Enum)

```typescript
export enum IconCategory {
  ARROWS = "arrows",
  BRAND = "brands",
  COMMERCE = "commerce",
  COMMUNICATION = "communications",
  DESIGN = "design",
  DEVELOPMENT = "technology & development",
  EDITOR = "editor",
  FINANCE = "finances",
  GAMES = "games",
  HEALTH = "health & wellness",
  MAP = "maps & travel",
  MEDIA = "media",
  NATURE = "nature",
  OBJECTS = "objects",
  OFFICE = "office",
  PEOPLE = "people",
  SYSTEM = "system",
  WEATHER = "weather",
}
```

### Figma Categories (FigmaCategory Enum)

Separate category system for Figma plugin organization:

```typescript
export enum FigmaCategory {
  ARROWS = "arrows",
  BRAND = "brands",
  COMMERCE = "commerce",
  COMMUNICATION = "communication",
  DESIGN = "design",
  DEVELOPMENT = "technology & development",
  EDUCATION = "education",
  FINANCE = "math & finance",
  GAMES = "games",
  HEALTH = "health & wellness",
  MAP = "maps & travel",
  MEDIA = "media",
  OFFICE = "office & editing",
  PEOPLE = "people",
  SECURITY = "security & warnings",
  SYSTEM = "system & devices",
  TIME = "time",
  WEATHER = "weather & nature",
}
```

## SVG File Format

### Standard Format

All SVG files follow this structure:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor">
  <path d="..." />
</svg>
```

**Characteristics:**
- Fixed viewBox: `0 0 256 256`
- Uses `currentColor` for fill (allows CSS color inheritance)
- Single or multiple `<path>` elements
- No stroke, only fill

### Duotone Format

Duotone icons use two layers (background and foreground):

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor">
  <path d="..." opacity="0.2"/>  <!-- Background layer -->
  <path d="..."/>                 <!-- Foreground layer -->
</svg>
```

**Note**: Duotone icons use 2 codepoints (`codepoint` and `codepoint + 1`). All codepoint bases are even numbers.

## Naming Conventions

### SVG Files

- **Assets Directory**: Kebab-case without weight suffix (e.g., `acorn.svg`, `address-book.svg`)
- **Raw Directory**: Kebab-case with weight suffix (e.g., `acorn-regular.svg`, `address-book-bold.svg`)
- **Weight Suffixes**: `-regular`, `-thin`, `-light`, `-bold`, `-fill`, `-duotone`

### Icon Names

- **Kebab-case**: Used in `name` field (e.g., `"cloud-lightning"`)
- **PascalCase**: Used in `pascal_name` field (e.g., `"CloudLightning"`)

## Catalog Access

### TypeScript Types

```typescript
import { icons, PhosphorIcon, IconEntry } from "@phosphor-icons/core";

// Extract valid icon names
type IconName = PhosphorIcon["name"];
// Result: "function" | "address-book" | "air-traffic-control" | ...

// Access icon catalog
const iconEntry: IconEntry = icons.find(icon => icon.name === "cloud-lightning");
```

### SVG Import

```typescript
// Direct import (assets directory)
import acornRegular from "@phosphor-icons/core/regular/acorn.svg";

// With assets prefix
import acornRegular from "@phosphor-icons/core/assets/regular/acorn.svg";

// Using import maps (assets prefix can be omitted)
import acornRegular from "@phosphor-icons/core/regular/acorn.svg";
```

## Technical Specifications

- **License**: MIT License (Copyright © 2023 Phosphor Icons)
- **Icon Dimensions**: 256×256 pixels (viewBox)
- **ViewBox**: `0 0 256 256` (all icons)
- **Color System**: Uses `currentColor` for CSS inheritance
- **Codepoints**: Stable decimal Unicode code points for font implementations
- **Version Tracking**: Icons track `published_in` and `updated_in` versions
- **Package Manager**: pnpm
- **Build System**: Vite + TypeScript

## Directory Organization

### Assets vs Raw

- **`assets/`**: Optimized, production-ready SVG files (no weight suffix in filename)
- **`raw/`**: Raw source SVG files (with weight suffix in filename)

### Weight Directories

Each weight has its own directory:
- `assets/bold/` - Bold stroke weight
- `assets/duotone/` - Two-tone variant
- `assets/fill/` - Filled variant
- `assets/light/` - Light stroke weight
- `assets/regular/` - Default/regular stroke weight
- `assets/thin/` - Thin stroke weight

## Related Files

- `src/icons.ts` - Main icon catalog array
- `src/types.ts` - TypeScript type definitions
- `src/index.ts` - Package exports
- `scripts/collate.ts` - Icon collation script
- `scripts/catalog.ts` - Catalog generation script
- `scripts/verify.ts` - Icon verification script
- `package.json` - Package configuration and exports

## References

- [Phosphor Icons GitHub Repository](https://github.com/phosphor-icons/core)
- [Phosphor Icons Website](https://phosphoricons.com)
- [NPM Package](https://www.npmjs.com/package/@phosphor-icons/core)

