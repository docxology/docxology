# Research exploration design contract

The site's existing [design system](docs/design/design-system.md) and
[component previews](docs/design/components/README.md) remain authoritative.
This contract extends them for collections, research trails, the research map,
and the probability laboratory.

## Tokens and typography

Reuse `style.css`'s warm dark surfaces, neutral hairlines, red link/focus ink,
Inter/system body stack, Georgia display stack, and 3px radius. No new palette,
font download, framework, icon library, or animation runtime. Tool spacing is
0.5, 1, 1.5, 2, or 3rem; text uses the existing body scale and 0.875rem metadata.

## Layout and components

The document owns scrolling. A constrained editorial introduction precedes
labelled controls and the working area. Responsive grids use `minmax(0, 1fr)`;
at narrow widths they become one column. Long identifiers and titles wrap.
Collections use numbered reading-order rows, explicit move buttons, and a
neutral surface for selection. Trails use ordered steps with learning goals,
prerequisites and explicitly editorial time estimates. The map uses a bounded
SVG neighborhood plus an equivalent complete paginated list. The laboratory
uses native inputs, output text, SVG plots and downloadable numerical tables.

## Interaction and motion

Native buttons, selects and disclosure elements carry the behavior. Selection
uses text/checkmarks and a tonal background, never a decorative accent stripe.
Feedback stays beside its control in a polite live region. No automatic layout
animation, force simulation, hover-only action, or dragging requirement.
Reduced motion therefore preserves exactly the same information and controls.

## Accessibility and resilience

All inputs have visible labels; touch targets are at least 44px. Keyboard users
can select, save, reorder, remove, export and explore without a pointer.
Disabled storage, corrupt input, missing records and failed fetches have visible
recovery paths. Shared collections are previews until explicitly saved.
Unenhanced pages retain curated trail links, model definitions and examples,
map domain links, and a bibliography route. No credentials or visitor tracking.

## Performance and verification

Page-specific external modules and CSS load only where used. The collection
export and graph datasets are separate, generated projections. SVGs display
bounded neighborhoods; full graph coverage remains in the list and JSON.
Existing Lighthouse floors remain unchanged. Browser QA covers 320px, enlarged
text, keyboard use, forced colors, no JavaScript, malformed URLs/storage, export
bytes, numerical oracles, and back/forward navigation.

## References and accepted limits

This is an extension of the existing component system, not a new visual theme.
The map expresses catalog metadata relationships, not citations or causality.
The laboratory's binary update and reinforced urn are teaching models, not
validated accounts of cognition or ant behavior. Reading-list persistence is
device/browser-local; shared URLs contain the selected public citation keys
and list title. External resources retain their own availability constraints.
