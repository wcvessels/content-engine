# frame-crop: the screenshot crop-decision rule (D6)

Canonical home for the screenshot cropping policy. Both lanes' `03-layout`
reference THIS file; nothing else restates the rule. `render.py` applies the
result deterministically. `05-qa` checks it.

House rule: zero em dash characters.

---

## Division of labor (fixed)

| Stage | Role | What it does |
|---|---|---|
| 03-layout | DECIDES (the 10% AI judgment) | runs a vision step, sets `crop` + `crop_reason` on each `screenshot` block |
| 04-render | APPLIES (the 60% deterministic) | `render.py` Pillow-crops the normalized box BEFORE downscale + base64; the original frame is never modified |
| 05-qa | CHECKS | crop improved focus and clipped no needed context |

The crop is OPTIONAL end to end. Default `null` = full frame. The whole step
can be skipped under time pressure with zero render breakage.

---

## The rule (use this exact policy in 03-layout)

When placing each screenshot, look at the frame and decide whether to trim it.

1. **Identify the relevant content region.** This is the shared screen, slide,
   app window, document, terminal, or whiteboard the speaker is demonstrating.
   It is the thing the reader needs to see to follow the step.

2. **Look for a separable webcam tile or participant gallery.** Video-call
   recordings often overlay a presenter's webcam or a row of participant
   thumbnails in a corner or along an edge. These are noise for a how-to doc.

3. **Crop ONLY when removing the tile cuts nothing relevant.** If the webcam
   tile or participant gallery sits in a separable region (a corner, a side
   band, a top/bottom strip) that can be removed WITHOUT clipping any part of
   the content region, output the content box. Otherwise output `null`.

4. **When unsure, keep the full frame.** A full frame is always safe. A crop
   that clips real content is a defect (it can hide a button, a value, or a
   menu the reader needs). Bias toward `null`.

Never crop to "zoom in" on a detail, never crop purely for aesthetics, never
crop a frame that has no webcam/participant tile. The only justification for a
non-null crop is removing a separable webcam/participant region.

---

## The output shape

03-layout writes these two fields on the `screenshot` block (schema in
`_standards/doc-model-schema.md` section 4.2):

```json
{
  "type": "screenshot",
  "frame_index": 14,
  "caption": "...",
  "crop": { "x": 0.0, "y": 0.0, "w": 0.78, "h": 1.0 },
  "crop_reason": "Removed the presenter webcam strip on the right; content box kept whole."
}
```

- `crop`: `null` (full frame) OR `{ "x", "y", "w", "h" }`, all normalized
  `0.0`-`1.0` relative to the frame. `x`,`y` = top-left corner of the kept box;
  `w`,`h` = its width/height as a fraction of the frame.
- `crop_reason`: one short sentence. State why a region was removed, or why the
  full frame was kept (for example "Full frame; no webcam tile present.").

### Validity (enforced by render.py, treated as null if violated)

- `x`, `y` in `[0, 1]`
- `w`, `h` in `(0, 1]`
- `x + w <= 1.0` and `y + h <= 1.0`

An out-of-range or malformed `crop` is treated as `null` (full frame) and
flagged for QA. render.py applies the box as
`(x*W, y*H, (x+w)*W, (y+h)*H)` in pixels on a COPY of the frame.

---

## Worked examples

| Frame | Decision | crop | crop_reason |
|---|---|---|---|
| Screen share with a small webcam in the bottom-right corner | crop it out | `{"x":0,"y":0,"w":1.0,"h":0.82}` | "Removed the bottom webcam tile; full app window kept." |
| Full-bleed slide, no webcam | keep full | `null` | "Full frame; slide fills the screen, no tile to remove." |
| Webcam overlaps the toolbar the step needs | keep full | `null` | "Webcam overlaps the toolbar; cropping would clip a needed control." |
| Participant gallery as a left side band, content on the right | crop the band | `{"x":0.22,"y":0,"w":0.78,"h":1.0}` | "Dropped the participant gallery on the left; document kept whole." |
| Unsure where the content ends | keep full | `null` | "Unsure of the content boundary; kept the full frame to be safe." |
