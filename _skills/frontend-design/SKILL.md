---
name: frontend-design
description: Aesthetic direction for the content-engine HTML deliverable. Use at stage 04-render to keep the rendered HTML looking intentional and polished rather than generic-AI. Advisory only; the deterministic markup lives in render-doc.
---

# frontend-design (pointer)

Advisory aesthetic layer for the HTML target. The deterministic markup and CSS
live in `../render-doc/render.py` + the inline theme; this skill is the 10%
judgment that keeps the result from looking like generic AI output.

House rule: zero em dash characters.

## Aim

- **Restraint over spectacle.** One accent color, generous whitespace, a clear
  type hierarchy, ~150ms transitions only. No gradients-everywhere, no neon, no
  drop-shadow soup, no hero-illustration filler.
- **Read like a real document, not a web page.** The deliverable is a guide or
  procedure someone will follow. Legibility and scan-ability win over flourish.
- **Brand tokens drive the look.** Colors and fonts come from
  `_config/design-system.md` via theme-factory (CSS variables), not hardcoded
  here. Changing the brand should re-skin the doc with no markup change.
- **Avoid the generic-AI tells:** centered everything, emoji bullets, purple
  gradient headers, rounded-everything, "✨ Features ✨" energy. The bundled
  `frontend-design` Claude skill carries the full do/avoid guidance; consult it
  when styling.

## Where it applies

Stage 04-render only. It informs the CSS variable values and any layout tuning;
it does not change the doc-model or the renderer's structure.
