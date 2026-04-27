#!/bin/bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$APP_DIR/dist"
BUNDLE_DIR="$DIST_DIR/UntappdBeerHistory"
ZIP_PATH="$DIST_DIR/UntappdBeerHistory-desktop.zip"

rm -rf "$BUNDLE_DIR"
mkdir -p "$BUNDLE_DIR"
mkdir -p "$DIST_DIR"

cp "$APP_DIR/README.md" "$BUNDLE_DIR/"
cp "$APP_DIR/QUICKSTART.md" "$BUNDLE_DIR/"
cp "$APP_DIR/requirements.txt" "$BUNDLE_DIR/"
cp "$APP_DIR/run.py" "$BUNDLE_DIR/"
cp "$APP_DIR/desktop_launcher.py" "$BUNDLE_DIR/"
cp "$APP_DIR/start_desktop_app.command" "$BUNDLE_DIR/"
cp "$APP_DIR/start_desktop_app.bat" "$BUNDLE_DIR/"
cp "$APP_DIR/streamlit_app.py" "$BUNDLE_DIR/"
cp "$APP_DIR/untapped.py" "$BUNDLE_DIR/"
cp "$APP_DIR/untapped_selenium.py" "$BUNDLE_DIR/"
cp "$APP_DIR/.gitignore" "$BUNDLE_DIR/"

chmod +x "$BUNDLE_DIR/start_desktop_app.command"

rm -f "$ZIP_PATH"
cd "$DIST_DIR"
zip -rq "$(basename "$ZIP_PATH")" "$(basename "$BUNDLE_DIR")"

echo "Created shareable desktop bundle:"
echo "  $ZIP_PATH"
