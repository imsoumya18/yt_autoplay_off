# Building YT Autoplay Off from Source

This guide walks you through building and packaging the distributable `YT Autoplay Off.app`.

The Xcode project is already included in this repo — no setup from scratch needed.

## Prerequisites

| Requirement | Version |
|---|---|
| macOS | 12 Monterey or later |
| Xcode | 14 or later |
| Safari | 15 or later |

---

## Step 1 — Open the project

```bash
open "YT Autoplay Off.xcodeproj"
```

Or double-click `YT Autoplay Off.xcodeproj` in Finder.

The extension source files (`manifest.json`, `content.js`, etc.) live in:

```
YT Autoplay Off Extension/Resources/
```

---

## Step 2 — Run locally for testing

1. Select **My Mac** as the run destination in the Xcode toolbar.
2. Press **Cmd + R**.
3. The container app launches and registers the extension with Safari.
4. In Safari, go to **Settings → Extensions**, find **YT Autoplay Off**, and enable it.
5. When prompted, choose **Always Allow on youtube.com**.
6. Open any YouTube playlist — autoplay should be disabled automatically.

> **First run only:** go to **Safari → Settings → Advanced**, enable **Show features for web developers**, then go to **Safari → Develop → Allow Unsigned Extensions**.

---

## Step 3 — Package for distribution

### Archive the build

1. Make sure **My Mac** is selected as the scheme destination.
2. Go to **Product → Archive**.
3. Xcode opens the **Organizer** window when the archive finishes.

### Export the .app

1. Select the archive and click **Distribute App**.
2. Choose **Copy App** (no signing or notarisation needed).
3. Click **Next** and choose an export folder.
4. You'll get a folder containing `YT Autoplay Off.app`.

### Compress and upload

```bash
cd /path/to/exported/folder
zip -r "YT-Autoplay-Off.app.zip" "YT Autoplay Off.app"
```

Upload the zip to a [new GitHub Release](https://github.com/imsoumya18/yt-autoplay-off/releases/new).

---

## Notes on signing

Because the app is unsigned, macOS Gatekeeper quarantines it when users download it. The `install.sh` script handles this automatically with:

```bash
xattr -cr "YT Autoplay Off.app"
```

For a smoother install experience, you can sign the app with a free Apple Developer account (Development certificate). This doesn't allow App Store distribution but removes the Gatekeeper warning entirely.
