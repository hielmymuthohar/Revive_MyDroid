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
- **🛡️ Safe & Reversible (Automatic Rollback):** Choose between `disable-user` or `uninstall --user 0`. Every session saves a timestamped JSON rollback log inside `backups/` so you can restore removed apps anytime with a single click.
- **⚡ Low-RAM Headunit Tweaks:** Automatically disables UI window/transition animations (`0.0x` or `0.5x`), enables **Stay Awake while charging** (AC/USB/Wireless), disables the lockscreen, and trims system caches.
- **📱 Auto-Download & Install Open Headunit:** Fetches the latest `.apk` release directly from [`andreknieriem/open-headunit`](https://github.com/andreknieriem/open-headunit) via GitHub API and installs it over ADB.
- **⚙️ Automated Headunit Optimizer (No Root):** Automatically wakes and unlocks the screen, grants necessary permissions (`pm grant` + overlay `appops`), sends automation intents, and navigates UI via ADB to set optimal **Resolution (720p/480p)**, **Frame Rate (30 FPS)**, **Hardware Codec (H.264)**, and **Audio Sink** routing for lag-free 2GB RAM performance.
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

1. **Clone this repository:**
   ```bash
   git clone https://github.com/hielmymuthohar/Revive_MyDroid.git
   cd Revive_MyDroid
   ```
2. **Connect your old Android phone via USB** (with **USB Debugging** enabled in Developer Options).
3. **Run the Interactive Tool:**
   - **Windows:** Double-click `run_windows.bat` (or run `python revive.py`).
   - **Linux / macOS:** `./run_unix.sh`
