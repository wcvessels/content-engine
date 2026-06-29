#!/usr/bin/env python3
"""render-doc self-test: prove HTML + PDF render from a SYNTHETIC doc-model.

No real manifest needed. This script:
  1. Generates a synthetic frame JPG with a labeled "WEBCAM" strip on the right
     and a "CONTENT" panel on the left, so an applied crop is visually checkable.
  2. Writes a synthetic manifest.json (just enough: frames[] + artifacts) and a
     synthetic docmodel.json (prose, callout, list, two screenshots: one cropped
     to drop the webcam strip, one full-frame, one missing-frame placeholder).
  3. Runs render.render() to produce sample.html + sample.pdf.
  4. Asserts: HTML non-empty + has expected structure; PDF starts with %PDF-;
     the cropped data-URI image is NARROWER than the full-frame one (crop applied).

Artifacts are LEFT in place as proof. Exit 0 = GREEN.
"""

import base64
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER_DIR = os.path.dirname(HERE)
sys.path.insert(0, RENDER_DIR)

import render  # noqa: E402
from PIL import Image  # noqa: E402


def make_frame(path, w=1280, h=720):
    """A frame: left 78% = teal CONTENT panel, right 22% = dark WEBCAM strip."""
    img = Image.new("RGB", (w, h), (24, 32, 40))
    split = int(w * 0.78)
    content = Image.new("RGB", (split, h), (47, 143, 127))   # teal
    webcam = Image.new("RGB", (w - split, h), (60, 40, 40))  # dark red-grey
    img.paste(content, (0, 0))
    img.paste(webcam, (split, 0))
    img.save(path, "JPEG", quality=90)
    return (w, h)


def data_uri_dims(data_uri):
    """Decode a data:image/jpeg;base64 URI and return (w, h)."""
    assert data_uri.startswith("data:image/jpeg;base64,"), data_uri[:40]
    raw = base64.b64decode(data_uri.split(",", 1)[1])
    return Image.open(io.BytesIO(raw)).size


