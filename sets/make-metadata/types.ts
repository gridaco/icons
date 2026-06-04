export type IConStyleVariant = "solid" | "outlined" | "thin" | "twotone" | "sharp" | "round";

export interface IconMeta {
  uri: string;
  name: string;
  variants: Array<IConStyleVariant>;
  font?: string;
  codepoint?: number;
  size: number;
  package: string;
  version: number;
  category: string;
  tags: string[];
}
