/**
 * YT Autoplay Off — background service worker (Manifest V3)
 *
 * Minimal background script. All the real work happens in content.js.
 * This service worker exists to satisfy the MV3 requirement and to
 * log a message when the extension is first installed.
 */

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(clients.claim()));

chrome.runtime.onInstalled.addListener(({ reason }) => {
  if (reason === 'install') {
    console.log('[YT Autoplay Off] Extension installed.');
  }
});
