#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CAPE="$SCRIPT_DIR/Cat-Cursor.cape"
DEST="$HOME/Library/Application Support/Mousecape/capes/com.happycadogt.cat-cursor.cape"
MOUSECAPE="/Applications/Mousecape.app"

alert() {
  osascript -e "display alert \"${1}\" message \"${2}\" as informational"
}

if [[ ! -d "$MOUSECAPE" ]]; then
  alert "未安装 Mousecape" "请先安装 Mousecape-swiftUI：\nhttps://github.com/sdmj76-team/Mousecape-swiftUI/releases\n\nMaCursor 和旧版 Mousecape 不能导入 .cape 文件。"
  open "https://github.com/sdmj76-team/Mousecape-swiftUI/releases"
  exit 1
fi

if [[ ! -f "$CAPE" ]]; then
  alert "找不到主题文件" "请确认 Cat-Cursor.cape 和本脚本在同一文件夹。"
  exit 1
fi

xattr -dr com.apple.quarantine "$CAPE" 2>/dev/null || true
xattr -dr com.apple.quarantine "$MOUSECAPE" 2>/dev/null || true

mkdir -p "$(dirname "$DEST")"
cp -f "$CAPE" "$DEST"

open -a Mousecape
sleep 2
open -a Mousecape "$DEST"

alert "已复制主题" "1. 看 Mousecape 左侧是否出现「猫标 Cat Cursor」\n2. 点选它\n3. 点 Apply / 应用\n\n若 Mousecape 窗口没出现：完全退出后从「应用程序」重新打开。\n若列表仍为空：菜单 Import 手动选 Cat-Cursor.cape。"
