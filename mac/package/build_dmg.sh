#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PACKAGE_DIR="$ROOT/package"
STAGING="$(mktemp -d /tmp/cat-cursor-dmg.XXXXXX)"
OUTPUT="$ROOT/dist/Cat-Cursor-Installer.dmg"
VOLUME_NAME="Cat Cursor"

cleanup() {
  rm -rf "$STAGING"
}
trap cleanup EXIT

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "DMG 只能在 macOS 上构建。"
  exit 1
fi

echo ">>> 构建 .cape 主题"
python3 "$ROOT/build_cape.py" --output "$ROOT/dist/Cat-Cursor.cape"

echo ">>> 准备安装包内容"
mkdir -p "$STAGING/lib"
cp "$ROOT/dist/Cat-Cursor.cape" "$STAGING/Cat-Cursor.cape"
cp "$PACKAGE_DIR/Install Cat Cursor.command" "$STAGING/"
cp "$ROOT/lib/install_core.sh" "$STAGING/lib/"
cp "$PACKAGE_DIR/README.txt" "$STAGING/"

chmod +x "$STAGING/Install Cat Cursor.command"
chmod +x "$STAGING/lib/install_core.sh"

if [[ -f "$OUTPUT" ]]; then
  rm -f "$OUTPUT"
fi

echo ">>> 生成 DMG"
hdiutil create \
  -volname "$VOLUME_NAME" \
  -srcfolder "$STAGING" \
  -ov \
  -format UDZO \
  "$OUTPUT"

echo ""
echo "完成: $OUTPUT"
echo "用户只需双击 DMG，再双击「Install Cat Cursor.command」即可安装。"
