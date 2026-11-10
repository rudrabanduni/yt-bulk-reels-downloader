#!/usr/bin/env bash
# ====================================================================
# Instagram Reels & Profiles Bulk Downloader (macOS & Linux launcher)
# ====================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

TARGET="gui.py"
if [ "$#" -gt 0 ]; then
    TARGET="download.py"
fi

if command -v python3 &>/dev/null; then
    python3 -u "$SCRIPT_DIR/$TARGET" "$@"
elif command -v python &>/dev/null; then
    python -u "$SCRIPT_DIR/$TARGET" "$@"
else
    echo "[ERROR] Python 3 is required to run this application."
    echo "Please install Python 3 from https://www.python.org/ or using your package manager."
    exit 1
fi
