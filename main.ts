import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Copy pattern only: the image is pre-rendered in the repo and copied
// byte-for-byte to the output directory. No subprocess, no network.
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dst = join(outDir, "entry.png");

if (!existsSync(src)) {
  throw new Error("entry.png is missing from the repository");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
// Guard: the copy must be whole, or the run is not deterministic.
if (statSync(src).size !== statSync(dst).size) {
  throw new Error("entry.png copy is incomplete");
}
