# Radix UI Icons Specification

This directory contains the [Radix UI Icons](https://github.com/radix-ui/icons) repository as a git submodule.

**License**: MIT License - See `vendor/radix-ui-icons/LICENSE` for details.

**Last Updated**: 2025-09-12

> **Note**: This submodule is maintained externally. Update this date when the submodule is updated to track changes in the upstream repository.

## Overview

Radix UI Icons is a crisp set of 15×15 icons designed by the WorkOS team. All icons are available as individual SVG files and React components. The icon set focuses on UI/UX icons for design tools and applications.

## Statistics

- **Total Icons**: 332 SVG files
- **Icon Size**: 15×15 pixels (fixed size)
- **Format**: SVG with React component wrappers
- **Package Version**: 1.3.2
- **React Support**: React 16.x, 17.x, 18.x, 19.x

## File Structure

### SVG Files

- **Location**: `packages/radix-icons/icons/` - Contains all 332 SVG icon files
- **Naming Convention**: Kebab-case (e.g., `accessibility.svg`, `arrow-left.svg`, `check-circled.svg`)
- **ViewBox**: All icons use `viewBox="0 0 15 15"`
- **Dimensions**: Fixed `width="15" height="15"`

### React Components

- **Location**: `packages/radix-icons/src/` - Contains 332 React component files
- **Naming Convention**: PascalCase with "Icon" suffix (e.g., `AccessibilityIcon.tsx`, `ArrowLeftIcon.tsx`)
- **Export Pattern**: Each component is exported as both named and default export
- **Index File**: `packages/radix-icons/src/index.tsx` - Exports all icons

### Manifest

- **Location**: `packages/radix-icons/manifest.json`
- **Structure**: JSON object with icon paths organized by size (currently only `:15`)
- **Format**: Maps icon names to file paths (e.g., `"accessibility": "icons/15/accessibility.svg"`)

## Data Structure

### SVG File Format

All SVG files follow this structure:

```xml
<svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="..." fill="currentColor"/>
</svg>
```

**Characteristics:**
- Fixed dimensions: 15×15
- Uses `currentColor` for fill (allows CSS color inheritance)
- Single `<path>` element per icon (optimized)
- No stroke, only fill

### React Component Format

Each icon is wrapped in a React component:

```typescript
import * as React from "react";
import type { IconProps } from "./types.js";

export const IconName = React.forwardRef<SVGSVGElement, IconProps>(
  function IconName({ color = "currentColor", ...props }, forwardedRef) {
    return (
      <svg
        width="15"
        height="15"
        viewBox="0 0 15 15"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        {...props}
        ref={forwardedRef}
      >
        <path d="..." fill={color} />
      </svg>
    );
  },
);

export default IconName;
```

**Component Props:**
- `color`: String (default: `"currentColor"`) - Controls the fill color
- `...props`: Spreads all other SVG attributes
- `forwardedRef`: React ref forwarding for direct SVG element access

### Manifest Structure

The `manifest.json` file structure:

```json
{
  "icons": {
    ":15": {
      "icon-name": "icons/15/icon-name.svg",
      ...
    }
  }
}
```

The `:15` key represents the 15×15 size variant (currently the only size available).

## Icon Categories

Icons are organized by function rather than explicit categories. Common groupings include:

- **Navigation**: arrows, chevrons, carets, triangles
- **Actions**: check, cross, plus, minus, dots
- **UI Elements**: buttons, inputs, switches, checkboxes
- **Layout**: panels, borders, corners, alignment
- **Typography**: font styles, text alignment, letter case
- **Media**: play, pause, speaker, video, image
- **Files**: file, folder, archive, document
- **Design Tools**: layers, opacity, shadows, transforms
- **Logos**: GitHub, Twitter, Vercel, Figma, etc.

## Naming Conventions

### SVG Files

- Kebab-case format
- Descriptive names (e.g., `arrow-left.svg`, `check-circled.svg`)
- Variants use suffixes (e.g., `lock-open-1.svg`, `lock-open-2.svg`)
- Filled variants use `-filled` suffix (e.g., `star-filled.svg`)

### React Components

- PascalCase with "Icon" suffix
- Matches SVG filename (e.g., `arrow-left.svg` → `ArrowLeftIcon.tsx`)
- Exported as both named and default export

## Technical Specifications

- **License**: MIT License (Copyright © 2022-present WorkOS)
- **Icon Dimensions**: 15×15 pixels (fixed)
- **ViewBox**: `0 0 15 15` (all icons)
- **Color System**: Uses `currentColor` for CSS inheritance
- **Optimization**: Single path element per icon
- **React Support**: React 16.x through 19.x
- **TypeScript**: Full TypeScript support with type definitions
- **Build System**: Uses pnpm workspace with TypeScript compilation

## Package Structure

The repository uses a monorepo structure:

- **Root**: Contains workspace configuration and shared tooling
- **packages/radix-icons/**: Main icon package
  - `icons/`: SVG source files
  - `src/`: React component source files
  - `manifest.json`: Icon manifest
  - `package.json`: Package configuration
- **packages/generate-icon-lib/**: Icon generation tooling

## Related Files

- `packages/radix-icons/src/types.ts` - TypeScript type definitions for IconProps
- `packages/radix-icons/src/index.tsx` - Main export file for all icons
- `packages/generate-icon-lib/` - Tooling for generating React components from SVGs
- `package.json` - Workspace and dependency configuration
- `pnpm-workspace.yaml` - pnpm workspace configuration

## References

- [Radix UI Icons GitHub Repository](https://github.com/radix-ui/icons)
- [Radix UI Icons Website](https://icons.radix-ui.com)
- [Radix UI Documentation](https://www.radix-ui.com/icons)

