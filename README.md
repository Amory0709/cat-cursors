# 猫标主题鼠标指针

中文 | [English](./README_en-US.md)

<!-- ![封面](./banner.png) -->

## 关于项目

- **原作者**：[哔哩哔哩 @406949928（HappyCadogt）](https://space.bilibili.com/406949928)
- **Linux 移植**：[GitHub @Tseshongfeeshur（Ryan）](https://github.com/Tseshongfeeshur)
- **macOS 移植**：本仓库 `mac/` 目录

截至项目发布（2026-02-10），原作者仅为 Windows 提供适配。Ryan 将其移植为 GNU/Linux 可用的 [XDG 光标主题包](https://specifications.freedesktop.org/icon-theme/latest/)；本仓库另含 macOS 版（基于 Mousecape）。

**特别感谢原作者 HappyCadogt 的付出，没有 TA 的设计与制作，就不可能有这些移植版本。**

## 项目内容

- 由 [**HappyCadogt**](https://space.bilibili.com/406949928) 设计并制作
- **全部**为动态图标
- 支持 **24 / 32 / 48 / 64 / 96 / 128 / 192 / 256** 多分辨率

## 适用平台

| 平台 | 状态 | 说明 |
| --- | --- | --- |
| Windows | 原版 | 请从 [B 站 @HappyCadogt](https://space.bilibili.com/406949928) 获取 |
| GNU/Linux | 已移植 | XDG 主题，KDE / GNOME 测试通过 |
| macOS | 已移植 | 需 [Mousecape](https://github.com/alexzielenski/Mousecape/releases)，见 [`mac/README.md`](./mac/README.md) |

---

## Linux 安装

### Arch Linux（推荐）

#### 使用 AUR 助手

```zsh
paru -S cat-cursors-git
```

或使用其他 AUR 助手：

```zsh
yay -S cat-cursors-git
```

#### 手动安装 AUR 包

```zsh
sudo pacman -S --needed base-devel
git clone https://aur.archlinux.org/cat-cursors-git.git
cd cat-cursors-git
makepkg -si
```

### 其他发行版（手动安装）

1. 安装 `git`

   Debian / Ubuntu：
   ```zsh
   sudo apt update
   sudo apt install git
   ```

   Fedora：
   ```zsh
   sudo dnf install git
   ```

   Arch Linux：
   ```zsh
   sudo pacman -S git
   ```

2. 克隆并安装到用户目录（推荐）：

   ```zsh
   git clone https://github.com/Tseshongfeeshur/cat-cursors.git hei_cursors
   mkdir -p ~/.local/share/icons/
   mv ./hei_cursors ~/.local/share/icons/
   ```

   或安装到系统目录（不建议，`pacman` 等包管理器无法追踪）：

   ```zsh
   git clone https://github.com/Tseshongfeeshur/cat-cursors.git hei_cursors
   sudo mkdir -p /usr/share/icons/
   sudo mv ./hei_cursors /usr/share/icons/
   ```

---

## Linux 应用方式

### KDE Plasma

1. 打开 **系统设置 → 外观和样式 → 颜色和主题 → 光标**，或运行：

   ```zsh
   systemsettings kcm_cursortheme
   ```

2. 选择「**猫标**」主题，点击「**应用**」
3. 在窗口上方选择合适的光标大小

### GNOME

1. 安装 `gnome-tweaks`

   Debian / Ubuntu：
   ```zsh
   sudo apt update
   sudo apt install gnome-tweaks
   ```

   Fedora：
   ```zsh
   sudo dnf install gnome-tweaks
   ```

   Arch Linux：
   ```zsh
   sudo pacman -S gnome-tweaks
   ```

2. 打开 **优化 → 外观 → 光标**
3. 在下拉菜单中选择「**Cat_cursor**」
4. 设置光标大小（示例为 48 像素）：

   ```zsh
   gsettings set org.gnome.desktop.interface cursor-size 48
   ```

### 其他桌面环境

请查阅对应桌面环境关于 XDG 光标主题的文档。

---

## macOS 安装

macOS **不支持**像 Windows / Linux 那样原生更换系统光标，需借助 [Mousecape](https://github.com/alexzielenski/Mousecape/releases)。

### 快速开始

1. 安装 Mousecape
2. 进入 `mac/` 目录，运行安装脚本：

   ```bash
   cd mac
   chmod +x install.sh
   ./install.sh
   ```

3. 首次使用请在 Mousecape 菜单执行 **Install Helper Tool**（登录后自动恢复光标）

### 其他方式

- 双击 `mac/dist/猫标-Cat-Cursor.cape` 手动导入
- 在 macOS 上运行 `mac/package/build_dmg.sh` 生成 DMG 安装包

完整说明、光标映射表与构建方法见 **[mac/README.md](./mac/README.md)**。

---

## 鸣谢

- **原作者 [HappyCadogt](https://space.bilibili.com/406949928)**：设计与制作
- **Ryan（Tseshongfeeshur）**：Linux XDG 移植
- **`xorg-xcursorgen`**：多分辨率光标生成工具

## 相关链接

- 博客介绍（Linux）：https://blog.ryanyuan.top/2026/02/10/cat-cursors/
- 原作者 B 站：https://space.bilibili.com/406949928
