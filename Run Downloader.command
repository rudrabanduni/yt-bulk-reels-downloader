#!/usr/bin/env bash
# ====================================================================
# Instagram Bulk Reels Downloader - macOS 1-Click Launcher
# ====================================================================
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

if command -v python3 &>/dev/null; then
    python3 "$DIR/gui.py"
elif command -v python &>/dev/null; then
    python "$DIR/gui.py"
else
    echo "[ERROR] Python 3 was not found on your Mac."
    echo "Please install Python 3 from https://www.python.org/ or using Homebrew."
    read -p "Press Enter to exit..."
fi
