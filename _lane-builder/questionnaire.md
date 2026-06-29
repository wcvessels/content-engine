# Lane questionnaire: the four questions a new lane answers

Answer these before you copy any skeleton. They pin everything a lane needs that is not already shared. If you cannot answer all four crisply, the lane is not ready to build; the answers ARE the specialization. The shared shelf (brand, voice, design, schema, renderer, QA bar) is already decided, so these four are the whole job.

Compare your answers against the two existing lanes as you go: the educational-guide lane and the SOP doc-only delta sit at opposite ends of the "how much may I infer?" spectrum, which is the deepest design choice a lane makes.

## 1. Domain: what document does this lane produce, and for whom?

- The doc type (a free string for `lane-config.md` `doc_type`, e.g. `guide`, `procedure`, `release-notes`, `kb-article`).
- The default reader (who opens the finished document and what they already know). Educational: "learner, low prior knowledge." SOP: "operator or new hire."
- The one-sentence purpose. This becomes the S5 one-liners (`{{LANE_02_ONE_LINER}}` / `{{LANE_03_ONE_LINER}}`) in the copied stage skeletons.

## 2. Extraction taxonomy: what typed items do you pull out of the transcript? (Stage 02)

- List the item TYPES this lane extracts. Educational pulls Concept / Procedure / Example / Fact-or-constraint / Pitfall / Objective-signal. The SOP delta pulls Step / Decision-point / Owner / Risk-or-gotcha / Reference / Prerequisite / Purpose / Scope-bound / Open-question. Yours will be its own set.
- For each type: what marks it in a transcript, and what does each item record (always at least: type, a one-line normalized statement, source segment indices, any `frame_index`)?
- The significance filter: what is the keep-or-cut test for this lane? Educational keeps a segment only if cutting it costs the learner a concept/procedure/fact/example/pitfall. Define your equivalent.

This goes in `stages/02-structure/references/<your-taxonomy>.md`, the canonical home for the type list. Nothing else restates it.

## 3. Ordering rule: how do the items become a sequence? (Stage 02)

The single most important design decision, because it sets HOW MUCH the lane may infer:

- Educational orders by DEPENDENCY: build a prerequisite graph, topo-sort, group into modules, foundations first. It MAY infer a structural prerequisite (concept B uses a term concept A defined) because that is an ORDERING decision, not a content claim. Such inferences are flagged `inferred:true` and never add a sentence the speaker did not say; they only change module order.
- The SOP delta orders by stated PROCEDURE order (the sequence the speaker stated), falling back to dependency then transcript order with an `order not stated` flag, and infers NOTHING about content (a step, owner, or branch is a factual assertion, so zero inference).

State your lane's ordering rule and, critically, where it sits on that inference spectrum. A lane that asserts facts (like an SOP) must be zero-inference on content. A lane that only sequences (like a guide) may infer order. Be explicit, because the fidelity audit checks exactly this.

## 4. Output structure: what sections does the finished document have, in what order? (Stage 03)

- The reader-facing section list, top to bottom. Educational: Title, Overview, Learning objectives, Prerequisites, Learning modules, Summary, References. SOP: Title, Purpose, Scope, Roles and owners, Prerequisites, Procedure, Decision points, Risks and gotchas, References, Open questions.
- For each section: its per-item shape. Educational module = objective then concept then example then screenshot, pitfalls as callouts. SOP step = numbered action then owner then expected result then decision/risk callout then screenshot.
- The empty-section fallback line (what prints when a section has no content). Educational prerequisites with none: "No prior setup needed." SOP open questions are reader-facing on purpose (an honest gap is information the reader needs).

This goes in `stages/03-layout/references/<your-doc-structure>.md`. It maps onto the shared `docmodel-1.0` blocks (prose / screenshot / callout / list), so you almost never need a new block type.

## After you answer

Take the four answers to `README.md` and run the copy-and-specialize steps. Stages 01/04/05 need no answers from you (they are shared plumbing); these four questions are the entire per-lane design.
