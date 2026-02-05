#!/usr/bin/env bash
# Wrapper to launch the Caffeine tray app.
# If pyenv is installed, prefer the system Python by setting PYENV_VERSION=system.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -n "${CAFFEINE_PY:-}" ]; then
  CAFFEINE_PY_PATH="$CAFFEINE_PY"
else
  if [ -f "$SCRIPT_DIR/caffeine.py" ]; then
    CAFFEINE_PY_PATH="$SCRIPT_DIR/caffeine.py"
  elif [ -f "$SCRIPT_DIR/../caffeine.py" ]; then
    CAFFEINE_PY_PATH="$SCRIPT_DIR/../caffeine.py"
  elif [ -f "./caffeine.py" ]; then
    CAFFEINE_PY_PATH="$(pwd)/caffeine.py"
  else
    echo "Could not find caffeine.py; set CAFFEINE_PY to its path" >&2
    exit 1
  fi
fi

if command -v pyenv >/dev/null 2>&1; then
  export PYENV_VERSION=system
fi

exec python3 "$CAFFEINE_PY_PATH" "$@"
