<p align="center">
  <img src="docs/previews/default.png" width="72" alt="跟着箭头的小猫">
  <img src="docs/previews/pointer.png" width="72" alt="猫咪链接光标">
  <img src="docs/previews/pointer_2.png" width="72" alt="猫咪抓取光标">
</p>

<h1 align="center">猫标 Cat Cursor 🐾</h1>
<p align="center">让一只小猫，陪你在 Mac 上点点点。</p>
<p align="center">中文 · <a href="README_en-US.md">English</a></p>

HappyCadogt「猫标」的 **macOS 移植**。Windows 原版和猫咪美术均由 [HappyCadogt](https://www.bilibili.com/video/BV1S2itBHEJH/) 创作。

> 🪟 **Windows 的小猫在这里：[原版下载（蓝奏云）](https://happycadogt.lanzoul.com/b01881lrdg)**，密码 **`1145`**。安装与更新请看[原作者视频及评论区](https://www.bilibili.com/video/BV1S2itBHEJH/)。下面是 Mac 的领养步骤 🐾

## 🐱 两种 Mac 养猫方式

| | 本仓库 + [Mousecape-swiftUI](https://github.com/sdmj76/Mousecape-swiftUI) | [neco0w0/CatCursor](https://github.com/neco0w0/CatCursor) |
| --- | --- | --- |
| 怎么用 | 导入 `.cape` 主题，再点 Apply；下方有图解 | [下载独立 App](https://github.com/neco0w0/CatCursor/releases/latest)，启动后从菜单栏控制；无需 Mousecape |
| 怎么显示 | 通过 Mousecape 替换系统光标 | 隐藏系统光标，由 App 绘制跟随鼠标的小猫 |
| 适合谁 | 想切换不同主题、编辑光标图片和点击热点 | 想用专门的小猫 App，调大小、开关点击猫爪动画 |
| 使用特点 | 动画最多 24 帧；部分 App 自定义光标可能覆盖主题 | 作者提示可能有轻微跟随延迟、切换 App 时闪回系统光标；形状识别不准时需校准 |

另一个项目的介绍来自其 README，**尚未在本机实测**。切换方案时，先恢复系统默认光标或退出原来的光标 App。

<details>
<summary>🧰 Mousecape 还能干什么？</summary>

Mousecape 是通用的 **Mac 光标管理器**，`.cape` 是一整套光标主题，小猫只是其中一种。

- **换装与备份**：导入、导出、预览和切换其他 `.cape` 主题，随时恢复系统默认。
- **自己做主题**：编辑静态图片、动画，以及真正响应点击的位置（热点）。
- **转换 Windows 光标**：支持导入 `.cur` / `.ani` 文件并转换为 Mac 主题。本仓库已经转换好，直接导入 `Cat-Cursor.cape` 即可。

更多功能见 [Mousecape 官方说明](https://github.com/sdmj76/Mousecape-swiftUI#features)。

</details>

## 🐈 Mac 先领回两样东西

| 下载 | 选哪个？ |
| --- | --- |
| [**Mousecape-swiftUI 光标管理器**](https://github.com/sdmj76/Mousecape-swiftUI/releases/latest) | 推荐官方 **1.2.0**：下载 `Mousecape_swiftUI_v1.2.0.zip`，解压后把 App 放进“应用程序” |
| [**猫标主题 v1.3.0**](https://github.com/Amory0709/cat-cursors/releases/tag/v1.3.0) | 在 Assets 下载 **`Cat-Cursor-macOS-v1.3.0.zip`** 并解压 |

管理器 1.2.0 支持 **macOS 14+、Apple Silicon / Intel**。请认准 **sdmj76/Mousecape-swiftUI**；旧版 Mousecape 是另一个项目。已有可用的 SwiftUI 版本可直接使用。

`Source code (zip)` 是源码，**不是安装包**。v1.0.0–v1.2.0 猫标旧包已撤下，请使用上面的修复版。

## 🐾 三步换上猫标

升级前先用 **文件 → 导出 Cape** 备份旧主题；同名覆盖时只替换已备份的猫标。无需运行 `.command`、`sudo`，也无需关闭系统安全功能。

### ① 导入：选这个 `.cape` 文件

打开 **Mousecape.app**，从屏幕顶部菜单选 **文件 → 导入 Cape…**（也可点窗口右上方的 **向下箭头入框** 图标）。进入解压后的文件夹，选中 **`Cat-Cursor.cape`**，点 **打开 / Open**。

<img src="docs/screenshots/01-import-cape.jpg" width="760" alt="导入窗口：选中 Cat-Cursor.cape，右下角蓝色按钮为打开">

### ② 应用：左边选小猫，右上点蓝色勾号

左侧选中 **猫标 Cat Cursor**，再点窗口最右上角的 **蓝色圆形勾号 ✓**，它就是 **应用 / Apply**。只导入还不够，点完后确认出现“已应用”。

<img src="docs/screenshots/02-select-and-apply.jpg" width="760" alt="Mousecape 主界面：左侧选中猫标 Cat Cursor，最右上角蓝色圆形勾号是 Apply">

### ③ 试一试：小猫有没有跟上？

在 Safari 打开安装包里的 **`Cursor Test.html`**：移到蓝色 **Link** 上试手型，在 **Text selection** 里拖选文字，在 **grab** 区域按住鼠标，再试横向和纵向缩放。最后对准 **Click hotspot** 的十字中心点击，看看落点是否对齐，也去 Finder 中试试。

<img src="docs/screenshots/03-cursor-test.jpg" width="760" alt="Safari 光标测试页：链接、文字选择、抓取、横纵缩放和底部点击热点测试区">

<sub>截图来自 Mousecape-swiftUI 1.2.0 中文界面与 Safari，仅展示操作位置。动画、透明度和点击位置请看自己屏幕上的实际光标；精确十字和禁止操作保留系统样式。</sub>

> 🐱 2026-10-15：修复主题在 **macOS 26.6.2 / Apple Silicon / Mousecape-swiftUI 1.2.0** 上完成导入和 Apply，使用者确认成功。这是单机记录，更多环境仍欢迎反馈。[验证记录](docs/VALIDATION.md)

## 🧶 小猫使用贴士

- **没变化？** 确认已点 Apply；只在 Dock 生效时，查看管理器的[官方排查说明](https://github.com/sdmj76/Mousecape-swiftUI#troubleshooting)。
- **想换回来？** 文件 → **恢复系统默认光标 / Reset System Cursor**（⌘R）；或导入之前导出的主题并 Apply。
- **有些还是系统光标？** 精确十字、禁止操作等角色按设计保留原样。动画最多 24 帧，长动画会减少姿势；开机自动应用由你自行选择。

## ♡ 谢谢把小猫带来的大家

**Windows 原作与美术：[HappyCadogt](https://space.bilibili.com/406949928)** · **Linux 素材移植：[Tseshongfeeshur / Ryan](https://github.com/Tseshongfeeshur/cat-cursors)** · **macOS 移植：[Amory0709](https://github.com/Amory0709)**

[完整署名](CREDITS.md) · [构建与校验](mac/README.md) · [问题反馈](https://github.com/Amory0709/cat-cursors/issues)
