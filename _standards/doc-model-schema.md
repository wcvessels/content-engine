# doc-model schema (docmodel-1.0)

The single contract every renderer reads. Stage 03-layout produces exactly one of these per deliverable; `_skills/render-doc/render.py` consumes nothing else. Lane-specific logic happens upstream (stages 01-03) and collapses into this shape, so the renderers never know which lane produced the model. This file also pins the provenance/sidecar rules (the grounding lives internally, never in the reader doc).

House rule applies to authored content rendered from this model: zero em dash characters, plain English.

---

## 1. Top-level shape

```json
{
  "schema": "docmodel-1.0",
  "meta": { ... },
  "sections": [ ... ],
  "footer": { ... }
}
```

`schema` MUST be the literal string `"docmodel-1.0"`. A renderer that reads any other value fails loud (do not guess a newer or older shape). This mirrors the manifest version pin in `manifest-contract.md`.

---

## 2. `meta` (document-level metadata)

| Field | Type | Required | Notes |
|---|---|---|---|
| `title` | string | yes | document title, shown on the title page and TOC |
| `subtitle` | string or null | no | one-line subtitle (audience + what they will do) |
| `doc_type` | string | yes | FREE STRING set by the lane's `lane-config.md`, e.g. `guide`, `procedure`. NOT a closed enum, so a new lane needs no schema edit. |
| `audience` | string or null | no | who this is for, plain English |
| `author` | string | yes | filled from `_config/identity.md` at render |
| `date` | string | yes | ISO date `YYYY-MM-DD` |
| `reading_time_min` | integer or null | no | estimated read time; omit or null when unknown |
| `learning_objectives` | array of string | no | educational lane; `[]` when not applicable |
| `estimated_duration` | string or null | no | sop lane (e.g. `"15 min"`); null when not applicable |
| `source` | object | yes | provenance meta, NOT rendered to the reader (see §6) |

`meta.source` shape:

```json
"source": {
  "video_title": "string or null",
  "manifest": "run_id string (from manifest run.run_id)"
}
```

`meta.source` is metadata only. It is read by the provenance tooling and never printed in a reader-facing field.

---

## 3. `sections` (the ordered document spine)

`sections` is an ordered array. Order IS reading order; the renderer honors it as given (lane stage 03 already resolved ordering). Each section:

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | stable section id (e.g. `s1`, `module-2`); used for in-page TOC anchors and `depends_on` |
| `heading` | string | yes | reader-facing heading text |
| `level` | integer | yes | `1` or `2` only; drives TOC nesting and heading hierarchy |
| `kind` | string | no | styling hint: `intro`, `concept`, `step`, `summary`. Unknown or absent -> plain section, no special styling. |
| `blocks` | array | yes | ordered content blocks (see §4); may be empty for a fallback-only section |
| `objective` | string or null | no | educational lane; one-line module objective, optional |
| `depends_on` | array of string | no | educational tour ordering; section ids this section depends on. Optional, advisory to layout only. |

`kind` and `level` are hints, not hard contracts. A renderer that does not recognize a `kind` renders a plain section. `level` outside {1,2} clamps to the nearest valid value.

---

## 4. Block types (inside `section.blocks[]`)

Every block has a `type`. Four types are defined. An unknown `type` MUST degrade to a plain prose block (render its `md` if present, else skip) rather than fail. This graceful-fallback rule is what lets one model serve polished HTML and a documented plain DOCX path with no per-target branching.

### 4.1 `prose`

