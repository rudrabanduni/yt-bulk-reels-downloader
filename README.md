# 🎬 Instagram Reels & Profiles Bulk Downloader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-brightgreen.svg)]()

A lightweight, zero-dependency application to download Instagram Reels and user profiles in bulk.

Comes with a clean, native **Graphical Window (GUI)** for 1-click double-tap downloading on both **Windows** and **macOS**, as well as an optional CLI mode.

No third-party Python packages (`pip`) required. Just run and download.

---

## 🖥️ Simple Interactive Window

When you double-click the app, a clean graphical interface opens:

```text
+-----------------------------------------------------------+
| 🎬 Instagram Bulk Reels Downloader                        |
+-----------------------------------------------------------+
| 1. What would you like to download?                       |
|    (o) All Reels from a Profile (Bulk download)           |
|    ( ) Single Reel or Multiple Reel Links                 |
|    ( ) Batch from Text File (reels.txt)                   |
|                                                           |
| 2. Provide Link or Username:                              |
|    +-------------------------------------------------+    |
|    | https://www.instagram.com/mindforgeh/           |    |
|    +-------------------------------------------------+    |
|    [📋 Paste Clipboard]  [📂 Browse File]  [🧹 Clear]     |
|                                                           |
|    [ ⬇️ Start Download ]   [ 📁 Open Downloads ]          |
|                                                           |
| Real-time Progress & Status:                              |
| +-------------------------------------------------------+ |
| | [+] Discovering Reels for @mindforgeh...              | |
| | [download] 100% of 4.5MB at 3.2MB/s                   | |
| | [SUCCESS] All media downloaded to downloads/ folder!  | |
| +-------------------------------------------------------+ |
+-----------------------------------------------------------+
```

---

## ✨ Features

- **Profile Bulk Crawling**: Enter a profile link (e.g. `https://www.instagram.com/username/` or `@username`), and it automatically discovers and downloads all accessible Reels from that creator.
- **Multiple Links at Once**: Paste several Reel URLs separated by spaces, commas, or line breaks.
- **Text File Batch Processing**: Put links into `reels.txt` and download everything in one go.
- **Chat Export Cleaner**: Automatically strips WhatsApp/Telegram chat prefixes and timestamps (e.g., `[16/10/26, 10:55 PM] Friend : https://...`), extracting only the valid Reel URLs.
- **Clipboard Mode**: Paste copied links instantly with one click.
- **Smart Deduplication Archive**: Keeps track of downloaded videos in an `archive.txt`. Already-downloaded videos are skipped automatically. If you delete a video from your disk, the engine automatically syncs and re-downloads it.
- **Zero-Install Auto-Setup**: If the `yt-dlp` download engine isn't present, the script automatically downloads the latest official release directly from GitHub on first run.
- **Self-Updating**: Keep up with Instagram backend changes with the "Check Updates" button.
- **Session Cookie Support**: Easily authenticate using a local `cookies.txt` for private or age-restricted content without exposing your password.

---

## 🚀 Quick Start & 1-Click Launching

### 🍎 For macOS (MacBook / iMac)

#### Option A: 1-Click Double-Click (Easiest)
1. Download or clone this repository.
2. In Finder, open the project folder.
3. Double-click **`Run Downloader.command`**.
   *(If prompted on macOS first run, right-click and choose "Open")*
4. The interactive downloader window will pop up immediately!

#### Option B: Put an App Icon on Your Desktop (Never touch terminal again!)
Open Terminal inside the folder once and run:
```bash
chmod +x create_mac_app.sh && ./create_mac_app.sh
```
This places a real **`Instagram Downloader.app`** right on your Desktop. You can double-click it anytime just like Spotify or Chrome!

---

### 🪟 For Windows

1. Download or clone this repository.
2. Double-click:
   - **`Run Downloader.bat`** (or `download.bat`): Launches the downloader window immediately.
   - **`Run Downloader (No Console).vbs`**: Launches the window silently with no command prompt window.
3. Choose your option (Profile, Reels, or File), paste the link, and click **Start Download**!

---

### 🐧 For Linux / Command Line Users
You can also run via command-line arguments:
```bash
# Launch GUI
python3 gui.py

# Or use CLI directly
python3 download.py https://www.instagram.com/mindforgeh/
python3 download.py reels.txt
```

---

## 📁 Output Directory Structure

All downloaded media is kept organized separate from the code:

```text
yt-bulk-reels-downloader/
│
├── downloads/
│   ├── reels/
│   │   ├── archive.txt           <-- Download history tracker
│   │   ├── ID1_Video_Title.mp4
│   │   └── ID2_Video_Title.mp4
│   │
│   └── USERNAME/
│       ├── archive.txt           <-- Profile-specific archive
│       └── ID3_Video_Title.mp4
│
├── gui.py                        <-- Interactive graphical window
├── download.py                   <-- Core engine (auto-installs yt-dlp if missing)
├── Run Downloader.bat            <-- Windows 1-click launcher
├── Run Downloader.command        <-- macOS 1-click launcher
├── create_mac_app.sh             <-- Creates a Desktop App on Mac
├── reels.example.txt             <-- Batch template
└── reels.txt                     <-- Your links file
```

---

## 🍪 Private Profiles & Age Restrictions (Cookies)

For public profiles and public reels, **no login is required**.

If you need to access private accounts that you follow or age-restricted content:
1. Export your Instagram cookies using a browser extension like **Get cookies.txt LOCALLY** (Chrome/Firefox).
2. Save the file as **`cookies.txt`** inside this project folder.
3. The downloader will automatically detect and apply your session cookies.
*(Note: Never share or commit your `cookies.txt` to GitHub. It is already included in `.gitignore`.)*

---

## 🔄 Keeping Updated

Instagram regularly updates its web APIs. If downloads ever stop working:
- Click the **`Check Updates`** button in the app window, or run:
  ```bash
  download.bat --update
  # or
  python3 download.py --update
  ```
This automatically updates the underlying engine to the latest release with upstream fixes.

---

## ⚖️ Disclaimer

This software is intended for personal backup and educational purposes only. Please respect the copyright and intellectual property rights of content creators. Use in accordance with the terms of service of the platform.

---

## 📄 License

This project is open-source and released under the [MIT License](LICENSE).
