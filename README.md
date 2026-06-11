<div align="center">
  <img src="Extension/icons/icon-128.png" width="90" alt="YT Autoplay Off icon" />
  <h1>YT Autoplay Off</h1>
  <p>A lightweight Safari extension that automatically disables autoplay on YouTube playlist pages.</p>

  <p>
    <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" />
    <img alt="License" src="https://img.shields.io/badge/license-MIT-green?style=flat-square" />
    <img alt="Platform" src="https://img.shields.io/badge/platform-macOS%2012%2B-lightgrey?style=flat-square" />
    <img alt="Safari" src="https://img.shields.io/badge/Safari-15%2B-0fb5ee?style=flat-square&logo=safari&logoColor=white" />
  </p>
</div>

---

## What it does

When you open a YouTube playlist, the player's autoplay toggle is automatically switched off — no button to press, no settings to configure. Every time YouTube tries to re-enable it during navigation, the extension silently flips it back.

**Before:** video ends → next video starts automatically  
**After:** video ends → playback stops

---

## Features

- **Automatic** — detects playlists and disables autoplay without any interaction
- **Persistent** — re-disables autoplay whenever YouTube turns it back on after SPA navigation
- **Zero config** — install once, forget about it
- **Lightweight** — one content script, no background network requests, no data collected
- **Open source** — fully auditable, MIT licensed

---

## Installation

> **Requirements:** macOS 12 Monterey or later · Safari 15 or later

### Option A — Download the app (recommended)

1. Download **`YT-Autoplay-Off.app.zip`** from the [Releases page](https://github.com/imsoumya18/yt-autoplay-off/releases/latest) and unzip it.
2. Move `YT Autoplay Off.app` to your **Applications** folder.
3. Open the app — it registers the extension with Safari.
4. In Safari, go to **Settings → Extensions** and enable **YT Autoplay Off**.
5. When prompted, choose **Always Allow on youtube.com**.

That's it. Open any YouTube playlist and autoplay is off.

<details>
<summary><b>Getting a "cannot be opened because the developer cannot be verified" warning?</b></summary>

Because this app is distributed outside the Mac App Store and without a paid Apple Developer certificate, macOS Gatekeeper will quarantine it. Remove the flag with these two commands:

```bash
xattr -cr ~/Applications/"YT Autoplay Off.app"
open ~/Applications/"YT Autoplay Off.app"
```

Alternatively, run the install script (Option B) which handles this automatically.

</details>

---

### Option B — Install script

Download the `.app` to your Downloads folder, then run:

```bash
curl -fsSL https://raw.githubusercontent.com/imsoumya18/yt-autoplay-off/main/install.sh | bash
```

The script removes the quarantine attribute, copies the app to `/Applications`, and opens it.

---

### Enabling unsigned extensions in Safari

Safari requires a one-time opt-in to allow extensions that aren't from the App Store:

1. Open **Safari → Settings → Advanced** and tick **Show features for web developers**.
2. Open **Safari → Develop → Allow Unsigned Extensions** (a checkmark appears).

> **Note:** This setting resets when Safari restarts. Re-enable it from the Develop menu if the extension stops working after a browser restart.

---

## How it works

The extension runs a single content script ([`Extension/content.js`](Extension/content.js)) on every `youtube.com` page.

```
YouTube page loads
       │
       ▼
Is a playlist URL? (list= param present)
       │ yes
       ▼
Wait for player to initialise (1–3 s)
       │
       ▼
Find autoplay toggle (.ytp-autonav-toggle-button)
       │
       ├─ aria-checked="true"  →  click to disable
       └─ aria-checked="false" →  already off, do nothing
       │
       ▼
MutationObserver watches for aria-checked changes
(re-disables immediately if YouTube turns it back on)
       │
       ▼
yt-navigate-finish / yt-page-data-updated events
(re-runs on every SPA navigation)
```

No data leaves your machine. The background service worker ([`Extension/background.js`](Extension/background.js)) does nothing beyond logging an install message.

---

## Project structure

```
yt-autoplay-off/
├── Extension/
│   ├── manifest.json       # MV3 extension manifest
│   ├── content.js          # core autoplay-disabling logic
│   ├── background.js       # minimal MV3 service worker
│   ├── popup.html          # toolbar popup UI
│   └── icons/              # extension icons (16, 32, 48, 128 px)
├── scripts/
│   └── generate_icons.py   # generates placeholder PNG icons
├── docs/
│   └── xcode-setup.md      # guide: build the .app in Xcode
├── install.sh              # convenience install script for users
├── .gitignore
└── README.md
```

---

## Building from source

See **[docs/xcode-setup.md](docs/xcode-setup.md)** for a complete step-by-step guide to:

- Creating the Safari Web Extension Xcode project
- Wiring in the extension files from this repo
- Archiving and exporting the `.app` for distribution

---

## Contributing

Contributions, bug reports, and feature requests are all welcome.

1. [Open an issue](https://github.com/imsoumya18/yt-autoplay-off/issues) to discuss what you'd like to change.
2. Fork the repository.
3. Create a branch: `git checkout -b fix/describe-the-fix`
4. Make your changes and test them in Safari.
5. Open a pull request.

Please keep pull requests focused — one fix or feature per PR.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Extension not listed in Safari settings | Re-open `YT Autoplay Off.app` to re-register it |
| Autoplay still happens | Check that **Develop → Allow Unsigned Extensions** is enabled |
| Extension disappears after Safari restart | Re-enable from **Safari → Develop → Allow Unsigned Extensions** |
| "Cannot be opened" on launch | Run `xattr -cr "/Applications/YT Autoplay Off.app"` in Terminal |

---

## License

[MIT](LICENSE) © [imsoumya18](https://github.com/imsoumya18)
