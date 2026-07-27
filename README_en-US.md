# **A Cat Cursor Theme**

[中文](./README.md) | English

<!-- ![Banner](./banner.png) -->

## About

- **Original Author**: [Bilibili @406949928 (HappyCadogt)](https://space.bilibili.com/406949928)
- **Linux port**: [GitHub @Tseshongfeeshur (Ryan)](https://github.com/Tseshongfeeshur)
- **macOS port**: `mac/` directory in this repository

As of the project release date (2026-02-10), the original author only provided a Windows version. Ryan ported it to an [XDG cursor theme package](https://specifications.freedesktop.org/icon-theme/latest/) for GNU/Linux. This repository also includes a macOS port based on [Mousecape](https://github.com/alexzielenski/Mousecape).

**Many thanks to HappyCadogt — without their work, none of these ports would exist.**

## Project Content

- Designed and created by **[HappyCadogt](https://space.bilibili.com/406949928)**
- **Fully** animated cursors
- Supports **24 / 32 / 48 / 64 / 96 / 128 / 192 / 256** pixel resolutions

## Supported Platforms

| Platform | Status | Notes |
| --- | --- | --- |
| Windows | Original | Download from [Bilibili @HappyCadogt](https://space.bilibili.com/406949928) |
| GNU/Linux | Ported | XDG theme; tested on KDE Plasma and GNOME |
| macOS | Ported | Requires [Mousecape](https://github.com/alexzielenski/Mousecape/releases); see [`mac/README.md`](./mac/README.md) |

---

## Linux Installation

### Arch Linux (recommended)

#### Install with an AUR helper

```zsh
paru -S cat-cursors-git
```

Or with another AUR helper:

```zsh
yay -S cat-cursors-git
```

#### Install the AUR package manually

```zsh
sudo pacman -S --needed base-devel
git clone https://aur.archlinux.org/cat-cursors-git.git
cd cat-cursors-git
makepkg -si
```

### Other distributions (manual installation)

1. Install `git`

   Debian / Ubuntu:
   ```zsh
   sudo apt update
   sudo apt install git
   ```

   Fedora:
   ```zsh
   sudo dnf install git
   ```

   Arch Linux:
   ```zsh
   sudo pacman -S git
   ```

2. Clone and install for the current user (recommended):

   ```zsh
   git clone https://github.com/Amory0709/cat-cursors.git hei_cursors
   mkdir -p ~/.local/share/icons/
   mv ./hei_cursors ~/.local/share/icons/
   ```

   Or install system-wide (not recommended):

   ```zsh
   git clone https://github.com/Amory0709/cat-cursors.git hei_cursors
   sudo mkdir -p /usr/share/icons/
   sudo mv ./hei_cursors /usr/share/icons/
   ```

---

## Applying the Theme on Linux

### KDE Plasma

1. Open **System Settings → Appearance & Style → Colors & Themes → Cursors**, or run:
   ```zsh
   systemsettings kcm_cursortheme
   ```

2. Select the "**A Cat**" theme and click "**Apply**"
3. Choose a comfortable cursor size

### GNOME

1. Install `gnome-tweaks`
2. Open **Tweaks → Appearance → Cursor**
3. Select "**Cat_cursor**" from the dropdown
4. Set cursor size, for example:
   ```zsh
   gsettings set org.gnome.desktop.interface cursor-size 48
   ```

### Other desktop environments

Refer to your environment's documentation for applying XDG cursor themes.

---

## macOS Installation

macOS does **not** support native system-wide cursor themes like Windows or Linux. You need [Mousecape](https://github.com/alexzielenski/Mousecape/releases).

### Quick start

1. Install Mousecape
2. Run the installer script:

   ```bash
   cd mac
   chmod +x install.sh
   ./install.sh
   ```

3. On first use, choose **Install Helper Tool** in the Mousecape menu so cursors persist after login

See **[mac/README.md](./mac/README.md)** for DMG packaging, manual import, and build instructions.

---

## Acknowledgements

- **[HappyCadogt](https://space.bilibili.com/406949928)** — original design
- **Ryan (Tseshongfeeshur)** — Linux port
- **`xorg-xcursorgen`** — multi-resolution cursor generation

## Links

- Blog post (Linux): https://blog.ryanyuan.top/2026/02/10/cat-cursors/
- Original author on Bilibili: https://space.bilibili.com/406949928
