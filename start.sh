#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: Python 3 is required." >&2
  exit 1
fi

python3 - <<'PY'
import sys

if sys.version_info < (3, 10):
    raise SystemExit("Error: Python 3.10 or newer is required.")
PY

# The safe build currently uses only the standard library. If future versions
# add packages, install them automatically from the same requirements file.
if grep -Ev '^[[:space:]]*(#|$)' requirements.txt | grep -q .; then
  python3 -m pip install -r requirements.txt
fi

exec python3 main.py "$@"