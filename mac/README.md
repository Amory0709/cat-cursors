# 猫标 macOS 版

[**HappyCadogt**](https://space.bilibili.com/406949928)（[哔哩哔哩 @406949928](https://space.bilibili.com/406949928)）设计的「猫标」鼠标指针 macOS 移植。

[返回主 README](../README.md)

## Apple Silicon 支持

旧版 Mousecape **不支持** Apple Silicon 和新版 macOS。请使用：

| 工具 | 链接 | 说明 |
| --- | --- | --- |
| **Mousecape-swiftUI** | [Releases](https://github.com/sdmj76-team/Mousecape-swiftUI/releases) | **推荐**，通用二进制，原生支持 `.cape` |
| **Trace** | [Releases](https://github.com/User1334/Trace/releases) | 备选，支持 `.cape` |
| MaCursor | [Releases](https://github.com/writronic/MaCursor/releases) | 仅 `.cursor` 格式，不直接兼容本仓库 `.cape` |

本仓库构建的 `Cat-Cursor.cape` 已针对现代工具优化：
- 动画帧数上限 **24 帧**（符合 Mousecape-swiftUI 限制）
- 默认尺寸 **64pt**

## 光标预览

| 样式 | 说明 | 预览 |
| --- | --- | --- |
| 默认箭头 | 日常指针 | ![default](../docs/previews/default.png) |
| 文本选择 | 输入文字 | ![text](../docs/previews/text.png) |
| 链接手型 | 悬停链接 | ![pointer](../docs/previews/pointer.png) |
| 等待加载 | 加载动画 | ![wait](../docs/previews/wait.png) |

完整样式表见 [主 README](../README.md#光标预览)。

## 设计者

全部光标美术与动画由 B 站 UP 主 **HappyCadogt** 原创设计，详见 [主 README 设计者章节](../README.md#设计者)。

## 前置要求

| 项目 | 要求 |
| --- | --- |
| 系统 | macOS 15 (Sequoia) 或更高（Mousecape-swiftUI） |
| 芯片 | Apple Silicon / Intel 均可 |
| 依赖 | [Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI/releases) 或 Trace |

## 安装方式

### 方式一：直接导入 `.cape`（推荐）

1. 安装 [Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI/releases)
2. 双击 `Cat-Cursor.cape`（Release 包或 [`dist/Cat-Cursor.cape`](./dist/Cat-Cursor.cape)）
3. 点击 **Apply**，并开启 **开机自动应用**

### 方式二：Release 安装脚本

1. 下载 [Releases](https://github.com/Amory0709/cat-cursors/releases/latest) 并解压
2. 双击 **Install Cat Cursor.command**

若提示「无法验证恶意软件」：**右键 > 打开**，或改用方式一（不必运行脚本）。

```bash
xattr -dr com.apple.quarantine ~/Downloads/Cat-Cursor-macOS
```

### 方式三：克隆仓库安装

```bash
cd mac
chmod +x install.sh
./install.sh
```

安装脚本会自动检测 Mousecape / Trace，并在 Apple Silicon 上引导安装 Mousecape-swiftUI。

### 方式四：手动导入（同方式一）

1. 双击 [`dist/Cat-Cursor.cape`](./dist/Cat-Cursor.cape)
2. 在 Mousecape-swiftUI 中选择「猫标 Cat Cursor」
3. 点击 **Apply**

### 方式五：自行构建 DMG

```bash
cd mac/package
chmod +x build_dmg.sh
./build_dmg.sh
```

## 首次使用必做

在 Mousecape-swiftUI 中：

**设置 > 通用 > 开启「开机自动应用」**

否则重启后光标可能恢复默认。

## 常见问题

**Q: Apple Silicon 上旧 Mousecape 不工作？**

A: 正常。请改装 [Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI/releases)。

**Q: 光标只在 Dock 区域生效？**

A: 打开 **系统设置 > 辅助功能 > 显示 > 指针**，点击 **重设颜色**，然后重新 Apply 主题。

**Q: Terminal 里仍是默认光标？**

A: 正常，部分 App 使用内置光标。

## 自行构建

```bash
pip install -r requirements.txt
python3 build_cape.py
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--size` | `64` | 光标尺寸（points） |
| `--max-frames` | `24` | 动画帧上限 |
| `--output` | `dist/Cat-Cursor.cape` | 输出路径 |

## 鸣谢

- **设计者 [HappyCadogt](https://space.bilibili.com/406949928)**
- **Amory0709**：macOS 移植
- **[Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI)**：Apple Silicon 光标管理工具
