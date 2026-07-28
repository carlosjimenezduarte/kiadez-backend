const fs = require("node:fs");
const path = require("node:path");
const NodeMediaServer = require("node-media-server");

const rootDir = path.resolve(__dirname, "..");
const mediaRoot = path.join(rootDir, "live-media");
const ffmpegPath = process.env.FFMPEG_PATH || "/usr/bin/ffmpeg";
const rtmpPort = Number(process.env.KIADEZ_LIVE_RTMP_PORT || 1935);
const httpPort = Number(process.env.KIADEZ_LIVE_HTTP_PORT || 8000);
const streamApp = process.env.KIADEZ_LIVE_APP || "live";
const defaultStreamKey = process.env.KIADEZ_LIVE_STREAM_KEY || "stream";

fs.mkdirSync(mediaRoot, { recursive: true });

const config = {
  logType: 3,
  rtmp: {
    port: rtmpPort,
    chunk_size: 60000,
    gop_cache: true,
    ping: 30,
    ping_timeout: 60,
  },
  http: {
    port: httpPort,
    mediaroot: mediaRoot,
    allow_origin: "*",
  },
  trans: {
    ffmpeg: ffmpegPath,
    tasks: [
      {
        app: streamApp,
        hls: true,
        hlsFlags: "[hls_time=2:hls_list_size=6:hls_flags=delete_segments+append_list]",
        hlsKeep: true,
      },
    ],
  },
};

const nms = new NodeMediaServer(config);

console.log("");
console.log("Kiadez live media server");
console.log(`OBS URL:       rtmp://127.0.0.1:${rtmpPort}/${streamApp}`);
console.log(`OBS clave:     ${defaultStreamKey}`);
console.log(`HLS local:     http://127.0.0.1:${httpPort}/${streamApp}/${defaultStreamKey}/index.m3u8`);
console.log(
  `Pagina local:  http://127.0.0.1:5173/live.html?src=http://127.0.0.1:${httpPort}/${streamApp}/${defaultStreamKey}/index.m3u8`,
);
console.log("");

nms.run();
