# Animation system

Animations support navigation, feedback, and visual continuity. Keep essential content and native links available when animation or JavaScript is unavailable. Source owners are [style.css](../../style.css), [index-page.js](../../js/index-page.js), [interactive.js](../../js/interactive.js), and the optional [hero-glitch.js](../../js/hero-glitch.js).

## Motion preferences

Shared CSS reduces animation/transition durations and disables smooth scrolling for `prefers-reduced-motion: reduce`. Interactive widgets additionally disable their transitions. The homepage entrance observer is created only when reduced motion is not requested; it does not hide content awaiting animation.

The optional canvas runtime observes changes to the motion preference. A reduced-motion visit loads one source image, draws a static frame, and schedules no animation loop. A later change back to motion can fetch the remaining source images once and resume the visible effect.

## Entrance and interaction effects

[index-page.js](../../js/index-page.js) adds `.animate` to homepage cards, stats, publication items, art cards, and contact cards when its IntersectionObserver reaches an 8% threshold. The shared `.animate` rule uses `fadeUp`; stats override it with `slideUp`. This entrance behavior belongs to the homepage module rather than the shared interactive runtime.

Hover transitions use the actual component rules in `style.css`; keep keyboard focus visible independently of hover. Speech and shortcut panels, scroll-to-top controls, anchor links, and reading progress use their scoped transitions. The reading-progress calculation is clamped to 0–100, updates in a requested animation frame, and lives within the main landmark. Search suggestion visibility changes immediately.

## Optional canvas effect

`hero-glitch.js` activates only when a `.hero-glitch-canvas` exists. The current [homepage](../../index.html) includes neither that canvas nor the module, so changes to this optional runtime do not establish a homepage performance improvement.

For pages that opt in, the runtime samples the declared artwork sources, caps normal-motion particles at 150, and caps device-pixel ratio at 1.65. Reduced motion uses a static image without particles, pointer drift, or source cycling. Animation frames pause when the hero leaves the viewport or the document becomes hidden, then resume when visible and motion is permitted. The resize handler recalculates the canvas and draws the appropriate frame.

This is a source contract, not a battery-use or frame-rate measurement. Validate it in a browser before adding it to a page.

## Adding or changing effects

1. Locate the owning CSS rule or external module and preserve native content and focus behavior.
2. Use opacity/transform for decorative movement where appropriate; reserve layout updates for components whose behavior requires them.
3. Respect reduced motion at initial load and, for long-running effects, when the preference changes.
4. Stop ongoing animation when its surface is offscreen or the document is hidden.
5. Run the declared [browser acceptance](../operations/site-runtime.md) and inspect responsive/forced-colors states under the [QA procedure](../operations/accessibility-qa.md).

CSS tokens and component contracts are documented in [design-system.md](design-system.md). Read current values from source rather than copying cache tags or timing constants into a new module.
