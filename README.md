# 🎬 Instagram Reels & Profiles Bulk Downloader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-brightgreen.svg)]()

An automated, lightweight, zero-dependency application to download Instagram Reels and user profiles in bulk.

No complex setups, no third-party Python packages (`pip`) required. Just run and download.

---

## ✨ Features

- **Profile Bulk Crawling**: Provide a profile link (e.g. `https://www.instagram.com/username/` or `@username`), and the downloader automatically discovers and downloads all accessible Reels from that creator.
- **Multiple Links at Once**: Paste several Reel URLs separated by spaces, commas, or line breaks.
- **Text File Batch Processing**: Put links into `reels.txt` and download everything in one go.
- **Chat Export Cleaner**: Automatically strips WhatsApp/Telegram chat prefixes and timestamps (e.g., `[16/10/26, 10:55 PM] Aditi : https://...`), extracting only the valid Reel URLs.
- **Clipboard Mode**: Type `clip` to automatically read copied links straight from your clipboard.
- **Smart Deduplication Archive**: Keeps track of downloaded videos in an `archive.txt`. Already-downloaded videos are skipped automatically. If you delete a video from your disk, the engine automatically syncs and re-downloads it.
- **Zero-Install Auto-Setup**: If the `yt-dlp` download engine isn't present, the script automatically downloads the latest official release directly from GitHub on first run.
- **Self-Updating**: Keep up with Instagram backend changes by typing `update` or running with `--update`.
- **Session Cookie Support**: Easily authenticate using a local `cookies.txt` for private or age-restricted content without exposing your password.

---

## 🚀 Quick Start

### Windows (Easiest)
1. Download or clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   ```
2. Double-click **`download.bat`**.
3. Paste a Profile URL, Reel link, or press **Enter** to process `reels.txt`.

### macOS & Linux
1. Open your terminal inside the project directory:
   ```bash
   chmod +x download.sh
   ./download.sh
   ```
   *(or run directly: `python3 download.py`)*

---

## 📖 Usage Examples

When you launch the program, you will see an interactive prompt:

```text
==========================================================
      Instagram Reels & Profiles Bulk Downloader          
==========================================================
You can provide:
  * A profile URL (e.g. https://www.instagram.com/name/ or @name)
  * A single Reel URL (e.g. https://www.instagram.com/reel/ID/)
  * Multiple URLs (separated by spaces or commas)
  * A text file path (e.g. reels or reels.txt)
  * Type 'clip' to read links from clipboard
  * Type 'multi' to paste multiple lines
  * Type 'update' to check for engine updates
  * Press ENTER to check for existing reels.txt

Enter Instagram URL(s), profile, or command:
```

### 1. Download an entire profile's accessible Reels
Paste the profile URL or handle:
```text
https://www.instagram.com/mindforgeh/
# or simply:
@mindforgeh
```
Videos will be saved directly into: `downloads/mindforgeh/`.

### 2. Download a single Reel or Post
```text
https://www.instagram.com/reel/DeotUomNFBl/
```
Videos will be saved directly into: `downloads/reels/`.

### 3. Download multiple links at once
```text
https://www.instagram.com/reel/ID1/ https://www.instagram.com/reel/ID2/
```

### 4. Batch download from Notepad (`reels.txt`)
Paste your links into `reels.txt` (see `reels.example.txt` for format) and simply press **Enter** at the prompt.

### 5. Command-Line Arguments
You can also pass links or files directly from the command line:
```bash
# Windows
download.bat reels.txt
download.bat https://www.instagram.com/mindforgeh/

# Linux / macOS / Python
python download.py reels.txt
python download.py https://www.instagram.com/mindforgeh/
```

---

## 📁 Output Directory Structure

All downloaded media is kept organized separate from the code:

```text
yt-dlp-instagram/
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
├── download.bat                  <-- Windows 1-click launcher
├── download.ps1                  <-- PowerShell launcher
├── download.sh                   <-- macOS/Linux launcher
├── download.py                   <-- Core engine (cross-platform)
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
- Type **`update`** in the program, or run:
  ```bash
  download.bat --update
  # or
  python download.py --update
  ```
This automatically updates the underlying engine to the latest release with upstream fixes.

---

## ⚖️ Disclaimer

This software is intended for personal backup and educational purposes only. Please respect the copyright and intellectual property rights of content creators. Use in accordance with the terms of service of the platform.

---

## 📄 License

This project is open-source and released under the [MIT License](LICENSE).
