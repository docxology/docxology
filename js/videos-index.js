/* videos/index.html progressive disclosure (CSP: script-src 'self').
 *
 * The generator server-renders the newest VIDEO_SSR_FLOOR_ROWS rows into
 * <ol class="video-list"> and emits the remaining rows as a compact
 * application/json payload (#video-tail-payload: [{u,t,m}, ...]).  This script
 * renders those rows into the existing list on demand ("Show more"), so the
 * raw-HTML floor stays small while every video page stays reachable from the
 * hub client-side.  The full crawlable inventory is the inline ItemList
 * JSON-LD (one itemListElement per video) plus data/videos.json; video page
 * URLs are unchanged.  Without JS, the noscript note points at the JSON and
 * the structured data.
 */
(function () {
    'use strict';

    var BATCH_SIZE = 100;
    var payloadEl = document.getElementById('video-tail-payload');
    var list = document.querySelector('ol.video-list');
    if (!payloadEl || !list) return;

    var tail;
    try {
        tail = JSON.parse(payloadEl.textContent);
    } catch (err) {
        console.error('video index: tail payload unreadable', err);
        return;
    }
    if (!Array.isArray(tail) || tail.length === 0) return;

    var nextIndex = 0;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'video-show-more';
    btn.className = 'btn btn-outline';

    function remaining() {
        return tail.length - nextIndex;
    }

    function updateLabel() {
        if (nextIndex >= tail.length) {
            btn.hidden = true;
            return;
        }
        btn.textContent = 'Show more (' + remaining() + ' of ' + tail.length + ' remaining)';
    }

    function esc(value) {
        return String(value == null ? '' : value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function appendBatch() {
        var end = Math.min(nextIndex + BATCH_SIZE, tail.length);
        var html = '';
        for (var i = nextIndex; i < end; i++) {
            var item = tail[i];
            html += '<li><a href="' + esc(item.u) + '">' + esc(item.t) + '</a>' +
                '<span class="muted"> - ' + esc(item.m) + '</span></li>';
        }
        list.insertAdjacentHTML('beforeend', html);
        nextIndex = end;
        updateLabel();
    }

    btn.addEventListener('click', appendBatch);
    list.parentNode.insertBefore(btn, list.nextSibling);
    appendBatch();
})();
