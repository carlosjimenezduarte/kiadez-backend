# Prueba local de Kiadez Live con OBS

Esta prueba valida el circuito real:

```text
OBS Studio -> RTMP local -> HLS local -> /live.html
```

## 1. Levantar el servidor RTMP/HLS

Desde `kiadez-frontend`:

```bash
npm run live:server
```

El servidor usa:

- RTMP: `rtmp://127.0.0.1:1935/live`
- Clave de transmision: `stream`
- HLS: `http://127.0.0.1:8000/live/stream/index.m3u8`

El servidor conserva el ultimo HLS generado para facilitar pruebas despues de cortar OBS.

## 2. Levantar la web

En otra terminal, desde `kiadez-frontend`:

```bash
npm run dev -- --host 127.0.0.1 --port 5173
```

Abrir:

```text
http://127.0.0.1:5173/live.html?src=http://127.0.0.1:8000/live/stream/index.m3u8
```

## 3. Configurar OBS Studio

En `Ajustes -> Emision`:

- Servicio: `Personalizado`
- Servidor: `rtmp://127.0.0.1:1935/live`
- Clave de transmision: `stream`

Para 16:9, usar una resolucion como `1920x1080` o `1280x720`.
Para 9:16, usar una resolucion como `1080x1920` o `720x1280`.

## 4. Produccion

En el servidor dedicado se recomienda cambiar esta prueba por MediaMTX, SRS, OvenMediaEngine o Nginx-RTMP supervisado por systemd y publicado por Nginx/HTTPS. FastAPI debe quedar fuera del transporte de video.
