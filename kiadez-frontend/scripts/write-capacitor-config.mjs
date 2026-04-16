import { writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");
const mode = process.argv[2] ?? "local";

const config = {
  appId: "com.kiadez.app",
  appName: "Kiadez",
  webDir: "dist",
};

if (mode === "remote") {
  config.server = {
    url: "https://kiadez.com",
    cleartext: false,
  };
} else if (mode !== "local") {
  console.error(`Modo de Capacitor no soportado: ${mode}`);
  process.exit(1);
}

const outputPath = path.join(rootDir, "capacitor.config.json");
writeFileSync(outputPath, `${JSON.stringify(config, null, 2)}\n`, "utf8");

console.log(`capacitor-config: modo ${mode} escrito en ${outputPath}`);
