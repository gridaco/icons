import fs from "fs-extra";
import path from "path";
import { __DIST, __RAW } from "../settings";
import glob from "glob";
import decompress from "decompress";

// const REPOSITORY_ZIP_URL =
//   "https://codeload.github.com/google/material-design-icons/zip/master";

// repository's directory structure
// - /src
//  - /[category]
//    - /[icon]
//      - /materialicons
//        - 20px.svg
//        - 24px.svg
//      - /materialiconsoutlined
//      - /materialiconsrond
//      - /materialiconssharp
//      - /materialiconstwotone

// How to process
// unarchive the repository zip file
// move the /src/ under raw/mdi
// iterate each [category]/[icon] directory, extract the biggest svg file.
// move the svg file to target dir with name [icon].svg

const TARGET_DIR = path.join(__DIST, "tmp/mdi");

// unarchive
const ARCHIVEFILE = path.join(__RAW, "mdi/archives/src.zip");
const UNARCHIVEDIR = path.join(__RAW, "mdi/archives/tmp");

decompress(ARCHIVEFILE, UNARCHIVEDIR);

const SRCDIR = path.join(__RAW, "mdi/archives/tmp/src");

// iterate each [category]/[icon] directory, extract the biggest svg file.
// move the svg file to target dir with name [icon].svg
// use glob to iterate all files
const files = glob.sync("**/*.svg", {
  cwd: SRCDIR,
});

const icons = {};
files.map((f) => {
  const _ps = f.split("/");
  const category = _ps[0];
  const icon = _ps[1];
  const variant = _ps[2];
  const filename = _ps[3];
  const size = parseInt(filename.replace("px.svg", ""));

  if (!icons[icon]) {
    icons[icon] = {
      name: icon,
      category,
      variants: new Set([variant]),
      sizes: new Set([size]),
    };
  } else {
    icons[icon].sizes.add(size);
    icons[icon].variants.add(variant);
  }
});

const VARIANT_NAME_MAP = {
  materialicons: "filled",
  materialiconsoutlined: "outlined",
  materialiconsround: "round",
  materialiconssharp: "sharp",
  materialiconstwotone: "twotone",
} as const;

// iterate icons, copy the file with new name under target dir
Object.keys(icons).map((key) => {
  const icon = icons[key];
  const defaultsize = Math.min(
    // limit to 24
    24,
    // biggest size as defualt
    Math.max(...(Array.from(icon.sizes) as number[])),
  );
  const { name, variants, category } = icon;

  for (const variant of Array.from(variants) as string[]) {
    // src file
    const srcfile = path.join(SRCDIR, category, name, variant, `${defaultsize}px.svg`);

    // target file
    const vname = VARIANT_NAME_MAP[variant];
    const targetfilename = vname === "filled" ? `${name}.svg` : `${name}_${vname}.svg`;
    const targetfile = path.join(TARGET_DIR, targetfilename);

    // copy
    fs.copy(srcfile, targetfile).then(() => {
      console.log(`- ${name}`, targetfilename);
    });
  }
});
