#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCAL_JDK="$ROOT_DIR/.jdks/current"

if [[ -z "${JAVA_HOME:-}" && -x "$LOCAL_JDK/bin/java" ]]; then
  export JAVA_HOME="$LOCAL_JDK"
fi

if [[ -n "${JAVA_HOME:-}" ]]; then
  export PATH="$JAVA_HOME/bin:$PATH"
fi

if [[ -z "${ANDROID_HOME:-}" && -d "$HOME/Android/Sdk" ]]; then
  export ANDROID_HOME="$HOME/Android/Sdk"
fi

if [[ -n "${ANDROID_HOME:-}" ]]; then
  export ANDROID_SDK_ROOT="$ANDROID_HOME"
  LOCAL_PROPERTIES="$ROOT_DIR/android/local.properties"
  if [[ ! -f "$LOCAL_PROPERTIES" ]]; then
    printf "sdk.dir=%s\n" "$ANDROID_HOME" > "$LOCAL_PROPERTIES"
  fi
fi

cd "$ROOT_DIR/android"
./gradlew "$@"
