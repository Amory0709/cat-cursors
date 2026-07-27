# 猫标主题鼠标指针（macOS）

中文 | [English](./README_en-US.md)

HappyCadogt 设计的猫咪动态光标 macOS 版。需配合光标管理工具使用（**推荐 [Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI/releases)**）。

## Apple Silicon 用户必读

旧版 [Mousecape](https://github.com/alexzielenski/Mousecape) 在 **Apple Silicon** 和新版 macOS 上已无法稳定工作。

| 工具 | Apple Silicon | 说明 |
| --- | --- | --- |
| **[Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI/releases)** | 支持 | **推荐**，通用二进制，直接导入 `.cape` |
| **[Trace](https://github.com/User1334/Trace/releases)** | 支持 | 备选，支持 `.cape` |
| **[MaCursor](https://github.com/writronic/MaCursor/releases)** | 支持 | 使用 `.cursor` 格式，需手动处理 |
| 旧版 Mousecape | 不推荐 | Intel 老系统可用，Apple Silicon 请避免 |

## 下载安装

前往 **[Releases](https://github.com/Amory0709/cat-cursors/releases/latest)** 下载最新安装包。

前置：先安装 **[Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI/releases)**。

**最简单（推荐）：** 解压后双击 **`Cat-Cursor.cape`** → 在 Mousecape 中点 **Apply**。

若要用安装脚本，见下方 [Gatekeeper 提示](#gatekeeper-无法打开安装脚本)。

## 光标预览

![猫标光标样式预览](./docs/previews/showcase.png)

| 样式 | 说明 | 预览 |
| --- | --- | --- |
| 默认箭头 | 日常指针，猫咪探头等动画 | ![default](./docs/previews/default.png) |
| 文本选择 | 输入文字时的 I 形光标 | ![text](./docs/previews/text.png) |
| 链接 / 手型 | 悬停链接、可点击区域 | ![pointer](./docs/previews/pointer.png) |
| 抓取 | 拖拽、闭合手型 | ![pointer_2](./docs/previews/pointer_2.png) |
| 等待 | 加载中动画 | ![wait](./docs/previews/wait.png) |
| 忙碌 | 后台处理但仍可点击 | ![progress](./docs/previews/progress.png) |
| 水平缩放 | 左右调整窗口/区域 | ![size_hor](./docs/previews/size_hor.png) |
| 垂直缩放 | 上下调整窗口/区域 | ![size_ver](./docs/previews/size_ver.png) |

> 以上均为动态光标，预览图为各样式的代表帧。完整动画请在安装后体验。

## 设计者

| | |
| --- | --- |
| **设计者** | [**HappyCadogt**](https://space.bilibili.com/406949928) |
| **哔哩哔哩** | [@406949928](https://space.bilibili.com/406949928) |
| **介绍视频** | [「加载中」的猫标](https://www.bilibili.com/video/BV1S2itBHEJH/) |

**HappyCadogt** 是「猫标」主题的原创设计者，负责全部光标的美术设计与动画制作。本仓库 macOS 版基于 TA 的作品移植，**版权归原作者所有**。如果喜欢这套光标，请前往 B 站关注并支持原作者。

## 关于项目

- **原创设计**：[哔哩哔哩 @HappyCadogt（UID: 406949928）](https://space.bilibili.com/406949928)
- **macOS 移植**：[GitHub @Amory0709](https://github.com/Amory0709)

- 手绘猫咪风格，**全部**为动态图标
- 映射 **28** 种 macOS 系统光标角色

## 适用平台

| 平台 | 说明 |
| --- | --- |
| **macOS** | 本仓库提供安装包，需 [Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI/releases) 或 Trace |
| **Windows** | 请从 [B 站 @HappyCadogt](https://space.bilibili.com/406949928) 下载原版 |

---

## macOS 安装

### 方式一：直接导入 `.cape`（推荐，无 Gatekeeper 脚本拦截）

1. 安装 **[Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI/releases)**
2. 从 [Releases](https://github.com/Amory0709/cat-cursors/releases/latest) 下载并解压
3. **双击 `Cat-Cursor.cape`**
4. 在 Mousecape 中选择「猫标 Cat Cursor」，点击 **Apply**
5. 在 **设置 > 通用** 开启 **开机自动应用**

### 方式二：Release 安装脚本

1. 完成方式一的前 2 步
2. 双击 **Install Cat Cursor.command**（若被拦截见下方 Gatekeeper 说明）

### Gatekeeper：无法打开安装脚本

从 GitHub 下载的 `.command` **未 Apple 签名**，macOS 可能提示「无法验证是否包含恶意软件」。**不是病毒**，是未签名脚本的正常拦截。

任选一种方式继续：

**A. 跳过脚本（最简单）**

直接双击 **`Cat-Cursor.cape`** 导入，不必运行 `.command`。

**B. 右键打开**

1. 在 `Install Cat Cursor.command` 上 **Control + 点击**（或右键）
2. 选 **打开**
3. 弹窗再点 **打开**

**C. 系统设置放行**

1. 先双击脚本触发拦截
2. 打开 **系统设置 > 隐私与安全性**
3. 底部点 **仍要打开**

**D. 终端移除隔离属性**

```bash
cd ~/Downloads/Cat-Cursor-macOS   # 改成你的解压路径
xattr -dr com.apple.quarantine .
chmod +x "Install Cat Cursor.command"
./Install Cat Cursor.command
```

### 方式三：克隆仓库安装

```bash
git clone https://github.com/Amory0709/cat-cursors.git
cd cat-cursors/mac
chmod +x install.sh
./install.sh
```

### 方式四：手动导入（仓库内文件）

双击 [`mac/dist/Cat-Cursor.cape`](./mac/dist/Cat-Cursor.cape)，在 Mousecape-swiftUI 中点击 **Apply**。

完整说明见 **[mac/README.md](./mac/README.md)**。

---

## 鸣谢

- **设计者 [HappyCadogt](https://space.bilibili.com/406949928)**（[哔哩哔哩 @406949928](https://space.bilibili.com/406949928)）：全部光标的美术设计与动画
- **Amory0709**：macOS 移植与本仓库维护
- **[Mousecape-swiftUI](https://github.com/sdmj76-team/Mousecape-swiftUI)**：Apple Silicon 推荐的光标管理工具

## 相关链接

- 设计者 B 站主页：https://space.bilibili.com/406949928
- 介绍视频：https://www.bilibili.com/video/BV1S2itBHEJH/
- 最新安装包：https://github.com/Amory0709/cat-cursors/releases/latest
