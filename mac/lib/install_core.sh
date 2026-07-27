#!/bin/zsh
set -euo pipefail

# Shared install logic for install.sh and DMG/ZIP installer.
# Usage: install_core.sh [directory-containing-cape]

INSTALLER_DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
INSTALLED_CAPE="$HOME/Library/Application Support/Mousecape/capes/com.happycadogt.cat-cursor.cape"

MOUSECAPE_SWIFTUI_URL="https://github.com/sdmj76-team/Mousecape-swiftUI/releases/latest"
MACURSOR_URL="https://github.com/writronic/MaCursor/releases/latest"
TRACE_URL="https://github.com/User1334/Trace/releases/latest"

resolve_cape_file() {
  local dir="$1"
  local candidates=(
    "$dir/Cat-Cursor.cape"
    "$dir/dist/Cat-Cursor.cape"
    "$dir/猫标-Cat-Cursor.cape"
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

is_apple_silicon() {
  [[ "$(uname -m)" == "arm64" ]]
}

prompt_install_manager() {
  local arch_note=""
  if is_apple_silicon; then
    arch_note="检测到 Apple Silicon。旧版 Mousecape 已无法在新系统上稳定工作，请安装下方推荐的 Mousecape-swiftUI。"
  fi

  osascript <<APPLESCRIPT
set intro to "需要安装光标管理工具才能替换 macOS 系统光标。${arch_note}"

set userChoice to button returned of (display dialog intro & return & return & "推荐：Mousecape-swiftUI（Apple Silicon / macOS 15+ 通用二进制）" buttons {"取消", "MaCursor", "Mousecape-swiftUI"} default button "Mousecape-swiftUI" with title "猫标 Cat Cursor")

if userChoice is "Mousecape-swiftUI" then
  open location "${MOUSECAPE_SWIFTUI_URL}"
else if userChoice is "MaCursor" then
  open location "${MACURSOR_URL}"
end if
APPLESCRIPT
}

detect_manager() {
  if [[ -d "/Applications/Mousecape.app" ]]; then
    print -r -- "mousecape"
    return 0
  fi

  if [[ -d "/Applications/Trace.app" ]]; then
    print -r -- "trace"
    return 0
  fi

  if [[ -d "/Applications/MaCursor.app" ]]; then
    print -r -- "macursor"
    return 0
  fi

  return 1
}

apply_with_mousecape() {
  local cape_source="$1"
  local mousecloak="/Applications/Mousecape.app/Contents/MacOS/mousecloak"

  mkdir -p "$(dirname "$INSTALLED_CAPE")"
  cp -f "$cape_source" "$INSTALLED_CAPE"

  open -a Mousecape "$INSTALLED_CAPE"
  sleep 2

  if [[ -x "$mousecloak" ]]; then
    "$mousecloak" --apply "$INSTALLED_CAPE" >/dev/null 2>&1 || return 1
  else
    alert "需要手动确认" "主题已导入 Mousecape。请在应用中选择「猫标 Cat Cursor」并点击 Apply。"
    return 0
  fi

  if is_apple_silicon; then
    alert "安装完成" "猫标光标已应用。请在 Mousecape 设置 > 通用 中开启「开机自动应用」，以便重启后自动恢复。"
  else
    alert "安装完成" "猫标光标已应用。请在 Mousecape 设置中开启开机自动应用 / Helper，以便重启后自动恢复。"
  fi
}

apply_with_open_only() {
  local cape_source="$1"
  local app_name="$2"
  local helper_hint="$3"

  open -a "$app_name" "$cape_source"
  alert "主题已打开" "$helper_hint"
}

if ! CAPE_SOURCE="$(resolve_cape_file "$INSTALLER_DIR")"; then
  alert "安装失败" "找不到 Cat-Cursor.cape 主题文件。"
  exit 1
fi

if ! MANAGER="$(detect_manager)"; then
  prompt_install_manager
  exit 1
fi

case "$MANAGER" in
  mousecape)
    if ! apply_with_mousecape "$CAPE_SOURCE"; then
      if is_apple_silicon; then
        alert "应用失败" "当前 Mousecape 可能过旧。请改装 Mousecape-swiftUI 后重试。"
        open "$MOUSECAPE_SWIFTUI_URL"
      else
        alert "应用失败" "请在 Mousecape 中手动选择主题并点击 Apply。"
      fi
      exit 1
    fi
    ;;
  macursor)
    alert "格式说明" "MaCursor 使用 .cursor 主题格式，当前安装包为 .cape。请优先安装 Mousecape-swiftUI；或在 MaCursor 中手动导入 Windows 原版猫标。"
    open "$MOUSECAPE_SWIFTUI_URL"
    ;;
  trace)
    apply_with_open_only "$CAPE_SOURCE" "Trace" "Trace 已打开主题文件。请在 Themes 中选择导入的主题并应用。"
    ;;
esac
