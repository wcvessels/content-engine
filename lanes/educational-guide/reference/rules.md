# educational-guide: structuring rules (ANCHOR)

How this lane turns a raw recording into a guided learning path. This is the lane's reason to exist; everything brand / voice / render lives outward in `../../_config` and `../../_skills`. The detailed per-stage encodings live in `../stages/02-structure/references/` and `../stages/03-layout/references/`; this file is the plain-English summary the lane is built around.

## The philosophy: understand-anything, then teach in order

A recording is a stream of talk. A guide is an ordered path a stranger can follow. The job is to (1) pull out the things worth understanding, (2) drop everything else, (3) put them in the order a learner can actually absorb, and (4) ground every line in the source so nothing is invented.

## 1. Typed extraction (stage 02)

Every kept item is one of these types (canonical list: `../stages/02-structure/references/concept-extraction.md`):

- **Concept**: a thing to understand.
- **Procedure**: a how-to that was demonstrated.
- **Example**: a worked case; attaches to a concept.
- **Fact / constraint**: a stated rule, limit, or number.
- **Pitfall**: a "watch out" tied to a concept or procedure.
- **Objective signal**: an explicit "by the end you'll be able to...".

Each item records: its type, a one-line normalized statement, the source segment indices (the provenance anchor), and any `frame_index`.

## 2. Significance filter

Keep an item only if cutting it costs the learner a concept / procedure / fact / example / pitfall. Greetings, screen-share fumbling, scheduling, tangents, and pure agreement are dropped. (Thresholds: `../lane-config.md`.)

## 3. Prerequisites: the one place inference is allowed

Two signals:

- **Stated** prerequisite ("before this you need X"), cited to the segment.
- **Structural** prerequisite (module B uses a term module A defined earlier).

Structural is the ONLY place this lane may infer a relationship the speaker did not state, because it is an **ordering** decision, not a content claim. It is recorded in the provenance sidecar as `inferred:true`. It NEVER adds an unsupported sentence to the reader doc; it only changes module order.

## 4. Dependency order -> modules (stage 02)

Build a directed prerequisite graph, topo-sort it (no back-edges), group items into **modules** (one cluster teaching one capability), and order modules foundations-first. Within a module: concept -> examples -> procedures -> pitfalls. Attach 1 to 3 **learning objectives** per module, each starting with an action verb; prefer stated objective signals, mark synthesized objectives `inferred:true`.

## 5. Screenshots placed at what they illustrate (stage 03)

A procedure maps to the frame at its `frame_index`; a concept maps to the frame whose `timestamp_s` falls in its segment span; ties broken by `frames[].sharpness` unless the screens are genuinely distinct; no frame = a clean text-only entry (common and fine). Cropping follows the shared rule in `../../../_skills/render-doc/frame-crop.md`.

## 6. Clean reader surface, grounding internal

The reader never sees a timestamp, a speaker tag, or a `frame NNNN` ref. All grounding lives in the provenance sidecar. If the source genuinely lacks something, the guide says so honestly ("not covered in the recording") rather than inventing it.
