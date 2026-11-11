# 🚗 ReviveMyDroid

**Give your old Android phone or tablet a second life as a dedicated, lightweight Android Auto Headunit — 100% Root-Free.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![ADB](https://img.shields.io/badge/Requires-ADB%20(No%20Root)-orange.svg)]()

Got an old 2GB RAM Android phone collecting dust in a drawer? Instead of letting it become e-waste, **ReviveMyDroid** strips away heavy manufacturer bloatware, optimizes system animations and power states via ADB, and transforms the device into a fast **Android Auto Wireless/USB Display Receiver** powered by [Open Headunit](https://github.com/andreknieriem/open-headunit).

---

## ✨ Key Features

- **🧹 Multi-Brand Non-Root Debloater:** Curated package lists for **Universal Google Bloat**, **Samsung**, **Xiaomi (MIUI/HyperOS)**, **Oppo/Realme (ColorOS/RealmeUI)**, **Vivo (FuntouchOS)**, and **Asus (ZenUI)**.
- **🗑️ 3rd-Party & User Apps Cleaner:** Scan and remove any remaining user-installed apps (social media, games, shopping apps) with 1-click batch removal (`[A]`) or selective numbers, complete with timestamped rollback backups.
- **🛡️ Safe & Reversible (Automatic Rollback):** Choose between `disable-user` or `uninstall --user 0`. Every session saves a timestamped JSON rollback log inside `backups/` so you can restore removed apps anytime with a single click.
- **⚡ Low-RAM Headunit Tweaks:** Automatically disables UI window/transition animations (`0.0x` or `0.5x`), enables **Stay Awake while charging** (AC/USB/Wireless), disables the lockscreen, and trims system caches.
- **📱 Auto-Download & Install Open Headunit:** Fetches the latest `.apk` release directly from [`andreknieriem/open-headunit`](https://github.com/andreknieriem/open-headunit) via GitHub API and installs it over ADB.
- **⚙️ Automated Headunit Optimizer (No Root):** Automatically wakes and unlocks the screen, grants necessary permissions (`pm grant` + overlay `appops`), sends automation intents, and navigates UI via ADB to set optimal **Resolution (720p/480p)**, **Frame Rate (30 FPS)**, **Hardware Codec (H.264)**, and **Audio Sink** routing for lag-free 2GB RAM performance.
- **🚗 Advanced Car Dashboard Tweaks:** Auto-power on when ignition is turned on, dedicated Kiosk mode launcher, custom screen density (DPI) for larger driving buttons, native 720p display downscaling, anti-glare dark mode, and cabin thermal/battery sleep protection.
- **📦 Zero External Dependencies:** Written purely in Python 3 Standard Library. No `pip install` required!

---

## 🎯 Low-RAM Daily Driving Settings (Automated)

ReviveMyDroid includes automated presets matching the optimal configuration for 2GB RAM receivers:

| Setting | Value | Why it matters |
| :--- | :--- | :--- |
| **Resolution** | **720p (1280x720)** or **480p** | Prevents thermal throttling, video stutter, and GPU/RAM exhaustion on older SoCs (avoids 1080p). |
| **Frame Rate** | **30 FPS** | Reduces decode overhead by 50% compared to 60 FPS while keeping maps and media perfectly readable. |
| **Video Codec** | **Hardware (H.264)** | Leverages the device's native hardware decoder block instead of taxing weak CPU cores. |
| **Audio Sink** | **Disabled (Optional)** | Eliminates audio latency by streaming media directly from your primary phone to your car's Bluetooth. |

---

## 🚀 Quick Start

### Option A: Interactive CLI (Manual)
1. **Clone this repository:**
   ```bash
   git clone https://github.com/hielmymuthohar/Revive_MyDroid.git
   cd Revive_MyDroid
   ```
2. **Connect your old Android phone via USB** (with **USB Debugging** enabled in Developer Options).
3. **Run the Interactive Tool:**
   - **Windows:** Double-click `run_windows.bat` (or run `python revive.py`).
   - **Linux / macOS:** `./run_unix.sh`

---

### Option B: Autonomous Setup via AI Agent (Zero-Effort 🤖)

Don't want to type commands or navigate menus yourself? You can command an **AI Coding Agent** (e.g. Antigravity, Claude Code, Cursor Agent, Windsurf) to execute the entire transformation autonomously from start to finish!

#### 📋 Prompt Template:
```text
Please transform my connected old Android device into a dedicated Android Auto Headunit using this repository:
https://github.com/hielmymuthohar/Revive_MyDroid

My phone is connected via USB with USB Debugging enabled. Please autonomously perform the entire setup end-to-end:
1. Verify the ADB connection (`adb devices`). If ADB platform-tools are missing on this PC, fetch them locally.
2. Detect the device brand/model and apply the safe non-root debloater profile to free up RAM.
3. Apply headunit system tweaks (disable UI animations to 0.0x, enable stay-awake while charging, disable lockscreen).
4. Download the latest Open Headunit APK release from GitHub and install it over ADB.
5. Run the automated configuration: pre-grant permissions, set Resolution to 720p @ 30 FPS, select Hardware H.264 codec, and disable receiver audio sink.
6. Notify me when setup is complete and the headunit is ready for daily driving.
```

---

## 🧹 Debloat Rules & User Apps Cleaner

ReviveMyDroid features a two-tiered cleaning engine designed to strip away non-essential background services and free maximum RAM for smooth display decoding:

### 1. OEM & System Bloatware Profiles
Curated package lists target heavy vendor services and background telemetry without breaking core Android functionality:
- **Google Common Bloat:** YouTube, Chrome, Google Search, Docs, Wellbeing, Talkback, Print Spooler, etc.
- **Samsung (OneUI / TouchWiz):** Bixby, Samsung Pay, AR Zone, Game Launcher, Dex, Samsung Cloud, etc.
- **Xiaomi (MIUI / HyperOS):** Mi Browser, Mi Video, Mi Pay, Analytics (`msa`), Joyose, Yellow Pages, Mi Cloud, etc.
- **Oppo / Realme (ColorOS / RealmeUI):** HeyTap, Theme Store, Game Space, Roaming, Browser, etc.
- **Vivo (FuntouchOS / OriginOS):** V-Appstore, iManager, Vivo Cloud, Jovi, Game Center, etc.
- **Asus (ZenUI):** Asus Support, ZenUI Services, Mobile Manager, etc.

### 2. User-Installed (3rd-Party) Apps Cleaner
Before turning a phone into a dedicated car display, old user-installed apps (games, social media, shopping apps) often silently run background sync services.
- **Automatic Detection:** Scans all non-system user packages (`pm list packages -3`).
- **Core Protection:** Essential headunit packages (like `com.andrerinas.headunitrevived`) are automatically whitelisted and protected.
- **Flexible Removal:** Choose `A` to strip all 3rd-party apps in one click for a clean slate, or pick specific apps by number (e.g. `1,3,5`).
- **Non-Root Reversible Modes:** Choose between `disable-user` (freeze app) or `uninstall --user 0` (removes app and cache while retaining system image).

---

## 🚗 Advanced Car Headunit Tweaks (Menu Option [6])

Take your dedicated headunit build to the next level with purpose-built vehicle integrations:

| Tweak | Command / Tech | Real-World Benefit |
| :--- | :--- | :--- |
| **🔑 Auto-Power On on Charge** | `fastboot oem off-mode-charge 0` / Qualcomm props | Boots the phone automatically when your car's ignition sends 5V USB power — never hold the physical power button again! |
| **🖥️ Dedicated Kiosk Mode** | `cmd package set-home-activity` + launcher freeze | Locks Open Headunit as the permanent default Home launcher. The phone never shows an Android desktop or wallpaper. |
| **👁️ Large Dashboard Touch Targets** | `wm density 160` (Customizable) | Enlarges Google Maps, Spotify, and call buttons for safer, effortless fingertip reach while driving. |
| **📉 Native 720p Display Downscaling** | `wm size 720x...` | Renders the entire Android OS at 720p instead of 1080p, reducing GPU memory bandwidth and keeping device cold under summer heat. |
| **🌙 Anti-Glare Dark Mode** | `cmd uimode night yes` | High-contrast dark dashboard aesthetic that eliminates nighttime cabin glare and saves OLED power. |
| **🛡️ Cabin Thermal & Battery Guard** | `settings put system screen_off_timeout 15000` | Screen stays awake indefinitely while driving (charging), but turns off in 15 seconds into deep sleep as soon as car engine shuts off. |

---

## ⏪ How to Restore / Rollback Removed Apps & Settings

Everything done by ReviveMyDroid is **100% reversible without factory resetting or flashing ROMs**.

### Restoring Removed Apps (Bloatware & 3rd-Party)
Every debloat session automatically saves a timestamped JSON backup log in the `backups/` directory (e.g. `rollback_Redmi_8A_Pro_20261111_233510.json`).

1. Connect your phone via USB and launch ReviveMyDroid (`python revive.py` or double-click `run_windows.bat`).
2. From the Main Menu, select:
   ```text
   [7] ⏪ Restore / Rollback Debloated Packages from Backup
   ```
3. A list of all previous backup sessions will be displayed. Enter the number corresponding to your backup file.
4. ReviveMyDroid will instantly restore all packages using Android's native `cmd package install-existing <pkg>` and `pm enable <pkg>` — **no internet connection or APK re-download needed!**

### Reverting System Tweaks & Display Settings
If you want to restore factory UI animations, normal lockscreen behavior, native panel resolution, or disable stay-awake:
1. Select **`[8] 🔄 Revert System & Display Tweaks to Factory Defaults`** from the Main Menu.
2. Window animations will be restored to `1.0x`, lockscreen re-enabled, screen timeout set to 60s, and display density/size reset to factory defaults.
