---
name: theme-factory
description: Turn the content-engine brand tokens in _config/design-system.md into the CSS variable block render-doc consumes (colors, fonts, scale). Use at stage 04-render so HTML and PDF share one brand source. The brand changes in one place and both targets re-skin.
---

# theme-factory (pointer)

Maps `_config/design-system.md` brand tokens to the `--ce-*` CSS custom
properties `render-doc` reads. One brand source, both targets (HTML + PDF)
re-skin together.

House rule: zero em dash characters.

## Aim

`render.py`'s default theme defines a `:root` block of CSS variables:

```
--ce-primary  --ce-accent  --ce-bg  --ce-text  --ce-muted  --ce-line
--ce-callout-tip  --ce-callout-warn  --ce-callout-note  --ce-callout-prereq
--ce-heading-font  --ce-body-font
```

theme-factory's job at 04-render is to produce the values for those variables
from `_config/design-system.md` (palette + typography), then pass the override
CSS into `build_html(css=...)` (or edit the `:root` block). Nothing else in the
renderer needs to change: the markup is brand-agnostic and reads only variables.

## Single-source discipline

- Brand FACTS live once in `_config/design-system.md` (Pattern 3).
- The variable NAMES live once in `render.py`'s `:root`.
- theme-factory is the bridge; it does not restate the palette or invent tokens
  the renderer does not read.

The bundled `theme-factory` Claude skill carries the palette/scale generation
method; use it when authoring `_config/design-system.md` at setup.