def main():
    frames_dir = os.path.join(HERE, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    frame_name = "frame_0001_000005.jpg"
    fw, fh = make_frame(os.path.join(frames_dir, frame_name))

    # Synthetic manifest: only the fields resolve_frame reads.
    manifest = {
        "schema_version": "1.0",
        "frames": [{"index": 1, "file": frame_name}],
        "artifacts": {"frames_dir": "frames"},
    }
    manifest_path = os.path.join(HERE, "selftest_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)

    # Synthetic docmodel exercising every block type + crop + missing frame.
    docmodel = {
        "schema": "docmodel-1.0",
        "meta": {
            "title": "render-doc Self-Test Guide",
            "subtitle": "Proves HTML and PDF render from a synthetic doc-model.",
            "doc_type": "guide",
            "audience": "the render-core builder",
            "author": "Will Vessels",
            "date": "2026-06-27",
            "reading_time_min": 2,
            "learning_objectives": [
                "Confirm prose, callout, list, and screenshot blocks render.",
                "Confirm the **crop** box is applied to a screenshot.",
            ],
            "source": {"video_title": None, "manifest": "selftest"},
        },
        "sections": [
            {
                "id": "intro", "heading": "Overview", "level": 1, "kind": "intro",
                "blocks": [
                    {"type": "prose",
                     "md": "This is a *synthetic* guide. It uses **inline markdown**, "
                           "a `code span`, and a [link](https://example.com)."},
                    {"type": "callout", "variant": "tip",
                     "md": "Callouts render with a colored rail and a label."},
                    {"type": "list", "ordered": True,
                     "items": ["First step.", "Second step with **bold**.", "Third."]},
                ],
            },
            {
                "id": "shots", "heading": "Screenshots and cropping", "level": 1,
                "kind": "concept",
                "blocks": [
                    {"type": "prose",
                     "md": "The frame below is cropped to drop the webcam strip on "
                           "the right (kept box = left 78%)."},
                    {"type": "screenshot", "frame_index": 1,
                     "caption": "Cropped: webcam strip removed.",
                     "alt": "Content panel only.",
                     "crop": {"x": 0.0, "y": 0.0, "w": 0.78, "h": 1.0},
                     "crop_reason": "Removed the webcam strip on the right; content kept whole."},
                    {"type": "screenshot", "frame_index": 1,
                     "caption": "Full frame (no crop).",
                     "alt": "Content plus webcam strip.",
                     "crop": None,
                     "crop_reason": "Full frame kept for comparison."},
                    {"type": "screenshot", "frame_index": 999,
                     "caption": "This frame is missing on purpose.",
                     "crop": None,
                     "crop_reason": "N/A"},
                    {"type": "callout", "variant": "warning",
                     "md": "The missing frame above must render a placeholder, not crash."},
                ],
            },
            {
                "id": "summary", "heading": "Summary", "level": 2, "kind": "summary",
                "blocks": [
                    {"type": "prose", "md": "If you can read this, sections rendered in order."},
                    {"type": "unknown_future_type", "md": "Unknown block type degrades to prose."},
                ],
            },
        ],
        "footer": {
            "disclaimer": "Synthetic self-test output. Not a real guide.",
            "confidentiality": "Internal use only",
        },
    }
    docmodel_path = os.path.join(HERE, "docmodel.json")
    with open(docmodel_path, "w", encoding="utf-8") as fh:
        json.dump(docmodel, fh, indent=2)

    # ---- Render ----
    produced = render.render(docmodel, HERE, "sample",
                             manifest_path=manifest_path, targets=("html", "pdf"))

    results = []

    # 1. HTML produced + non-empty + structurally sane.
    html_path = produced.get("html")
    html = open(html_path, "r", encoding="utf-8").read()
    assert html_path and os.path.getsize(html_path) > 0, "HTML empty"
    for needle in ('<nav class="toc"', "render-doc Self-Test Guide",
                   "<strong>inline markdown</strong>", "<code>code span</code>",
                   '<a href="https://example.com">link</a>',
                   'class="callout callout-tip"', "<ol class=\"doc-list\"",
                   "frame-placeholder", "Unknown block type degrades to prose",
                   "data:image/jpeg;base64,"):
        assert needle in html, "HTML missing: %r" % needle
    results.append("HTML: produced, non-empty, structure + markdown + image OK")

    # 2. PDF produced + valid header.
    pdf_path = produced.get("pdf")
    assert pdf_path and os.path.getsize(pdf_path) > 0, "PDF empty"
    head = open(pdf_path, "rb").read(5)
    assert head == b"%PDF-", "PDF header wrong: %r" % head
    results.append("PDF: produced, valid %%PDF- header (%d bytes)" % os.path.getsize(pdf_path))

    # 3. Crop applied: cropped image width < full-frame image width.
    cropped = render.resolve_frame(1, manifest_path,
                                   crop={"x": 0.0, "y": 0.0, "w": 0.78, "h": 1.0})
    full = render.resolve_frame(1, manifest_path, crop=None)
    cw, _ = data_uri_dims(cropped)
    full_w, _ = data_uri_dims(full)
    expected = int(round(0.78 * fw))
    assert cw < full_w, "crop not applied: cropped width %d >= full %d" % (cw, full_w)
    assert abs(cw - expected) <= 2, "crop width %d != expected ~%d" % (cw, expected)
    results.append("CROP: applied (full %dpx -> cropped %dpx, expected ~%dpx)"
                   % (full_w, cw, expected))

    # 4. Missing frame -> None (placeholder path), no exception.
    assert render.resolve_frame(999, manifest_path) is None, "missing frame did not return None"
    results.append("MISSING-FRAME: resolve_frame returns None (placeholder path) OK")

    print("SELF-TEST GREEN")
    for r in results:
        print("  [PASS] " + r)
    print("Artifacts:")
    print("  HTML: " + html_path)
    print("  PDF : " + pdf_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
