// YT Autoplay Off — background script
// All the real work happens in content.js. This script only logs on install.

browser.runtime.onInstalled.addListener(({ reason }) => {
    if (reason === 'install') {
        console.log('[YT Autoplay Off] Extension installed.');
    }
});
