#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ -f "$SCRIPT_DIR/Cat-Cursor.cape" || -f "$SCRIPT_DIR/猫标-Cat-Cursor.cape" ]]; then
  INSTALL_ROOT="$SCRIPT_DIR"
elif [[ -f "$SCRIPT_DIR/../dist/猫标-Cat-Cursor.cape" ]]; then
  INSTALL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
else
  osascript -e 'display alert "安装失败" message "找不到 Cat-Cursor.cape 主题文件。"'
  exit 1
fi

LIB_SCRIPT="$SCRIPT_DIR/lib/install_core.sh"
if [[ ! -f "$LIB_SCRIPT" ]]; then
  LIB_SCRIPT="$INSTALL_ROOT/lib/install_core.sh"
fi

exec zsh "$LIB_SCRIPT" "$INSTALL_ROOT"
