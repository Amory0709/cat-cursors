# 猫标 Cat Cursor — macOS 移植

中文 | [English](./README_en-US.md)

**Windows 原版与全部原创美术：HappyCadogt「猫标」**。本仓库将其移植为 macOS 的 Mousecape 主题，不是 Windows 原版项目。

| 平台 / 工作 | 原作者或项目 |
| --- | --- |
| **Windows 原版** | [HappyCadogt（B 站 UID 406949928）](https://space.bilibili.com/406949928) · [「加载中」的猫标](https://www.bilibili.com/video/BV1S2itBHEJH/)；Windows 下载按原作者发布说明获取 |
| GNU/Linux 素材移植 | [Tseshongfeeshur / Ryan — cat-cursors](https://github.com/Tseshongfeeshur/cat-cursors)；本仓库 PNG/config 的上游 |
| macOS 移植与维护 | [Amory0709 — 本仓库](https://github.com/Amory0709/cat-cursors) |

完整署名与权利说明：[CREDITS.md](./CREDITS.md)。原 MIT 文本保留不变，移植不表示拥有原作者美术版权。

## 获取修复版

修复分支的安装包由 [Validate and package](https://github.com/Amory0709/cat-cursors/actions/workflows/validate.yml) 生成。打开对应本次修复提交的成功运行，下载 **Cat-Cursor-macOS-candidate** artifact（GitHub 可能要求登录）。其中包含 ZIP、DMG 和独立 `.cape`。

**旧 Releases 不会因为源码修改而自动更新。** 只有新的 `v*` 标签触发、且验证通过后，才会生成新的 [Release 安装包](https://github.com/Amory0709/cat-cursors/releases)。`mac/dist/` 是构建输出，不再提交两个不同内容的旧主题文件。

候选包的自动测试不等于在你的 Mac 上实际完成 Apply。验证边界和手工验收见 [docs/VALIDATION.md](./docs/VALIDATION.md)。

## 安装：只需导入和 Apply

1. 从官方页面安装 [Mousecape-swiftUI](https://github.com/sdmj76/Mousecape-swiftUI/releases/latest)。其当前 README 要求 macOS 14+，提供 Intel / Apple Silicon 通用版本；实际以所下载版本说明为准。
2. 先打开 Mousecape，再把 **Cat-Cursor.cape** 拖进窗口，或使用 **Import**。
3. 确认导入，选中 **猫标 Cat Cursor**，点击 **Apply / 应用**。
4. 用包内 **Cursor Test.html** 在 Safari 检查链接、文字、抓取、缩放及点击位置。

升级旧主题时，可先用管理器的 **File > Reset System Cursor（Cmd+R）** 恢复默认，再导入新文件；不要删除整个主题库。是否覆盖已有同名主题，由你在管理器导入对话框中决定。

`.command` 只是可选的导入助手，不会直接执行底层光标命令、不修改管理器私有目录，也不会把「打开请求成功」说成「已应用」。被 macOS 拦截时，直接跳过脚本，按上面步骤导入数据文件即可。**不需要关闭 Gatekeeper、递归清除隔离属性或运行 sudo。**

## 本轮修复

- 使用 Mousecape 实际识别的 WindowServer 标识，修复手型、抓取、横向/纵向缩放的错误映射；目前覆盖 **21 个标识、9 组素材**，不再把条目数量当作已验证角色数量。
- 默认 **32 个逻辑点**，同时提供 **1x / 2x 无损 PNG** 图像。Hotspot 按实际 PNG 像素计算，并在构建时验证边界。
- 按时间轴采样动画，保留完整循环时长。最多 **24 帧**；长动画会减少姿势和帧率，不能保证与 Windows 原版同样流畅。
- 不把「禁止操作」错误地替换成「等待」，也不把精确十字光标替换成普通箭头。缺少对应素材的角色不覆盖，保留原生功能含义。
- ZIP、DMG 和 Windows 主机打包共用清单，包含中文说明、导入助手、测试页、署名和 SHA256SUMS。

PNG 是上游解码器支持的格式，**HEIF 不是导入的必要条件**。本次选用 PNG 是为了无损透明度和减少构建依赖，不把所有导入失败归因于格式。

## 光标预览

![猫标样式代表帧](./docs/previews/showcase.png)

这些是原素材的代表帧，不是本轮修复已通过系统应用验收的证明。

## 排查与恢复

**导入没出现：** 确認下载的是新构建包，在已打开的 Mousecape 内使用 Import。脚本识别不到改名/非标准位置的 App 时，请手动导入，或设置 `MOUSECAPE_APP` 路径。

**只在 Dock 生效：** 管理器官方 [排查说明](https://github.com/sdmj76/Mousecape-swiftUI#troubleshooting) 指出自定义系统指针颜色可能干扰全局应用，可按说明重设颜色后重新 Apply。

**某个应用不变化：** 部分应用使用自己的光标；同时在 Finder、Safari 测试，不通过删除配置或关闭系统安全机制解决。权限仅按管理器和 macOS 的实际提示处理。

**恢复默认：** Mousecape → File → Reset System Cursor（Cmd+R）。登录后自动应用可在管理器设置中自行开启。

反馈请附：macOS 版本、芯片、Mousecape 版本、主题构建提交、发生在导入/Apply/切换角色的哪一步，以及截图或日志。不要发送敏感系统信息。

## 开发与自行构建

Python 3.10+；CI 使用 Python 3.12。安装主题的用户不需要 Python。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r mac/requirements.txt
python -m unittest discover -s tests -v
python scripts/build_release.py --version candidate
# 仅 macOS 可加 --dmg
```

构建输出：`dist/Cat-Cursor-macOS-vcandidate.zip`；主题：`mac/dist/Cat-Cursor.cape`。

Windows 主机可运行 `scripts/build-release.ps1` 生成相同的 **macOS** ZIP；它不是 Windows 光标安装器。Windows 原版请回到上方原作者链接。

详细参数：[mac/README.md](./mac/README.md)。
