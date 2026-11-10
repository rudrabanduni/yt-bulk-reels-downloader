#!/usr/bin/env bash
# ====================================================================
# Creates a Native macOS Desktop App: "Instagram Downloader.app"
# ====================================================================
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$HOME/Desktop/Instagram Downloader.app"

echo "Creating 'Instagram Downloader.app' on your Desktop..."

mkdir -p "$APP_DIR/Contents/MacOS"
mkdir -p "$APP_DIR/Contents/Resources"

cat << 'EOF' > "$APP_DIR/Contents/Info.plist"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.instagram.reels.downloader</string>
    <key>CFBundleName</key>
    <string>Instagram Downloader</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

cat << EOF > "$APP_DIR/Contents/MacOS/launcher"
#!/usr/bin/env bash
cd "$DIR"
if command -v python3 &>/dev/null; then
    python3 "$DIR/gui.py"
elif command -v python &>/dev/null; then
    python "$DIR/gui.py"
else
    osascript -e 'display dialog "Python 3 is required. Please install Python 3." buttons {"OK"} default button "OK" with icon stop'
fi
EOF

chmod +x "$APP_DIR/Contents/MacOS/launcher"
chmod +x "$DIR/Run Downloader.command"

echo "=========================================================="
echo " [SUCCESS] 'Instagram Downloader.app' is on your Desktop!"
echo " You can now double-click it anytime from your Desktop."
echo " You never have to open the Terminal again!"
echo "=========================================================="
