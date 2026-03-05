import { copyFile, mkdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');
const appFilePath = path.join(projectRoot, 'src', 'App.svelte');
const distDir = path.join(projectRoot, 'dist');
const indexHtmlPath = path.join(distDir, 'index.html');

const appSource = await readFile(appFilePath, 'utf8');
const htmlRouteMatches = [...appSource.matchAll(/['"`](\/[^'"`]+\.html)['"`]\s*:/g)];
const htmlRoutes = [...new Set(htmlRouteMatches.map((match) => match[1]))]
  .filter((route) => route !== '/index.html')
  .sort();

await Promise.all(
  htmlRoutes.map(async (route) => {
    const relativePath = route.replace(/^\//, '');
    const targetFile = path.join(distDir, relativePath);
    await mkdir(path.dirname(targetFile), { recursive: true });
    await copyFile(indexHtmlPath, targetFile);
  })
);

console.log(`create-route-aliases: ${htmlRoutes.length} aliases creados`);
