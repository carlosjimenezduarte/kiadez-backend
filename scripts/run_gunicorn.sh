#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_MODULE="${APP_MODULE:-app.main:app}"
GUNICORN_BIN="${GUNICORN_BIN:-$ROOT_DIR/venv/bin/gunicorn}"
CONFIG_FILE="${GUNICORN_CONFIG:-$ROOT_DIR/deploy/gunicorn.conf.py}"

if [[ ! -x "$GUNICORN_BIN" ]]; then
  echo "Gunicorn no esta instalado en $GUNICORN_BIN" >&2
  echo "Ejecuta: ./venv/bin/pip install -r requirements-production.txt" >&2
  exit 1
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "No se encontro la configuracion de Gunicorn en $CONFIG_FILE" >&2
  exit 1
fi

cd "$ROOT_DIR"
exec "$GUNICORN_BIN" -c "$CONFIG_FILE" "$APP_MODULE"

