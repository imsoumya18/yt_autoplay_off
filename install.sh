#!/usr/bin/env bash
# install.sh — installs YT Autoplay Off.app and opens it so Safari can
# register the extension.
#
# Usage (from the folder where you downloaded the .app):
#   chmod +x install.sh
#   ./install.sh
#
# Or with curl (one-liner shown in the README):
#   curl -fsSL https://raw.githubusercontent.com/imsoumya18/yt-autoplay-off/main/install.sh | bash

set -euo pipefail

APP_NAME="YT Autoplay Off.app"
APPLICATIONS="/Applications/$APP_NAME"
DOWNLOADS="$HOME/Downloads/$APP_NAME"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_APP="$SCRIPT_DIR/$APP_NAME"

echo "========================================"
echo "  YT Autoplay Off — Installer"
echo "========================================"
echo ""

# ── 1. Locate the .app ────────────────────────────────────────────────────────
if [[ -d "$DOWNLOADS" ]]; then
  SOURCE="$DOWNLOADS"
elif [[ -d "$SCRIPT_APP" ]]; then
  SOURCE="$SCRIPT_APP"
else
  echo "Error: Could not find '$APP_NAME'."
  echo ""
  echo "Please place the downloaded .app in your Downloads folder"
  echo "or in the same directory as this script, then re-run."
  exit 1
fi

echo "Found: $SOURCE"
echo ""

# ── 2. Remove macOS quarantine ─────────────────────────────────────────────────
echo "Removing quarantine flag..."
xattr -cr "$SOURCE" 2>/dev/null || true

# ── 3. Copy to /Applications ──────────────────────────────────────────────────
if [[ -d "$APPLICATIONS" ]]; then
  echo "Removing existing installation..."
  rm -rf "$APPLICATIONS"
fi

echo "Copying to Applications..."
cp -r "$SOURCE" "$APPLICATIONS"

# ── 4. Open the app ───────────────────────────────────────────────────────────
echo "Opening YT Autoplay Off..."
open "$APPLICATIONS"

echo ""
echo "========================================"
echo "  Almost done! Two more steps:"
echo "========================================"
echo ""
echo "  1. In Safari, go to:"
echo "     Settings → Extensions"
echo "     and enable 'YT Autoplay Off'"
echo ""
echo "  2. If asked for website access,"
echo "     choose 'Always Allow on youtube.com'"
echo ""
echo "  Visit any YouTube playlist — autoplay"
echo "  is now off automatically."
echo ""
