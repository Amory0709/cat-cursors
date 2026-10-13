#!/bin/bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [[ -f "$HERE/lib/install_core.sh" ]]; then
  exec /bin/bash "$HERE/lib/install_core.sh" "$HERE"
elif [[ -f "$HERE/../lib/install_core.sh" ]]; then
  exec /bin/bash "$HERE/../lib/install_core.sh" "$HERE/.."
fi
echo 'Incomplete package: lib/install_core.sh is missing.' >&2
exit 1
