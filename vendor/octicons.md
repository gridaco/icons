# Octicons Specification

This directory contains the [Primer Octicons](https://github.com/primer/octicons) repository as a git submodule.

**License**: MIT License - See `vendor/octicons/LICENSE` for details.

**Last Updated**: 2025-12-10

> **Note**: This submodule is maintained externally. Update this date when the submodule is updated to track changes in the upstream repository.

## Overview

Octicons are a set of SVG icons built by GitHub for GitHub. They are designed to be simple, consistent, and optimized for use in GitHub's interface. The icon set includes icons for common actions, states, and concepts used throughout GitHub's products.

## Statistics

- **Total SVG Files**: 720 files
- **Unique Icons**: ~380 unique icon names
- **Icon Sizes**: 12, 16, 24, 32, 48, 96 pixels (majority are 16 and 24; some icons exist in other sizes)
- **Package Version**: 19.21.1

## File Structure

### SVG Icons

- **Location**: `icons/` - Contains all SVG icon files
- **Naming Convention**: `icon-name-<size>.svg` (e.g., `alert-16.svg`, `alert-24.svg`, `alert-32.svg`, `alert-48.svg`, `alert-96.svg`)
- **Size Variants**: 12, 16, 24, 32, 48, 96
- **Special Variants**: Some icons have `-inset` variants (e.g., `accessibility-inset-16.svg`, `accessibility-inset-24.svg`)

### Library Implementations

The repository contains multiple library implementations:

- **Node.js**: `lib/octicons_node/` - JavaScript API for Node.js
- **React**: `lib/octicons_react/` - React component library
- **Styled Octicons**: `lib/octicons_styled/` - React components with Styled System props
- **Ruby Gem**: `lib/octicons_gem/` - Ruby gem with Ruby API
- **Rails Helper**: `lib/octicons_helper/` - Rails helper for using octicons
- **Jekyll Plugin**: `lib/octicons_jekyll/` - Jekyll plugin for using octicons

### Build Data

- **Build Script**: `script/build.js` - Generates `lib/build/data.json` from SVG files
- **Keywords**: `keywords.json` - Searchable keywords for each icon

## Data Structure

### SVG File Format

#### 16×16 Icons

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <path d="..."/>
</svg>
```

#### 24×24 Icons

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
  <path d="..."/>
</svg>
```

**Characteristics:**

- Fixed dimensions: `width` and `height` attributes match viewBox
- Single or multiple `<path>` elements
- Uses `fill` attribute (typically `currentColor` or specific color)
- Optimized with SVGO

### Keywords Structure

The `keywords.json` file maps icon names to searchable keywords:

```json
{
  "alert": ["warning", "triangle", "exclamation", "point"],
  "archive": ["box", "catalog"],
  "arrow-down": ["point", "direction"],
  ...
}
```

Each icon name maps to an array of keywords that can be used for searching and filtering.

### Build Data Structure

The build process generates `lib/build/data.json` which contains:

- Icon metadata
- SVG paths
- Dimensions
- Keywords
- Other metadata for library consumption

## Naming Conventions

### SVG Files

- **Format**: `icon-name-<size>.svg`
- **Size Suffix**: `-16` or `-24`
- **Special Variants**: `-inset` suffix for inset variants
- **Examples**:
  - `alert-16.svg`, `alert-24.svg`
  - `accessibility-16.svg`, `accessibility-24.svg`, `accessibility-inset-16.svg`

### Icon Names

- **Format**: Kebab-case
- **Examples**: `alert`, `arrow-down`, `accessibility-inset`, `ai-model`

## Size Variants

### Size Variants

- **12×12**: Present for some icons
- **16×16**: Core set
- **24×24**: Core set
- **32×32, 48×48, 96×96**: Present for select icons
- **ViewBox**: Matches the width/height for each size
- **Note**: Not all icons are available in every size.

## Special Variants

### Inset Variants

Some icons have `-inset` variants that provide an inset/padded version:

- **Format**: `icon-name-inset-<size>.svg`
- **Examples**: `accessibility-inset-16.svg`, `accessibility-inset-24.svg`
- **Use Case**: Icons that need padding or spacing within a container

## Library APIs

### Node.js API

```javascript
const octicons = require("@primer/octicons");

// Get icon data
const alert = octicons["alert-16"];
console.log(alert.toSVG());
```

### React API

```jsx
import { AlertIcon } from "@primer/octicons-react";

function MyComponent() {
  return <AlertIcon size={16} />;
}
```

### Ruby API

```ruby
require 'octicons'

# Get icon SVG
Octicons::Octicon.new('alert-16').to_svg
```

## Build Process

The repository uses a build system that:

1. **Processes SVGs**: Optimizes SVG files using SVGO
2. **Generates Data**: Creates `lib/build/data.json` with icon metadata
3. **Builds Libraries**: Generates framework-specific libraries

### Build Scripts

- `build`: Generates build data from SVG files
- `svgo`: Optimizes SVG files using SVGO
- `version`: Updates version numbers across libraries

## Technical Specifications

- **License**: MIT License (Copyright © 2025 GitHub Inc.)
- **ViewBox**: `0 0 16 16` (16px icons), `0 0 24 24` (24px icons)
- **Optimization**: SVGO with custom configuration
- **Build Tool**: Node.js with custom build scripts
- **Package Manager**: Yarn
- **Framework Support**: Node.js, React, Ruby (Rails, Jekyll)

## Icon Categories

Icons are organized by function rather than explicit categories. Common groupings include:

- **Actions**: check, x, plus, minus, arrow-_, chevron-_
- **Status**: alert, check-circle, x-circle, issue-\*
- **Navigation**: arrow-_, chevron-_, triangle-\*
- **Content**: file-_, folder-_, book, markdown
- **Communication**: comment, mail, bell, broadcast
- **Development**: code, git-\*, branch, commit
- **UI Elements**: checkbox, radio, button, input
- **GitHub-specific**: github, repo, pull-request, issue

## Related Files

- `script/build.js` - Build script for generating data.json
- `script/version` - Version management script
- `keywords.json` - Icon keywords for search
- `svgo.config.js` - SVGO optimization configuration
- `lib/octicons_node/` - Node.js library
- `lib/octicons_react/` - React library
- `lib/octicons_gem/` - Ruby gem
- `package.json` - Package configuration

## References

- [Octicons GitHub Repository](https://github.com/primer/octicons)
- [Octicons Website](https://primer.style/octicons)
- [Node.js Package](https://www.npmjs.com/package/@primer/octicons)
- [React Package](https://www.npmjs.com/package/@primer/octicons-react)
- [Ruby Gem](https://rubygems.org/gems/octicons)
