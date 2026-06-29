# _standards (routing)

Fixed contracts and bars. These do NOT change per install (that is `_config/`). Every lane reads these outward; nothing re-declares them.

## Files here

| File | What it pins | Loaded by |
|---|---|---|
| `doc-model-schema.md` | the `docmodel-1.0` schema (the one contract all renderers read) + the provenance/sidecar rules | 03-layout (produces it), 04-render + 05-qa (consume it) |
| `manifest-contract.md` | which manifest fields the lanes rely on and why; points at the pinned JSON Schema | 01-ingest |
| `schema/manifest-1.0.schema.json` | canonical field-type contract: verbatim engine copy, pinned to `"1.0"` (frozen) | 01-ingest (validates 1.0 manifests) |
| `schema/manifest-1.1.schema.json` | same, pinned to `"1.1"` (the 1.0 schema minus `contactsheet_jpg`); accepted set is {1.0, 1.1} | 01-ingest (validates 1.1 manifests) |
| `qa-bar.md` | the Stage 05 ship gate: the 16-item fidelity + polish checklist | 05-qa |

## See also

- `README.md` here: the anchor explaining `_config` + `_standards` as the canonical shared layer.
- `../_config/` for the per-install DIALS (brand, voice, design, audience, render prefs).
- `../_skills/` for shared CODE (the renderer).
