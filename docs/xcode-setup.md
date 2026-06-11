# Building YT Autoplay Off from Source

This guide walks you through creating the distributable `YT Autoplay Off.app` in Xcode.

## Prerequisites

| Requirement | Version |
|---|---|
| macOS | 12 Monterey or later |
| Xcode | 14 or later |
| Safari | 15 or later |

---

## Step 1 — Create a new Safari Web Extension project

1. Open **Xcode**.
2. Go to **File → New → Project…**
3. Select the **macOS** tab, then choose **Safari Extension App**.
4. Fill in the fields:
   - **Product Name:** `YT Autoplay Off`
   - **Bundle Identifier:** `com.yourname.yt-autoplay-off` _(replace `yourname`)_
   - **Language:** Swift
   - **Include Extension:** ✔ checked
5. Click **Next**, choose a location, and click **Create**.

---

## Step 2 — Replace the generated extension files

Xcode creates placeholder web extension files inside the extension target folder (typically named `YT Autoplay Off Extension/`). Delete those files and replace them with the ones from this repo.

Your Xcode project's extension folder should end up looking like this:

```
YT Autoplay Off Extension/
├── manifest.json         ← Extension/manifest.json
├── content.js            ← Extension/content.js
├── background.js         ← Extension/background.js
├── popup.html            ← Extension/popup.html
└── icons/
    ├── icon-16.png
    ├── icon-32.png
    ├── icon-48.png
    └── icon-128.png
```

In Xcode, make sure all new files are added to the **Extension target** (not the container app target). You can check by clicking each file in the Project Navigator and verifying the target membership in the **File Inspector** on the right.

---

## Step 3 — Update the container app UI (optional)

The native macOS container app exists only to register the extension with Safari. The Xcode template generates a `ContentView.swift` with a message like "Enable the extension in Safari…". You can leave it as-is or customise the copy to match the extension name.

---

## Step 4 — Run locally for testing

1. Select your **Mac** as the run destination in the toolbar.
2. Press **Cmd + R**.
3. The container app launches and the extension is registered with Safari.
4. Open Safari → **Settings → Extensions**, find **YT Autoplay Off**, and enable it.
5. Grant access to `youtube.com` when prompted.
6. Open a YouTube playlist to verify autoplay is disabled.

---

## Step 5 — Package for distribution

### Archive the build

1. Make sure **My Mac** is the selected scheme destination.
2. Go to **Product → Archive**.
3. Xcode will open the **Organizer** window when the archive is complete.

### Export the .app

1. Select the archive and click **Distribute App**.
2. Choose **Copy App** (no signing or notarisation required for local distribution).
3. Click **Next** and choose an export destination.
4. You'll get a folder containing `YT Autoplay Off.app`.

### Compress and upload

```bash
cd /path/to/exported/folder
zip -r "YT-Autoplay-Off.app.zip" "YT Autoplay Off.app"
```

Upload the zip to your [GitHub Release](https://github.com/imsoumya18/yt-autoplay-off/releases/new).

---

## Notes on signing

Because the app is built without an Apple Developer certificate, macOS Gatekeeper will quarantine it when users download it. The `install.sh` script and the README both handle this by running:

```bash
xattr -cr "YT Autoplay Off.app"
```

If you want a smoother install experience you can sign the app with a **free** Apple Developer account (which provides a Development certificate). This won't allow Mac App Store distribution but removes the Gatekeeper warning.
