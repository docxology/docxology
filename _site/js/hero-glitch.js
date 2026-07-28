const canvas = document.querySelector(".hero-glitch-canvas");

if (canvas) {
  const hero = canvas.closest(".hero");
  const ctx = canvas.getContext("2d", { alpha: false, willReadFrequently: true });
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const sources = [
    "assets/hero-art/ant-head.webp",
    "assets/hero-art/decentral-antelligence-agency.webp",
    "assets/hero-art/an-ant-is-a-colony.webp",
    "assets/hero-art/mesh-network.webp",
    "assets/hero-art/army-ants.webp",
  ];

  const state = {
    width: 1,
    height: 1,
    dpr: 1,
    active: 0,
    renderedActive: -1,
    visible: true,
    boostUntil: 0,
    pointer: { x: 0, y: 0, target: 0, value: 0 },
    particles: [],
  };

  const images = await Promise.all(
    sources.map(
      (src) =>
        new Promise((resolve) => {
          const img = new Image();
          img.decoding = "async";
          img.onload = () => resolve(img);
          img.onerror = () => resolve(null);
          img.src = src;
        }),
    ),
  ).then((loaded) => loaded.filter(Boolean));

  if (images.length > 0 && ctx && hero) {
    const sampleCanvas = document.createElement("canvas");
    const sampleCtx = sampleCanvas.getContext("2d", { willReadFrequently: true });
    const sampleSize = { width: 120, height: 76 };
    sampleCanvas.width = sampleSize.width;
    sampleCanvas.height = sampleSize.height;

    function coverRect(img, width, height, scaleBoost = 1) {
      const scale = Math.max(width / img.naturalWidth, height / img.naturalHeight) * scaleBoost;
      const drawWidth = img.naturalWidth * scale;
      const drawHeight = img.naturalHeight * scale;
      return {
        x: (width - drawWidth) / 2,
        y: (height - drawHeight) / 2,
        width: drawWidth,
        height: drawHeight,
      };
    }

    function resize() {
      const rect = hero.getBoundingClientRect();
      state.dpr = Math.min(window.devicePixelRatio || 1, 1.65);
      state.width = Math.max(1, Math.floor(rect.width * state.dpr));
      state.height = Math.max(1, Math.floor(rect.height * state.dpr));
      canvas.width = state.width;
      canvas.height = state.height;
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `${rect.height}px`;
      state.renderedActive = -1;
      sampleParticles(images[state.active]);
    }

    function sampleParticles(img) {
      if (!sampleCtx || !img) return;
      sampleCtx.clearRect(0, 0, sampleSize.width, sampleSize.height);
      sampleCtx.fillStyle = "#fff";
      sampleCtx.fillRect(0, 0, sampleSize.width, sampleSize.height);
      const rect = coverRect(img, sampleSize.width, sampleSize.height, 1.04);
      sampleCtx.filter = "grayscale(1) contrast(1.45)";
      sampleCtx.drawImage(img, rect.x, rect.y, rect.width, rect.height);
      sampleCtx.filter = "none";

      const data = sampleCtx.getImageData(0, 0, sampleSize.width, sampleSize.height).data;
      const candidates = [];
      for (let y = 0; y < sampleSize.height; y += 2) {
        for (let x = 0; x < sampleSize.width; x += 2) {
          const i = (y * sampleSize.width + x) * 4;
          const lum = data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114;
          if (lum < 115) candidates.push({ x: x / sampleSize.width, y: y / sampleSize.height, lum });
        }
      }

      state.particles = candidates
        .sort(() => Math.random() - 0.5)
        .slice(0, reduceMotion.matches ? 42 : 150)
        .map((point, index) => ({
          x: point.x * state.width,
          y: point.y * state.height,
          phase: Math.random() * Math.PI * 2,
          speed: 0.00035 + Math.random() * 0.00065,
          size: (point.lum < 45 ? 1.55 : 1) * state.dpr,
          red: index % 5 === 0,
        }));
    }

    function drawImageBands(img, time, intensity) {
      const rect = coverRect(img, state.width, state.height, reduceMotion.matches ? 1.02 : 1.1);
      const driftX = state.pointer.x * (24 + intensity * 20) * state.dpr;
      const driftY = state.pointer.y * (18 + intensity * 14) * state.dpr;
      const bandHeight = reduceMotion.matches ? 28 * state.dpr : 8 * state.dpr;

      ctx.save();
      ctx.filter = `grayscale(1) contrast(${1.42 + intensity * 0.35}) brightness(${0.46 + intensity * 0.07})`;
      for (let y = 0; y < state.height; y += bandHeight) {
        const wave = Math.sin(y * 0.018 + time * 0.0032) * (5 + intensity * 14) * state.dpr;
        ctx.save();
        ctx.beginPath();
        ctx.rect(0, y, state.width, bandHeight + 1);
        ctx.clip();
        ctx.drawImage(img, rect.x + driftX + wave, rect.y + driftY, rect.width, rect.height);
        ctx.restore();
      }
      ctx.restore();
    }

    function drawRedGhost(img, time, intensity) {
      if (reduceMotion.matches) return;
      const rect = coverRect(img, state.width, state.height, 1.1);
      const bands = 5 + Math.floor(intensity * 4);
      for (let i = 0; i < bands; i += 1) {
        const y = (time * (0.045 + i * 0.008) + i * state.height * 0.19) % state.height;
        const h = (6 + ((i * 7) % 24) + intensity * 20) * state.dpr;
        const shift = (Math.sin(time * 0.006 + i) * 22 + 16 + intensity * 34) * state.dpr;
        ctx.save();
        ctx.beginPath();
        ctx.rect(0, y, state.width, h);
        ctx.clip();
        ctx.filter = "grayscale(1) contrast(2.2) brightness(0.85)";
        ctx.drawImage(img, rect.x + shift, rect.y, rect.width, rect.height);
        ctx.globalCompositeOperation = "source-atop";
        ctx.fillStyle = `rgba(255,0,0,${0.18 + intensity * 0.2})`;
        ctx.fillRect(0, y, state.width, h);
        ctx.restore();
      }
    }

    function drawPixelSort(time, intensity) {
      if (reduceMotion.matches) return;
      const bands = 4 + Math.floor(intensity * 5);
      for (let i = 0; i < bands; i += 1) {
        const y = Math.floor((time * (0.028 + i * 0.005) + i * 151 * state.dpr) % state.height);
        const h = Math.max(3, Math.floor((4 + ((i * 5) % 18)) * state.dpr));
        const shift = Math.floor((Math.sin(time * 0.012 + i * 2.1) * 36 + intensity * 54) * state.dpr);
        ctx.save();
        ctx.globalAlpha = 0.34 + intensity * 0.22;
        ctx.drawImage(canvas, 0, y, state.width, h, shift, y, state.width, h);
        ctx.globalAlpha = 0.16 + intensity * 0.18;
        ctx.fillStyle = "#ff0000";
        ctx.fillRect(0, y, state.width, Math.max(1, state.dpr));
        ctx.restore();
      }
    }

    function drawParticles(time, intensity) {
      if (!state.particles.length) return;
      ctx.save();
      ctx.globalCompositeOperation = "screen";
      for (const point of state.particles) {
        const wander = reduceMotion.matches ? 0 : Math.sin(time * point.speed + point.phase) * (6 + intensity * 12) * state.dpr;
        const x = point.x + wander + state.pointer.x * 10 * state.dpr;
        const y = point.y + Math.cos(time * point.speed + point.phase) * (2 + intensity * 5) * state.dpr;
        ctx.fillStyle = point.red ? "rgba(255,0,0,0.72)" : "rgba(255,255,255,0.28)";
        ctx.fillRect(x, y, point.size, point.size);
      }
      ctx.restore();
    }

    function drawFrame(time) {
      const cycleMs = reduceMotion.matches ? 18000 : 7600;
      const nextActive = Math.floor(time / cycleMs) % images.length;
      if (nextActive !== state.active) {
        state.active = nextActive;
        state.boostUntil = time + 900;
        sampleParticles(images[state.active]);
      }

      const boost = time < state.boostUntil ? 1 : 0;
      state.pointer.value += (state.pointer.target - state.pointer.value) * 0.075;
      const cyclePhase = (time % cycleMs) / cycleMs;
      const transitionPulse = cyclePhase > 0.9 ? (cyclePhase - 0.9) * 10 : 0;
      const intensity = reduceMotion.matches ? 0 : Math.min(1, state.pointer.value + boost * 0.7 + transitionPulse * 0.55);

      ctx.fillStyle = "#000";
      ctx.fillRect(0, 0, state.width, state.height);
      drawImageBands(images[state.active], time, intensity);
      drawPixelSort(time, intensity);
      drawRedGhost(images[state.active], time, intensity);
      drawParticles(time, intensity);

      if (!reduceMotion.matches && transitionPulse > 0.74) {
        ctx.save();
        ctx.globalAlpha = Math.min(0.16, (transitionPulse - 0.74) * 0.42);
        ctx.fillStyle = "#ff0000";
        ctx.fillRect(0, 0, state.width, state.height);
        ctx.restore();
      }

      ctx.save();
      const vignette = ctx.createRadialGradient(
        state.width / 2,
        state.height * 0.43,
        state.width * 0.08,
        state.width / 2,
        state.height * 0.44,
        state.width * 0.72,
      );
      vignette.addColorStop(0, "rgba(0,0,0,0.08)");
      vignette.addColorStop(0.54, "rgba(0,0,0,0.34)");
      vignette.addColorStop(1, "rgba(0,0,0,0.86)");
      ctx.fillStyle = vignette;
      ctx.fillRect(0, 0, state.width, state.height);
      ctx.restore();

      state.renderedActive = state.active;
    }

    function loop(time) {
      if (state.visible && !document.hidden) {
        drawFrame(time);
      }
      window.setTimeout(
        () => window.requestAnimationFrame(loop),
        reduceMotion.matches ? 700 : 0,
      );
    }

    hero.addEventListener("pointermove", (event) => {
      if (reduceMotion.matches) return;
      const rect = hero.getBoundingClientRect();
      state.pointer.x = (event.clientX - rect.left) / rect.width - 0.5;
      state.pointer.y = (event.clientY - rect.top) / rect.height - 0.5;
      state.pointer.target = 0.45;
    });

    hero.addEventListener("pointerleave", () => {
      state.pointer.target = 0;
    });

    hero.querySelectorAll("a").forEach((link) => {
      link.addEventListener("pointerenter", () => {
        state.boostUntil = performance.now() + 700;
      });
      link.addEventListener("focus", () => {
        state.boostUntil = performance.now() + 700;
      });
    });

    reduceMotion.addEventListener("change", () => {
      state.renderedActive = -1;
      sampleParticles(images[state.active]);
    });

    const observer = new IntersectionObserver(([entry]) => {
      state.visible = Boolean(entry?.isIntersecting);
    });
    observer.observe(hero);

    window.addEventListener("resize", resize, { passive: true });
    resize();
    window.requestAnimationFrame(loop);
  }
}
