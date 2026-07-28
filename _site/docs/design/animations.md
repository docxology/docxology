# Animation System

Added: 2026-07-05

## Philosophy

The site uses **micro-interactions** — subtle, purposeful animations that enhance usability without distracting. All animations respect `prefers-reduced-motion: reduce` (disabled entirely).

## Animation Types

### Entrance Animations
```css
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

Applied via `.animate` class (triggered by the IntersectionObserver in the external `js/interactive.js` runtime):
- Cards (`.card`, `.stat`, `.pub-item`, `.art-card`, `.connect-card`)
- Fade in with upward slide when scrolled into view (threshold: 8%)

### Hover Transitions
All interactive cards share a `.25s` transition on:
- `border-color` — shift from `var(--border)` to `var(--border-hover)` (red)
- `transform` — subtle `translateY(-2px)` elevation
- `box-shadow` — increased shadow for depth

### Interactive Components
| Component | Animation | Duration |
|-----------|-----------|----------|
| TTS Panel | Scale + fade entrance | 0.25s |
| TTS Toggle | Scale on hover | 0.25s |
| Scroll-to-top | Fade + translate | 0.25s |
| Shortcuts overlay | Backdrop blur + fade | 0.25s |
| Anchor links | Opacity on hover | 0.2s |
| Reading progress | Width via rAF | 0.1s linear |
| Search suggestions | Instant (display toggle) | — |

### Complex Animations (hero-glitch.js)
The hero section on `index.html` uses a canvas-based particle system:
- 150 particles sampled from 5 artwork images
- Gentle sine-wave oscillation on each particle
- DPR-aware rendering (capped at 1.65× for performance)
- 42 particles when reduced motion is preferred
- Resize handler recalculates positions

## Performance

- All scroll listeners use `{ passive: true }` for non-blocking scroll
- Progress bar updates use `requestAnimationFrame` throttling
- Canvas rendering uses `willReadFrequently: true` for sampled data
- Particle count caps at 150 for battery/mobile
- No animation on elements below the fold until IntersectionObserver triggers

## CSS Custom Properties as Animation Tokens

```css
--gold-glow: rgba(232,226,212,0.13);    /* Card glow on hover */
--red-glow: rgba(226,59,46,0.16);       /* TTS highlight */
```

## Adding New Animations

1. Define `@keyframes` in the animations section of `style.css`
2. Ensure the `prefers-reduced-motion` override disables it:
   ```css
   @media (prefers-reduced-motion: reduce) {
       .your-class { animation: none !important; transition: none !important; }
   }
   ```
3. Use `opacity` + `transform` properties for GPU-composited animations (avoid `left`, `top`, `width` for non-progress elements)
4. For entrance animations, use the existing `.animate` class with IntersectionObserver
