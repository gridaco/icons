import type { IconMeta, IConStyleVariant } from "./types";

interface GoogleFontsIconMeta {
  name: string;
  version: number;
  popularity: number;
  codepoint: number;
  unsupported_families: Array<string>;
  categories: Array<string>;
  tags: Array<string>;
  sizes_px: Array<number>;
}

const uri = (name: string) => "https://icons.reflect-ui.com/material/" + name;

const default_mdi_variants = ["solid", "outlined", "twotone", "sharp", "round"] as const;

export default function map(meta: Array<GoogleFontsIconMeta>) {
  return meta.map((i) => {
    // remove each item from unsoported_families from default_mdi_variants
    const variants: IConStyleVariant[] = default_mdi_variants.filter(
      (v) => !i.unsupported_families.includes(v),
    );

    return <IconMeta>{
      uri: uri(i.name),
      name: i.name,
      variants: variants,
      size: i.sizes_px[0],
      package: "material",
      version: i.version,
      codepoint: i.codepoint,
      tags: i.tags,
      category: i.categories[0],
    };
  });
}
