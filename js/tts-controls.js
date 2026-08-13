/**
 * TTS Controls — Web Speech API text-to-speech for danielarifriedman.com
 *
 * Features:
 * - Floating control panel (play/pause/stop/speed/voice)
 * - Auto-detects page content (main > section, article, .content)
 * - Respects prefers-reduced-motion
 * - Keyboard shortcut: "T" to toggle TTS panel
 * - Voices: prefers British English (UK) then US English, falls back to any
 * - Memory: persists voice & speed preference in sessionStorage
 * - ARIA live region for current utterance status
 *
 * Usage:
 *   <button class="tts-toggle" aria-label="Read aloud (T)">🔊</button>
 *   Add data-tts="skip" to elements to exclude from reading (nav, .filter-row, etc.)
 */

(function () {
  'use strict';

  // ── config ──
  const CFG = {
    storageKey: 'daf-tts-prefs',
    defaultSpeed: 0.95,
    defaultVoice: '',          // auto-detect
    autoScroll: true,
    paragraphBreak: 300,       // ms pause between paragraphs
  };

  // ── state ──
  const state = {
    synth: window.speechSynthesis,
    utterance: null,
    isPaused: false,
    isActive: false,
    paragraphs: [],
    currentIndex: 0,
    panelOpen: false,
    speaking: false,
  };

  // ── DOM refs (set on init) ──
  let panel, toggleBtn, playBtn, pauseBtn, stopBtn, statusEl, speedEl, voiceEl, progressEl;
  let reduceMotion = false;

  // ── detect reduced motion ──
  const rmq = window.matchMedia('(prefers-reduced-motion: reduce)');
  reduceMotion = rmq.matches;
  rmq.addEventListener('change', () => { reduceMotion = rmq.matches; });

  // ── helpers ──
  function qs(s, ctx) { return (ctx || document).querySelector(s); }
  function qsa(s, ctx) { return Array.from((ctx || document).querySelectorAll(s)); }

  function loadPrefs() {
    try {
      const raw = sessionStorage.getItem(CFG.storageKey);
      if (raw) return JSON.parse(raw);
    } catch (_) { /* ignore */ }
    return { speed: CFG.defaultSpeed, voice: CFG.defaultVoice };
  }

  function savePrefs(prefs) {
    try { sessionStorage.setItem(CFG.storageKey, JSON.stringify(prefs)); } catch (_) { /* ignore */ }
  }

  function getVoices() {
    const all = state.synth.getVoices();
    // prefer British English, then US English, then any English, then any
    const uk = all.find(v => v.lang && v.lang.startsWith('en-GB') && v.localService);
    const us = all.find(v => v.lang && v.lang.startsWith('en-US') && v.localService);
    const anyEn = all.find(v => v.lang && v.lang.startsWith('en'));
    const any = all.find(v => v.lang);
    return uk || us || anyEn || any || all[0] || null;
  }

  function findVoice(name) {
    const all = state.synth.getVoices();
    return all.find(v => v.name === name) || getVoices();
  }

  // ── collect paragraphs ──
  function collectParagraphs() {
    const main = document.querySelector('main') || document.body;
    const textNodes = [];

    // Walk all text-bearing elements, skip [data-tts="skip"] and hidden items
    const candidates = qsa('p, h1, h2, h3, h4, h5, h6, li, td, th, .pub-item .title, .about-text p, .media-item, .art-highlight, .card p, .sidebar-card li', main);

    candidates.forEach(el => {
      // skip elements marked skip or inside skip parents
      if (el.closest('[data-tts="skip"], nav, .filter-row, .media-tabs, table thead, .footer-links, .profile-links')) return;
      const text = el.textContent.trim();
      if (text.length < 15) return; // skip very short fragments
      // skip boilerplate
      if (/^(Skip to|Toggle menu|©|\d+\s+copies)/.test(text)) return;
      const tag = el.tagName.toLowerCase();
      const prefix = (tag.match(/^h[1-6]$/) ? tag.toUpperCase() + ': ' : '');
      textNodes.push(prefix + text);
    });

    return textNodes;
  }

  // ── speak ──
  function speakParagraphs(paragraphs, startIndex) {
    if (!paragraphs || paragraphs.length === 0) {
      setStatus('No readable content found on this page.');
      return;
    }

    state.paragraphs = paragraphs;
    state.currentIndex = startIndex || 0;
    state.speaking = true;
    speakNext();
  }

  function speakNext() {
    if (state.currentIndex >= state.paragraphs.length) {
      finish();
      return;
    }

    const text = state.paragraphs[state.currentIndex];
    const prefs = loadPrefs();
    const voice = findVoice(prefs.voice);

    const utter = new SpeechSynthesisUtterance(text);
    utter.voice = voice;
    utter.rate = prefs.speed;
    utter.pitch = 1.0;
    utter.volume = 1.0;

    utter.onstart = () => {
      setStatus(`Reading paragraph ${state.currentIndex + 1} of ${state.paragraphs.length}…`);
      highlightParagraph(state.currentIndex);
      if (CFG.autoScroll) scrollToCurrent();
      updateProgress();
    };

    utter.onend = () => {
      state.currentIndex++;
      if (state.currentIndex < state.paragraphs.length) {
        setTimeout(() => speakNext(), CFG.paragraphBreak);
      } else {
        finish();
      }
    };

    utter.onerror = (e) => {
      if (e.error !== 'canceled' && e.error !== 'interrupted') {
        console.warn('TTS error:', e.error);
        setStatus('Speech error — ' + e.error);
      }
      // Don't crash on cancellations
      if (e.error === 'canceled' || e.error === 'interrupted') {
        state.speaking = false;
      }
    };

    state.utterance = utter;
    state.synth.speak(utter);
  }

  function highlightParagraph(index) {
    // Remove previous highlight
    qsa('.tts-highlight').forEach(el => el.classList.remove('tts-highlight'));
    // Find and highlight current paragraph
    // We use the original candidate elements
    const candidates = qsa('p, h1, h2, h3, h4, h5, h6, li, td, th, .pub-item .title, .about-text p, .media-item, .art-highlight, .card p, .sidebar-card li', document.querySelector('main') || document.body);
    let count = 0;
    for (const el of candidates) {
      if (el.closest('[data-tts="skip"], nav, .filter-row, .media-tabs, table thead, .footer-links, .profile-links')) continue;
      const text = el.textContent.trim();
      if (text.length < 15) continue;
      if (/^(Skip to|Toggle menu|©|\d+\s+copies)/.test(text)) continue;
      if (count === index) {
        el.classList.add('tts-highlight');
        el.scrollIntoView({ behavior: reduceMotion ? 'instant' : 'smooth', block: 'center' });
        return;
      }
      count++;
    }
  }

  function scrollToCurrent() {
    const active = qs('.tts-highlight');
    if (active) {
      active.scrollIntoView({ behavior: reduceMotion ? 'instant' : 'smooth', block: 'center' });
    }
  }

  function updateProgress() {
    if (progressEl && state.paragraphs.length > 0) {
      progressEl.style.width = ((state.currentIndex / state.paragraphs.length) * 100) + '%';
    }
  }

  function finish() {
    state.speaking = false;
    state.isPaused = false;
    state.currentIndex = 0;
    setStatus('Finished reading');
    qsa('.tts-highlight').forEach(el => el.classList.remove('tts-highlight'));
    if (progressEl) progressEl.style.width = '0%';
    updateButtons();
  }

  function pauseTTS() {
    if (state.synth.speaking && !state.synth.paused) {
      state.synth.pause();
      state.isPaused = true;
      setStatus('Paused');
      updateButtons();
    }
  }

  function resumeTTS() {
    if (state.synth.paused) {
      state.synth.resume();
      state.isPaused = false;
      setStatus('Resumed');
      updateButtons();
    }
  }

  function stopTTS() {
    if (state.synth.speaking) {
      state.synth.cancel();
    }
    state.speaking = false;
    state.isPaused = false;
    state.currentIndex = 0;
    qsa('.tts-highlight').forEach(el => el.classList.remove('tts-highlight'));
    if (progressEl) progressEl.style.width = '0%';
    setStatus('Stopped');
    updateButtons();
  }

  function togglePlayPause() {
    if (state.speaking) {
      if (state.isPaused) {
        resumeTTS();
      } else {
        pauseTTS();
      }
    } else {
      // Start fresh
      state.paragraphs = collectParagraphs();
      speakParagraphs(state.paragraphs, 0);
    }
    updateButtons();
  }

  // ── UI ──
  function setStatus(msg) {
    if (statusEl) statusEl.textContent = msg;
  }

  function updateButtons() {
    if (!playBtn || !pauseBtn || !stopBtn) return;
    if (state.speaking && !state.isPaused) {
      playBtn.style.display = 'none';
      pauseBtn.style.display = 'inline-flex';
      stopBtn.style.display = 'inline-flex';
    } else if (state.isPaused) {
      playBtn.style.display = 'inline-flex';
      playBtn.textContent = '▶';
      playBtn.setAttribute('aria-label', 'Resume');
      pauseBtn.style.display = 'none';
      stopBtn.style.display = 'inline-flex';
    } else {
      playBtn.style.display = 'inline-flex';
      playBtn.textContent = '▶';
      playBtn.setAttribute('aria-label', 'Read aloud');
      pauseBtn.style.display = 'none';
      stopBtn.style.display = 'none';
    }
  }

  function togglePanel() {
    state.panelOpen = !state.panelOpen;
    panel.classList.toggle('tts-open', state.panelOpen);
    panel.setAttribute('aria-hidden', String(!state.panelOpen));
    if (toggleBtn) {
      toggleBtn.setAttribute('aria-expanded', String(state.panelOpen));
    }
    if (state.panelOpen && voiceEl) {
      populateVoiceList(voiceEl);
    }
  }

  function populateVoiceList(select) {
    // Preserve current selection
    const currentVal = select.value;
    const currentPrefs = loadPrefs();
    select.innerHTML = '';
    const voices = state.synth.getVoices();
    const seen = new Set();
    voices.forEach(v => {
      // deduplicate by name
      if (seen.has(v.name)) return;
      seen.add(v.name);
      const opt = document.createElement('option');
      opt.value = v.name;
      opt.textContent = v.name + (v.lang ? ` (${v.lang})` : '');
      select.appendChild(opt);
    });
    // restore selection
    if (currentVal && [...select.options].some(o => o.value === currentVal)) {
      select.value = currentVal;
    } else if (currentPrefs.voice) {
      select.value = currentPrefs.voice;
    }
  }

  // ── build panel ──
  function createPanel() {
    if (qs('#tts-panel')) return qs('#tts-panel');

    panel = document.createElement('div');
    panel.id = 'tts-panel';
    panel.className = 'tts-panel';
    panel.setAttribute('role', 'region');
    panel.setAttribute('aria-label', 'Text to speech controls');
    panel.setAttribute('aria-hidden', 'true');

    panel.innerHTML = `
      <div class="tts-header">
        <span class="tts-title">Read Aloud</span>
        <button class="tts-close" aria-label="Close text-to-speech panel">&times;</button>
      </div>
      <div class="tts-body">
        <div class="tts-row">
          <button class="tts-btn tts-play" aria-label="Read aloud">▶</button>
          <button class="tts-btn tts-pause" aria-label="Pause" style="display:none">⏸</button>
          <button class="tts-btn tts-stop" aria-label="Stop" style="display:none">⏹</button>
        </div>
        <div class="tts-row">
          <label class="tts-label">
            Speed
            <input type="range" class="tts-speed" min="0.3" max="2.0" step="0.05" value="0.95"
                   aria-label="Reading speed">
            <span class="tts-speed-val">0.95×</span>
          </label>
        </div>
        <div class="tts-row">
          <label class="tts-label">
            Voice
            <select class="tts-voice" aria-label="Voice selection"></select>
          </label>
        </div>
        <div class="tts-row tts-auto-label">
          <label>
            <input type="checkbox" class="tts-autoscroll" checked>
            Auto-scroll
          </label>
        </div>
        <div class="tts-progress-track">
          <div class="tts-progress-bar" style="width:0%"></div>
        </div>
        <div class="tts-status" aria-live="polite" aria-atomic="true">Ready</div>
      </div>
    `;

    document.body.appendChild(panel);

    // cache refs
    playBtn = qs('.tts-play', panel);
    pauseBtn = qs('.tts-pause', panel);
    stopBtn = qs('.tts-stop', panel);
    statusEl = qs('.tts-status', panel);
    speedEl = qs('.tts-speed', panel);
    voiceEl = qs('.tts-voice', panel);
    progressEl = qs('.tts-progress-bar', panel);

    // close button
    qs('.tts-close', panel).addEventListener('click', () => {
      togglePanel();
    });

    // play/pause
    playBtn.addEventListener('click', togglePlayPause);
    pauseBtn.addEventListener('click', togglePlayPause);
    stopBtn.addEventListener('click', stopTTS);

    // speed
    const prefs = loadPrefs();
    speedEl.value = prefs.speed;
    qs('.tts-speed-val').textContent = prefs.speed.toFixed(2) + '×';

    speedEl.addEventListener('input', function () {
      const val = parseFloat(this.value);
      qs('.tts-speed-val').textContent = val.toFixed(2) + '×';
      savePrefs({ ...loadPrefs(), speed: val });
      // If currently speaking, restart current paragraph with new speed
      if (state.speaking && state.utterance) {
        const idx = state.currentIndex;
        state.synth.cancel();
        // slight delay to let cancel propagate
        setTimeout(() => speakNext(), 50);
      }
    });

    // voice
    voiceEl.addEventListener('change', function () {
      savePrefs({ ...loadPrefs(), voice: this.value });
    });

    // autoscroll
    const autoCb = qs('.tts-autoscroll', panel);
    autoCb.addEventListener('change', function () {
      CFG.autoScroll = this.checked;
    });

    // Keyboard: Escape closes panel
    panel.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        e.preventDefault();
        if (state.panelOpen) togglePanel();
      }
    });

    return panel;
  }

  // ── create toggle button ──
  function createToggle() {
    if (qs('.tts-toggle')) return qs('.tts-toggle');

    toggleBtn = document.createElement('button');
    toggleBtn.className = 'tts-toggle';
    toggleBtn.setAttribute('aria-label', 'Open text-to-speech controls (T)');
    toggleBtn.setAttribute('aria-expanded', 'false');
    toggleBtn.setAttribute('title', 'Read aloud (T)');
    toggleBtn.innerHTML = '<span class="tts-toggle-icon">🔊</span>';
    toggleBtn.addEventListener('click', togglePanel);
    document.body.appendChild(toggleBtn);
    return toggleBtn;
  }

  // ── global keyboard shortcut ──
  function handleKeydown(e) {
    // Don't fire when user is typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
    if (e.key === 't' || e.key === 'T') {
      e.preventDefault();
      if (!panel) panel = createPanel();
      if (!toggleBtn) toggleBtn = createToggle();
      togglePanel();
    }
  }

  // ── public API for other scripts ──
  window.__tts = {
    toggle: () => { togglePanel(); },
    speak: (text) => {
      if (typeof text === 'string') {
        stopTTS();
        const paragraphs = text.split('\n').filter(p => p.trim().length > 20);
        speakParagraphs(paragraphs, 0);
      } else {
        stopTTS();
        state.paragraphs = collectParagraphs();
        speakParagraphs(state.paragraphs, 0);
      }
    },
    stop: stopTTS,
    pause: pauseTTS,
    resume: resumeTTS,
  };

  // ── init ──
  function init() {
    if (typeof speechSynthesis === 'undefined') return; // no TTS support

    panel = createPanel();
    toggleBtn = createToggle();

    // Populate voices once loaded (Chrome loads async)
    if (state.synth.getVoices().length > 0) {
      populateVoiceList(voiceEl);
    }
    state.synth.addEventListener('voiceschanged', () => {
      if (voiceEl) populateVoiceList(voiceEl);
    }, { once: false });

    document.addEventListener('keydown', handleKeydown);

    // If URL has ?tts or #tts, auto-open
    if (window.location.search.includes('tts') || window.location.hash === '#tts') {
      setTimeout(() => togglePanel(), 500);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();