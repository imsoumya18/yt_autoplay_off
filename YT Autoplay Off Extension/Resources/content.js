/**
 * YT Autoplay Off — content script
 *
 * Runs on every youtube.com page. When a playlist is detected (the `list`
 * query parameter is present), it finds the autonav toggle and turns it off.
 * A MutationObserver keeps it off across YouTube's SPA navigations.
 */
(function () {
    'use strict';

    // YouTube occasionally changes class names; try these in order.
    const AUTOPLAY_SELECTORS = [
        '.ytp-autonav-toggle-button',
        '[class*="autonav-toggle-button"]',
        'button[aria-checked][class*="autonav"]',
    ];

    function isPlaylistPage() {
        return new URLSearchParams(window.location.search).has('list');
    }

    function findAutoplayButton() {
        for (const selector of AUTOPLAY_SELECTORS) {
            const el = document.querySelector(selector);
            if (el) return el;
        }
        return null;
    }

    function disableAutoplay() {
        if (!isPlaylistPage()) return;

        const button = findAutoplayButton();
        if (!button) return;

        if (button.getAttribute('aria-checked') === 'true') {
            button.click();
        }
    }

    function debounce(fn, delay) {
        let timer;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }

    const debouncedDisable = debounce(disableAutoplay, 400);

    // Watch for aria-checked changes — YouTube re-enables autoplay after some
    // SPA navigations, so we intercept and immediately flip it back.
    const observer = new MutationObserver(debouncedDisable);
    observer.observe(document.documentElement, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['aria-checked'],
    });

    // YouTube-specific navigation events (fired on SPA route changes).
    window.addEventListener('yt-navigate-finish', disableAutoplay);
    window.addEventListener('yt-page-data-updated', disableAutoplay);

    // Give the player time to paint on initial load.
    setTimeout(disableAutoplay, 1500);
    setTimeout(disableAutoplay, 3000); // retry for slow connections
})();
