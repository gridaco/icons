import type { IconMeta } from "./types";

const variants_legacy_back_map = {
  default: "solid",
  outlined: "outlined",
  twotone: "twotone",
};

export default function maplegacyjson(obj: object) {
  const result = {};
  Object.values(obj).forEach((i) => {
    const { variant, family } = i;

    if (result[family]) {
      result[family].variants.push(variant);
    } else {
      result[family] = <IconMeta>{
        name: family,
        variants: [variants_legacy_back_map[variant]],
        size: 24,
        package: "ant-design",
        version: 1,
        category: null,
        tags: [],
      };
    }
  });

  return Object.values(result);
}
