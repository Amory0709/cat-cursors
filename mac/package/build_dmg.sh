#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
if [[ "$(uname -s)" != Darwin ]]; then
  echo 'DMG creation requires macOS.' >&2
  exit 1
fi
python3 "$ROOT/scripts/build_release.py" --version "${VERSION:-candidate}" --dmg
