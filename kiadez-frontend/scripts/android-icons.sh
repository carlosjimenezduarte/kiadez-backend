#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_ICON="${1:-$ROOT_DIR/public/logo-kiadez.png}"
RES_DIR="$ROOT_DIR/android/app/src/main/res"

if ! command -v magick >/dev/null 2>&1; then
  echo "Error: ImageMagick ('magick') no esta disponible en PATH." >&2
  exit 1
fi

if [[ ! -f "$SRC_ICON" ]]; then
  echo "Error: no se encontro el icono fuente: $SRC_ICON" >&2
  exit 1
fi

generate_legacy_icon() {
  local density="$1"
  local size="$2"
  local inset="$(( size * 88 / 100 ))"
  local target_dir="$RES_DIR/mipmap-$density"

  magick "$SRC_ICON" \
    -auto-orient \
    -resize "${inset}x${inset}" \
    -background none \
    -gravity center \
    -extent "${size}x${size}" \
    "$target_dir/ic_launcher.png"

  cp "$target_dir/ic_launcher.png" "$target_dir/ic_launcher_round.png"
}

generate_foreground_icon() {
  local density="$1"
  local canvas="$2"
  local inset="$(( canvas * 66 / 100 ))"
  local target_dir="$RES_DIR/mipmap-$density"

  magick "$SRC_ICON" \
    -auto-orient \
    -resize "${inset}x${inset}" \
    -background none \
    -gravity center \
    -extent "${canvas}x${canvas}" \
    "$target_dir/ic_launcher_foreground.png"
}

generate_legacy_icon "mdpi" 48
generate_legacy_icon "hdpi" 72
generate_legacy_icon "xhdpi" 96
generate_legacy_icon "xxhdpi" 144
generate_legacy_icon "xxxhdpi" 192

generate_foreground_icon "mdpi" 108
generate_foreground_icon "hdpi" 162
generate_foreground_icon "xhdpi" 216
generate_foreground_icon "xxhdpi" 324
generate_foreground_icon "xxxhdpi" 432

echo "Iconos Android generados desde: $SRC_ICON"
