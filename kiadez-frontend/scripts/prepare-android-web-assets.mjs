import { existsSync, readdirSync, rmSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");

const distDir = path.join(rootDir, "dist");
const androidPublicDir = path.join(rootDir, "android", "app", "src", "main", "assets", "public");

function removeHostedBinaryArtifacts(dirPath) {
  if (!existsSync(dirPath)) {
    return [];
  }

  const removed = [];

  for (const entry of readdirSync(dirPath)) {
    const entryPath = path.join(dirPath, entry);
    const stat = statSync(entryPath);

    if (stat.isDirectory()) {
      if (entry === "app") {
        rmSync(entryPath, { recursive: true, force: true });
        removed.push(entryPath);
        continue;
      }

      removed.push(...removeHostedBinaryArtifacts(entryPath));
      continue;
    }

    if (entry.endsWith(".apk") || entry.endsWith(".aab")) {
      rmSync(entryPath, { force: true });
      removed.push(entryPath);
    }
  }

  return removed;
}

const removedPaths = [
  ...removeHostedBinaryArtifacts(distDir),
  ...removeHostedBinaryArtifacts(androidPublicDir),
];

if (removedPaths.length === 0) {
  console.log("prepare-android-web-assets: sin artefactos hospedados para retirar");
} else {
  console.log("prepare-android-web-assets: artefactos retirados");
  for (const removedPath of removedPaths) {
    console.log(` - ${path.relative(rootDir, removedPath)}`);
  }
}
