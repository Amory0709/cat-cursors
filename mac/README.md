# 猫标 macOS 版

HappyCadogt 设计的「猫标」鼠标指针 macOS 移植。输出为 [Mousecape](https://github.com/alexzielenski/Mousecape) 可导入的 `.cape` 主题。

[返回主 README](../README.md)

## 为什么需要 Mousecape

macOS 没有官方的光标主题机制，无法像 Windows 那样双击安装，也无法像 Linux 那样在系统设置里切换 XDG 主题。Mousecape 通过系统接口替换光标，是目前最常用的方案。

## 前置要求

| 项目 | 要求 |
| --- | --- |
| 系统 | macOS 10.15 或更高 |
| 依赖 | [Mousecape](https://github.com/alexzielenski/Mousecape/releases) |

## 安装方式

### 方式一：安装脚本（推荐）

```bash
cd mac
chmod +x install.sh
./install.sh
```

脚本会自动：

1. 将主题复制到 `~/Library/Application Support/Mousecape/capes/`
2. 在 Mousecape 中导入主题
3. 调用 `mousecloak --apply` 应用光标
4. 弹出完成提示

### 方式二：手动导入

1. 双击 [`dist/猫标-Cat-Cursor.cape`](./dist/猫标-Cat-Cursor.cape)
2. 在 Mousecape 中选择「猫标 Cat Cursor」
3. 点击 **Apply**

### 方式三：DMG 安装包

在 macOS 上构建 DMG（需本机执行，无法在 Windows / Linux 交叉编译）：

```bash
cd mac/package
chmod +x build_dmg.sh
./build_dmg.sh
```

生成文件：`mac/dist/猫标-Cat-Cursor-Installer.dmg`

用户流程：

1. 双击 DMG 挂载
2. 双击 **Install Cat Cursor.command**
3. 按弹窗提示完成

## 首次使用必做

在 Mousecape 菜单栏选择：

**Mousecape → Install Helper Tool**

否则重启或重新登录后，光标可能恢复为系统默认。这是 macOS 的机制限制，不是主题 bug。

## 包含的光标映射

| macOS 系统角色 | 动画源 |
| --- | --- |
| 箭头、移动、十字、消失项等 | `default` |
| 文本选择（I-beam） | `text` |
| 链接、拖拽、帮助、上下文菜单等 | `pointer` |
| 抓取（闭合手） | `pointer_2` |
| 等待（Wait） | `wait` |
| 忙碌但可点击 | `progress` |
| 水平缩放 | `size_hor` |
| 垂直缩放 | `size_ver` / `size_ver_2` |

共映射 **28** 种 macOS 光标角色。

## 自行构建

### 依赖

```bash
pip install -r requirements.txt
```

### 生成 .cape

```bash
cd mac
python3 build_cape.py
```

可选参数：

```bash
python3 build_cape.py --size 48 --output dist/猫标-Cat-Cursor.cape
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--size` | `48` | 光标显示尺寸（macOS points） |
| `--output` | `dist/猫标-Cat-Cursor.cape` | 输出路径 |

## 目录结构

```
mac/
├── build_cape.py              # 从 Linux 源 PNG 构建 .cape
├── install.sh                 # 一键安装脚本
├── requirements.txt           # Python 构建依赖
├── lib/
│   └── install_core.sh        # 安装核心逻辑（脚本与 DMG 共用）
├── package/
│   ├── build_dmg.sh           # DMG 打包脚本
│   ├── Install Cat Cursor.command
│   └── README.txt
└── dist/
    ├── 猫标-Cat-Cursor.cape       # 预构建主题
    └── 猫标-Cat-Cursor-Installer.dmg  # 运行 build_dmg.sh 后生成
```

## 常见问题

**Q: 安装后部分 App 仍是默认光标？**

A: 正常。Terminal 等 App 会使用内置光标，macOS 无法强制全部替换。

**Q: 重启后光标变回默认？**

A: 请在 Mousecape 中执行 **Install Helper Tool**。

**Q: 没有安装 Mousecape 能直接用吗？**

A: 不能。macOS 不支持零依赖的原生光标主题安装。

## 鸣谢

- 原作者：[哔哩哔哩 @HappyCadogt](https://space.bilibili.com/406949928)
- Linux 移植：[Ryan / Tseshongfeeshur](https://github.com/Tseshongfeeshur/cat-cursors)（本仓库 fork 并含 macOS 版）
- 光标管理工具：[Mousecape](https://github.com/alexzielenski/Mousecape)

## English summary

This folder builds a Mousecape `.cape` theme from the Linux port source PNGs.

```bash
pip install -r requirements.txt
python3 build_cape.py
chmod +x install.sh && ./install.sh
```

Install [Mousecape](https://github.com/alexzielenski/Mousecape/releases) first, then run `install.sh` or double-click the `.cape` file in `dist/`.
