# Heroicons Specification

This directory contains the [Heroicons](https://github.com/tailwindlabs/heroicons) repository as a git submodule.

**License**: MIT License - See `vendor/heroicons/LICENSE` for details.

**Last Updated**: 2025-09-18

> **Note**: This submodule is maintained externally. Update this date when the submodule is updated to track changes in the upstream repository.

## Overview

Heroicons is a set of beautiful hand-crafted SVG icons designed by the makers of Tailwind CSS. Icons are available in multiple sizes (16×16, 20×20, 24×24) and styles (outline, solid). The icons are optimized for UI development and designed to work seamlessly with Tailwind CSS utility classes.

## Statistics

- **Total SVG Files**: 1,288 source files
- **Icon Sizes**: 16×16, 20×20, 24×24 pixels
- **Icon Styles**: Outline (24px only), Solid (all sizes)
- **24×24 Outline**: 324 icons
- **24×24 Solid**: 324 icons
- **20×20 Solid**: 324 icons
- **16×16 Solid**: 316 icons
- **Package Version**: 2.2.0

## File Structure

### Source Files

- **Location**: `src/<size>/<style>/` - Contains source SVG files
- **Sizes**: `16`, `20`, `24`
- **Styles**: `outline` (24px only), `solid` (all sizes)
- **Naming Convention**: Kebab-case (e.g., `academic-cap.svg`, `adjustments-horizontal.svg`)

### Optimized Files

- **Location**: `optimized/<size>/<style>/` - Contains SVGO-optimized SVG files
- **Optimization**: Uses SVGO with size-specific and style-specific configurations
- **Config Files**: `svgo.16.solid.mjs`, `svgo.20.solid.mjs`, `svgo.24.outline.mjs`, `svgo.24.solid.mjs`

### Distribution Files

- **Location**: `<size>/<style>/` - Final optimized files for distribution
- **Structure**: Mirrors source structure but contains optimized SVGs

### Framework Builds

- **React**: `react/` - React component builds
- **Vue**: `vue/` - Vue component builds

## Data Structure

### SVG File Format

#### Outline Style (24×24 only)

```xml
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="..." stroke="#0F172A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

**Characteristics:**

- Uses `stroke` instead of `fill`
- `fill="none"` to allow stroke rendering
- `stroke-width="1.5"` for consistent line weight
- `stroke-linecap="round"` and `stroke-linejoin="round"` for rounded corners
- Default stroke color: `#0F172A` (can be overridden with `stroke="currentColor"`)

#### Solid Style (all sizes)

```xml
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="..." fill="#0F172A"/>
</svg>
```

**Characteristics:**

- Uses `fill` instead of `stroke`
- `fill="none"` on root SVG element
- Individual paths use `fill="#0F172A"` (can be overridden with `fill="currentColor"`)
- No stroke attributes

### Size Variants

- **16×16**: Small icons for compact UIs (solid only)
- **20×20**: Medium icons for standard UIs (solid only)
- **24×24**: Large icons for prominent UIs (outline and solid)

### Style Variants

- **Outline**: Stroke-based icons with rounded line caps and joins (24px only)
- **Solid**: Fill-based icons with solid shapes (all sizes)

## Naming Conventions

### SVG Files

- **Format**: Kebab-case
- **Examples**: `academic-cap.svg`, `adjustments-horizontal.svg`, `archive-box-arrow-down.svg`
- **No Size/Style Suffix**: Filenames don't include size or style information (handled by directory structure)

### React Components

- **Format**: PascalCase with "Icon" suffix
- **Examples**: `AcademicCapIcon`, `AdjustmentsHorizontalIcon`
- **Import Path**: `@heroicons/react/<size>/<style>`
- **Example**: `import { BeakerIcon } from '@heroicons/react/24/solid'`

### Vue Components

- **Format**: PascalCase with "Icon" suffix
- **Examples**: `AcademicCapIcon`, `AdjustmentsHorizontalIcon`
- **Import Path**: `@heroicons/vue/<size>/<style>`
- **Example**: `import { BeakerIcon } from '@heroicons/vue/24/solid'`

## Directory Organization

### Source Structure

```
src/
├── 16/
│   └── solid/
│       └── *.svg (316 files)
├── 20/
│   └── solid/
│       └── *.svg (324 files)
└── 24/
    ├── outline/
    │   └── *.svg (324 files)
    └── solid/
        └── *.svg (324 files)
```

### Distribution Structure

```
16/
└── solid/
    └── *.svg (optimized)

20/
└── solid/
    └── *.svg (optimized)

24/
├── outline/
│   └── *.svg (optimized)
└── solid/
    └── *.svg (optimized)
```

## Build Process

The repository uses a build system that:

1. **Optimizes SVGs**: Uses SVGO with size and style-specific configurations
2. **Generates Framework Components**: Builds React and Vue component libraries
3. **Outputs Distribution Files**: Creates optimized SVG files in size/style directories

### Build Scripts

- `build-24-outline`: Builds 24×24 outline icons
- `build-24-solid`: Builds 24×24 solid icons
- `build-20-solid`: Builds 20×20 solid icons
- `build-16-solid`: Builds 16×16 solid icons
- `build-react`: Generates React component library
- `build-vue`: Generates Vue component library

## Styling

Icons are designed to be styled using CSS:

- **Color**: Set via `stroke="currentColor"` (outline) or `fill="currentColor"` (solid)
- **Size**: Controlled via `width` and `height` attributes or CSS
- **Tailwind CSS**: Works seamlessly with utility classes like `text-gray-500`, `size-6`

### Example Usage

```html
<!-- Outline icon with Tailwind classes -->
<svg
  class="size-6 text-gray-500"
  fill="none"
  viewBox="0 0 24 24"
  stroke="currentColor"
  stroke-width="1.5"
>
  <path stroke-linecap="round" stroke-linejoin="round" d="..." />
</svg>

<!-- Solid icon with Tailwind classes -->
<svg class="size-6 text-blue-500" fill="none" viewBox="0 0 24 24">
  <path fill="currentColor" d="..." />
</svg>
```

## Technical Specifications

- **License**: MIT License (Copyright © Tailwind Labs, Inc.)
- **ViewBox**: `0 0 24 24` (24px icons), `0 0 20 20` (20px icons), `0 0 16 16` (16px icons)
- **Color System**: Uses `currentColor` for CSS inheritance
- **Optimization**: SVGO with custom configurations per size/style
- **Build Tool**: Node.js with custom build scripts
- **Framework Support**: React and Vue via separate packages

## Related Files

- `scripts/build.js` - Build script for framework components
- `scripts/verify-names.js` - Icon name verification
- `scripts/deprecated.js` - Deprecated icon handling
- `svgo.*.mjs` - SVGO configuration files for optimization
- `react/` - React component library
- `vue/` - Vue component library
- `package.json` - Package configuration and build scripts

## References

- [Heroicons GitHub Repository](https://github.com/tailwindlabs/heroicons)
- [Heroicons Website](https://heroicons.com)
- [Heroicons React Package](https://www.npmjs.com/package/@heroicons/react)
- [Heroicons Vue Package](https://www.npmjs.com/package/@heroicons/vue)
