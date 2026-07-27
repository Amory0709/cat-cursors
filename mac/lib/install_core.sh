#!/bin/zsh
set -euo pipefail

# Shared install logic for install.sh and DMG installer.
# Usage: install_core.sh [directory-containing-cape]

INSTALLER_DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
MOUSECAPE_APP="/Applications/Mousecape.app"
MOUSECLOAK="$MOUSECAPE_APP/Contents/MacOS/mousecloak"
SUPPORT_DIR="$HOME/Library/Application Support/Mousecape/capes"
INSTALLED_CAPE="$SUPPORT_DIR/com.happycadogt.cat-cursor.cape"

resolve_cape_file() {
  local dir="$1"
  local candidates=(
    "$dir/Cat-Cursor.cape"
    "$dir/猫标-Cat-Cursor.cape"
    "$dir/dist/猫标-Cat-Cursor.cape"
  )

  for candidate in "${candidates[@]}"; do
    if [[ -f "$candidate" ]]; then
      print -r -- "$candidate"
      return 0
    fi
  done

  return 1
}

alert() {
  local title="$1"
  local message="$2"
  osascript -e "display alert \"${title}\" message \"${message}\" as informational"
}

confirm_open_mousecape_download() {
  osascript <<'APPLESCRIPT'
set userChoice to button returned of (display dialog "需要先安装 Mousecape 才能替换 macOS 系统光标。" & return & return & "是否打开 Mousecape 下载页？" buttons {"取消", "打开下载页"} default button "打开下载页" with title "猫标 Cat Cursor")
if userChoice is "打开下载页" then
  open location "https://github.com/alexzielenski/Mousecape/releases"
end if
APPLESCRIPT
}

if ! CAPE_SOURCE="$(resolve_cape_file "$INSTALLER_DIR")"; then
  alert "安装失败" "找不到 Cat-Cursor.cape 主题文件。"
  exit 1
fi

if [[ ! -d "$MOUSECAPE_APP" ]]; then
  confirm_open_mousecape_download
  exit 1
fi

mkdir -p "$SUPPORT_DIR"
cp -f "$CAPE_SOURCE" "$INSTALLED_CAPE"

open -a Mousecape "$INSTALLED_CAPE"
sleep 2

if [[ -x "$MOUSECLOAK" ]]; then
  "$MOUSECLOAK" --apply "$INSTALLED_CAPE" >/dev/null 2>&1
else
  alert "需要手动确认" "主题已导入 Mousecape。请在窗口中点击 Apply 完成应用。"
  exit 0
fi

alert "安装完成" "猫标光标已应用。首次使用请在 Mousecape 菜单执行 Install Helper Tool，以便重启后自动恢复。"
