# APK Android con Capacitor (Svelte)

Este proyecto ya fue preparado para empaquetar una APK Android real usando Capacitor.

## Requisitos

- Node.js y npm
- Android Studio
- Android SDK instalado
- JDK 17 o JDK 21 (no JDK 25)

Si tienes varias versiones de Java, antes de compilar exporta `JAVA_HOME` apuntando a JDK 21/17.

## Opción sin sudo: JDK 21 local en el proyecto

Si no puedes instalar Java a nivel sistema, puedes usar un JDK local:

```bash
mkdir -p .jdks
cd .jdks
curl -L 'https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jdk/hotspot/normal/eclipse' -o temurin21.tar.gz
tar -xzf temurin21.tar.gz
rm -f temurin21.tar.gz
ln -sfn jdk-21* current
cd ..
```

Los scripts `android:apk:debug` y `android:apk:release` detectan automáticamente `.jdks/current`.

## Flujo mínimo (rápido)

1. Preparar web + copiar a Android:

```bash
npm run android:prepare
```

2. Abrir Android Studio:

```bash
npm run cap:open:android
```

3. En Android Studio:

- Espera sincronización de Gradle.
- `Build > Build Bundle(s) / APK(s) > Build APK(s)`.
- Instala la APK en el teléfono.

## Modo producción web pura (wrapper a kiadez.com)

Este proyecto está configurado para abrir directamente `https://kiadez.com` dentro de la app nativa:

- `capacitor.config.json` usa `server.url = "https://kiadez.com"`.
- En este modo, la APK no depende del `dist` para renderizar pantallas, sino del sitio en producción.

Flujo recomendado:

```bash
npm run android:prepare:remote
npm run android:apk:debug
```

## Flujo por terminal (debug APK)

```bash
npm run android:prepare
npm run android:apk:debug
```

La APK queda en:

`android/app/build/outputs/apk/debug/app-debug.apk`

## Importante para que la app funcione en teléfono

- El backend API debe estar accesible desde internet por HTTPS (por ejemplo `https://api.kiadez.com`).
- CORS del backend debe permitir el origen de Capacitor en Android: `http://localhost`.
- La app ya usa `VITE_API_BASE_URL` de `.env.production` al hacer `npm run build`.

## Release firmado (producción)

- Crea keystore.
- Configura firma en `android/app/build.gradle`.
- Ejecuta:

```bash
npm run android:prepare
npm run android:apk:release
```

La APK release queda en:

`android/app/build/outputs/apk/release/app-release-unsigned.apk`
