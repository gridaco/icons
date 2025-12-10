# Lucide Icons Specification

This directory contains the [Lucide Icons](https://github.com/lucide-icons/lucide) repository as a git submodule.

**License**: ISC License - See `vendor/lucide-icons/LICENSE` for details. (Portions derived from Feather Icons are MIT licensed.)

**Last Updated**: 2025-12-10

> **Note**: This submodule is maintained externally. Update this date when the submodule is updated to track changes in the upstream repository.

## Overview

Lucide is an open-source icon library that provides 1000+ vector (SVG) files for displaying icons and symbols in digital and non-digital projects. It is a fork of Feather Icons, designed to be beautiful, consistent, and community-driven. The library provides official packages for multiple frameworks and platforms.

## Statistics

- **Total Icons**: 1,655 SVG files
- **Metadata Files**: 1,655 JSON files (one per icon)
- **Categories**: 43 categories
- **Icon Size**: 24×24 pixels (fixed size)
- **Format**: Stroke-based SVG design

## File Structure

### SVG Icons

- **Location**: `icons/` - Contains all 1,655 SVG icon files
- **Naming Convention**: Kebab-case (e.g., `activity.svg`, `a-arrow-down.svg`, `accessibility.svg`)
- **Metadata**: Each icon has a corresponding JSON file (e.g., `activity.json`)

### Icon Metadata

- **Location**: `icons/*.json` - JSON metadata files for each icon
- **Schema**: Defined in `icon.schema.json`
- **Contents**: Tags, categories, contributors, aliases, deprecation info

### Categories

- **Location**: `categories/` - Contains 43 category definition files
- **Format**: JSON files with title and icon reference
- **Schema**: Defined in `category.schema.json`

### Framework Packages

The repository contains multiple framework-specific packages:

- **Core**: `packages/lucide/` - Base JavaScript package
- **React**: `packages/lucide-react/` - React components
- **Vue**: `packages/lucide-vue-next/` - Vue 3 components
- **Svelte**: `packages/lucide-svelte/` - Svelte components
- **Solid**: `packages/lucide-solid/` - SolidJS components
- **Preact**: `packages/lucide-preact/` - Preact components
- **Angular**: `packages/lucide-angular/` - Angular components
- **React Native**: `packages/lucide-react-native/` - React Native components
- **Astro**: `packages/astro/` - Astro components
- **Static**: `packages/lucide-static/` - Static SVG exports

## Data Structure

### SVG File Format

All SVG files follow this structure:

```xml
<svg
  xmlns="http://www.w3.org/2000/svg"
  width="24"
  height="24"
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="..." />
</svg>
```

**Characteristics:**
- Fixed dimensions: 24×24 pixels
- ViewBox: `0 0 24 24`
- Uses `stroke` instead of `fill` (stroke-based design)
- `fill="none"` to allow stroke rendering
- `stroke="currentColor"` for CSS color inheritance
- `stroke-width="2"` for consistent line weight
- `stroke-linecap="round"` and `stroke-linejoin="round"` for rounded corners
- Single or multiple `<path>` elements

### Icon Metadata Structure

Each icon has a corresponding JSON file with metadata:

```json
{
  "$schema": "../icon.schema.json",
  "contributors": ["username1", "username2"],
  "tags": ["tag1", "tag2", "tag3"],
  "categories": ["category1", "category2"],
  "aliases": [
    {
      "name": "alias-name",
      "deprecated": true,
      "deprecationReason": "alias.typo",
      "toBeRemovedInVersion": "v1.0.0"
    }
  ],
  "deprecated": true,
  "deprecationReason": "icon.brand",
  "toBeRemovedInVersion": "v1.0.0"
}
```

**Fields:**
- `$schema`: Reference to icon schema
- `contributors`: Array of GitHub usernames who contributed
- `tags`: Array of searchable tags
- `categories`: Array of category names (must match category files)
- `aliases`: Optional array of alternative names (may be deprecated)
- `deprecated`: Optional flag for deprecated icons
- `deprecationReason`: Reason for deprecation (if deprecated)
- `toBeRemovedInVersion`: Version when icon will be removed (if deprecated)

### Category Structure

Category files define icon categories:

```json
{
  "$schema": "../category.schema.json",
  "title": "Category Display Name",
  "icon": "icon-name"
}
```

## Categories

All 43 categories are defined in `categories/` directory:

- `accessibility`, `account`, `animals`, `arrows`, `brands`, `buildings`, `charts`, `communication`, `connectivity`, `cursors`, `design`, `development`, `devices`, `emoji`, `files`, `finance`, `food-beverage`, `gaming`, `home`, `layout`, `mail`, `math`, `medical`, `multimedia`, `nature`, `navigation`, `notifications`, `people`, `photography`, `science`, `seasons`, `security`, `shapes`, `shopping`, `social`, `sports`, `sustainability`, `text`, `time`, `tools`, `transportation`, `travel`, `weather`

## Naming Conventions

### SVG Files

- **Format**: Kebab-case
- **Examples**: `activity.svg`, `a-arrow-down.svg`, `accessibility.svg`
- **No Size/Style Suffix**: All icons are 24×24, no size variants

### Icon Names

- **Format**: Kebab-case
- **Examples**: `activity`, `a-arrow-down`, `accessibility`
- **Aliases**: Icons may have alternative names defined in metadata

## Design Principles

Lucide icons follow these design principles (inherited from Feather):

- **Stroke-based**: Uses strokes instead of fills
- **Consistent Weight**: 2px stroke width
- **Rounded Corners**: Round line caps and joins
- **24×24 Grid**: All icons fit within 24×24 viewBox
- **Minimal**: Simple, clean designs
- **Consistent**: Uniform style across all icons

## Technical Specifications

- **License**: ISC License (portions from Feather Icons are MIT licensed)
- **Icon Dimensions**: 24×24 pixels (fixed)
- **ViewBox**: `0 0 24 24` (all icons)
- **Color System**: Uses `currentColor` for CSS inheritance
- **Stroke Width**: 2px (consistent across all icons)
- **Line Caps**: Round (`stroke-linecap="round"`)
- **Line Joins**: Round (`stroke-linejoin="round"`)
- **Package Manager**: pnpm
- **Build System**: Custom build tools with TypeScript
- **Node Version**: Requires Node.js >= 23.0.0

## Brand Logo Policy

Lucide **does not accept** brand logos and does not plan to add them in the future. This is documented in `BRAND_LOGOS_STATEMENT.md` and is due to legal restrictions, design consistency concerns, and practical maintenance reasons.

## Build Process

The repository uses a monorepo structure with pnpm workspaces:

1. **Icon Processing**: Icons are optimized and validated
2. **Metadata Validation**: JSON files are validated against schemas
3. **Package Building**: Framework-specific packages are built from source
4. **Type Generation**: TypeScript types are generated for all packages

### Build Scripts

- `build`: Builds all packages
- `optimize`: Optimizes SVG files
- `checkIcons`: Validates icons and categories
- `lint:json`: Validates JSON schemas

## Related Files

- `icon.schema.json` - JSON schema for icon metadata
- `category.schema.json` - JSON schema for category definitions
- `scripts/` - Build and maintenance scripts
- `tools/build-icons/` - Icon building tools
- `packages/shared/` - Shared utilities for packages
- `BRAND_LOGOS_STATEMENT.md` - Official statement on brand logos

## References

- [Lucide Icons GitHub Repository](https://github.com/lucide-icons/lucide)
- [Lucide Icons Website](https://lucide.dev)
- [Lucide Icons Guide](https://lucide.dev/guide/)
- [Lucide Packages](https://lucide.dev/packages)
- [Figma Plugin](https://www.figma.com/community/plugin/939567362549682242/Lucide-Icons)

