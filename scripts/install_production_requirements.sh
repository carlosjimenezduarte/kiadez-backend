#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIP_BIN="${PIP_BIN:-$ROOT_DIR/venv/bin/pip}"

if [[ ! -x "$PIP_BIN" ]]; then
  echo "No se encontro pip en $PIP_BIN" >&2
  echo "Ajusta PIP_BIN o crea el virtualenv en $ROOT_DIR/venv" >&2
  exit 1
fi

cd "$ROOT_DIR"
exec "$PIP_BIN" install -r requirements-production.txt

