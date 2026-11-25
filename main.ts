// The Tuesday World — front page summing up Tuesday 24 November 2026.
// Entry point for the make.fun program/v1 entry: it copies the pre-rendered
// front page (entry.png, drawn at build time by draw.py) into the output
// directory. Node 22, standard library only, no network, no randomness.
import { copyFile, mkdir, readdir, readFile, rm, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const SOURCE_NAME = "entry.png";

const repoRoot = path.dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? path.join(repoRoot, "out");

// Remove every entry inside `dir` while leaving `dir` itself in place.
// The grader mounts the output directory, so deleting it is forbidden.
async function clearContents(dir: string): Promise<void> {
  let names: string[];
  try {
    names = await readdir(dir);
  } catch (err: unknown) {
    if ((err as NodeJS.ErrnoException)?.code === "ENOENT") return;
    throw err;
  }
  for (const name of names) {
    await rm(path.join(dir, name), { recursive: true, force: true });
  }
}

async function main(): Promise<void> {
  const source = path.join(repoRoot, SOURCE_NAME);
  const bytes = await readFile(source);
  if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
    throw new Error(`${SOURCE_NAME} is not a PNG file`);
  }
  await mkdir(outDir, { recursive: true });
  await clearContents(outDir);
  const target = path.join(outDir, SOURCE_NAME);
  await copyFile(source, target);
  const copied = await stat(target);
  if (copied.size !== bytes.length) {
    throw new Error(`copied ${copied.size} bytes, expected ${bytes.length}`);
  }
  console.log(`wrote ${target} (${copied.size} bytes)`);
}

main().catch((err: unknown) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
