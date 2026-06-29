# educational-guide: lane-config

The lane dials. These are the only fixed lane-level choices; per-run facts (this video, this reader) are collected conversationally at `stages/01-ingest/`, never here. Brand / voice / design / render prefs are NOT here, they live once in `../../_config/` and are read outward.

## Document type

- `doc_type`: **`guide`** (a free string written into the doc-model `meta.doc_type`; not a closed enum, so `_lane-builder` can add a lane without editing any contract).

## Default reader

- **Learner, low prior knowledge.** Wants to DO the thing by the end, not just read about it. Assume general computer literacy, not domain expertise.
- Overridable per run at `stages/01-ingest/`. The default profile and reading level live in `../../_config/audience-defaults.md`; this line names which reader THIS lane assumes when the run does not say.

## Significance thresholds (the keep/cut rule for stage 02)

Promote a segment to a typed item ONLY if cutting it would cost the learner one of: a **concept**, a **procedure**, a **fact/constraint**, a worked **example**, or a **pitfall**. Everything else is chatter and gets dropped:

- Drop: greetings, "let me share my screen", scheduling, off-topic tangents, pure agreement/acknowledgement, filler.
- Keep a borderline item if it is a stated **objective signal** ("by the end you'll be able to...") or a stated **prerequisite** ("before this you need...").
- When unsure, keep AND mark it for the stage-02 checkpoint rather than silently cutting; the human decides.

## Ordering rule (named here, defined in references)

**Dependency order**: build the prerequisite graph and topo-sort so every prerequisite precedes its dependents, then group into foundations-first modules. Full rule in `reference/rules.md` + `stages/02-structure/references/dependency-ordering.md`.
