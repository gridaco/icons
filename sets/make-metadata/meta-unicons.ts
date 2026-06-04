import type { IconMeta } from "./types";

const uri = (name: string) => "https://icons.reflect-ui.com/unicons/" + name;

const variant_map = {
  line: "outlined",
  thinline: "thin",
  solid: "solid",
  monochrome: "twotone",
} as const;

export default function map(meta: Array<any>) {
  return meta.map((i) => {
    return <IconMeta>{
      uri: uri(i.name),
      name: i.name,
      variants: i.styles.map((v) => variant_map[v]),
      size: 24,
      package: "unicons",
      version: 1,
      category: i.category,
      tags: i.tags,
    };
  });
}
