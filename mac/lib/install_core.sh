#!/bin/bash
set -euo pipefail
# Import only. Never modify Mousecape's private library or invoke mousecloak.
resolve_cape() {
  local candidate
  for candidate in "$1/Cat-Cursor.cape" "$1/dist/Cat-Cursor.cape"; do
    if [[ -f "$candidate" ]]; then printf '%s\n' "$candidate"; return 0; fi
  done
  return 1
}
resolve_app() {
  local candidate
  if [[ -n "${MOUSECAPE_APP:-}" ]]; then
    [[ -d "$MOUSECAPE_APP" ]] || return 1
    printf '%s\n' "$MOUSECAPE_APP"
    return 0
  fi
  for candidate in "$HOME/Applications/Mousecape.app" /Applications/Mousecape.app; do
    if [[ -d "$candidate" ]]; then printf '%s\n' "$candidate"; return 0; fi
  done
  return 1
}
is_macos() { [[ "$(uname -s)" == Darwin ]]; }
validate_plist() { /usr/bin/plutil -lint "$1"; }
bundle_id() { /usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$1/Contents/Info.plist"; }
open_theme() { /usr/bin/open -a "$1" "$2"; }
verify_package() {
  if [[ -f "$1/SHA256SUMS" ]]; then
    (cd "$1" && /usr/bin/shasum -a 256 -c SHA256SUMS)
  fi
}
notify_import() {
  /usr/bin/osascript -e 'display dialog "已请求 Mousecape 打开主题。请确认导入，选中「猫标 Cat Cursor」，再点 Apply。脚本没有自动应用光标。" buttons {"知道了"} default button 1 with title "猫标：请确认导入并应用"' || true
}
main() {
  if ! is_macos; then echo 'This installer requires macOS.' >&2; return 1; fi
  local root="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}" cape app ident
  if ! cape="$(resolve_cape "$root")"; then
    echo 'Missing Cat-Cursor.cape. Download the complete package or build it first.' >&2
    return 1
  fi
  verify_package "$root" || return 1
  validate_plist "$cape" || return 1
  if ! app="$(resolve_app)"; then
    echo 'Install Mousecape-swiftUI, then import Cat-Cursor.cape and click Apply.' >&2
    echo 'https://github.com/sdmj76/Mousecape-swiftUI/releases/latest' >&2
    return 1
  fi
  ident="$(bundle_id "$app" 2>/dev/null)" || ident=unknown
  case "$ident" in
    com.alexzielenski.*)
      echo 'Legacy Mousecape detected. Install Mousecape-swiftUI or import manually.' >&2
      return 1 ;;
    com.sdmj76.*) ;;
    *) echo "Unrecognized app identity ($ident). Use Mousecape Import manually." >&2; return 1 ;;
  esac
  if ! open_theme "$app" "$cape"; then
    echo 'Could not open the theme. Open Mousecape and use Import manually.' >&2
    return 1
  fi
  echo 'Open request sent; import/application is NOT yet confirmed.'
  echo 'Confirm the import, select 猫标 Cat Cursor, then click Apply in Mousecape.'
  echo 'Use the manager reset/restore command to return to the system cursors.'
  notify_import
}
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then main "$@"; fi
