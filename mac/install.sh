#!/bin/bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
exec /bin/bash "$HERE/lib/install_core.sh" "$HERE"