```json
{ "type": "prose", "md": "Click **Settings**, then choose *Export*." }
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `md` | string | yes | INLINE markdown only: `**bold**`, `*italic*`, `` `code` ``, `[text](url)` links. NO block-level HTML, NO headings, NO tables, NO fenced code blocks. Each renderer converts inline markdown its own way (a ~30-line escaper + regex pass, no markdown library). |

### 4.2 `screenshot`

```json
{
  "type": "screenshot",
  "frame_index": 14,
  "caption": "The export settings panel.",
  "alt": "Export settings panel with the format dropdown open.",
  "crop": null,
  "crop_reason": "Full frame; no webcam tile present."
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `frame_index` | integer | yes | references `frames[].index` in the source manifest. Resolution to a file path is a render-time step (see §5). A reference, NOT bytes. |
| `caption` | string or null | no | short reader-facing caption under the image |
| `alt` | string or null | no | accessibility alt text |
| `crop` | null or object | no | OPTIONAL crop box. `null` (or absent) = use the full frame. When set: `{ "x": num, "y": num, "w": num, "h": num }`, all normalized 0.0-1.0 relative to the frame (x,y = top-left corner; w,h = width/height fraction). See §4.2.1. |
| `crop_reason` | string or null | no | short string: why this region was cropped, or why the full frame was kept. Audited at 05-qa. |

If `frame_index` does not resolve to a real frame at render time, the renderer emits a visible placeholder block and logs it for QA. It NEVER hard-fails the render (missing-frame guard).

#### 4.2.1 The `crop` field (D6)

`crop` lets 03-layout trim a screenshot to the relevant on-screen content, removing a webcam tile or participant gallery ONLY when that does not cut relevant context. The division of labor is fixed:

- **03-layout decides** the box using vision, per the shared rule in `_skills/render-doc/frame-crop.md` ("identify the relevant content region; if a webcam tile or participant gallery occupies a separable region that can be removed without cutting any relevant content, output the content box; otherwise output null; when unsure, keep the full frame"). It writes `crop` + `crop_reason`.
- **04-render applies** it deterministically with Pillow: `box = (x*W, y*H, (x+w)*W, (y+h)*H)` in pixels, crop BEFORE downscale + base64 embed. The original frame in `output/ingest/frames/` is never modified (non-destructive, resurrectable).
- **05-qa checks** the crop improved focus and clipped no needed context.

Validity: `x`, `y` in `[0,1]`; `w`, `h` in `(0,1]`; `x+w <= 1.0`; `y+h <= 1.0`. An out-of-range or malformed `crop` is treated as `null` (full frame) and flagged for QA. `crop` is OPTIONAL end to end: the default null = full frame, and the whole crop step can be skipped under time pressure with zero render breakage.

### 4.3 `callout`

```json
{ "type": "callout", "variant": "warning", "md": "Do not delete the source file before the export finishes." }
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `variant` | string | yes | `tip`, `warning`, `note`, or `prereq`. Unknown variant -> styled as a plain `note`. |
| `md` | string | yes | inline markdown only (same grammar as `prose.md`) |

### 4.4 `list`

```json
{ "type": "list", "ordered": true, "items": ["Open the menu.", "Choose **Export**.", "Confirm."] }
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `ordered` | boolean | yes | `true` -> numbered list, `false` -> bullet list |
| `items` | array of string | yes | each item is inline markdown only (same grammar as `prose.md`); non-empty |

---

## 5. Screenshot resolution (render-time)

The renderer resolves `frame_index` -> file path with one helper, `resolve_frame(frame_index, manifest_path)`:

1. Load the run manifest, build `index -> file` from `frames[]`.
2. Join with `artifacts.frames_dir` resolved RELATIVE TO THE MANIFEST FILE'S OWN DIRECTORY (`os.path.join(os.path.dirname(manifest_path), frames_dir)`), NOT the current working directory.

Because Stage 01-ingest already COPIED frames into `output/ingest/frames/` with in-bundle absolute paths, downstream render works off those copies and never re-resolves the relative `frames_dir` field. Frame filenames follow the engine naming `frame_NNNN_HHMMSS.jpg`.

Per built target (HTML, PDF): read the jpg, apply `crop` if set (Pillow), optional downscale to ~1200px if the file balloons, then base64-encode and inline as `data:image/jpeg;base64,...`. Placement correctness is solved upstream by 03-layout (the block's position in `section.blocks[]`); the renderer just honors order.

---

## 6. Provenance + sidecar rules (folded in here, §8.1 of the blueprint)

The reader-facing document carries ZERO citations: no `[HH:MM:SS]`, no `frame NNNN`, no speaker tags, no `[ref: ...]`. All grounding lives in a SEPARATE sidecar file, written to `output/`, NEVER embedded in or attached to any rendered deliverable.

### 6.1 The sidecar file (`{slug}-provenance.json`)

Built incrementally: Stage 02 writes item-level entries, Stage 03 extends to block + screenshot level. Shape:

```json
{
  "slug": "string",
  "lane": "lane name from lane-config.md",
  "source": {
    "input_type": "manifest | plain transcript",
    "manifest": "path or run_id",
    "transcript": "path or null",
    "coverage": "HH:MM:SS to HH:MM:SS",
    "exclusions": "none | list applied"
  },
  "blocks": [
    {
      "block_id": "module-2.concept-1",
      "section": "Learning Modules > Configuring exports",
      "reader_text_hash": "sha256 of the rendered block text",
      "type": "concept",
      "source_segments": [42, 43, 44],
      "source_spans": [ { "start_s": 612.4, "end_s": 631.0, "speaker": "Alex" } ],
      "frames": [ { "frame_index": 7, "file": "frame_0007_001012.jpg", "timestamp_s": 612.0 } ],
      "inferred": false,
      "inference_note": null
    }
  ],
  "screenshots": [
    { "placed_in": "module-2.procedure-1.step-3", "frame_index": 7, "file": "frame_0007_001012.jpg" }
  ]
}
```

### 6.2 The grounding rules

- Every reader-facing block has a `blocks[]` entry naming the real `source_segments` it came from.
- `source_segments` are manifest segment indices (or, for a plain-transcript input, line ranges within transcript bounds).
- The `[HH:MM:SS]` / `frame NNNN` grammar lives HERE, in the sidecar, never in the reader doc.
- `inferred: true` flags the ONLY not-directly-stated items: the educational lane's structural prerequisites and synthesized objectives. These are ordering or phrasing decisions, never new factual claims. `inference_note` explains the reordering or synthesis. The SOP lane has ZERO `inferred: true` content entries (an SOP step, owner, or branch is a factual assertion, so zero inference).
- `screenshots[]` records every placed frame so 05-qa can confirm each rendered screenshot is grounded and sits in the right section.

### 6.3 The render-time split

Stages 02 and 03 keep an internal `[ref]` tag on each block. Stage 04-render performs the split: it writes every block's `[ref]` to `output/{slug}-provenance.json` (and the human-readable `output/{slug}-provenance.md`) and produces a clean doc-model with refs removed before rendering. The sidecar is internal; it is the input to the Stage 05 fidelity audit (`_standards/qa-bar.md`).

---

## 7. Design rules that make the model work (summary)

- **Prose is inline-markdown strings**, never block HTML; each renderer converts its own way.
- **Screenshots are references, not bytes**; file resolution is a render-time step (§5).
- **`kind` / `variant` are styling hints**; an unknown value falls back to a plain block. This is what lets one model serve polished HTML and a documented plain DOCX with no per-target branching.
- **Provenance lives in metadata + a separate sidecar**, never in body text.
- **`doc_type` is a free string**, so `_lane-builder` can add a lane with no schema edit.
- **`crop` is optional and degrades to full frame**, so the crop feature never blocks a render.

This schema is FROZEN for the submission. A field addition is a `1.1` bump, which would edit this file once and nothing else (single source of truth).
