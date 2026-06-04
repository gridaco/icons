import { IconMeta } from "./types";
import fs from "fs";
import path from "path";
import map_unicons from "./meta-unicons";
import map_mdi from "./meta-mdi";
import map_radix from "./meta-radix";
import map_antd_legacy from "./meta-antd";

const mapped_unicons = map_unicons(require("../raw/unicons/json/meta.json"));
const mapped_mdi = map_mdi(require("../raw/mdi/icons.json").icons);
const mapped_radix = map_radix(require("../metadata/radix.names.json"));
const mapped_antd = map_antd_legacy(require("../metadata/antd.config.json"));

const all = [...mapped_antd, ...mapped_unicons, ...mapped_mdi, ...mapped_radix] as IconMeta[];

// save file as json
fs.writeFileSync(path.join(__dirname, "./out.json"), JSON.stringify(all, null, 2));

console.log("done");
console.log("total icon names:", all.length);
console.log(
  "total icons:",
  all.reduce((a, b) => a + b.variants.length, 0),
);
