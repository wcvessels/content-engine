# Educational doc structure: the reader-facing shape (CANONICAL home)

The section order and per-module shape the educational guide takes (specialization slot S4). Stage 03 reads this to lay the ordered spine into the `docmodel-1.0` sections. Nothing here restates brand/voice (that is `_config`) or the schema (that is `_standards/doc-model-schema.md`); this is purely the document SHAPE.

## The reader-facing structure (top to bottom)

1. **Title page / header.** Guide title; brand letterhead (filled at render); a one-line subtitle = audience + what they'll be able to do. -> `meta.title`, `meta.subtitle`.
2. **Overview.** 2 to 4 short paragraphs: what the guide covers and why it matters. -> a `level:1` intro section.
3. **Learning objectives.** "By the end you'll be able to..." bullets, action verbs. -> `meta.learning_objectives` + a short objectives section.
4. **Prerequisites.** Stated prerequisites first; structural ones phrased gently ("you'll get more from this if you already know X"); if none, the literal line "No prior setup needed." -> a `callout` `variant:"prereq"` or a short section.
5. **Learning modules (the ordered path).** The heart. Modules in dependency order. Each module:
   - a heading + an "In this module you'll learn to..." lead (the module objective)
   - concept explanations in prose
   - embedded screenshots at the concept/procedure they illustrate, with a short caption
   - procedures as numbered steps, with the step's screenshot under it
   - pitfalls as "Watch out:" callouts (`variant:"warning"`)
   - a one-line recap
   Map to a `level:1` section per module, with `objective` and `depends_on` set; blocks ordered concept -> example -> procedure -> pitfall.
6. **Summary.** "What you've learned", mirroring the objectives, plus any stated next steps. -> a `level:1` summary section (`kind:"summary"`).
7. **References.** Tools/docs/links the recording pointed to; if none, "No external references mentioned."

Footer/disclaimer come from `_config` at render. No citations, timestamps, or speaker tags anywhere in the reader surface.

## The per-module block order (the educational shape)

Within each module section, blocks go: **objective lead (prose)** -> **concept (prose)** -> **example (prose or list)** -> **procedure (ordered list)** -> **screenshot (under the step it shows)** -> **pitfall (callout)** -> **recap (prose)**. Omit any block type the module does not have; never insert an empty one. A module with no screenshot is fine and common.

## Empty-section fallbacks (so structure 12 of the qa-bar passes)

Every structural section is present even when the source had nothing for it; it carries the stated fallback line rather than being dropped:

- Prerequisites with none -> "No prior setup needed."
- References with none -> "No external references mentioned."
- A module that teaches a capability with no stated objective -> a synthesized objective (marked `inferred:true` upstream), never a blank lead.

## Screenshot placement + crop (mechanic is shared)

Pick the frame the item maps to (procedure -> its `frame_index`; concept -> the frame whose `timestamp_s` falls in its span; ties by `sharpness`). The crop decision uses the shared rule in `../../../../_skills/render-doc/frame-crop.md` and is recorded on the `screenshot` block as `crop` + `crop_reason`. Placement correctness is solved here (the block's position in `section.blocks[]`); the renderer just honors that position.
